# ==========================================
# FACADE PATTERN — Esempio Reale
# Sistema di Checkout E-commerce
# ==========================================
#
# Scenario: completare un ordine online coinvolge 4 sottosistemi
# (catalogo, pagamento, spedizione, notifiche) che devono essere
# orchestrati nella sequenza corretta.
#
# Senza la Facade il client dovrebbe gestire tutto manualmente.
# Con la Facade chiama UN metodo: facade.complete_order()

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional


# ==========================================
# 0. STRUTTURE DATI
# ==========================================

@dataclass
class CartItem:
    """Un prodotto nel carrello."""
    product_id: str
    name: str
    quantity: int
    unit_price: float

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class OrderResult:
    """Risultato restituito dalla Facade al client."""
    success: bool
    order_id: Optional[str] = None
    tracking_code: Optional[str] = None
    total: float = 0.0
    message: str = ""


# ==========================================
# 1. SOTTOSISTEMA — Catalogo / Inventario
# ==========================================

class CatalogService:
    """Gestisce la disponibilità dei prodotti."""

    def __init__(self):
        # Inventario simulato: product_id → quantità
        self._stock: dict[str, int] = {
            "LAPTOP-001": 10,
            "MOUSE-042":  50,
            "MONITOR-27":  5,
            "WEBCAM-HD":   0,   # esaurito
        }

    def check_availability(self, product_id: str, quantity: int) -> bool:
        """Verifica se il prodotto è disponibile."""
        available = self._stock.get(product_id, 0)
        ok = available >= quantity
        print(f"  [Catalogo] {product_id} × {quantity}: "
              f"{'✓ disponibile' if ok else f'✗ solo {available} rimasti'}")
        return ok

    def reserve_stock(self, product_id: str, quantity: int):
        """Decrementa lo stock (riserva)."""
        self._stock[product_id] -= quantity
        print(f"  [Catalogo] Stock riservato: {product_id} × {quantity}")

    def release_stock(self, product_id: str, quantity: int):
        """Ripristina lo stock (rollback)."""
        self._stock[product_id] += quantity
        print(f"  [Catalogo] ↩ Stock rilasciato: {product_id} × {quantity}")


# ==========================================
# 2. SOTTOSISTEMA — Pagamenti
# ==========================================

class PaymentService:
    """Simula un gateway di pagamento (es. Stripe)."""

    # Carte bloccate per simulare fallimenti
    _BLOCKED = {"0000-0000-0000-0000"}

    def process_payment(self, card_number: str, amount: float) -> Optional[str]:
        """
        Tenta di addebitare l'importo sulla carta.
        Restituisce un transaction_id se va a buon fine, None se rifiutato.
        """
        if card_number in self._BLOCKED:
            print(f"  [Pagamento] ✗ Carta ****{card_number[-4:]} rifiutata")
            return None

        txn_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
        print(f"  [Pagamento] ✓ Addebito €{amount:.2f} su ****{card_number[-4:]} → {txn_id}")
        return txn_id


# ==========================================
# 3. SOTTOSISTEMA — Spedizioni
# ==========================================

class ShippingService:
    """Crea spedizioni e genera codici tracking."""

    def create_shipment(self, address: str, n_items: int) -> str:
        """Crea una spedizione e restituisce il codice tracking."""
        tracking = f"TRK-{uuid.uuid4().hex[:8].upper()}"
        print(f"  [Spedizione] ✓ Spedizione creata: {tracking}")
        print(f"               Destinazione: {address}")
        print(f"               Articoli: {n_items} pezzi")
        return tracking


# ==========================================
# 4. SOTTOSISTEMA — Notifiche
# ==========================================

class NotificationService:
    """Invia email di conferma o errore."""

    @staticmethod
    def send_confirmation(email: str, order_id: str, total: float, tracking: str):
        """Email di conferma ordine con tracking."""
        print(f"  [Email] ✉ Conferma a {email}: ordine {order_id}, €{total:.2f}, tracking {tracking}")

    @staticmethod
    def send_error(email: str, reason: str):
        """Email di errore."""
        print(f"  [Email] ✉ Errore a {email}: {reason}")


# ==========================================
# 5. LA FACADE — CheckoutFacade
# ==========================================
# Orchestra i 4 sottosistemi in sequenza, gestisce il rollback
# se qualcosa va storto, e restituisce un unico OrderResult.
#
# Il client NON conosce nessun sottosistema. Chiama solo:
#   facade.complete_order(items, email, address, card_number)

