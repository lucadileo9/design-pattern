"""
Iterator Pattern - IL PROBLEMA
================================
Abbiamo una biblioteca con più sezioni, e ogni sezione contiene una lista di libri.
Vogliamo stampare tutti i titoli disponibili.

Il problema: il client deve conoscere la struttura interna della biblioteca
(sezioni → libri), gestire i loop annidati da solo, e se la struttura cambia
(es. aggiungiamo sotto-sezioni) il codice client va riscritto.
"""


# ── Struttura dati ──────────────────────────────────────────────────────────

class Book:
    def __init__(self, title: str, author: str):
        self.title = title
        self.author = author


class Section:
    def __init__(self, name: str):
        self.name = name
        self.books: list[Book] = []

    def add_book(self, book: Book):
        self.books.append(book)


class Library:
    def __init__(self, name: str):
        self.name = name
        self.sections: list[Section] = []

    def add_section(self, section: Section):
        self.sections.append(section)


# ── Codice client ────────────────────────────────────────────────────────────

def main():
    # Costruiamo la biblioteca
    library = Library("Biblioteca Centrale")

    fiction = Section("Narrativa")
    fiction.add_book(Book("Il nome della rosa", "Umberto Eco"))
    fiction.add_book(Book("Se questo è un uomo", "Primo Levi"))
    fiction.add_book(Book("I Promessi Sposi", "Alessandro Manzoni"))

    science = Section("Scienza")
    science.add_book(Book("Breve storia del tempo", "Stephen Hawking"))
    science.add_book(Book("Il gene egoista", "Richard Dawkins"))

    philosophy = Section("Filosofia")
    philosophy.add_book(Book("La repubblica", "Platone"))
    philosophy.add_book(Book("Critica della ragion pura", "Immanuel Kant"))
    philosophy.add_book(Book("Essere e tempo", "Martin Heidegger"))

    library.add_section(fiction)
    library.add_section(science)
    library.add_section(philosophy)

    # PROBLEMA: il client deve sapere che la biblioteca ha sezioni,
    #     e che le sezioni hanno libri. Conosce tutta la struttura interna.
    print(f"=== {library.name} ===\n")
    for section in library.sections:               # il client gestisce il 1° livello
        print(f"  [{section.name}]")
        for book in section.books:                 # il client gestisce il 2° livello
            print(f"    - {book.title} ({book.author})")

    # Se volessimo cercare un libro specifico, la logica di ricerca
    #     (con tutti i loop annidati) è ancora responsabilità del client:
    print("\n--- Ricerca: libri di autori italiani ---")
    italian_authors = {"Umberto Eco", "Primo Levi", "Alessandro Manzoni"}
    for section in library.sections:               # loop annidato ripetuto
        for book in section.books:
            if book.author in italian_authors:
                print(f"  ✓ {book.title} — {book.author}")

    # Se domani aggiungessimo una struttura a tre livelli
    #     (Biblioteca → Piani → Sezioni → Libri), TUTTI i loop qui sopra
    #     andrebbero riscritti. 

if __name__ == "__main__":
    main()
