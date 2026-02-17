from abc import ABC, abstractmethod

# ==========================================
# 1. DEFINIZIONE DEL PRODOTTO (INTERFACCIA)
# ==========================================
# Come abbiamo visto lo scopo di questa classe è definire l'interfaccia comune 
# per tutti i prodotti che la factory può creare. Questa interfaccia verrà poi usata 
# dal client per interagire con i prodotti senza conoscere la loro classe concreta
class Prodotto(ABC):
    @abstractmethod
    def operazione(self) -> str:
        """Ogni prodotto deve saper eseguire un'operazione."""
        pass

# ==========================================
# 2. PRODOTTI CONCRETI (X, Y, Z)
# ==========================================
# Queste classi forniscono implementazioni diverse del metodo operazione().

class ProdottoX(Prodotto):
    def operazione(self) -> str:
        return "Risultato del Prodotto X"

class ProdottoY(Prodotto):
    def operazione(self) -> str:
        return "Risultato del Prodotto Y"

class ProdottoZ(Prodotto):
    def operazione(self) -> str:
        return "Risultato del Prodotto Z"

# ==========================================
# 3. IL CREATORE (LA FACTORY ASTRATTA)
# ==========================================
# Questa qui è la factory astratta che dichiara il factory method, che deve essere implementato
# dalle sottoclassi concrete. Il creatore può anche contenere logica di business che dipende dai prodotti creati, 
# ma non conosce la classe concreta dei prodotti.
class Creatore(ABC):
    @abstractmethod
    def factory_method(self) -> Prodotto:
        """Le sottoclassi implementeranno questo metodo per creare oggetti."""
        pass

    def esegui_business_logic(self):
        """
        Nota: La responsabilità primaria del creatore non è solo creare prodotti,
        ma spesso contiene logica di business che dipende da essi.
        """
        # Chiamiamo il factory method per creare un oggetto Prodotto.
        prodotto = self.factory_method()
        
        # Ora usiamo il prodotto senza sapere esattamente di quale classe sia.
        risultato = prodotto.operazione()
        print(f"Creatore: Ho lavorato con il prodotto e ottenuto: {risultato}")

# ==========================================
# 4. CREATORI CONCRETI
# ==========================================
# Ogni sottoclasse decide quale prodotto istanziare.
# Attenzione: il punto è che il Client userà una factory astratta, istanzierà una sottoclasse concreta, e chiamerà 
# il metodo esegui_business_logic() senza sapere quale prodotto concreto è stato creato. Ma come vediamo al client non 
# interessa dietro le quinte quel che succede, interessa solo il risultato finale.
# In realtà dietro le quinte quel che è successo è che il client ha eseguito la funzione, la quale a sua volta
# ha chiamato il factory method, che ha creato un prodotto concreto (che dipende dalla factory concreta che è stata istanziata),
# a sua volta quel prodotto ha eseguito la sua operazione, e anche qui il metodo operazione
# è stato chiamato senza sapere quale prodotto concreto fosse, e alla fine il risultato è stato stampato.

class CreatoreX(Creatore):
    def factory_method(self) -> Prodotto:
        return ProdottoX()

class CreatoreY(Creatore):
    def factory_method(self) -> Prodotto:
        return ProdottoY()

class CreatoreZ(Creatore):
    def factory_method(self) -> Prodotto:
        return ProdottoZ()

# ==========================================
# 5. CODICE CLIENT
# ==========================================
# Il client lavora con i creatori tramite la loro interfaccia base[cite: 63, 64].

def codice_client(creatore: Creatore):
    print("Client: Non so chi mi ha creato il prodotto, ma so come usarlo.")
    creatore.esegui_business_logic()

if __name__ == "__main__":
    # Per eseguire questo esempio basta:
    # python example.py
    print("--- Avvio con Creatore X ---")
    codice_client(CreatoreX())
    
    print("\n--- Avvio con Creatore Y ---")
    codice_client(CreatoreY())
    
    print("\n--- Avvio con Creatore Z ---")
    codice_client(CreatoreZ())