from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

# =======================================================================
# COMPARISON WITH THE FACTORY METHOD
# =======================================================================
# In the Factory Method we had ONE single type of product (DatabaseConnection)
# and one factory for each of its concrete types.
#
# The problem that arises is this: in reality an application never
# uses just a database — it needs an entire coherent infrastructure:
# a database, a logger, maybe a cache.
#
# If we used the Factory Method for each one, nothing would guarantee that
# the chosen logger is compatible with the chosen database.
# For example: what prevents us from mixing a MySQLConnection (production)
# with a ConsoleLogger (local development)?
#
# The Abstract Factory solves this: it groups RELATED products into
# families, and guarantees that whoever creates the database also creates
# the right logger for that environment. Consistency is enforced at the architectural level.
# =======================================================================


# ==========================================
# 0. CONFIGURATION
# ==========================================
@dataclass
class ConnectionConfig:
    max_retries: int = 3
    timeout_seconds: int = 30
    pool_size: int = 5


# ==========================================
# 1. PRODUCT A — DatabaseConnection
# ==========================================
# Same interface as the Factory Method. Nothing changes here:
# the Abstract Factory reuses already known products and groups them into families.

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
# 2. PRODUCT B — Logger
# ==========================================
# This is the second type of product in the family.
# Each environment uses a radically different logging strategy:
# rotating file in production, HTTP calls in cloud, stdout in local.
# But externally they all expose the exact same interface.

class Logger(ABC):
    @abstractmethod
    def info(self, message: str):
        pass

    @abstractmethod
    def error(self, message: str):
        pass

    @abstractmethod
    def flush(self):
        """Flushes and closes the logger's output channel."""
        pass


# ==========================================
# 3. CONCRETE PRODUCTS — "Production" Family
# N.B. Each family includes both products: DatabaseConnection + Logger.
# This family will then be managed by a concrete factory that creates both
# and therefore represents the family itself.
# ==========================================

class MySQLConnection(DatabaseConnection):
    """MySQL with internal connection pool (unchanged from the Factory Method)."""
    def __init__(self, host: str, user: str, password: str, schema: str, config: ConnectionConfig):
        self._dsn = f"mysql://{user}:***@{host}/{schema}"
        self._config = config
        self._pool: list[str] = []
        self._active = False

    def _init_pool(self):
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
        conn = self._pool[0]   # get a connection from the pool
        return f"[MySQL]  Executing '{sql}' on {conn}."

    def health_check(self) -> bool:
        ok = bool(self._pool) and self._active
        print(f"[MySQL]  Health check pool: {'OK' if ok else 'FAILED'}")
        return ok

    def close(self):
        self._pool.clear()
        self._active = False
        print("[MySQL]  Pool released, connection closed.")


class FileLogger(Logger):
    """
    File logger with automatic rotation (typical of production).
    Internally manages the write buffer and file rotation
    when it exceeds a certain size — all hidden from the outside.
    """
    def __init__(self, log_path: str, max_size_mb: int = 100):
        self._path = log_path
        self._max_size_mb = max_size_mb
        self._buffer: list[str] = []
        self._rotations = 0

    def _should_rotate(self) -> bool:
        """Private logic: checks if the file exceeds the threshold."""
        return len(self._buffer) > 5  # simplified simulation

    def _rotate(self):
        """Private logic: renames the current file and opens a new one."""
        self._rotations += 1
        print(f"  [FileLogger]  File rotation: '{self._path}' → '{self._path}.{self._rotations}.bak'")
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
        print(f"  [FileLogger]  Flushing {len(self._buffer)} lines to disk. Closing handle.")
        self._buffer.clear()


# ==========================================
# 4. CONCRETE PRODUCTS — "Cloud" Family
# ==========================================

class MongoDBConnection(DatabaseConnection):
    """MongoDB with replica set and automatic failover (unchanged)."""
    def __init__(self, nodes: list[str], cluster: str, use_ssl: bool, config: ConnectionConfig):
        self._nodes = nodes
        self._cluster = cluster
        self._ssl = use_ssl
        self._config = config
        self._primary: Optional[str] = None

    def _elect_primary(self) -> str:
        elected = self._nodes[0]
        print(f"[MongoDB] Primary election: '{elected}' wins over {len(self._nodes)} nodes.")
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


class CloudLogger(Logger):
    """
    Logger that sends logs to a cloud service (e.g. Azure Monitor, Datadog).
    Internally accumulates logs into a batch and sends them via HTTP in bulk,
    managing JSON serialization and the API key.
    """
    def __init__(self, endpoint: str, api_key: str, batch_size: int = 50):
        self._endpoint = endpoint
        self._api_key = api_key
        self._batch_size = batch_size
        self._batch: list[dict] = []

    def _send_batch(self):
        """Private logic: serializes the batch to JSON and calls the HTTP endpoint."""
        print(f"  [CloudLogger] POST {self._endpoint} — sending {len(self._batch)} events (JSON).")
        self._batch.clear()

    def info(self, message: str):
        self._batch.append({"level": "INFO", "msg": message})
        print(f"  [CloudLogger] Enqueued INFO: '{message}' (batch: {len(self._batch)}/{self._batch_size})")
        if len(self._batch) >= self._batch_size:
            self._send_batch()

    def error(self, message: str):
        # Errors are sent immediately, without waiting for the batch
        self._batch.append({"level": "ERROR", "msg": message})
        print(f"  [CloudLogger] Immediate send ERROR: '{message}'")
        self._send_batch()

    def flush(self):
        if self._batch:
            print(f"  [CloudLogger] Final flush: sending {len(self._batch)} remaining events.")
            self._send_batch()
        print("  [CloudLogger] Connection to endpoint closed.")


