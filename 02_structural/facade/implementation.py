# ==========================================
# THE FACADE PATTERN — The subsystems remain IDENTICAL
# ==========================================
# Classes X, Y, Z are not touched: the Facade wraps them
# and offers the client a simplified interface.


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
        print(f"[Y] Authentication with API key '{api_key[:8]}...'... OK.")
        return True

    def fetch_metrics_y(self) -> dict:
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
# THE FACADE
# ==========================================
# The Facade:
#  - Knows which subsystems are needed and how to use them
#  - Exposes a simple and descriptive method to the client
#  - Internally handles the order of operations, data merging,
#    and resource cleanup
#
# The client doesn't even know that X, Y and Z exist.

class ReportFacade:
    """
    Facade that hides the complexity of X, Y and Z.

    The client calls ONE single method: generate_report().
    Everything else (login, fetch, merge, render, logout) is internal.
    """

    def __init__(self, user_x: str, password_x: str, api_key_y: str):
        # The Facade creates and configures the subsystems internally
        self._x = InventoryServiceX()
        self._y = AnalyticsServiceY()
        self._z = ReportEngineZ()

        # Credentials stored privately
        self._user_x = user_x
        self._password_x = password_x
        self._api_key_y = api_key_y

    # --------------------------------------------------
    # Public method — the only thing the client sees
    # --------------------------------------------------
    def generate_report(self, title: str = "Inventory + Sales Report"):
        """
        Generates a complete report, orchestrating X → Y → merge → Z.
        The client doesn't need to know any subsystem.
        """
        print(f"Facade: starting report generation '{title}'\n")

        # Step 1-2: login and data from X
        self._x.login_x(self._user_x, self._password_x)
        inventory = self._x.request_data_x()

        # Step 3-4: authentication and data from Y
        self._y.authenticate_y(self._api_key_y)
        metrics = self._y.fetch_metrics_y()

        # Step 5: merge (logic that was previously in the client)
        merged_data = self._merge_data(inventory, metrics)

        # Step 6: report generation with Z
        self._z.initialize_z(title)
        for product, values in merged_data.items():
            self._z.add_row_z(product, values["quantity"], values["price"])
        self._z.finalize_z()

        # Step 7: cleanup — the client doesn't have to remember this
        self._x.logout_x()
        self._y.disconnect_y()

        print("\nFacade: report completed successfully.")

    # --------------------------------------------------
    # Private method — the merge logic is encapsulated
    # --------------------------------------------------
    @staticmethod
    def _merge_data(inventory: dict, metrics: dict) -> dict:
        """Merges inventory data with sales metrics."""
        result = {}
        for product in inventory:
            result[product] = {
                "quantity": inventory[product],
                "price":    metrics.get(product, 0.0),
            }
        return result


# ==========================================
# CLIENT CODE — simple, clean, decoupled
# ==========================================
# The client:
#  - Doesn't know X, Y, Z
#  - Doesn't have to remember the order of operations
#  - Doesn't have to manage resource cleanup
#  - If X changes its API, only the Facade is updated

def client_code(facade: ReportFacade):
    """The client receives the Facade and calls a single method."""
    facade.generate_report("Quarterly Report Q3")


# ==========================================
# USAGE
# ==========================================
# It's also important to note that the application output is identical to before, but the client is much simpler and decoupled.
if __name__ == "__main__":
    # Configuration: the client creates the Facade with the credentials,
    # then uses it without worrying about anything else.
    facade = ReportFacade(
        user_x="admin",
        password_x="password123",
        api_key_y="ak-93jf82hd-prod-key",
    )
    client_code(facade)
