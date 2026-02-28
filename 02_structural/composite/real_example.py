# ==========================================
# COMPOSITE — Real Example: Restaurant Menu
# ==========================================
# A restaurant menu has a tree structure:
#   - Individual dishes (leaves): "Bruschetta", "Carbonara", etc.
#   - Sections (composites): "Appetizers", "First Courses", "Drinks", etc.
#
# Sections can contain dishes or sub-sections
# (e.g. "Drinks" → "Non-Alcoholic" / "Alcoholic").
#
# The client wants to be able to ask any element:
#   - display()            → print the structure
#   - count_dishes()       → how many dishes are there
#   - get_average_price()  → average price of contained dishes
# … without distinguishing between a single dish and an entire section.

from abc import ABC, abstractmethod


# ==========================================
# COMPONENT — common interface
# ==========================================

class MenuComponent(ABC):
    """Common interface for dishes and menu sections."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def display(self, indentation: int = 0) -> None:
        """Prints the element (and its children, if any)."""
        ...

    @abstractmethod
    def count_dishes(self) -> int:
        """Number of dishes (leaves) contained."""
        ...

    @abstractmethod
    def get_prices(self) -> list[float]:
        """List of all prices of contained dishes."""
        ...

    def get_average_price(self) -> float:
        """Average price calculated from collected prices."""
        prices = self.get_prices()
        if not prices:
            return 0.0
        return sum(prices) / len(prices)


# ==========================================
# LEAF — single dish
# ==========================================

class Dish(MenuComponent):
    """Leaf: a dish with name, price and (optional) description."""

    def __init__(self, name: str, price: float, description: str = ""):
        super().__init__(name)
        self.price = price
        self.description = description

    def display(self, indentation: int = 0) -> None:
        prefix = "  " * indentation
        desc = f"  — {self.description}" if self.description else ""
        print(f"{prefix}• {self.name}: €{self.price:.2f}{desc}")

    def count_dishes(self) -> int:
        return 1

    def get_prices(self) -> list[float]:
        return [self.price]


# ==========================================
# COMPOSITE — menu section
# ==========================================

class MenuSection(MenuComponent):
    """Composite: a section that contains dishes and/or sub-sections."""

    def __init__(self, name: str):
        super().__init__(name)
        self._children: list[MenuComponent] = []

    def add(self, component: MenuComponent) -> None:
        self._children.append(component)

    def remove(self, component: MenuComponent) -> None:
        self._children.remove(component)

    # --- interface operations (delegated to children) ---

    def display(self, indentation: int = 0) -> None:
        prefix = "  " * indentation
        print(f"{prefix}📂 {self.name}")
        for child in self._children:
            child.display(indentation + 1)

    def count_dishes(self) -> int:
        return sum(child.count_dishes() for child in self._children)

    def get_prices(self) -> list[float]:
        prices: list[float] = []
        for child in self._children:
            prices.extend(child.get_prices())
        return prices


# ==========================================
# USAGE — building and navigating the menu
# ==========================================

if __name__ == "__main__":

    # --- Appetizers ---
    bruschetta = Dish("Bruschetta", 6.00, "tomato, basil, EVO oil")
    caprese = Dish("Caprese", 8.50, "buffalo mozzarella, tomato")
    platter = Dish("Mixed Platter", 12.00, "local cured meats and cheeses")

    appetizers = MenuSection("Appetizers")
    appetizers.add(bruschetta)
    appetizers.add(caprese)
    appetizers.add(platter)

    # --- First Courses ---
    carbonara = Dish("Carbonara", 11.00)
    amatriciana = Dish("Amatriciana", 10.50)
    risotto = Dish("Porcini Mushroom Risotto", 13.00)

    first_courses = MenuSection("First Courses")
    first_courses.add(carbonara)
    first_courses.add(amatriciana)
    first_courses.add(risotto)

    # --- Main Courses ---
    tagliata = Dish("Beef Tagliata", 18.00, "with arugula and parmesan")
    sea_bass = Dish("Baked Sea Bass", 16.50)

    main_courses = MenuSection("Main Courses")
    main_courses.add(tagliata)
    main_courses.add(sea_bass)

    # --- Drinks with sub-sections ---
    water = Dish("Still/Sparkling Water", 2.50)
    cola = Dish("Cola", 3.50)
    juice = Dish("Fruit Juice", 3.00)

    non_alcoholic = MenuSection("Non-Alcoholic")
    non_alcoholic.add(water)
    non_alcoholic.add(cola)
    non_alcoholic.add(juice)

    beer = Dish("Craft Beer 0.4L", 5.50)
    red_wine = Dish("House Red Wine (glass)", 4.50)
    white_wine = Dish("House White Wine (glass)", 4.50)

    alcoholic = MenuSection("Alcoholic")
    alcoholic.add(beer)
    alcoholic.add(red_wine)
    alcoholic.add(white_wine)

    drinks = MenuSection("Drinks")
    drinks.add(non_alcoholic)           # sub-section inside section
    drinks.add(alcoholic)               # sub-section inside section

    # --- Complete menu (root) ---
    menu = MenuSection("Restaurant Menu 'Da Luca'")
    menu.add(appetizers)
    menu.add(first_courses)
    menu.add(main_courses)
    menu.add(drinks)

    # ---- 1. Display the entire menu ----
    print("=" * 50)
    print("  FULL MENU")
    print("=" * 50)
    menu.display()

    # ---- 2. Statistics (uniform across leaves and composites) ----
    print(f"\nTotal dishes in menu:      {menu.count_dishes()}")
    print(f"Average price (all):       €{menu.get_average_price():.2f}")
    print(f"Average price (appetizers):€{appetizers.get_average_price():.2f}")
    print(f"Dishes in 'Drinks':        {drinks.count_dishes()}")
    print(f"Dishes in 'Non-Alcoholic': {non_alcoholic.count_dishes()}")

    # A leaf works exactly like a composite:
    print(f"\nAverage price 'Carbonara': €{carbonara.get_average_price():.2f}")
    print(f"Dishes in 'Carbonara':     {carbonara.count_dishes()}")

    # ---- 3. Removing a dish ----
    print("\n--- Removing 'Amatriciana' from First Courses ---")
    first_courses.remove(amatriciana)
    first_courses.display()
    print(f"New average price (first courses): €{first_courses.get_average_price():.2f}")
