# --- CODICE PROBLEMATICO (SENZA SINGLETON) ---

class CassaComune:
    def __init__(self):
        self.soldi = 100  # Budget iniziale della gita
        print("Aperta una nuova cassa comune!")

    def paga_gelato(self, importo):
        self.soldi -= importo
        print(f"Pagati {importo}€. Residuo in questa cassa: {self.soldi}€")

# Studente A vuole pagare un gelato
cassa_studente_a = CassaComune() 
cassa_studente_a.paga_gelato(10)

# Studente B vuole pagare un gelato
# PROBLEMA: Lo studente B crea una NUOVA cassa invece di usare la stessa! [cite: 8, 10]
cassa_studente_b = CassaComune() 
cassa_studente_b.paga_gelato(10)

print(f"Lo studente A vede in cassa: {cassa_studente_a.soldi}€")
print(f"Lo studente B vede in cassa: {cassa_studente_b.soldi}€")
# Risultato: I soldi non sono stati scalati dalla stessa fonte. Abbiamo un'incoerenza.