class CheckoutFacade:
    """
    Facade per il checkout e-commerce.
    Un unico metodo complete_order() nasconde 4 sottosistemi.
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
        Completa l'ordine orchestrando i sottosistemi:
          1. Verifica disponibilità
          2. Riserva stock
          3. Processa pagamento  (se fallisce → rollback stock)
          4. Crea spedizione
          5. Invia conferma
        """
        print(f"\n{'='*55}")
        print(f"  CHECKOUT — Ordine per {email}")
        print(f"{'='*55}")

        # --- 1. Verifica disponibilità ---
        print("\n📦 Passo 1 — Verifica disponibilità")
        for item in items:
            if not self._catalog.check_availability(item.product_id, item.quantity):
                msg = f"Prodotto '{item.name}' non disponibile"
                self._notifications.send_error(email, msg)
                return OrderResult(success=False, message=msg)

        # --- 2. Riserva stock ---
        print("\n📦 Passo 2 — Riserva stock")
        reserved: list[CartItem] = []
        for item in items:
            self._catalog.reserve_stock(item.product_id, item.quantity)
            reserved.append(item)

        # --- 3. Pagamento ---
        total = sum(item.subtotal for item in items)
        print(f"\n💳 Passo 3 — Pagamento (totale: €{total:.2f})")
        txn_id = self._payment.process_payment(card_number, total)

        if txn_id is None:
            # Rollback: rilascia lo stock riservato
            print("\n  ↩ ROLLBACK — Rilascio stock")
            for item in reserved:
                self._catalog.release_stock(item.product_id, item.quantity)
            msg = "Pagamento rifiutato"
            self._notifications.send_error(email, msg)
            return OrderResult(success=False, message=msg)

        # --- 4. Spedizione ---
        print("\n🚚 Passo 4 — Creazione spedizione")
        n_items = sum(item.quantity for item in items)
        tracking = self._shipping.create_shipment(address, n_items)

        # --- 5. Conferma ---
        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        print(f"\n✉️  Passo 5 — Conferma ordine {order_id}")
        self._notifications.send_confirmation(email, order_id, total, tracking)

        print(f"\n{'='*55}")
        print(f"  ✅ ORDINE COMPLETATO")
        print(f"{'='*55}")

        return OrderResult(
            success=True,
            order_id=order_id,
            tracking_code=tracking,
            total=total,
            message="Ordine completato con successo",
        )


# ==========================================
# 6. CODICE CLIENT
# ==========================================
# Il client prepara i dati e chiama UN metodo.
# Non conosce nessun sottosistema, non gestisce rollback.

def codice_client(facade: CheckoutFacade):

    # --- Scenario 1: ordine che va a buon fine ---
    print("\n" + "─" * 55)
    print("  SCENARIO 1: Ordine standard (successo)")
    print("─" * 55)

    carrello = [
        CartItem("LAPTOP-001", "Laptop Gaming Pro", 1, 1299.99),
        CartItem("MOUSE-042",  "Mouse Wireless",    2,   34.99),
    ]

    risultato = facade.complete_order(
        items=carrello,
        email="marco.rossi@email.it",
        address="Via Roma 42, Milano",
        card_number="4532-1234-5678-9012",
    )

    print(f"\n  → success={risultato.success}, order={risultato.order_id}, "
          f"tracking={risultato.tracking_code}, totale=€{risultato.total:.2f}")

    # --- Scenario 2: carta rifiutata → rollback automatico ---
    print("\n\n" + "─" * 55)
    print("  SCENARIO 2: Carta rifiutata (rollback automatico)")
    print("─" * 55)

    carrello_2 = [
        CartItem("MONITOR-27", "Monitor 4K 27\"", 2, 499.99),
    ]

    risultato_2 = facade.complete_order(
        items=carrello_2,
        email="laura.bianchi@email.it",
        address="Corso Vittorio 15, Torino",
        card_number="0000-0000-0000-0000",   # carta bloccata
    )

    print(f"\n  → success={risultato_2.success}, messaggio='{risultato_2.message}'")

    # --- Scenario 3: prodotto esaurito ---
    print("\n\n" + "─" * 55)
    print("  SCENARIO 3: Prodotto esaurito")
    print("─" * 55)

    carrello_3 = [
        CartItem("WEBCAM-HD", "Webcam Full HD", 1, 59.99),  # stock = 0
    ]

    risultato_3 = facade.complete_order(
        items=carrello_3,
        email="marco.rossi@email.it",
        address="Via Roma 42, Milano",
        card_number="4532-1234-5678-9012",
    )

    print(f"\n  → success={risultato_3.success}, messaggio='{risultato_3.message}'")


# ==========================================
# 7. ENTRY POINT
# ==========================================
if __name__ == "__main__":
    facade = CheckoutFacade()
    codice_client(facade)
