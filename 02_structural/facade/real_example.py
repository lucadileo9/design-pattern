# ==========================================
# FACADE PATTERN — Real Example
# E-commerce Checkout System
# ==========================================
#
# Scenario: completing an online order involves 4 subsystems
# (catalog, payment, shipping, notifications) that must be
# orchestrated in the correct sequence.
#
# Without the Facade the client would have to manage everything manually.
# With the Facade it calls ONE method: facade.complete_order()

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional


# ==========================================
# 0. DATA STRUCTURES
# ==========================================

@dataclass
class CartItem:
    """A product in the cart."""
    product_id: str
    name: str
    quantity: int
    unit_price: float

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class OrderResult:
    """Result returned by the Facade to the client."""
    success: bool
    order_id: Optional[str] = None
    tracking_code: Optional[str] = None
    total: float = 0.0
    message: str = ""


# ==========================================
# 1. SUBSYSTEM — Catalog / Inventory
# ==========================================

class CatalogService:
    """Manages product availability."""

    def __init__(self):
        # Simulated inventory: product_id → quantity
        self._stock: dict[str, int] = {
            "LAPTOP-001": 10,
            "MOUSE-042":  50,
            "MONITOR-27":  5,
            "WEBCAM-HD":   0,   # out of stock
        }

    def check_availability(self, product_id: str, quantity: int) -> bool:
        """Checks if the product is available."""
        available = self._stock.get(product_id, 0)
        ok = available >= quantity
        print(f"  [Catalog] {product_id} × {quantity}: "
              f"{'✓ available' if ok else f'✗ only {available} left'}")
        return ok

    def reserve_stock(self, product_id: str, quantity: int):
        """Decrements stock (reservation)."""
        self._stock[product_id] -= quantity
        print(f"  [Catalog] Stock reserved: {product_id} × {quantity}")

    def release_stock(self, product_id: str, quantity: int):
        """Restores stock (rollback)."""
        self._stock[product_id] += quantity
        print(f"  [Catalog] ↩ Stock released: {product_id} × {quantity}")


# ==========================================
# 2. SUBSYSTEM — Payments
# ==========================================

class PaymentService:
    """Simulates a payment gateway (e.g. Stripe)."""

    # Blocked cards to simulate failures
    _BLOCKED = {"0000-0000-0000-0000"}

    def process_payment(self, card_number: str, amount: float) -> Optional[str]:
        """
        Attempts to charge the amount to the card.
        Returns a transaction_id if successful, None if declined.
        """
        if card_number in self._BLOCKED:
            print(f"  [Payment] ✗ Card ****{card_number[-4:]} declined")
            return None

        txn_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
        print(f"  [Payment] ✓ Charge €{amount:.2f} on ****{card_number[-4:]} → {txn_id}")
        return txn_id


# ==========================================
# 3. SUBSYSTEM — Shipping
# ==========================================

class ShippingService:
    """Creates shipments and generates tracking codes."""

    def create_shipment(self, address: str, n_items: int) -> str:
        """Creates a shipment and returns the tracking code."""
        tracking = f"TRK-{uuid.uuid4().hex[:8].upper()}"
        print(f"  [Shipping] ✓ Shipment created: {tracking}")
        print(f"              Destination: {address}")
        print(f"              Items: {n_items} pieces")
        return tracking


# ==========================================
# 4. SUBSYSTEM — Notifications
# ==========================================

class NotificationService:
    """Sends confirmation or error emails."""

    @staticmethod
    def send_confirmation(email: str, order_id: str, total: float, tracking: str):
        """Order confirmation email with tracking."""
        print(f"  [Email] ✉ Confirmation to {email}: order {order_id}, €{total:.2f}, tracking {tracking}")

    @staticmethod
    def send_error(email: str, reason: str):
        """Error email."""
        print(f"  [Email] ✉ Error to {email}: {reason}")


# ==========================================
# 5. THE FACADE — CheckoutFacade
# ==========================================
# Orchestrates the 4 subsystems in sequence, handles rollback
# if something goes wrong, and returns a single OrderResult.
#
# The client does NOT know any subsystem. It only calls:
#   facade.complete_order(items, email, address, card_number)