# ==========================================
# 5. CONCRETE PRODUCTS — "LocalDev" Family
# ==========================================

class SQLiteConnection(DatabaseConnection):
    """SQLite with file locking and integrity check (unchanged)."""
    def __init__(self, file_path: str, config: ConnectionConfig):
        self._file_path = file_path
        self._config = config
        self._locked = False

    def _acquire_lock(self):
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
        print(f"  [SQLite]  Lock released, file '{self._file_path}' closed.")


class ConsoleLogger(Logger):
    """
    Logger to stdout with ANSI colored prefix (typical of local development).
    The complexity here is managing ANSI codes and human-readable
    formatting — useless in production, valuable locally.
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
        # stdout has no state: there's nothing to flush
        print(f"  [Console] {self.GREY}(flush: stdout has no buffer to close){self.RESET}")


# ==========================================
# 6. THE ABSTRACT FACTORY
# ==========================================
# This is the turning point compared to the Factory Method: instead of a single
# factory method `create_database()`, here we have an interface that
# declares the creation of the ENTIRE family of related products.
#
# Each concrete factory guarantees that its products are compatible
# with each other: it's impossible to get a production MySQL accidentally
# coupled with a development ConsoleLogger.

class InfrastructureFactory(ABC):
    """
    Abstract Factory: defines the contract for creating a complete
    and coherent family of infrastructure components.
    """
    @abstractmethod
    def create_database(self) -> DatabaseConnection:
        pass

    @abstractmethod
    def create_logger(self) -> Logger:
        pass

# These are the concrete factories that represent each product family.

class ProductionFactory(InfrastructureFactory):
    """Production family: MySQL (pool 10) + FileLogger with rotation."""
    def create_database(self) -> DatabaseConnection:
        config = ConnectionConfig(max_retries=3, timeout_seconds=10, pool_size=10)
        return MySQLConnection("10.0.0.5", "admin", "P@ssw0rd123!", "prod_db", config)

    def create_logger(self) -> Logger:
        return FileLogger("/var/log/app/production.log", max_size_mb=500)


class CloudFactory(InfrastructureFactory):
    """Cloud family: MongoDB (replica set) + CloudLogger with HTTP batching."""
    def create_database(self) -> DatabaseConnection:
        config = ConnectionConfig(max_retries=5, timeout_seconds=20, pool_size=1)
        nodes = ["mongo-1.cluster.net", "mongo-2.cluster.net", "mongo-3.cluster.net"]
        return MongoDBConnection(nodes, "Cluster-Alpha", use_ssl=True, config=config)

    def create_logger(self) -> Logger:
        return CloudLogger("https://monitor.azure.com/logs/ingest", api_key="az-key-***", batch_size=50)


class LocalDevFactory(InfrastructureFactory):
    """LocalDev family: SQLite (file lock) + colored ConsoleLogger."""
    def create_database(self) -> DatabaseConnection:
        config = ConnectionConfig(max_retries=1, timeout_seconds=5, pool_size=1)
        return SQLiteConnection("./dev_data.db", config)

    def create_logger(self) -> Logger:
        return ConsoleLogger()


# ==========================================
# 7. CLIENT CODE — Application
# ==========================================
# The client receives the factory as a dependency and knows nothing about
# the concrete products. It works EXCLUSIVELY with DatabaseConnection and Logger.
#
# This is the advantage over the Factory Method: the client gets
# an entire coherent family of objects with a single dependency.
# Changing environment = passing a different factory. Zero changes to client.

class Application:
    def __init__(self, factory: InfrastructureFactory):
        # The factory builds the components guaranteeing compatibility
        self._db: DatabaseConnection = factory.create_database()
        self._log: Logger = factory.create_logger()

    def run(self):
        self._log.info("Starting application.")

        connected = False
        for attempt in range(1, 4):
            self._log.info(f"Connection attempt {attempt}/3...")
            connected = self._db.open()
            if connected:
                break

        if not connected:
            self._log.error("Unable to connect after 3 attempts.")
            self._log.flush()
            return

        result = self._db.query("SELECT version()")
        self._log.info(f"Query executed: {result}")

        if self._db.health_check():
            self._log.info("Health check passed. System operational.")
        else:
            self._log.error("Health check failed!")

        self._db.close()
        self._log.info("Application terminated correctly.")
        self._log.flush()


# ==========================================
# 8. ENTRY POINT
# ==========================================
if __name__ == "__main__":
    W = 60

    print("=" * W)
    print("  PRODUCTION  (MySQL + FileLogger)")
    print("=" * W)
    Application(ProductionFactory()).run()

    print("\n" + "=" * W)
    print("  CLOUD/NoSQL  (MongoDB + CloudLogger)")
    print("=" * W)
    Application(CloudFactory()).run()

    print("\n" + "=" * W)
    print("  LOCAL DEVELOPMENT  (SQLite + ConsoleLogger)")
    print("=" * W)
    Application(LocalDevFactory()).run()