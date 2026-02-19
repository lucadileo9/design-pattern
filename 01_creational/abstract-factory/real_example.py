from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

# =======================================================================
# CONFRONTO CON IL FACTORY METHOD
# =======================================================================
# Nel Factory Method avevamo UN solo tipo di prodotto (DatabaseConnection)
# e una factory per ogni suo tipo concreto.
#
# Il problema che sorge è questo: nella realtà un'applicazione non
# usa mai solo un database — ha bisogno di un'intera infrastruttura
# coerente: un database, un logger, magari una cache.
#
# Se usassimo il Factory Method per ognuno, niente garantirebbe che
# il logger scelto sia compatibile con il database scelto.
# Ad esempio: chi ci vieta di mescolare un MySQLConnection (produzione)
# con un ConsoleLogger (sviluppo locale)?
#
# L'Abstract Factory risolve questo: raggruppa prodotti CORRELATI in
# famiglie, e garantisce che chi crea il database crei anche il logger
# giusto per quell'ambiente. La consistenza è forzata a livello architetturale.
# =======================================================================


# ==========================================
# 0. CONFIGURAZIONE
# ==========================================
@dataclass
class ConnectionConfig:
    max_retries: int = 3
    timeout_seconds: int = 30
    pool_size: int = 5


# ==========================================
# 1. PRODOTTO A — DatabaseConnection
# ==========================================
# Stessa interfaccia del Factory Method. Non cambia nulla qui:
# l'Abstract Factory riusa prodotti già noti e li aggruppa in famiglie.

class DatabaseConnection(ABC):
    @abstractmethod
    def open(self) -> bool:
        pass

    @abstractmethod
    def query(self, sql: str) -> str:
        pass

    @abstractmethod
    def health_check(self) -> bool:
        pass

    @abstractmethod
    def close(self):
        pass


# ==========================================
# 2. PRODOTTO B — Logger
# ==========================================
# Questo è il secondo tipo di prodotto della famiglia.
# Ogni ambiente usa una strategia di logging radicalmente diversa:
# file rotante in produzione, chiamate HTTP in cloud, stdout in locale.
# Ma verso l'esterno espongono tutti la stessa identica interfaccia.

class Logger(ABC):
    @abstractmethod
    def info(self, message: str):
        pass

    @abstractmethod
    def error(self, message: str):
        pass

    @abstractmethod
    def flush(self):
        """Svuota e chiude il canale di output del logger."""
        pass


# ==========================================
# 3. PRODOTTI CONCRETI — Famiglia "Production"
# N.B. Ogni famiglia comprende entrambi i prodotti: DatabaseConnection + Logger.
# tale famiglia sarà poi gestitta da una factory concreta che li crea entrambi
# e che quindi rappresenta la famiglia stessa.
# ==========================================

class MySQLConnection(DatabaseConnection):
    """MySQL con connection pool interno (invariato dal Factory Method)."""
    def __init__(self, host: str, user: str, password: str, schema: str, config: ConnectionConfig):
        self._dsn = f"mysql://{user}:***@{host}/{schema}"
        self._config = config
        self._pool: list[str] = []
        self._active = False

    def _init_pool(self):
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


class FileLogger(Logger):
    """
    Logger su file con rotazione automatica (tipico di produzione).
    Internamente gestisce il buffer di scrittura e la rotazione del file
    quando supera una certa dimensione — tutto nascosto all'esterno.
    """
    def __init__(self, log_path: str, max_size_mb: int = 100):
        self._path = log_path
        self._max_size_mb = max_size_mb
        self._buffer: list[str] = []
        self._rotations = 0

    def _should_rotate(self) -> bool:
        """Logica privata: controlla se il file supera la soglia."""
        return len(self._buffer) > 5  # simulazione semplificata

    def _rotate(self):
        """Logica privata: rinomina il file corrente e ne apre uno nuovo."""
        self._rotations += 1
        print(f"  [FileLogger]  Rotazione file: '{self._path}' → '{self._path}.{self._rotations}.bak'")
        self._buffer.clear()

    def info(self, message: str):
        entry = f"INFO  | {message}"
        self._buffer.append(entry)
        print(f"  [FileLogger]  {entry} → {self._path}")
        if self._should_rotate():
            self._rotate()

    def error(self, message: str):
        entry = f"ERROR | {message}"
        self._buffer.append(entry)
        print(f"  [FileLogger]  {entry} → {self._path}")

    def flush(self):
        print(f"  [FileLogger]  Flush di {len(self._buffer)} righe su disco. Chiusura handle.")
        self._buffer.clear()


