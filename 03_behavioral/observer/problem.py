# ==========================================
# THE PROBLEM THAT THE OBSERVER SOLVES
# ==========================================
# A shopkeeper (Shop) periodically receives new products.
# Some customers are interested in specific products and want
# to know when they arrive.
#
# Without the Observer pattern, each customer must POLL:
# repeatedly ask the shop "Has my product arrived?".
# The shop gets bombarded with requests, and customers waste
# time checking continuously.


import time


# ==========================================
# THE SHOP — knows nothing about the customers
# ==========================================
# The shop manages its own products. It has no mechanism
# to notify customers: THEY have to check themselves.

class Shop:
    """The shop: manages the inventory, but doesn't notify anyone."""

    def __init__(self, name: str):
        self.name = name
        self.available_products: list[str] = []

    def add_product(self, product: str) -> None:
        """Adds a product to the inventory — no notification."""
        self.available_products.append(product)
        print(f"[{self.name}] New product in stock: '{product}'")

    def has_product(self, product: str) -> bool:
        """The customer must call this method to check."""
        return product in self.available_products


# ==========================================
# THE CUSTOMER — must poll manually
# ==========================================
# The customer wants a specific product. The only way to
# know if it has arrived is to repeatedly ask the shop.

class Customer:
    """A customer who is waiting for a specific product."""

    def __init__(self, name: str, desired_product: str):
        self.name = name
        self.desired_product = desired_product

    def check_availability(self, shop: Shop) -> bool:
        """
        POLLING: the customer actively asks the shop.
        They must do this repeatedly, hoping the product has arrived.
        """
        available = shop.has_product(self.desired_product)
        if available:
            print(f"  [{self.name}] Yay! '{self.desired_product}' is available!")
        else:
            print(f"  [{self.name}] '{self.desired_product}' is not here yet...")
        return available


# ==========================================
# POLLING SIMULATION
# ==========================================
# Each customer checks the shop continuously.
# The shop gets bombarded with useless requests.
# If there are 100 customers, the load becomes unsustainable.

if __name__ == "__main__":

    shop = Shop("Electronics Express")

    mario = Customer("Mario", "PlayStation 6")
    giulia = Customer("Giulia", "iPhone 20")
    luca = Customer("Luca", "PlayStation 6")

    print("=" * 50)
    print("  POLLING — customers check repeatedly")
    print("=" * 50)

    # --- Turn 1: no products yet ---
    print("\n--- Turn 1: customers check ---")
    mario.check_availability(shop)      # nothing
    giulia.check_availability(shop)     # nothing
    luca.check_availability(shop)       # nothing

    # --- The shop receives a product ---
    print("\n--- The shop receives goods ---")
    shop.add_product("PlayStation 6")

    # --- Turn 2: customers check AGAIN ---
    print("\n--- Turn 2: customers check ---")
    mario.check_availability(shop)      # found!
    giulia.check_availability(shop)     # nothing (wants iPhone)
    luca.check_availability(shop)       # found!

    # --- The shop receives another product ---
    print("\n--- The shop receives more goods ---")
    shop.add_product("iPhone 20")

    # --- Turn 3: EVERYONE must check again ---
    print("\n--- Turn 3: customers check ---")
    mario.check_availability(shop)      # already found before, waste
    giulia.check_availability(shop)     # finally!
    luca.check_availability(shop)       # already found before, waste

    # PROBLEMS:
    # 1. Each customer must check EVERY time, even when it's not
    #    needed
    # 2. The shop receives N requests per turn (with 100 customers = 100
    #    repeated requests every turn).
    # 3. If the shop adds a product between turns,
    #    customers only notice on the next turn (delay).
    # 4. The client (the main) must manually orchestrate the polling.
    # Also note that the shop is constantly being interrogated,
    # so it is constantly being disturbed, unable to, for example,
    # focus on other activities
