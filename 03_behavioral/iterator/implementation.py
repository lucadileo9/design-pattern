"""
Iterator Pattern - LA SOLUZIONE
=================================
Stessa biblioteca di problem.py, ma ora la logica di attraversamento
è incapsulata nelle classi dedicate (Iterator / Aggregate).

Il client usa sempre e solo has_next() + next() — non sa nulla
della struttura interna, e non cambierà se la struttura cambia.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


# ── Interfacce ───────────────────────────────────────────────────────────────

class Iterator(ABC):
    """Interfaccia comune per tutti gli iteratori."""

    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self) -> "Book":
        pass


class Aggregate(ABC):
    """Interfaccia comune per tutte le collezioni iterabili."""

    @abstractmethod
    def create_iterator(self) -> Iterator:
        pass


# ── Struttura dati ───────────────────────────────────────────────────────────

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


class Library(Aggregate):
    def __init__(self, name: str):
        self.name = name
        self.sections: list[Section] = []

    def add_section(self, section: Section):
        self.sections.append(section)

    def create_iterator(self) -> Iterator:
        return LibraryIterator(self.sections)


# ── Iteratore concreto ───────────────────────────────────────────────────────

class LibraryIterator(Iterator):
    """
    Tutta la complessità dell'attraversamento vive qui,
    non nel client. Il client non sa nulla di sezioni o loop annidati.
    """

    def __init__(self, sections: list[Section]):
        self._sections = sections
        self._section_index = 0
        self._book_index = 0

    def has_next(self) -> bool:
        # Avanza tra le sezioni finché non trova un libro disponibile
        while self._section_index < len(self._sections):
            section = self._sections[self._section_index]
            if self._book_index < len(section.books):
                return True
            # Sezione esaurita: passa alla successiva
            self._section_index += 1
            self._book_index = 0
        return False

    def next(self) -> Book:
        book = self._sections[self._section_index].books[self._book_index]
        self._book_index += 1
        return book


# ── Codice client ────────────────────────────────────────────────────────────

def main():
    # Costruiamo la stessa biblioteca di problem.py
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

    # Il client usa solo has_next() + next(): non sa nulla di sezioni o
    #    loop annidati. Se la struttura interna cambia, questo codice non cambia.
    print(f"=== {library.name} ===\n")
    iterator = library.create_iterator()
    while iterator.has_next():
        book = iterator.next()
        print(f"  - {book.title} ({book.author})")

    # Ricerca: stessa interfaccia, zero conoscenza della struttura interna.
    print("\n--- Ricerca: libri di autori italiani ---")
    italian_authors = {"Umberto Eco", "Primo Levi", "Alessandro Manzoni"}
    iterator = library.create_iterator()          # nuovo iteratore, posizione indipendente
    while iterator.has_next():
        book = iterator.next()
        if book.author in italian_authors:
            print(f"  ✓ {book.title} — {book.author}")

    # Se domani aggiungessimo un livello (Piani → Sezioni → Libri),
    #    basta creare un nuovo FloorIterator e aggiornare create_iterator().
    #    Il codice client qui sopra rimane identico.
    # Da notare inoltre che il pattern non tocca la complessità intrinseca dell'attraversamento: 
    # se la struttura è complessa, anche l'iteratore sarà complesso. Ma almeno il client è semplice e stabile.


if __name__ == "__main__":
    main()
