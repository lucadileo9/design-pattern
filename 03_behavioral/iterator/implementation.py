"""
Iterator Pattern - THE SOLUTION
=================================
Same library as problem.py, but now the traversal logic
is encapsulated in dedicated classes (Iterator / Aggregate).

The client only ever uses has_next() + next() — it knows nothing
about the internal structure, and won't change if the structure changes.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


# ── Interfaces ───────────────────────────────────────────────────────────────

class Iterator(ABC):
    """Common interface for all iterators."""

    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self) -> "Book":
        pass


class Aggregate(ABC):
    """Common interface for all iterable collections."""

    @abstractmethod
    def create_iterator(self) -> Iterator:
        pass


# ── Data Structure ───────────────────────────────────────────────────────────

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


# ── Concrete Iterator ────────────────────────────────────────────────────────

class LibraryIterator(Iterator):
    """
    All the traversal complexity lives here,
    not in the client. The client knows nothing about sections or nested loops.
    """

    def __init__(self, sections: list[Section]):
        self._sections = sections
        self._section_index = 0
        self._book_index = 0

    def has_next(self) -> bool:
        # Advance through sections until a book is available
        while self._section_index < len(self._sections):
            section = self._sections[self._section_index]
            if self._book_index < len(section.books):
                return True
            # Section exhausted: move to the next one
            self._section_index += 1
            self._book_index = 0
        return False

    def next(self) -> Book:
        book = self._sections[self._section_index].books[self._book_index]
        self._book_index += 1
        return book


# ── Client Code ──────────────────────────────────────────────────────────────

def main():
    # Build the same library as in problem.py
    library = Library("Central Library")

    fiction = Section("Fiction")
    fiction.add_book(Book("Il nome della rosa", "Umberto Eco"))
    fiction.add_book(Book("Se questo è un uomo", "Primo Levi"))
    fiction.add_book(Book("I Promessi Sposi", "Alessandro Manzoni"))

    science = Section("Science")
    science.add_book(Book("Breve storia del tempo", "Stephen Hawking"))
    science.add_book(Book("Il gene egoista", "Richard Dawkins"))

    philosophy = Section("Philosophy")
    philosophy.add_book(Book("La repubblica", "Platone"))
    philosophy.add_book(Book("Critica della ragion pura", "Immanuel Kant"))
    philosophy.add_book(Book("Essere e tempo", "Martin Heidegger"))

    library.add_section(fiction)
    library.add_section(science)
    library.add_section(philosophy)

    # The client only uses has_next() + next(): it knows nothing about sections
    #    or nested loops. If the internal structure changes, this code stays the same.
    print(f"=== {library.name} ===\n")
    iterator = library.create_iterator()
    while iterator.has_next():
        book = iterator.next()
        print(f"  - {book.title} ({book.author})")

    # Search: same interface, zero knowledge of the internal structure.
    print("\n--- Search: books by Italian authors ---")
    italian_authors = {"Umberto Eco", "Primo Levi", "Alessandro Manzoni"}
    iterator = library.create_iterator()          # new iterator, independent position
    while iterator.has_next():
        book = iterator.next()
        if book.author in italian_authors:
            print(f"  ✓ {book.title} — {book.author}")

    # If tomorrow we added a level (Floors → Sections → Books),
    #    we'd just create a new FloorIterator and update create_iterator().
    #    The client code above would remain identical.
    # Also note that the pattern does not reduce the intrinsic complexity of traversal:
    # if the structure is complex, the iterator will be complex too. But at least the client is simple and stable.


if __name__ == "__main__":
    main()
