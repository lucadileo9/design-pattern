import threading
import time

# =======================================================================
# CONTESTO: perché esiste il Singleton in questo esempio?
# =======================================================================
# Un connection pool è una risorsa costosa: aprire connessioni a un DB
# richiede handshake di rete, autenticazione, allocazione di memoria.
# Se ogni parte dell'applicazione ne creasse uno proprio, avremmo
# decine di pool separati che consumano risorse inutilmente.
#
# La soluzione: esiste UN SOLO pool condiviso da tutta l'app.
# Chiunque lo chieda ottiene sempre lo stesso oggetto — mai una copia.
# Questo è esattamente il compito del Singleton.
# =======================================================================


# ==========================================
# FASE 1 — IL MECCANISMO BASE DEL SINGLETON
# ==========================================
# In Python, quando scrivi   obj = MiaClasse()   vengono chiamati
# due metodi in sequenza:
#
#   1. __new__(cls)  → CREA l'oggetto in memoria, chiamato prima di __init__ in automatico
#   2. __init__(self) → INIZIALIZZA l'oggetto già creato (tipicamente sovrascritto dallo sviluppatore)
#
# Di solito non si tocca __new__ e Python lo gestisce da solo.
# Nel Singleton lo sovrascriviamo per INTERCETTARE la creazione
# e restituire sempre la stessa istanza invece di crearne una nuova.
#
# _istanza è un attributo di CLASSE, essendo condiviso
# da tutti e funge da "memoria" — ricorda se l'oggetto esiste già.

class DatabaseConnectionPool:

    _istanza = None          # Nessun pool ancora creato
    _lock = threading.Lock() # Protegge la creazione in contesti multi-thread

    def __new__(cls):
        # ---------------------------------------------------------------
        # Ogni volta che qualcuno scrive DatabaseConnectionPool(),
        # Python passa di qui PRIMA di fare qualsiasi altra cosa.
        #
        # Se _istanza è None → è la prima volta, creiamo l'oggetto.
        # Se _istanza esiste già → restituiamo quello esistente, stop.
        # ---------------------------------------------------------------
        # 1° check 
        if cls._istanza is None:
            with cls._lock:
                # 2° check — dentro il lock: un altro thread potrebbe aver
                # già creato l'istanza nell'attimo tra il primo controllo
                # e l'acquisizione del lock. Ricontrolliamo per sicurezza.
                if cls._istanza is None:
                    print("[Pool] Prima chiamata: creo il pool e apro le connessioni.")
                    # super().__new__(cls) è la chiamata "normale" che Python farebbe
                    # se non avessimo sovrascritto __new__. La chiamiamo noi
                    # esplicitamente UNA sola volta, e salviamo il risultato.
                    cls._istanza = super().__new__(cls)

                    # Inizializziamo lo stato del pool (fatto una volta sola)
                    cls._istanza.connessioni_disponibili = ["Conn_1", "Conn_2", "Conn_3"]
                    cls._istanza.connessioni_in_uso = []

        # In entrambi i casi, restituiamo SEMPRE la stessa istanza
        return cls._istanza

    # -------------------------------------------------------
    # I metodi di business del pool (non c'entrano col Singleton)
    # -------------------------------------------------------

    def ottieni_connessione(self):
        with self._lock: # Questo mi assicura che solo un thread alla volta modifichi le liste
            if not self.connessioni_disponibili:
                print("[Pool] ATTENZIONE: nessuna connessione libera, riprova più tardi.")
                return None
            conn = self.connessioni_disponibili.pop()
            self.connessioni_in_uso.append(conn)
            print(f"[Pool] Erogata {conn} | Libere: {len(self.connessioni_disponibili)} | In uso: {len(self.connessioni_in_uso)}")
            return conn

    def rilascia_connessione(self, conn):
        with self._lock: # Anche qui, proteggiamo la modifica delle liste con il lock
            self.connessioni_in_uso.remove(conn)
            self.connessioni_disponibili.append(conn)
            print(f"[Pool] Rilasciata {conn} | Libere: {len(self.connessioni_disponibili)} | In uso: {len(self.connessioni_in_uso)}")


# ==========================================
# FASE 2 — VERIFICA CHE SIA DAVVERO UNA SOLA ISTANZA
# ==========================================
# Creiamo il pool da tre "luoghi" diversi dell'applicazione.
# Ci aspettiamo che siano tutti lo stesso oggetto in memoria.

