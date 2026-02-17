# ==========================================
# PRODOTTI CONCRETI (X, Y, Z)
# ==========================================
# In questo scenario spesso non c'è nemmeno un'interfaccia 
# comune formale, il che rende tutto ancora più fragile.

class ProdottoX:
    def operazione_specifica_x(self):
        return "Risultato del Prodotto X"

class ProdottoY:
    def operazione_diversa_y(self):
        return "Risultato del Prodotto Y"

class ProdottoZ:
    def operazione_z(self):
        return "Risultato del Prodotto Z"

# ==========================================
# IL PROBLEMA: IL CLIENT ACCOPPIATO
# ==========================================
class ApplicazioneClient:
    def esegui_logica(self, tipo_prodotto):
        print(f"Client: Sto provando a creare un prodotto di tipo {tipo_prodotto}")
        
        # --- INIZIO DEL DISASTRO ---
        # Il client deve conoscere tutte le classi concrete.
        # Se aggiungiamo "ProdottoW", dobbiamo modificare questo file e questa funzione.
        if tipo_prodotto == "X":
            prodotto = ProdottoX()
            risultato = prodotto.operazione_specifica_x()
        elif tipo_prodotto == "Y":
            prodotto = ProdottoY()
            risultato = prodotto.operazione_diversa_y()
        elif tipo_prodotto == "Z":
            prodotto = ProdottoZ()
            risultato = prodotto.operazione_z()
        else:
            raise Exception("Tipo di prodotto sconosciuto!")
        # --- FINE DEL DISASTRO ---

        print(f"Risultato ottenuto: {risultato}")

# ==========================================
# UTILIZZO
# ==========================================
# Come vediamo c0è troppo logica nella sezione di esegui_logica(), nonostante ci 
# comportamenti simili c'è tanto codice ripetuto (DRY)
# Inoltre, se vogliamo aggiungere un nuovo tipo di prodotto, dobbiamo modificare questa funzione, il che viola il principio di Open/Closed.
if __name__ == "__main__":
    app = ApplicazioneClient()
    
    # Per ogni nuovo tipo di prodotto, il client deve essere informato 
    # e il codice sopra deve essere cambiato.
    app.esegui_logica("X")
    app.esegui_logica("Y")
    app.esegui_logica("Z")