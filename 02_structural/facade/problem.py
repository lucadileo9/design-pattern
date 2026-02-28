# ==========================================
# THE SUBSYSTEM — three complex services
# ==========================================
# Each class has its own interface, its own methods,
# its own protocol (first login, then request data).
# In a real system these would be libraries or external microservices.

class InventoryServiceX:
    """Subsystem X — manages inventory data."""
    def login_x(self, user: str, password: str) -> bool:
        print(f"[X] Login for '{user}'... OK.")
        return True

    def request_data_x(self) -> dict:
        print("[X] Retrieving inventory data...")
        return {"widget_a": 150, "widget_b": 89, "gadget_x": 320}

    def logout_x(self):
        print("[X] Inventory session closed.")


class AnalyticsServiceY:
    """Subsystem Y — provides analytics/sales data."""
    def authenticate_y(self, api_key: str) -> bool:
        # Note: the method has a different name from X (authenticate, not login)
        print(f"[Y] Authentication with API key '{api_key[:8]}...'... OK.")
        return True

    def fetch_metrics_y(self) -> dict:
        # Note: returns the same keys but with different values (average prices)
        print("[Y] Retrieving sales metrics...")
        return {"widget_a": 45.0, "widget_b": 12.5, "gadget_x": 78.0}

    def disconnect_y(self):
        print("[Y] Analytics connection closed.")


class ReportEngineZ:
    """Subsystem Z — visual report generator."""
    def initialize_z(self, title: str):
        print(f"[Z] Initializing report: '{title}'")

    def add_row_z(self, product: str, quantity: int, price: float):
        total = quantity * price
        print(f"[Z]   {product:<15} | Qty: {quantity:>5} | Price: €{price:>7.2f} | Total: €{total:>10.2f}")

    def finalize_z(self):
        print("[Z] Report completed and saved.")


# ==========================================
# THE PROBLEM: THE CLIENT AS ORCHESTRATOR
# ==========================================
# The client must know EVERY subsystem, EVERY method,
# and the CORRECT order of operations. It is the "glue".
#
# Obvious problems:
#  1. If X changes a method name (e.g. login_x → connect_x),
#     this code breaks.
#  2. If we add a fourth subsystem, we must modify this code.
#  3. Every client that wants to generate a report must repeat ALL this logic.
#  4. If a step is forgotten (e.g. login), the system fails.

def client_code():
    print("Client: I need to generate a report. Preparing everything manually...\n")

    # --- Step 1: Login to the inventory service ---
    x = InventoryServiceX()
    x.login_x("admin", "password123")

    # --- Step 2: Retrieve inventory data ---
    inventory = x.request_data_x()

    # --- Step 3: Authenticate to the analytics service ---
    y = AnalyticsServiceY()
    y.authenticate_y("ak-93jf82hd-prod-key")

    # --- Step 4: Retrieve sales data ---
    metrics = y.fetch_metrics_y()

    # --- Step 5: Data merging (logic in the client's hands!) ---
    # The client must know that the keys are the same in both dicts.
    # If a subsystem changes the keys, everything breaks.
    merged_data = {}
    for product in inventory:
        merged_data[product] = {
            "quantity": inventory[product],
            "price":    metrics.get(product, 0.0),
        }

    # --- Step 6: Report generation ---
    z = ReportEngineZ()
    z.initialize_z("Inventory + Sales Report")
    for product, values in merged_data.items():
        z.add_row_z(product, values["quantity"], values["price"])
    z.finalize_z()

    # --- Step 7: Cleanup (easy to forget!) ---
    x.logout_x()
    y.disconnect_y()


# ==========================================
# USAGE
# ==========================================
# If another module of the app wants to generate the same report,
# it must copy all this code. Any change to X, Y or Z
# forces changes in ALL places where this logic is duplicated.
if __name__ == "__main__":
    client_code()