# ==========================================
# 4. PRODOTTI CONCRETI — Famiglia "Cloud"
# ==========================================

class MongoDBConnection(DatabaseConnection):
    """MongoDB con replica set e failover automatico (invariato)."""
    def __init__(self, nodes: list[str], cluster: str, use_ssl: bool, config: ConnectionConfig):
        self._nodes = nodes
        self._cluster = cluster
        self._ssl = use_ssl
        self._config = config
        self._primary: Optional[str] = None

    def _elect_primary(self) -> str:
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


class CloudLogger(Logger):
    """
    Logger che invia i log a un servizio cloud (es. Azure Monitor, Datadog).
    Internamente accumula i log in un batch e li invia via HTTP in blocco,
    gestendo la serializzazione JSON e la chiave API.
    """
    def __init__(self, endpoint: str, api_key: str, batch_size: int = 50):
        self._endpoint = endpoint
        self._api_key = api_key
        self._batch_size = batch_size
        self._batch: list[dict] = []

    def _send_batch(self):
        """Logica privata: serializza il batch in JSON e chiama l'endpoint HTTP."""
        print(f"  [CloudLogger] POST {self._endpoint} — invio {len(self._batch)} eventi (JSON).")
        self._batch.clear()

    def info(self, message: str):
        self._batch.append({"level": "INFO", "msg": message})
        print(f"  [CloudLogger] Accodato INFO: '{message}' (batch: {len(self._batch)}/{self._batch_size})")
        if len(self._batch) >= self._batch_size:
            self._send_batch()

    def error(self, message: str):
        # Gli errori vengono inviati immediatamente, senza aspettare il batch
        self._batch.append({"level": "ERROR", "msg": message})
        print(f"  [CloudLogger] Invio immediato ERROR: '{message}'")
        self._send_batch()

    def flush(self):
        if self._batch:
            print(f"  [CloudLogger] Flush finale: invio {len(self._batch)} eventi residui.")
            self._send_batch()
        print("  [CloudLogger] Connessione all'endpoint chiusa.")


# ==========================================
# 5. PRODOTTI CONCRETI — Famiglia "LocalDev"
# ==========================================

class SQLiteConnection(DatabaseConnection):
    """SQLite con file locking e controllo di integrità (invariato)."""
    def __init__(self, file_path: str, config: ConnectionConfig):
        self._file_path = file_path
        self._config = config
        self._locked = False

    def _acquire_lock(self):
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
        print(f"  [SQLite]  Lock rilasciato, file '{self._file_path}' chiuso.")


class ConsoleLogger(Logger):
    """
    Logger su stdout con prefisso colorato ANSI (tipico di sviluppo locale).
    La complessità qui è la gestione dei codici ANSI e il formatting
    human-readable — inutile in produzione, prezioso in locale.
    """
    RESET  = "\033[0m"
    GREEN  = "\033[92m"
    RED    = "\033[91m"
    GREY   = "\033[90m"

    def info(self, message: str):
        print(f"  [Console] {self.GREEN}INFO {self.RESET} {message}")

    def error(self, message: str):
        print(f"  [Console] {self.RED}ERROR{self.RESET} {message}")

    def flush(self):
        # stdout non ha stato: non c'è nulla da svuotare
        print(f"  [Console] {self.GREY}(flush: stdout non ha buffer da chiudere){self.RESET}")


# ==========================================
# 6. LA ABSTRACT FACTORY
# ==========================================
# Questa è la svolta rispetto al Factory Method: invece di una singola
# factory method `create_database()`, qui abbiamo un'interfaccia che
# dichiara la creazione di TUTTA la famiglia di prodotti correlati.
#
# Ogni factory concreta garantisce che i suoi prodotti siano compatibili
# tra loro: è impossibile ottenere un MySQL di produzione accoppiato
# per errore a un ConsoleLogger di sviluppo.

