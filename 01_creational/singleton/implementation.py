# --- SOLUZIONE CON SINGLETON ---

class CassaComuneSingleton:
    _istanza = None  # Campo statico per memorizzare l'unica istanza 

    def __new__(cls):
        # Se l'istanza non esiste ancora, la creiamo 
        if cls._istanza is None:
            print("\n--- Creazione dell'UNICA cassa comune per tutta la gita ---")
            cls._istanza = super(CassaComuneSingleton, cls).__new__(cls)
            cls._istanza.soldi = 100 # Inizializzazione unica 
        return cls._istanza # Restituiamo sempre la stessa istanza

    def paga_gelato(self, importo):
        self.soldi -= importo
        print(f"Pagati {importo}€. Residuo cassa condivisa: {self.soldi}€")

# Studente A prova a creare la cassa
cassa_a = CassaComuneSingleton()
cassa_a.paga_gelato(10)

# Studente B prova a creare la cassa
# Non riceverà un nuovo oggetto, ma quello creato dallo studente A! 
cassa_b = CassaComuneSingleton()
cassa_b.paga_gelato(10)

print(f"Identità oggetto A: {id(cassa_a)}")
print(f"Identità oggetto B: {id(cassa_b)}")
print(f"Entrambi vedono il saldo corretto: {cassa_a.soldi}€") 
# Ora il saldo è 80€ perché entrambi hanno attinto dalla stessa fonte! 