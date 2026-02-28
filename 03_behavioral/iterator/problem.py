"""
Iterator Pattern - THE PROBLEM
================================
We have a library with multiple sections, and each section contains a list of books.
We want to print all the available titles.

The problem: the client must know the internal structure of the library
(sections → books), manage the nested loops on its own, and if the structure changes
(e.g., we add sub-sections) the client code must be rewritten.
"""


# ── Data Structure ──────────────────────────────────────────────────────────

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


# ── Client Code ──────────────────────────────────────────────────────────────

def main():
    # Build the library
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

    # PROBLEM: the client must know that the library has sections,
    #     and that sections have books. It knows the entire internal structure.
    print(f"=== {library.name} ===\n")
    for section in library.sections:               # the client handles the 1st level
        print(f"  [{section.name}]")
        for book in section.books:                 # the client handles the 2nd level
            print(f"    - {book.title} ({book.author})")

    # If we wanted to search for a specific book, the search logic
    #     (with all the nested loops) is still the client's responsibility:
    print("\n--- Search: books by Italian authors ---")
    italian_authors = {"Umberto Eco", "Primo Levi", "Alessandro Manzoni"}
    for section in library.sections:               # repeated nested loop
        for book in section.books:
            if book.author in italian_authors:
                print(f"  ✓ {book.title} — {book.author}")

    # If tomorrow we added a three-level structure
    #     (Library → Floors → Sections → Books), ALL the loops above
    #     would need to be rewritten.

if __name__ == "__main__":
    main()
