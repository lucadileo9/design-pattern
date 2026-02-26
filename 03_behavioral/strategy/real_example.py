# ==========================================
# STRATEGY — Esempio reale: Pagamento E-commerce
# ==========================================
# Un ordine (Contesto) deve essere pagato. Il metodo di pagamento
# viene scelto dall'utente al momento del checkout (a runtime).
#
# L'ordine non sa COME avviene il pagamento — sa solo che la
# strategia scelta ha un metodo paga() che restituisce True/False.
# Aggiungere "Apple Pay" domani → nuova classe, zero modifiche.

from abc import ABC, abstractmethod
from dataclasses import dataclass


# ==========================================
# STRATEGY — interfaccia comune
# ==========================================

class MetodoPagamento(ABC):
    """Interfaccia: ogni metodo di pagamento implementa paga()."""

    @abstractmethod
    def paga(self, importo: float) -> bool:
        """Esegue il pagamento. Restituisce True se andato a buon fine."""
        ...

    @abstractmethod
    def descrizione(self) -> str:
        """Nome leggibile del metodo di pagamento."""
        ...


# ==========================================
# STRATEGIE CONCRETE
# ==========================================

class CartaDiCredito(MetodoPagamento):
    """Pagamento con carta: valida numero e CVV, contatta il gateway."""

    def __init__(self, numero_carta: str, cvv: str):
        self.numero_carta = numero_carta
        self.cvv = cvv

    def paga(self, importo: float) -> bool:
        # Simulazione: carta valida se ha 16 cifre e cvv 3 cifre
        if len(self.numero_carta) != 16 or len(self.cvv) != 3:
            print(f"  ❌ Carta rifiutata: dati non validi")
            return False

        mascherata = "****-****-****-" + self.numero_carta[-4:]
        print(f"  💳 Contatto gateway bancario...")
        print(f"  💳 Addebito di €{importo:.2f} sulla carta {mascherata}")
        return True

    def descrizione(self) -> str:
        return f"Carta di Credito (****{self.numero_carta[-4:]})"


class PayPal(MetodoPagamento):
    """Pagamento PayPal: verifica email, reindirizza al portale."""

    def __init__(self, email: str):
        self.email = email

    def paga(self, importo: float) -> bool:
        if "@" not in self.email:
            print(f"  ❌ PayPal: email non valida")
            return False

        print(f"  🅿️ Reindirizzamento a PayPal...")
        print(f"  🅿️ Pagamento di €{importo:.2f} confermato da {self.email}")
        return True

    def descrizione(self) -> str:
        return f"PayPal ({self.email})"


class Criptovaluta(MetodoPagamento):
    """Pagamento crypto: genera indirizzo wallet, attende conferma."""

    def __init__(self, wallet: str):
        self.wallet = wallet

    def paga(self, importo: float) -> bool:
        if len(self.wallet) < 10:
            print(f"  ❌ Crypto: indirizzo wallet non valido")
            return False

        indirizzo_corto = self.wallet[:6] + "..." + self.wallet[-4:]
        print(f"  🪙 Invio a wallet {indirizzo_corto}...")
        print(f"  🪙 Transazione di €{importo:.2f} confermata sulla blockchain")
        return True

    def descrizione(self) -> str:
        return f"Crypto ({self.wallet[:6]}...{self.wallet[-4:]})"


# ==========================================
# CONTESTO — l'ordine
# ==========================================
# L'ordine gestisce il carrello e il totale. Quando è il momento
# di pagare, delega alla strategia corrente — senza if/elif.
# Ovviamente non è detto che la classe context si occupi SOLO 
# delle strategie, ma anche di altra logica di business (es. gestione carrello, calcolo totale).

@dataclass
class ArticoloCarrello:
    nome: str
    prezzo: float
    quantita: int = 1


class Ordine:
    """Contesto: gestisce il carrello e delega il pagamento alla strategia."""

    def __init__(self):
        self.articoli: list[ArticoloCarrello] = []
        self._metodo_pagamento: MetodoPagamento | None = None

    def aggiungi(self, nome: str, prezzo: float, quantita: int = 1) -> None:
        self.articoli.append(ArticoloCarrello(nome, prezzo, quantita))

    def get_totale(self) -> float:
        return sum(a.prezzo * a.quantita for a in self.articoli)

    def imposta_pagamento(self, metodo: MetodoPagamento) -> None:
        """L'utente sceglie il metodo di pagamento al checkout."""
        self._metodo_pagamento = metodo

    def paga(self) -> bool:
        """Delega il pagamento alla strategia — zero logica qui dentro."""
        if not self.articoli:
            print("Carrello vuoto!")
            return False

        if self._metodo_pagamento is None:
            print("Nessun metodo di pagamento selezionato!")
            return False

        totale = self.get_totale()
        print(f"\n--- Checkout ---")
        print(f"Totale: €{totale:.2f}")
        print(f"Metodo: {self._metodo_pagamento.descrizione()}")

        successo = self._metodo_pagamento.paga(totale)

        if successo:
            print(f"  ✅ Ordine completato!")
        else:
            print(f"  ⚠️ Pagamento fallito, riprova.")

        return successo


# ==========================================
# UTILIZZO
# ==========================================

if __name__ == "__main__":

    print("=" * 50)
    print("  STRATEGY — Pagamento E-commerce")
    print("=" * 50)

    # --- Scenario 1: pagamento con carta ---
    ordine1 = Ordine()
    ordine1.aggiungi("Tastiera meccanica", 89.99)
    ordine1.aggiungi("Mouse wireless", 34.99)

    ordine1.imposta_pagamento(CartaDiCredito("1234567890123456", "789"))
    ordine1.paga()

    # --- Scenario 2: pagamento con PayPal ---
    ordine2 = Ordine()
    ordine2.aggiungi("Monitor 27\"", 349.00)

    ordine2.imposta_pagamento(PayPal("mario@example.com"))
    ordine2.paga()

    # --- Scenario 3: pagamento con Criptovaluta ---
    ordine3 = Ordine()
    ordine3.aggiungi("SSD 1TB", 79.99)
    ordine3.aggiungi("RAM 16GB", 54.99, 2)

    ordine3.imposta_pagamento(Criptovaluta("0xABCDEF1234567890ABCD"))
    ordine3.paga()

    # --- Scenario 4: carta non valida ---
    ordine4 = Ordine()
    ordine4.aggiungi("Cavo USB-C", 9.99)

    ordine4.imposta_pagamento(CartaDiCredito("123", "7"))   # dati troppo corti
    ordine4.paga()

