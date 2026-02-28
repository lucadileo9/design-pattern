# ==========================================
# THE PROBLEM THAT COMPOSITE SOLVES
# ==========================================
# We have a tree structure: an e-commerce catalog with
# PRODUCTS (leaves) and CATEGORIES (internal nodes) that can
# contain other products or sub-categories.
#
# We want to calculate the total price of a category (recursively
# summing all contained products, even in sub-categories).
#
# Without the Composite pattern, the client must manually distinguish
# between products and categories — with if/isinstance everywhere.


# ==========================================
# THE CLASSES — no common interface
# ==========================================
# Product and Category are completely separate classes.
# They don't share an interface, they have no common method.
# The client must know exactly which type it's talking to.

class Product:
    """A leaf: a single product with name and price."""
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


class Category:
    """An internal node: contains products and/or sub-categories."""
    def __init__(self, name: str):
        self.name = name
        self.children: list = []    # mix of Product and Category — no common type

    def add(self, element):
        self.children.append(element)


# ==========================================
# THE PROBLEM: THE CLIENT DOES EVERYTHING
# ==========================================
# To calculate the total price of a category, the client must:
#   1. Iterate over children
#   2. For EACH child, check if it's a Product or Category
#   3. If it's a Product → take the price
#   4. If it's a Category → recursively call the same logic
#
# This logic is in the CLIENT, not in the tree. If we add
# a new node type (e.g. "Bundle", "Gift package"),
# we must update EVERY function that traverses the tree.

def calculate_total_price(element) -> float:
    """
    Recursive function that the CLIENT must write and maintain.
    Requires isinstance() for each node type — fragile!
    """
    if isinstance(element, Product):
        return element.price
    elif isinstance(element, Category):
        total = 0.0
        for child in element.children:
            total += calculate_total_price(child)   # manual recursion
        return total
    else:
        # If we add a new type, this branch silently
        # ignores it
        return 0.0


def print_catalog(element, indentation: int = 0) -> None:
    """
    Another function that the CLIENT must write, with the SAME
    if/isinstance pattern — duplicated code for every operation!
    """
    prefix = "  " * indentation
    if isinstance(element, Product):
        print(f"{prefix}📦 {element.name} — €{element.price:.2f}")
    elif isinstance(element, Category):
        print(f"{prefix}📁 {element.name}")
        for child in element.children:
            print_catalog(child, indentation + 1)


# ==========================================
# USAGE
# ==========================================
# Every operation on the tree requires its own function
# full of if/isinstance. If we add a "Bundle" type,
# ALL these functions need to be modified.

if __name__ == "__main__":

    # Building the tree
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

    # Print
    print("=== Catalog ===")
    print_catalog(catalog)

    # Total price — requires the function with isinstance
    print(f"\nTotal catalog price: €{calculate_total_price(catalog):.2f}")
    print(f"Total 'Computers' price: €{calculate_total_price(computers):.2f}")
    print(f"Single 'Laptop Gaming' price: €{calculate_total_price(laptop):.2f}")

    # PROBLEM: if tomorrow we add a "Bundle" type (e.g. laptop +
    # mouse package at a discounted price), we must modify ALL the
    # functions that traverse the tree.
