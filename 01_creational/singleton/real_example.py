import threading
import time

# =======================================================================
# CONTEXT: why does the Singleton exist in this example?
# =======================================================================
# A connection pool is an expensive resource: opening connections to a DB
# requires network handshakes, authentication, memory allocation.
# If every part of the application created its own, we'd have
# dozens of separate pools consuming resources needlessly.
#
# The solution: there exists ONE SINGLE pool shared by the entire app.
# Whoever requests it always gets the same object — never a copy.
# This is exactly the Singleton's job.
# =======================================================================


# ==========================================
# PHASE 1 — THE BASIC SINGLETON MECHANISM
# ==========================================
# In Python, when you write   obj = MyClass()   two methods are called
# in sequence:
#
#   1. __new__(cls)  → CREATES the object in memory, called before __init__ automatically
#   2. __init__(self) → INITIALIZES the already created object (typically overridden by the developer)
#
# Usually you don't touch __new__ and Python handles it on its own.
# In the Singleton we override it to INTERCEPT the creation
# and always return the same instance instead of creating a new one.
#
# _instance is a CLASS attribute, being shared
# by all and acts as "memory" — it remembers if the object already exists.

class DatabaseConnectionPool:

    _instance = None          # No pool created yet
    _lock = threading.Lock()  # Protects creation in multi-thread contexts

    def __new__(cls):
        # ---------------------------------------------------------------
        # Every time someone writes DatabaseConnectionPool(),
        # Python passes through here BEFORE doing anything else.
        #
        # If _instance is None → it's the first time, we create the object.
        # If _instance already exists → we return the existing one, stop.
        # ---------------------------------------------------------------
        # 1st check
        if cls._instance is None:
            with cls._lock:
                # 2nd check — inside the lock: another thread might have
                # already created the instance in the moment between the first check
                # and acquiring the lock. We recheck for safety.
                if cls._instance is None:
                    print("[Pool] First call: creating the pool and opening connections.")
                    # super().__new__(cls) is the "normal" call that Python would make
                    # if we hadn't overridden __new__. We call it ourselves
                    # explicitly ONE time only, and save the result.
                    cls._instance = super().__new__(cls)

                    # Initialize the pool state (done only once)
                    cls._instance.available_connections = ["Conn_1", "Conn_2", "Conn_3"]
                    cls._instance.in_use_connections = []

        # In both cases, we ALWAYS return the same instance
        return cls._instance

    # -------------------------------------------------------
    # Business methods of the pool (unrelated to the Singleton)
    # -------------------------------------------------------

    def get_connection(self):
        with self._lock:  # This ensures that only one thread at a time modifies the lists
            if not self.available_connections:
                print("[Pool] WARNING: no free connections, try again later.")
                return None
            conn = self.available_connections.pop()
            self.in_use_connections.append(conn)
            print(f"[Pool] Provided {conn} | Available: {len(self.available_connections)} | In use: {len(self.in_use_connections)}")
            return conn

    def release_connection(self, conn):
        with self._lock:  # Here too, we protect the list modification with the lock
            self.in_use_connections.remove(conn)
            self.available_connections.append(conn)
            print(f"[Pool] Released {conn} | Available: {len(self.available_connections)} | In use: {len(self.in_use_connections)}")


# ==========================================
# PHASE 2 — VERIFYING IT'S TRULY A SINGLE INSTANCE
# ==========================================
# We create the pool from three different "places" in the application.
# We expect them all to be the same object in memory.

print("=" * 55)
print("  PHASE 2 — Verifying instance uniqueness")
print("=" * 55)

pool_from_auth_module    = DatabaseConnectionPool()  # creates the pool
pool_from_report_module  = DatabaseConnectionPool()  # gets the same one
pool_from_api_module     = DatabaseConnectionPool()  # gets the same one

# `is` compares memory addresses, not values
print(f"auth   is report : {pool_from_auth_module is pool_from_report_module}")   # True
print(f"report is api    : {pool_from_report_module is pool_from_api_module}")     # True
print(f"id auth   : {id(pool_from_auth_module)}")
print(f"id report : {id(pool_from_report_module)}")
print(f"id api    : {id(pool_from_api_module)}")


# ==========================================
# PHASE 3 — THE PROBLEM: MULTITHREADING
# ==========================================
# In a real application, multiple threads start concurrently.
# Without precautions, two threads could both read
# cls._instance is None → True at the same moment, and create
# TWO distinct pools — breaking the Singleton's uniqueness.
#
# The solution is "double-checked locking":
#
#   1st check → without lock (fast): if the instance already exists,
#               most threads exit immediately.
#   lock      → only if the instance doesn't exist yet, acquires
#               the lock to block other threads.
#   2nd check → inside the lock: rechecks because another thread
#               might have created the instance in the moment between
#               the 1st check and acquiring the lock.
#
#  In the __new__ function the two `if cls._instance is None`
# are exactly these two checks.

print("\n" + "=" * 55)
print("  PHASE 3 — Simulation with 5 concurrent threads")
print("=" * 55)

def thread_work(thread_id):
    # Each thread executes this function independently and concurrently.

    # The call DatabaseConnectionPool() tries to create a new pool,
    # but the __new__ we overrode intercepts the call
    # and always returns only cls._instance — the same object for everyone.
    pool = DatabaseConnectionPool()

    # We verify that each thread received EXACTLY the same object
    # in memory: id() returns the RAM address of the instance.
    # All threads will print the same number → same instance.
    print(f"[Thread-{thread_id}] pool id: {id(pool)}")

    # Each thread tries to get a connection from the shared pool.
    # get_connection() uses the lock internally, so here too
    # there are no race conditions: only one thread at a time modifies
    # the available_connections / in_use_connections lists.
    conn = pool.get_connection()
    if conn:
        time.sleep(0.5)  # simulates query execution time
        # After finishing, the connection is returned to the pool
        # so other waiting threads can use it.
        pool.release_connection(conn)

# We create 5 threads that start almost simultaneously.
# This is the critical case: all 5 will call DatabaseConnectionPool()
# at the same moment, and without double-checked locking they could
# create duplicate instances. With the lock, only the first one creates — the others wait
# and then find cls._instance already set.
threads = [threading.Thread(target=thread_work, args=(i,)) for i in range(5)]
for t in threads:
    t.start()   # starts the thread (asynchronous execution from here on)
for t in threads:
    t.join()    # waits for ALL threads to finish before proceeding

print("\nAll threads used the same pool.")
# We call DatabaseConnectionPool() one last time just to read the state.
# It creates nothing — it returns as always the already existing instance.
print(f"Available connections at the end: {DatabaseConnectionPool().available_connections}")