# ==========================================
# COMPOSITE PATTERN — SOLUZIONE
# ==========================================
# Definiamo un'interfaccia comune (ComponenteCatalogo) che viene
# implementata sia dai PRODOTTI (foglie) sia dalle CATEGORIE
# (nodi interni — composite).
#
# Il client chiama .get_prezzo() su qualsiasi elemento, senza
# sapere se è un prodotto singolo o un'intera categoria con
# sotto-categorie annidate. Niente più if/isinstance!

from abc import ABC, abstractmethod


# ==========================================
# COMPONENT — l'interfaccia comune
# ==========================================
# Dichiara le operazioni condivise da foglie e composite.
# Ogni nodo dell'albero, che sia semplice o composto, è un
# ComponenteCatalogo.

class ComponenteCatalogo(ABC):
    """Interfaccia comune per foglie (Prodotto) e composite (Categoria)."""

    def __init__(self, nome: str):
        self.nome = nome

    @abstractmethod
    def get_prezzo(self) -> float:
        """Restituisce il prezzo (singolo o totale della sotto-struttura)."""
        ...

    @abstractmethod
    def mostra(self, indentazione: int = 0) -> None:
        """Stampa la struttura con indentazione."""
        ...


# ==========================================
# LEAF — il prodotto (foglia)
# ==========================================
# Un Prodotto non ha figli. È il caso base della ricorsione:
# get_prezzo() restituisce semplicemente il proprio prezzo.

class Prodotto(ComponenteCatalogo):
    """Foglia: un singolo prodotto con nome e prezzo."""

    def __init__(self, nome: str, prezzo: float):
        super().__init__(nome)
        self.prezzo = prezzo

    def get_prezzo(self) -> float:
        return self.prezzo                      # caso base — nessuna ricorsione

    def mostra(self, indentazione: int = 0) -> None:
        prefisso = "  " * indentazione
        print(f"{prefisso}📦 {self.nome} — €{self.prezzo:.2f}")


# ==========================================
# COMPOSITE — la categoria (nodo interno)
# ==========================================
# Una Categoria contiene figli (ComponenteCatalogo), che possono
# essere sia Prodotti sia altre Categorie — struttura ricorsiva.
#
# get_prezzo() delega ai figli e somma: il client non si accorge
# della differenza rispetto a un singolo prodotto.

class Categoria(ComponenteCatalogo):
    """Composite: contiene figli di tipo ComponenteCatalogo."""

    def __init__(self, nome: str):
        super().__init__(nome)
        self._figli: list[ComponenteCatalogo] = []

    # --- gestione figli (solo nel Composite) ---

    def aggiungi(self, componente: ComponenteCatalogo) -> None:
        self._figli.append(componente)

    def rimuovi(self, componente: ComponenteCatalogo) -> None:
        self._figli.remove(componente)

    # --- operazioni dell'interfaccia ---

    def get_prezzo(self) -> float:
        # Delega ai figli: somma ricorsiva. Il Composite non sa
        # se un figlio è Prodotto o un'altra Categoria — non gli interessa.
        return sum(figlio.get_prezzo() for figlio in self._figli)

    def mostra(self, indentazione: int = 0) -> None:
        prefisso = "  " * indentazione
        print(f"{prefisso}📁 {self.nome} (totale: €{self.get_prezzo():.2f})")
        for figlio in self._figli:
            figlio.mostra(indentazione + 1)     # chiamata polimorfica


# ==========================================
# UTILIZZO
# ==========================================
# Il client lavora SEMPRE con ComponenteCatalogo.
# Non fa mai isinstance(), non distingue foglie da composite.

if __name__ == "__main__":

    # --- Costruzione dell'albero (identico al problem.py) ---
    laptop = Prodotto("Laptop Gaming", 1299.99)
    mouse = Prodotto("Mouse Wireless", 34.99)
    cuffie = Prodotto("Cuffie Bluetooth", 79.99)
    monitor = Prodotto("Monitor 4K", 499.99)
    webcam = Prodotto("Webcam HD", 59.99)

    informatica = Categoria("Informatica")
    informatica.aggiungi(laptop)
    informatica.aggiungi(mouse)

    accessori = Categoria("Accessori")
    accessori.aggiungi(cuffie)
    accessori.aggiungi(webcam)

    catalogo = Categoria("Catalogo")
    catalogo.aggiungi(informatica)
    catalogo.aggiungi(accessori)
    catalogo.aggiungi(monitor)      # prodotto direttamente nella radice

    # --- Il client usa solo l'interfaccia comune ---
    print("=== Catalogo ===")
    catalogo.mostra()

    print(f"\nPrezzo totale catalogo: €{catalogo.get_prezzo():.2f}")
    print(f"Prezzo totale 'Informatica': €{informatica.get_prezzo():.2f}")
    print(f"Prezzo singolo 'Laptop Gaming': €{laptop.get_prezzo():.2f}")

    # VANTAGGIO: se aggiungiamo un nuovo tipo di foglia (es. "Bundle"),
    # basta che implementi ComponenteCatalogo. Nessuna funzione del
    # client va modificata — il polimorfismo gestisce tutto.