class InfrastructureFactory(ABC):
    """
    Abstract Factory: definisce il contratto per creare una famiglia
    completa e coerente di componenti infrastrutturali.
    """
    @abstractmethod
    def create_database(self) -> DatabaseConnection:
        pass

    @abstractmethod
    def create_logger(self) -> Logger:
        pass

# Queste sono le factory concrete che rappresentano ciascuna famiglia di prodotti.

class ProductionFactory(InfrastructureFactory):
    """Famiglia Production: MySQL (pool 10) + FileLogger con rotazione."""
    def create_database(self) -> DatabaseConnection:
        config = ConnectionConfig(max_retries=3, timeout_seconds=10, pool_size=10)
        return MySQLConnection("10.0.0.5", "admin", "P@ssw0rd123!", "prod_db", config)

    def create_logger(self) -> Logger:
        return FileLogger("/var/log/app/production.log", max_size_mb=500)


class CloudFactory(InfrastructureFactory):
    """Famiglia Cloud: MongoDB (replica set) + CloudLogger con batching HTTP."""
    def create_database(self) -> DatabaseConnection:
        config = ConnectionConfig(max_retries=5, timeout_seconds=20, pool_size=1)
        nodes = ["mongo-1.cluster.net", "mongo-2.cluster.net", "mongo-3.cluster.net"]
        return MongoDBConnection(nodes, "Cluster-Alpha", use_ssl=True, config=config)

    def create_logger(self) -> Logger:
        return CloudLogger("https://monitor.azure.com/logs/ingest", api_key="az-key-***", batch_size=50)


class LocalDevFactory(InfrastructureFactory):
    """Famiglia LocalDev: SQLite (file lock) + ConsoleLogger colorato."""
    def create_database(self) -> DatabaseConnection:
        config = ConnectionConfig(max_retries=1, timeout_seconds=5, pool_size=1)
        return SQLiteConnection("./dev_data.db", config)

    def create_logger(self) -> Logger:
        return ConsoleLogger()


# ==========================================
# 7. CODICE CLIENT — Application
# ==========================================
# Il client riceve la factory come dipendenza e non sa nulla dei prodotti
# concreti. Lavora ESCLUSIVAMENTE con DatabaseConnection e Logger.
#
# Questo è il vantaggio rispetto al Factory Method: il client ottiene
# un'intera famiglia coerente di oggetti con una sola dipendenza.
# Cambiare ambiente = passare una factory diversa. Zero modifiche al client.

class Application:
    def __init__(self, factory: InfrastructureFactory):
        # La factory costruisce i componenti garantendo la compatibilità
        self._db: DatabaseConnection = factory.create_database()
        self._log: Logger = factory.create_logger()

    def run(self):
        self._log.info("Avvio applicazione.")

        connected = False
        for attempt in range(1, 4):
            self._log.info(f"Tentativo di connessione {attempt}/3...")
            connected = self._db.open()
            if connected:
                break

        if not connected:
            self._log.error("Impossibile connettersi dopo 3 tentativi.")
            self._log.flush()
            return

        result = self._db.query("SELECT version()")
        self._log.info(f"Query eseguita: {result}")

        if self._db.health_check():
            self._log.info("Health check superato. Sistema operativo.")
        else:
            self._log.error("Health check fallito!")

        self._db.close()
        self._log.info("Applicazione terminata correttamente.")
        self._log.flush()


# ==========================================
# 8. ENTRY POINT
# ==========================================
if __name__ == "__main__":
    W = 60

    print("=" * W)
    print("  PRODUZIONE  (MySQL + FileLogger)")
    print("=" * W)
    Application(ProductionFactory()).run()

    print("\n" + "=" * W)
    print("  CLOUD/NoSQL  (MongoDB + CloudLogger)")
    print("=" * W)
    Application(CloudFactory()).run()

    print("\n" + "=" * W)
    print("  SVILUPPO LOCALE  (SQLite + ConsoleLogger)")
    print("=" * W)
    Application(LocalDevFactory()).run()