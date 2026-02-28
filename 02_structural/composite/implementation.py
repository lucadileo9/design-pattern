# ==========================================
# COMPOSITE PATTERN — SOLUTION
# ==========================================
# We define a common interface (CatalogComponent) that is
# implemented by both PRODUCTS (leaves) and CATEGORIES
# (internal nodes — composites).
#
# The client calls .get_price() on any element, without
# knowing whether it's a single product or an entire category
# with nested sub-categories. No more if/isinstance!

from abc import ABC, abstractmethod


# ==========================================
# COMPONENT — the common interface
# ==========================================
# Declares the operations shared by leaves and composites.
# Every node in the tree, whether simple or composite, is a
# CatalogComponent.

class CatalogComponent(ABC):
    """Common interface for leaves (Product) and composites (Category)."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def get_price(self) -> float:
        """Returns the price (single or total of the sub-structure)."""
        ...

    @abstractmethod
    def display(self, indentation: int = 0) -> None:
        """Prints the structure with indentation."""
        ...


# ==========================================
# LEAF — the product (leaf)
# ==========================================
# A Product has no children. It's the base case of the recursion:
# get_price() simply returns its own price.

class Product(CatalogComponent):
    """Leaf: a single product with name and price."""

    def __init__(self, name: str, price: float):
        super().__init__(name)
        self.price = price

    def get_price(self) -> float:
        return self.price                       # base case — no recursion

    def display(self, indentation: int = 0) -> None:
        prefix = "  " * indentation
        print(f"{prefix}📦 {self.name} — €{self.price:.2f}")


# ==========================================
# COMPOSITE — the category (internal node)
# ==========================================
# A Category contains children (CatalogComponent), which can
# be either Products or other Categories — recursive structure.
#
# get_price() delegates to children and sums: the client doesn't
# notice the difference compared to a single product.

class Category(CatalogComponent):
    """Composite: contains children of type CatalogComponent."""

    def __init__(self, name: str):
        super().__init__(name)
        self._children: list[CatalogComponent] = []

    # --- child management (only in the Composite) ---

    def add(self, component: CatalogComponent) -> None:
        self._children.append(component)

    def remove(self, component: CatalogComponent) -> None:
        self._children.remove(component)

    # --- interface operations ---

    def get_price(self) -> float:
        # Delegates to children: recursive sum. The Composite doesn't know
        # if a child is a Product or another Category — it doesn't care.
        return sum(child.get_price() for child in self._children)

    def display(self, indentation: int = 0) -> None:
        prefix = "  " * indentation
        print(f"{prefix}📁 {self.name} (total: €{self.get_price():.2f})")
        for child in self._children:
            child.display(indentation + 1)      # polymorphic call


# ==========================================
# USAGE
# ==========================================
# The client ALWAYS works with CatalogComponent.
# It never uses isinstance(), never distinguishes leaves from composites.

if __name__ == "__main__":

    # --- Building the tree (identical to problem.py) ---
    laptop = Product("Laptop Gaming", 1299.99)
    mouse = Product("Mouse Wireless", 34.99)
    headphones = Product("Bluetooth Headphones", 79.99)
    monitor = Product("Monitor 4K", 499.99)
    webcam = Product("Webcam HD", 59.99)

    computers = Category("Computers")
    computers.add(laptop)
    computers.add(mouse)

    accessories = Category("Accessories")
    accessories.add(headphones)
    accessories.add(webcam)

    catalog = Category("Catalog")
    catalog.add(computers)
    catalog.add(accessories)
    catalog.add(monitor)            # product directly at the root

    # --- The client uses only the common interface ---
    print("=== Catalog ===")
    catalog.display()

    print(f"\nTotal catalog price: €{catalog.get_price():.2f}")
    print(f"Total 'Computers' price: €{computers.get_price():.2f}")
    print(f"Single 'Laptop Gaming' price: €{laptop.get_price():.2f}")

    # ADVANTAGE: if we add a new leaf type (e.g. "Bundle"),
    # it just needs to implement CatalogComponent. No client
    # function needs to be modified — polymorphism handles everything.