# ==========================================
# IL PROBLEMA CHE IL COMPOSITE RISOLVE
# ==========================================
# Abbiamo una struttura ad albero: un catalogo e-commerce con
# PRODOTTI (foglie) e CATEGORIE (nodi interni) che possono
# contenere altri prodotti o sotto-categorie.
#
# Vogliamo calcolare il prezzo totale di una categoria (sommando
# ricorsivamente tutti i prodotti contenuti, anche in sotto-categorie).
#
# Senza il pattern Composite, il client deve distinguere manualmente
# tra prodotti e categorie — con if/isinstance ovunque.


# ==========================================
# LE CLASSI — nessuna interfaccia comune
# ==========================================
# Prodotto e Categoria sono classi completamente separate.
# Non condividono un'interfaccia, non hanno un metodo comune.
# Il client deve sapere esattamente con quale tipo sta parlando.

class Prodotto:
    """Una foglia: un singolo prodotto con nome e prezzo."""
    def __init__(self, nome: str, prezzo: float):
        self.nome = nome
        self.prezzo = prezzo


class Categoria:
    """Un nodo interno: contiene prodotti e/o sotto-categorie."""
    def __init__(self, nome: str):
        self.nome = nome
        self.figli: list = []       # mix di Prodotto e Categoria — nessun tipo comune

    def aggiungi(self, elemento):
        self.figli.append(elemento)


# ==========================================
# IL PROBLEMA: IL CLIENT FA TUTTO LUI
# ==========================================
# Per calcolare il prezzo totale di una categoria, il client deve:
#   1. Scorrere i figli
#   2. Per OGNI figlio, controllare se è Prodotto o Categoria
#   3. Se è Prodotto → prendere il prezzo
#   4. Se è Categoria → chiamare ricorsivamente la stessa logica
#
# Questa logica è nel CLIENT, non nell'albero. Se aggiungiamo
# un nuovo tipo di nodo (es. "Bundle", "Pacchetto regalo"),
# dobbiamo aggiornare OGNI funzione che attraversa l'albero.

def calcola_prezzo_totale(elemento) -> float:
    """
    Funzione ricorsiva che il CLIENT deve scrivere e mantenere.
    Richiede isinstance() per ogni tipo di nodo — fragile!
    """
    if isinstance(elemento, Prodotto):
        return elemento.prezzo
    elif isinstance(elemento, Categoria):
        totale = 0.0
        for figlio in elemento.figli:
            totale += calcola_prezzo_totale(figlio)      # ricorsione manuale
        return totale
    else:
        # Se aggiungiamo un nuovo tipo, questo ramo silenziosamente
        # lo ignora 
        return 0.0


def stampa_catalogo(elemento, indentazione: int = 0) -> None:
    """
    Altra funzione che il CLIENT deve scrivere, con lo STESSO
    pattern if/isinstance — codice duplicato per ogni operazione!
    """
    prefisso = "  " * indentazione
    if isinstance(elemento, Prodotto):
        print(f"{prefisso}📦 {elemento.nome} — €{elemento.prezzo:.2f}")
    elif isinstance(elemento, Categoria):
        print(f"{prefisso}📁 {elemento.nome}")
        for figlio in elemento.figli:
            stampa_catalogo(figlio, indentazione + 1)


# ==========================================
# UTILIZZO
# ==========================================
# Ogni operazione sull'albero richiede la propria funzione
# piena di if/isinstance. Se aggiungiamo un tipo "Bundle",
# TUTTE queste funzioni vanno modificate.

if __name__ == "__main__":

    # Costruzione dell'albero
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

    # Stampa
    print("=== Catalogo ===")
    stampa_catalogo(catalogo)

    # Prezzo totale — richiede la funzione con isinstance
    print(f"\nPrezzo totale catalogo: €{calcola_prezzo_totale(catalogo):.2f}")
    print(f"Prezzo totale 'Informatica': €{calcola_prezzo_totale(informatica):.2f}")
    print(f"Prezzo singolo 'Laptop Gaming': €{calcola_prezzo_totale(laptop):.2f}")

    # PROBLEMA: se domani aggiungiamo un tipo "Bundle" (es. pacchetto
    # laptop + mouse a prezzo scontato), dobbiamo modificare TUTTE le
    # funzioni che attraversano l'albero. .
