from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

# ==========================================
# 0. CONFIGURAZIONE (ISOLAMENTO DELLA CONFIG)
# ==========================================
# In un'app reale questi valori verrebbero letti da variabili d'ambiente,
# file .env, o sistemi come HashiCorp Vault / Azure Key Vault.
# Isolare la config in un oggetto dedicato significa che cambiarla
# non tocca né l'interfaccia né la logica di business.

@dataclass
class ConnectionConfig:
    max_retries: int = 3
    timeout_seconds: int = 30
    pool_size: int = 5

# ==========================================
# 1. IL PRODOTTO (INTERFACCIA)
# ==========================================
# L'interfaccia comune che tutti i database devono implementare.
class DatabaseConnection(ABC):
    """
    Contratto comune che tutti i database devono rispettare.
    Il Creator e il Client lavorano solo con questa interfaccia.
    """
    @abstractmethod
    def open(self) -> bool:
        """Apre la connessione. Ritorna True se l'operazione è andata a buon fine."""
        pass

    @abstractmethod
    def query(self, sql: str) -> str:
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Verifica che la connessione sia ancora attiva e funzionante."""
        pass

    @abstractmethod
    def close(self):
        pass

# ==========================================
# 2. PRODOTTI CONCRETI
# ==========================================
# Ogni classe gestisce internamente logiche molto diverse
# (pool di connessioni, elezione del nodo primario, file locking...),
# ma espone all'esterno solo i quattro metodi dell'interfaccia.
# Questo è il punto centrale: la complessità è *incapsulata* qui dentro.

class MySQLConnection(DatabaseConnection):
    """
    Simula MySQL con connection pool interno.
    Il pool viene creato e gestito privatamente: nessuno fuori da questa
    classe deve sapere che esiste.
    """
    def __init__(self, host: str, user: str, password: str, schema: str, config: ConnectionConfig):
        self._dsn = f"mysql://{user}:***@{host}/{schema}"
        self._config = config
        self._pool: list[str] = []
        self._active = False

    def _init_pool(self):
        """Logica privata: popola il pool con N connessioni."""
        for i in range(self._config.pool_size):
            self._pool.append(f"conn_{i}")
        print(f"[MySQL]  Pool di {self._config.pool_size} connessioni inizializzato.")

    def open(self) -> bool:
        print(f"[MySQL]  Connessione a {self._dsn} (timeout {self._config.timeout_seconds}s)...")
        self._init_pool()
        print("[MySQL]  Verifica permessi utente... OK.")
        self._active = True
        return True

    def query(self, sql: str) -> str:
        conn = self._pool[0]   # preleva una connessione dal pool
        return f"[MySQL]  Eseguo '{sql}' su {conn}."

    def health_check(self) -> bool:
        ok = bool(self._pool) and self._active
        print(f"[MySQL]  Health check pool: {'OK' if ok else 'FALLITO'}")
        return ok

    def close(self):
        self._pool.clear()
        self._active = False
        print("[MySQL]  Pool rilasciato, connessione chiusa.")


class MongoDBConnection(DatabaseConnection):
    """
    Simula MongoDB con replica set e failover automatico.
    La logica di elezione del primary node è completamente nascosta.
    """
    def __init__(self, nodes: list[str], cluster: str, use_ssl: bool, config: ConnectionConfig):
        self._nodes = nodes
        self._cluster = cluster
        self._ssl = use_ssl
        self._config = config
        self._primary: Optional[str] = None

    def _elect_primary(self) -> str:
        """
        Logica privata: simula l'algoritmo di elezione Raft-like di MongoDB.
        In produzione contatta ogni nodo, raccoglie i voti e sceglie il primary.
        """
        elected = self._nodes[0]
        print(f"[MongoDB] Elezione primary: '{elected}' vince su {len(self._nodes)} nodi.")
        return elected

    def open(self) -> bool:
        ssl_label = "ON" if self._ssl else "OFF"
        print(f"[MongoDB] Connessione al cluster '{self._cluster}' — SSL {ssl_label}...")
        self._primary = self._elect_primary()
        print(f"[MongoDB] Connected to primary: {self._primary}. OK.")
        return True

    def query(self, sql: str) -> str:
        return f"[MongoDB] Traduco '{sql}' in aggregation pipeline BSON su {self._primary}."

    def health_check(self) -> bool:
        ok = self._primary is not None
        print(f"[MongoDB] isMaster su '{self._primary}': {'OK' if ok else 'FALLITO'}")
        return ok

    def close(self):
        self._primary = None
        print(f"[MongoDB] Disconnesso dal cluster '{self._cluster}'.")


class SQLiteConnection(DatabaseConnection):
    """
    Simula SQLite con file locking e controllo di integrità.
    SQLite usa un lock a livello di file per garantire scritture serializzate.
    """
    def __init__(self, file_path: str, config: ConnectionConfig):
        self._file_path = file_path
        self._config = config
        self._locked = False

    def _acquire_lock(self):
        """Logica privata: acquisisce il lock esclusivo sul file .db."""
        self._locked = True
        print(f"[SQLite]  Lock esclusivo acquisito su '{self._file_path}'.")

    def _integrity_check(self):
        """Logica privata: esegue PRAGMA integrity_check sul file."""
        print("[SQLite]  PRAGMA integrity_check: OK (0 errori trovati).")

    def open(self) -> bool:
        print(f"[SQLite]  Apertura file: {self._file_path}...")
        self._acquire_lock()
        self._integrity_check()
        return True

    def query(self, sql: str) -> str:
        return f"[SQLite]  Eseguo su file locale: {sql}"

    def health_check(self) -> bool:
        ok = self._locked
        print(f"[SQLite]  File lock attivo: {'OK' if ok else 'FALLITO'}")
        return ok

    def close(self):
        self._locked = False
        print(f"[SQLite]  Lock rilasciato, file '{self._file_path}' chiuso.")


# ==========================================
# 3. IL CREATORE (ABSTRACT FACTORY METHOD)
# ==========================================
class DatabaseManager(ABC):
    """
    Il Creator gestisce la logica di business ad alto livello.
    Non sa nulla delle implementazioni concrete: sa solo che esiste
    una DatabaseConnection con cui può aprire, interrogare e chiudere.

    Nota: la retry logic qui è completamente generica — funziona
    identicamente per MySQL, MongoDB e SQLite senza una riga di
    codice specifico per ciascuno.
    """
    @abstractmethod
    def create_database(self) -> DatabaseConnection:
        """Il Factory Method vero e proprio."""
        pass

    def initialize_system(self):
        """
        Logica di alto livello: apre la connessione con retry automatico,
        esegue una query e verifica lo stato del sistema.
        È completamente ignara di quale database stia usando.
        """
        db = self.create_database()

        # --- Retry logic generica (uguale per tutti i db) ---
        connected = False
        for attempt in range(1, 4):
            print(f"\n[Manager] Tentativo di connessione {attempt}/3...")
            connected = db.open()
            if connected:
                break

        if not connected:
            print("[Manager] ERRORE: impossibile connettersi dopo 3 tentativi.")
            return

        # --- Logica di business, ancora generica ---
        print(db.query("SELECT version()"))

        if db.health_check():
            print("[Manager] Sistema operativo. Connessione verificata.")

        db.close()


# ==========================================
# 4. FACTORY CONCRETE (GESTIONE CONFIGURAZIONE)
# ==========================================
# Ogni manager sa come costruire il proprio database con i parametri giusti.
# Se la configurazione di produzione cambia (es. più connessioni nel pool),
# si modifica solo qui — il resto del codice non viene toccato.

class ProductionMySQLManager(DatabaseManager):
    def create_database(self) -> DatabaseConnection:
        config = ConnectionConfig(max_retries=3, timeout_seconds=10, pool_size=10)
        return MySQLConnection("10.0.0.5", "admin", "P@ssw0rd123!", "prod_db", config)

class CloudMongoManager(DatabaseManager):
    def create_database(self) -> DatabaseConnection:
        config = ConnectionConfig(max_retries=5, timeout_seconds=20, pool_size=1)
        nodes = ["mongo-1.cluster.net", "mongo-2.cluster.net", "mongo-3.cluster.net"]
        return MongoDBConnection(nodes, "Cluster-Alpha", use_ssl=True, config=config)

class LocalDevManager(DatabaseManager):
    def create_database(self) -> DatabaseConnection:
        config = ConnectionConfig(max_retries=1, timeout_seconds=5, pool_size=1)
        return SQLiteConnection("./dev_data.db", config)


# ==========================================
# 5. CODICE CLIENT
# ==========================================
# Il client conosce solo i Manager concreti (sa che esistono ambienti diversi),
# ma non ha mai una dipendenza diretta su MySQLConnection, MongoDBConnection
# o SQLiteConnection. Tutta la complessità è incapsulata nei livelli precedenti.

if __name__ == "__main__":
    print("=" * 52)
    print("  AMBIENTE PRODUZIONE (MySQL + connection pool)")
    print("=" * 52)
    ProductionMySQLManager().initialize_system()

    print("\n" + "=" * 52)
    print("  AMBIENTE CLOUD/NoSQL (MongoDB + replica set)")
    print("=" * 52)
    CloudMongoManager().initialize_system()

    print("\n" + "=" * 52)
    print("  AMBIENTE SVILUPPO LOCALE (SQLite + file lock)")
    print("=" * 52)
    LocalDevManager().initialize_system()