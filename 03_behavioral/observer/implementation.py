# ==========================================
# OBSERVER PATTERN — SOLUZIONE
# ==========================================
# Invece di far controllare i clienti ripetutamente (polling),
# è il NEGOZIO a notificare i clienti quando arriva un prodotto.
#
# Il negozio (Subject) mantiene una lista di clienti registrati
# (Observer) e chiama il loro metodo aggiorna() automaticamente
# quando aggiunge un nuovo prodotto al magazzino.
#
# I clienti non devono più fare nulla: si registrano una volta
# e vengono avvisati solo quando serve.

from abc import ABC, abstractmethod


# ==========================================
# OBSERVER — interfaccia comune
# ==========================================
# Tutti gli observer implementano aggiorna(). Il Subject non
# conosce i dettagli — sa solo che può chiamare questo metodo.

class Observer(ABC):
    """Interfaccia per chi vuole essere notificato dal negozio."""

    @abstractmethod
    def aggiorna(self, prodotto: str) -> None:
        """Chiamato dal Subject quando arriva un nuovo prodotto."""
        ...


# ==========================================
# SUBJECT — il negozio che notifica
# ==========================================
# Il negozio mantiene una lista di observer e li avvisa
# automaticamente ogni volta che arriva un nuovo prodotto.
# Non sa chi sono, non gli interessa — chiama aggiorna() e basta.

class Negozio:
    """Subject: gestisce il magazzino e notifica gli observer."""

    def __init__(self, nome: str):
        self.nome = nome
        self.prodotti_disponibili: list[str] = []
        self._observer: list[Observer] = []

    # --- Gestione observer ---

    def registra(self, observer: Observer) -> None:
        """Un cliente si iscrive alle notifiche."""
        self._observer.append(observer)

    def rimuovi(self, observer: Observer) -> None:
        """Un cliente si cancella dalle notifiche."""
        self._observer.remove(observer)

    # --- Logica di business ---

    def aggiungi_prodotto(self, prodotto: str) -> None:
        """Aggiunge un prodotto e NOTIFICA tutti gli observer."""
        self.prodotti_disponibili.append(prodotto)
        print(f"[{self.nome}] Nuovo prodotto in magazzino: '{prodotto}'")
        self._notifica(prodotto)

    def _notifica(self, prodotto: str) -> None:
        """Chiama aggiorna() su ogni observer registrato."""
        for observer in self._observer:
            observer.aggiorna(prodotto)


# ==========================================
# OBSERVER CONCRETI — i clienti
# ==========================================
# Ogni cliente reagisce alla notifica a modo suo.
# Il negozio non sa cosa fanno — chiama aggiorna() e basta.

class Cliente(Observer):
    """Un cliente interessato a un prodotto specifico."""

    def __init__(self, nome: str, prodotto_desiderato: str):
        self.nome = nome
        self.prodotto_desiderato = prodotto_desiderato

    def aggiorna(self, prodotto: str) -> None:
        """Reagisce solo se il prodotto è quello che aspetta."""
        if prodotto == self.prodotto_desiderato:
            print(f"  [{self.nome}] Il '{prodotto}' è arrivato! Vado a comprarlo!")
        else:
            print(f"  [{self.nome}] '{prodotto}'? Non mi interessa.")

# N.B.: si tratta solamente di un altro osservatore, ma con un metodo di aggiornamento diverso
class Rivenditore(Observer):
    """Un rivenditore che vuole sapere di TUTTI i nuovi arrivi."""

    def __init__(self, nome: str):
        self.nome = nome
        self.prodotti_visti: list[str] = []

    def aggiorna(self, prodotto: str) -> None:
        """Prende nota di ogni nuovo prodotto (compra all'ingrosso)."""
        self.prodotti_visti.append(prodotto)
        print(f"  [{self.nome}] Nuovo arrivo '{prodotto}' — lo aggiungo alla lista acquisti.")


# ==========================================
# UTILIZZO
# ==========================================
# I clienti si registrano UNA VOLTA. Il negozio li avvisa
# automaticamente — zero polling, zero sprechi.

if __name__ == "__main__":

    negozio = Negozio("Elettronica Express")

    # --- Creazione observer ---
    mario = Cliente("Mario", "PlayStation 6")
    giulia = Cliente("Giulia", "iPhone 20")
    luca = Cliente("Luca", "PlayStation 6")
    ingrosso = Rivenditore("TechBuy Ingrosso")

    # --- Registrazione (una sola volta) ---
    negozio.registra(mario)
    negozio.registra(giulia)
    negozio.registra(luca)
    negozio.registra(ingrosso)

    print("=" * 50)
    print("  OBSERVER — il negozio avvisa i clienti")
    print("=" * 50)

    # --- Arriva un prodotto: il negozio notifica TUTTI ---
    print("\n--- Arriva 'PlayStation 6' ---")
    negozio.aggiungi_prodotto("PlayStation 6")
    # Mario e Luca reagiscono, Giulia ignora, Ingrosso prende nota

    # --- Arriva un altro prodotto ---
    print("\n--- Arriva 'iPhone 20' ---")
    negozio.aggiungi_prodotto("iPhone 20")
    # Giulia reagisce, Mario e Luca ignorano, Ingrosso prende nota

    # --- Rimozione di un observer (Luca ha già comprato) ---
    print("\n--- Luca si cancella dalle notifiche ---")
    negozio.rimuovi(luca)

    print("\n--- Arriva 'Samsung Galaxy S30' ---")
    negozio.aggiungi_prodotto("Samsung Galaxy S30")
    # Luca NON viene più notificato

    # --- Riepilogo del rivenditore ---
    print(f"\n[{ingrosso.nome}] Prodotti visti oggi: {ingrosso.prodotti_visti}")

# La cosa importante da notare è che lato client tutto quello che viene fatto è solo aggiungere il nuovo prodotto
# alla lista dei prodotti disponibili, senza preoccuparsi di chi è interessato o meno.
# Il negozio si occupa di notificare in automatico tutti i clienti registrati
# e ogni cliente decide se reagire o meno alla notifica, senza che il negozio debba saperlo,
# permettendo un disaccoppiamento totale tra le due parti. 