class CheckoutFacade:
    """
    Facade for e-commerce checkout.
    A single method complete_order() hides 4 subsystems.
    """

    def __init__(self):
        self._catalog = CatalogService()
        self._payment = PaymentService()
        self._shipping = ShippingService()
        self._notifications = NotificationService()

    def complete_order(
        self,
        items: list[CartItem],
        email: str,
        address: str,
        card_number: str,
    ) -> OrderResult:
        """
        Completes the order by orchestrating the subsystems:
          1. Check availability
          2. Reserve stock
          3. Process payment  (if it fails → rollback stock)
          4. Create shipment
          5. Send confirmation
        """
        print(f"\n{'='*55}")
        print(f"  CHECKOUT — Order for {email}")
        print(f"{'='*55}")

        # --- 1. Check availability ---
        print("\n📦 Step 1 — Check availability")
        for item in items:
            if not self._catalog.check_availability(item.product_id, item.quantity):
                msg = f"Product '{item.name}' not available"
                self._notifications.send_error(email, msg)
                return OrderResult(success=False, message=msg)

        # --- 2. Reserve stock ---
        print("\n📦 Step 2 — Reserve stock")
        reserved: list[CartItem] = []
        for item in items:
            self._catalog.reserve_stock(item.product_id, item.quantity)
            reserved.append(item)

        # --- 3. Payment ---
        total = sum(item.subtotal for item in items)
        print(f"\n💳 Step 3 — Payment (total: €{total:.2f})")
        txn_id = self._payment.process_payment(card_number, total)

        if txn_id is None:
            # Rollback: release the reserved stock
            print("\n  ↩ ROLLBACK — Releasing stock")
            for item in reserved:
                self._catalog.release_stock(item.product_id, item.quantity)
            msg = "Payment declined"
            self._notifications.send_error(email, msg)
            return OrderResult(success=False, message=msg)

        # --- 4. Shipping ---
        print("\n🚚 Step 4 — Create shipment")
        n_items = sum(item.quantity for item in items)
        tracking = self._shipping.create_shipment(address, n_items)

        # --- 5. Confirmation ---
        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        print(f"\n✉️  Step 5 — Order confirmation {order_id}")
        self._notifications.send_confirmation(email, order_id, total, tracking)

        print(f"\n{'='*55}")
        print(f"  ✅ ORDER COMPLETED")
        print(f"{'='*55}")

        return OrderResult(
            success=True,
            order_id=order_id,
            tracking_code=tracking,
            total=total,
            message="Order completed successfully",
        )


# ==========================================
# 6. CLIENT CODE
# ==========================================
# The client prepares the data and calls ONE method.
# It doesn't know any subsystem, doesn't handle rollback.

def client_code(facade: CheckoutFacade):

    # --- Scenario 1: order that succeeds ---
    print("\n" + "─" * 55)
    print("  SCENARIO 1: Standard order (success)")
    print("─" * 55)

    cart = [
        CartItem("LAPTOP-001", "Laptop Gaming Pro", 1, 1299.99),
        CartItem("MOUSE-042",  "Mouse Wireless",    2,   34.99),
    ]

    result = facade.complete_order(
        items=cart,
        email="marco.rossi@email.it",
        address="Via Roma 42, Milano",
        card_number="4532-1234-5678-9012",
    )

    print(f"\n  → success={result.success}, order={result.order_id}, "
          f"tracking={result.tracking_code}, total=€{result.total:.2f}")

    # --- Scenario 2: card declined → automatic rollback ---
    print("\n\n" + "─" * 55)
    print("  SCENARIO 2: Card declined (automatic rollback)")
    print("─" * 55)

    cart_2 = [
        CartItem("MONITOR-27", "Monitor 4K 27\"", 2, 499.99),
    ]

    result_2 = facade.complete_order(
        items=cart_2,
        email="laura.bianchi@email.it",
        address="Corso Vittorio 15, Torino",
        card_number="0000-0000-0000-0000",   # blocked card
    )

    print(f"\n  → success={result_2.success}, message='{result_2.message}'")

    # --- Scenario 3: product out of stock ---
    print("\n\n" + "─" * 55)
    print("  SCENARIO 3: Product out of stock")
    print("─" * 55)

    cart_3 = [
        CartItem("WEBCAM-HD", "Webcam Full HD", 1, 59.99),  # stock = 0
    ]

    result_3 = facade.complete_order(
        items=cart_3,
        email="marco.rossi@email.it",
        address="Via Roma 42, Milano",
        card_number="4532-1234-5678-9012",
    )

    print(f"\n  → success={result_3.success}, message='{result_3.message}'")


# ==========================================
# 7. ENTRY POINT
# ==========================================
if __name__ == "__main__":
    facade = CheckoutFacade()
    client_code(facade)