print("=" * 55)
print("  FASE 2 — Verifica unicità dell'istanza")
print("=" * 55)

pool_dal_modulo_auth    = DatabaseConnectionPool()  # crea il pool
pool_dal_modulo_report  = DatabaseConnectionPool()  # ottiene lo stesso
pool_dal_modulo_api     = DatabaseConnectionPool()  # ottiene lo stesso

# is confronta gli indirizzi in memoria, non i valori
print(f"auth   is report : {pool_dal_modulo_auth is pool_dal_modulo_report}")   # True
print(f"report is api    : {pool_dal_modulo_report is pool_dal_modulo_api}")     # True
print(f"id auth   : {id(pool_dal_modulo_auth)}")
print(f"id report : {id(pool_dal_modulo_report)}")
print(f"id api    : {id(pool_dal_modulo_api)}")


# ==========================================
# FASE 3 — PROBLEMA: IL MULTITHREADING
# ==========================================
# In un'applicazione reale più thread partono contemporaneamente.
# Senza precauzioni, due thread potrebbero entrambi leggere
# cls._istanza is None → True nello stesso istante, e creare
# DUE pool distinti — rompendo l'unicità del Singleton.
#
# La soluzione è il "double-checked locking":
#
#   1° check  → senza lock (veloce): se l'istanza esiste già,
#               la maggior parte dei thread esce subito.
#   lock      → solo se l'istanza non esiste ancora, acquisisce
#               il lock per bloccare gli altri thread.
#   2° check  → dentro il lock: ricontrolla perché un altro thread
#               potrebbe aver creato l'istanza nell'attimo tra
#               il 1° check e l'acquisizione del lock.
#
#  Nella funzione __new__ i due `if cls._istanza is None`
# sono esattamente questi due controlli.

print("\n" + "=" * 55)
print("  FASE 3 — Simulazione con 5 thread concorrenti")
print("=" * 55)

def lavoro_thread(id_thread):
    # Ogni thread esegue questa funzione in modo indipendente e concorrente.

    # La chiamata DatabaseConnectionPool() vuole creare un nuovo pool,
    # ma il __new__ che abbiamo sovrascritto intercetta la chiamata
    # e restituisce sempre e solo cls._istanza — lo stesso oggetto per tutti.
    pool = DatabaseConnectionPool()

    # Verifichiamo che ogni thread abbia ricevuto ESATTAMENTE lo stesso oggetto
    # in memoria: id() restituisce l'indirizzo RAM dell'istanza.
    # Tutti i thread stamperanno lo stesso numero → stessa istanza.
    print(f"[Thread-{id_thread}] pool id: {id(pool)}")

    # Ogni thread tenta di prendere una connessione dal pool condiviso.
    # ottieni_connessione() usa il lock internamente, quindi anche qui
    # non ci sono race condition: un solo thread alla volta modifica
    # le liste connessioni_disponibili / connessioni_in_uso.
    conn = pool.ottieni_connessione()
    if conn:
        time.sleep(0.5)  # simula il tempo di esecuzione di una query
        # Dopo aver finito, la connessione viene restituita al pool
        # così gli altri thread in attesa possono usarla.
        pool.rilascia_connessione(conn)

# Creiamo 5 thread che partono quasi simultaneamente.
# È questo il caso critico: tutti e 5 chiameranno DatabaseConnectionPool()
# nello stesso istante, e senza il double-checked locking potrebbero
# creare istanze duplicate. Con il lock, solo il primo crea — gli altri aspettano
# e poi trovano cls._istanza già valorizzata.
threads = [threading.Thread(target=lavoro_thread, args=(i,)) for i in range(5)]
for t in threads:
    t.start()   # avvia il thread (esecuzione asincrona da qui in poi)
for t in threads:
    t.join()    # aspetta che TUTTI i thread abbiano finito prima di proseguire

print("\nTutti i thread hanno usato lo stesso pool.")
# Chiamiamo DatabaseConnectionPool() un'ultima volta solo per leggere lo stato.
# Non crea nulla — restituisce come sempre l'istanza già esistente.
print(f"Connessioni libere alla fine: {DatabaseConnectionPool().connessioni_disponibili}")