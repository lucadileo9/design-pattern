from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

# ==========================================
# 0. CONFIGURATION (CONFIG ISOLATION)
# ==========================================
# In a real app these values would be read from environment variables,
# .env files, or systems like HashiCorp Vault / Azure Key Vault.
# Isolating the config in a dedicated object means that changing it
# doesn't touch the interface or the business logic.

@dataclass
class ConnectionConfig:
    max_retries: int = 3
    timeout_seconds: int = 30
    pool_size: int = 5

# ==========================================
# 1. THE PRODUCT (INTERFACE)
# ==========================================
# The common interface that all databases must implement.
class DatabaseConnection(ABC):
    """
    Common contract that all databases must respect.
    The Creator and the Client work only with this interface.
    """
    @abstractmethod
    def open(self) -> bool:
        """Opens the connection. Returns True if the operation was successful."""
        pass

    @abstractmethod
    def query(self, sql: str) -> str:
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Verifies that the connection is still active and working."""
        pass

    @abstractmethod
    def close(self):
        pass

# ==========================================
# 2. CONCRETE PRODUCTS
# ==========================================
# Each class internally handles very different logic
# (connection pools, primary node election, file locking...),
# but externally exposes only the four interface methods.
# This is the key point: the complexity is *encapsulated* within.

class MySQLConnection(DatabaseConnection):
    """
    Simulates MySQL with an internal connection pool.
    The pool is created and managed privately: nobody outside this
    class needs to know it exists.
    """
    def __init__(self, host: str, user: str, password: str, schema: str, config: ConnectionConfig):
        self._dsn = f"mysql://{user}:***@{host}/{schema}"
        self._config = config
        self._pool: list[str] = []
        self._active = False

    def _init_pool(self):
        """Private logic: populates the pool with N connections."""
        for i in range(self._config.pool_size):
            self._pool.append(f"conn_{i}")
        print(f"[MySQL]  Pool of {self._config.pool_size} connections initialized.")

    def open(self) -> bool:
        print(f"[MySQL]  Connecting to {self._dsn} (timeout {self._config.timeout_seconds}s)...")
        self._init_pool()
        print("[MySQL]  Verifying user permissions... OK.")
        self._active = True
        return True

    def query(self, sql: str) -> str:
        conn = self._pool[0]   # grab a connection from the pool
        return f"[MySQL]  Executing '{sql}' on {conn}."

    def health_check(self) -> bool:
        ok = bool(self._pool) and self._active
        print(f"[MySQL]  Health check pool: {'OK' if ok else 'FAILED'}")
        return ok

    def close(self):
        self._pool.clear()
        self._active = False
        print("[MySQL]  Pool released, connection closed.")


class MongoDBConnection(DatabaseConnection):
    """
    Simulates MongoDB with replica set and automatic failover.
    The primary node election logic is completely hidden.
    """
    def __init__(self, nodes: list[str], cluster: str, use_ssl: bool, config: ConnectionConfig):
        self._nodes = nodes
        self._cluster = cluster
        self._ssl = use_ssl
        self._config = config
        self._primary: Optional[str] = None

    def _elect_primary(self) -> str:
        """
        Private logic: simulates the Raft-like election algorithm of MongoDB.
        In production, it contacts each node, collects votes and chooses the primary.
        """
        elected = self._nodes[0]
        print(f"[MongoDB] Primary election: '{elected}' wins among {len(self._nodes)} nodes.")
        return elected

    def open(self) -> bool:
        ssl_label = "ON" if self._ssl else "OFF"
        print(f"[MongoDB] Connecting to cluster '{self._cluster}' — SSL {ssl_label}...")
        self._primary = self._elect_primary()
        print(f"[MongoDB] Connected to primary: {self._primary}. OK.")
        return True

    def query(self, sql: str) -> str:
        return f"[MongoDB] Translating '{sql}' to BSON aggregation pipeline on {self._primary}."

    def health_check(self) -> bool:
        ok = self._primary is not None
        print(f"[MongoDB] isMaster on '{self._primary}': {'OK' if ok else 'FAILED'}")
        return ok

    def close(self):
        self._primary = None
        print(f"[MongoDB] Disconnected from cluster '{self._cluster}'.")


class SQLiteConnection(DatabaseConnection):
    """
    Simulates SQLite with file locking and integrity checking.
    SQLite uses a file-level lock to guarantee serialized writes.
    """
    def __init__(self, file_path: str, config: ConnectionConfig):
        self._file_path = file_path
        self._config = config
        self._locked = False

    def _acquire_lock(self):
        """Private logic: acquires an exclusive lock on the .db file."""
        self._locked = True
        print(f"[SQLite]  Exclusive lock acquired on '{self._file_path}'.")

    def _integrity_check(self):
        """Private logic: runs PRAGMA integrity_check on the file."""
        print("[SQLite]  PRAGMA integrity_check: OK (0 errors found).")

    def open(self) -> bool:
        print(f"[SQLite]  Opening file: {self._file_path}...")
        self._acquire_lock()
        self._integrity_check()
        return True

    def query(self, sql: str) -> str:
        return f"[SQLite]  Executing on local file: {sql}"

    def health_check(self) -> bool:
        ok = self._locked
        print(f"[SQLite]  File lock active: {'OK' if ok else 'FAILED'}")
        return ok

    def close(self):
        self._locked = False
        print(f"[SQLite]  Lock released, file '{self._file_path}' closed.")


# ==========================================
# 3. THE CREATOR (ABSTRACT FACTORY METHOD)
# ==========================================
class DatabaseManager(ABC):
    """
    The Creator manages high-level business logic.
    It knows nothing about concrete implementations: it only knows that
    a DatabaseConnection exists with which it can open, query, and close.

    Note: the retry logic here is completely generic — it works
    identically for MySQL, MongoDB, and SQLite without a single line
    of database-specific code.
    """
    @abstractmethod
    def create_database(self) -> DatabaseConnection:
        """The actual Factory Method."""
        pass

    def initialize_system(self):
        """
        High-level logic: opens the connection with automatic retry,
        executes a query, and verifies the system status.
        It is completely unaware of which database it's using.
        """
        db = self.create_database()

        # --- Generic retry logic (same for all databases) ---
        connected = False
        for attempt in range(1, 4):
            print(f"\n[Manager] Connection attempt {attempt}/3...")
            connected = db.open()
            if connected:
                break

        if not connected:
            print("[Manager] ERROR: unable to connect after 3 attempts.")
            return

        # --- Business logic, still generic ---
        print(db.query("SELECT version()"))

        if db.health_check():
            print("[Manager] System operational. Connection verified.")

        db.close()


# ==========================================
# 4. CONCRETE FACTORIES (CONFIGURATION MANAGEMENT)
# ==========================================
# Each manager knows how to build its own database with the right parameters.
# If the production configuration changes (e.g. more connections in the pool),
# only this part is modified — the rest of the code is untouched.

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
# 5. CLIENT CODE
# ==========================================
# The client only knows the concrete Managers (knows that different environments exist),
# but never has a direct dependency on MySQLConnection, MongoDBConnection,
# or SQLiteConnection. All the complexity is encapsulated in the previous layers.

if __name__ == "__main__":
    print("=" * 52)
    print("  PRODUCTION ENVIRONMENT (MySQL + connection pool)")
    print("=" * 52)
    ProductionMySQLManager().initialize_system()

    print("\n" + "=" * 52)
    print("  CLOUD/NoSQL ENVIRONMENT (MongoDB + replica set)")
    print("=" * 52)
    CloudMongoManager().initialize_system()

    print("\n" + "=" * 52)
    print("  LOCAL DEVELOPMENT ENVIRONMENT (SQLite + file lock)")
    print("=" * 52)
    LocalDevManager().initialize_system()