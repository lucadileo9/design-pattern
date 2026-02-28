# ==========================================
# OBSERVER PATTERN — SOLUTION
# ==========================================
# Instead of having customers check repeatedly (polling),
# it is the SHOP that notifies customers when a product arrives.
#
# The shop (Subject) maintains a list of registered customers
# (Observers) and calls their update() method automatically
# when it adds a new product to the inventory.
#
# Customers no longer have to do anything: they register once
# and get notified only when needed.

from abc import ABC, abstractmethod


# ==========================================
# OBSERVER — common interface
# ==========================================
# All observers implement update(). The Subject doesn't
# know the details — it only knows it can call this method.

class Observer(ABC):
    """Interface for anyone who wants to be notified by the shop."""

    @abstractmethod
    def update(self, product: str) -> None:
        """Called by the Subject when a new product arrives."""
        ...


# ==========================================
# SUBJECT — the shop that notifies
# ==========================================
# The shop maintains a list of observers and notifies them
# automatically every time a new product arrives.
# It doesn't know who they are, it doesn't care — it calls update() and that's it.

class Shop:
    """Subject: manages the inventory and notifies observers."""

    def __init__(self, name: str):
        self.name = name
        self.available_products: list[str] = []
        self._observers: list[Observer] = []

    # --- Observer management ---

    def register(self, observer: Observer) -> None:
        """A customer subscribes to notifications."""
        self._observers.append(observer)

    def remove(self, observer: Observer) -> None:
        """A customer unsubscribes from notifications."""
        self._observers.remove(observer)

    # --- Business logic ---

    def add_product(self, product: str) -> None:
        """Adds a product and NOTIFIES all observers."""
        self.available_products.append(product)
        print(f"[{self.name}] New product in stock: '{product}'")
        self._notify(product)

    def _notify(self, product: str) -> None:
        """Calls update() on every registered observer."""
        for observer in self._observers:
            observer.update(product)


# ==========================================
# CONCRETE OBSERVERS — the customers
# ==========================================
# Each customer reacts to the notification in their own way.
# The shop doesn't know what they do — it calls update() and that's it.

class Customer(Observer):
    """A customer interested in a specific product."""

    def __init__(self, name: str, desired_product: str):
        self.name = name
        self.desired_product = desired_product

    def update(self, product: str) -> None:
        """Reacts only if the product is the one they're waiting for."""
        if product == self.desired_product:
            print(f"  [{self.name}] The '{product}' has arrived! I'm going to buy it!")
        else:
            print(f"  [{self.name}] '{product}'? Not interested.")

# N.B.: this is simply another observer, but with a different update method
class Reseller(Observer):
    """A reseller who wants to know about ALL new arrivals."""

    def __init__(self, name: str):
        self.name = name
        self.seen_products: list[str] = []

    def update(self, product: str) -> None:
        """Takes note of every new product (buys wholesale)."""
        self.seen_products.append(product)
        print(f"  [{self.name}] New arrival '{product}' — adding it to the purchase list.")


# ==========================================
# USAGE
# ==========================================
# Customers register ONCE. The shop notifies them
# automatically — zero polling, zero waste.

if __name__ == "__main__":

    shop = Shop("Electronics Express")

    # --- Create observers ---
    mario = Customer("Mario", "PlayStation 6")
    giulia = Customer("Giulia", "iPhone 20")
    luca = Customer("Luca", "PlayStation 6")
    wholesale = Reseller("TechBuy Wholesale")

    # --- Registration (just once) ---
    shop.register(mario)
    shop.register(giulia)
    shop.register(luca)
    shop.register(wholesale)

    print("=" * 50)
    print("  OBSERVER — the shop notifies customers")
    print("=" * 50)

    # --- A product arrives: the shop notifies EVERYONE ---
    print("\n--- 'PlayStation 6' arrives ---")
    shop.add_product("PlayStation 6")
    # Mario and Luca react, Giulia ignores, Wholesale takes note

    # --- Another product arrives ---
    print("\n--- 'iPhone 20' arrives ---")
    shop.add_product("iPhone 20")
    # Giulia reacts, Mario and Luca ignore, Wholesale takes note

    # --- Removing an observer (Luca already bought) ---
    print("\n--- Luca unsubscribes from notifications ---")
    shop.remove(luca)

    print("\n--- 'Samsung Galaxy S30' arrives ---")
    shop.add_product("Samsung Galaxy S30")
    # Luca is NO LONGER notified

    # --- Reseller summary ---
    print(f"\n[{wholesale.name}] Products seen today: {wholesale.seen_products}")

# The important thing to notice is that on the client side all that's done is adding the new product
# to the available products list, without worrying about who is interested or not.
# The shop takes care of automatically notifying all registered customers
# and each customer decides whether or not to react to the notification, without the shop needing to know,
# allowing total decoupling between the two parts. 