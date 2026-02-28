# ==========================================
# STRATEGY — Real Example: E-commerce Payment
# ==========================================
# An order (Context) must be paid. The payment method
# is chosen by the user at checkout time (at runtime).
#
# The order doesn't know HOW the payment happens — it only knows
# that the chosen strategy has a pay() method that returns True/False.
# Adding "Apple Pay" tomorrow → new class, zero modifications.

from abc import ABC, abstractmethod
from dataclasses import dataclass


# ==========================================
# STRATEGY — common interface
# ==========================================

class PaymentMethod(ABC):
    """Interface: every payment method implements pay()."""

    @abstractmethod
    def pay(self, amount: float) -> bool:
        """Processes the payment. Returns True if successful."""
        ...

    @abstractmethod
    def description(self) -> str:
        """Human-readable name of the payment method."""
        ...


# ==========================================
# CONCRETE STRATEGIES
# ==========================================

class CreditCard(PaymentMethod):
    """Card payment: validates number and CVV, contacts the gateway."""

    def __init__(self, card_number: str, cvv: str):
        self.card_number = card_number
        self.cvv = cvv

    def pay(self, amount: float) -> bool:
        # Simulation: card is valid if it has 16 digits and cvv 3 digits
        if len(self.card_number) != 16 or len(self.cvv) != 3:
            print(f"  ❌ Card declined: invalid data")
            return False

        masked = "****-****-****-" + self.card_number[-4:]
        print(f"  💳 Contacting bank gateway...")
        print(f"  💳 Charging €{amount:.2f} to card {masked}")
        return True

    def description(self) -> str:
        return f"Credit Card (****{self.card_number[-4:]})"


class PayPal(PaymentMethod):
    """PayPal payment: verifies email, redirects to the portal."""

    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float) -> bool:
        if "@" not in self.email:
            print(f"  ❌ PayPal: invalid email")
            return False

        print(f"  🅿️ Redirecting to PayPal...")
        print(f"  🅿️ Payment of €{amount:.2f} confirmed by {self.email}")
        return True

    def description(self) -> str:
        return f"PayPal ({self.email})"


class Cryptocurrency(PaymentMethod):
    """Crypto payment: generates wallet address, awaits confirmation."""

    def __init__(self, wallet: str):
        self.wallet = wallet

    def pay(self, amount: float) -> bool:
        if len(self.wallet) < 10:
            print(f"  ❌ Crypto: invalid wallet address")
            return False

        short_address = self.wallet[:6] + "..." + self.wallet[-4:]
        print(f"  🪙 Sending to wallet {short_address}...")
        print(f"  🪙 Transaction of €{amount:.2f} confirmed on the blockchain")
        return True

    def description(self) -> str:
        return f"Crypto ({self.wallet[:6]}...{self.wallet[-4:]})"


# ==========================================
# CONTEXT — the order
# ==========================================
# The order manages the cart and the total. When it's time
# to pay, it delegates to the current strategy — without if/elif.
# Of course, the context class doesn't necessarily handle ONLY
# the strategies, but also other business logic (e.g., cart management, total calculation).

@dataclass
class CartItem:
    name: str
    price: float
    quantity: int = 1


class Order:
    """Context: manages the cart and delegates payment to the strategy."""

    def __init__(self):
        self.items: list[CartItem] = []
        self._payment_method: PaymentMethod | None = None

    def add(self, name: str, price: float, quantity: int = 1) -> None:
        self.items.append(CartItem(name, price, quantity))

    def get_total(self) -> float:
        return sum(item.price * item.quantity for item in self.items)

    def set_payment(self, method: PaymentMethod) -> None:
        """The user chooses the payment method at checkout."""
        self._payment_method = method

    def pay(self) -> bool:
        """Delegates payment to the strategy — zero logic in here."""
        if not self.items:
            print("Empty cart!")
            return False

        if self._payment_method is None:
            print("No payment method selected!")
            return False

        total = self.get_total()
        print(f"\n--- Checkout ---")
        print(f"Total: €{total:.2f}")
        print(f"Method: {self._payment_method.description()}")

        success = self._payment_method.pay(total)

        if success:
            print(f"  ✅ Order completed!")
        else:
            print(f"  ⚠️ Payment failed, please try again.")

        return success


# ==========================================
# USAGE
# ==========================================

if __name__ == "__main__":

    print("=" * 50)
    print("  STRATEGY — E-commerce Payment")
    print("=" * 50)

    # --- Scenario 1: card payment ---
    order1 = Order()
    order1.add("Mechanical keyboard", 89.99)
    order1.add("Wireless mouse", 34.99)

    order1.set_payment(CreditCard("1234567890123456", "789"))
    order1.pay()

    # --- Scenario 2: PayPal payment ---
    order2 = Order()
    order2.add("27\" Monitor", 349.00)

    order2.set_payment(PayPal("mario@example.com"))
    order2.pay()

    # --- Scenario 3: cryptocurrency payment ---
    order3 = Order()
    order3.add("SSD 1TB", 79.99)
    order3.add("RAM 16GB", 54.99, 2)

    order3.set_payment(Cryptocurrency("0xABCDEF1234567890ABCD"))
    order3.pay()

    # --- Scenario 4: invalid card ---
    order4 = Order()
    order4.add("USB-C cable", 9.99)

    order4.set_payment(CreditCard("123", "7"))   # data too short
    order4.pay()

