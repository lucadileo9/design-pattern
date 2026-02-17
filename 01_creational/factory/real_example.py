from abc import ABC, abstractmethod

# ==========================================
# 1. IL PRODOTTO (INTERFACCIA)
# ==========================================
# Qui stiamo definindo l'interfaccia comune che tutti i database devono implementare.
class DatabaseConnection(ABC):
    """
    Tutti i database devono seguire questa interfaccia comune. 
    """
    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def query(self, sql):
        pass

# ==========================================
# 2. PRODOTTI CONCRETI (SIMULAZIONE LOGICA)
# ==========================================
# Qui definiamo le classi concrete che implementano l'interfaccia DatabaseConnection.
# Ovviamente in uno scenario davvero reale ci sarebbero molte più complessità, come gestione di pool di connessioni, error handling, supporto a transazioni, ecc.

class MySQLConnection(DatabaseConnection):
    def __init__(self, host, user, password, schema):
        self.connection_string = f"mysql://{user}:{password}@{host}/{schema}"

    def open(self):
        # Simula l'handshake e la verifica delle credenziali 
        print(f"[MySQL] Connessione in corso a {self.connection_string}...")
        print("[MySQL] Verifica permessi utente... OK.")

    def query(self, sql):
        return f"[MySQL] Eseguo query relazionale: {sql}"

class MongoDBConnection(DatabaseConnection):
    def __init__(self, uri, cluster, use_ssl=True):
        self.uri = uri
        self.cluster = cluster
        self.ssl_status = "abilitato" if use_ssl else "disabilitato"

    def open(self):
        # Simula l'inizializzazione di un driver NoSQL 
        print(f"[MongoDB] Connessione al cluster '{self.cluster}' via {self.uri}...")
        print(f"[MongoDB] Protocollo SSL {self.ssl_status}... OK.")

    def query(self, sql):
        return f"[MongoDB] Mappatura query SQL '{sql}' in formato BSON/Document..."

class SQLiteConnection(DatabaseConnection):
    def __init__(self, file_path):
        self.file_path = file_path

    def open(self):
        # Simula l'apertura di un file locale [cite: 83]
        print(f"[SQLite] Apertura file database in: {self.file_path}...")
        print("[SQLite] Controllo integrità file... OK.")

    def query(self, sql):
        return f"[SQLite] Eseguo query leggera su file locale: {sql}"

# ==========================================
# 3. IL CREATORE (ABSTRACT FACTORY METHOD)
# ==========================================
class DatabaseManager(ABC):
    """
    Il 'Creator' non si occupa solo di creare, ma gestisce la 
    logica di business core legata ai prodotti.
    """
    @abstractmethod
    def create_database(self) -> DatabaseConnection:
        """Il Factory Method vero e proprio. """
        pass

    def initialize_system(self):
        """
        Logica di alto livello: il sistema non sa QUALE db sta usando,
        sa solo che deve aprirlo e fare una query iniziale. 
        """
        db = self.create_database()
        db.open()
        print(db.query("SELECT version()"))

# ==========================================
# 4. FACTORY CONCRETE (GESTIONE CONFIGURAZIONE)
# ==========================================
# Ovviamente in un'app reale, ogni manager potrebbe avere una logica di creazione più complessa, 
# magari con lettura di configurazioni da file, gestione di errori, pool di connessioni, ecc.
class ProductionMySQLManager(DatabaseManager):
    def create_database(self) -> DatabaseConnection:
        # Qui simuliamo la lettura da un file .env o vault aziendale [cite: 63, 101]
        return MySQLConnection("10.0.0.5", "admin", "P@ssw0rd123!", "prod_db")

class CloudMongoManager(DatabaseManager):
    def create_database(self) -> DatabaseConnection:
        # Configurazione specifica per Atlas/Cloud
        return MongoDBConnection("mongodb+srv://main-node", "Cluster-Alpha", use_ssl=True)

class LocalDevManager(DatabaseManager):
    def create_database(self) -> DatabaseConnection:
        # Configurazione per ambiente di sviluppo locale
        return SQLiteConnection("./dev_data.db")

# ==========================================
# 5. CODICE CLIENT
# ==========================================
if __name__ == "__main__":
    # Qui è importante notare che il codice client non ha alcuna dipendenza diretta con le classi concrete dei database.
    # Quello che lui sa è solo quale database manager usare, e da lì in poi è tutto astratto.
    # Egli chiama il metodo 'initialize_system' che è definito nell'abstract creator, questo metodo poi
    
    # chiama il factory method 'create_database' che è implementato in maniera diversa nei vari manager concreti.
    # In particolare ogni manager concreto ritorna un'istanza di un database diverso

    # poi torniamo nel metodo 'initialize_system' che userà l'istanza di database ritornata per
    # aprire la connessione e fare una query, senza sapere che tipo di database sta effettivamente usando.
    
    
    print("--- AMBIENTE PRODUZIONE ---")
    app_prod = ProductionMySQLManager()
    app_prod.initialize_system()

    print("\n--- AMBIENTE CLOUD/NOSQL ---")
    app_cloud = CloudMongoManager()
    app_cloud.initialize_system()