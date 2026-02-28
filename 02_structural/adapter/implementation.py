from abc import ABC, abstractmethod

# ==========================================
# DATA SOURCES — unchanged from the problem
# ==========================================
# These classes are not touched. They are external code, third-party libraries,
# or legacy systems: we have no control over their output format.
# The point of the Adapter is precisely not having to modify them.

class CompanyDatabase:
    def retrieve_sales(self) -> list[dict]:
        return [
            {"product": "Widget A", "amount": 1500.0, "date": "2024-01-15"},
            {"product": "Widget B", "amount": 890.0,  "date": "2024-01-16"},
        ]

class ExternalSupplierAPI:
    def fetch_orders(self) -> list[dict]:
        return [
            {"item_name": "Gadget X", "total_eur": 3200.0, "order_date": "15-01-2024"},
            {"item_name": "Gadget Y", "total_eur": 210.5,  "order_date": "16-01-2024"},
        ]

class CSVParser:
    def read_file(self) -> list[tuple]:
        # (description, value_in_cents, day, month, year)
        return [
            ("Component Z", 75000, 15, 1, 2024),
            ("Component W", 42500, 16, 1, 2024),
        ]


# ==========================================
# 1. THE TARGET (interface that the client knows)
# ==========================================
# We define the standard format that the ReportGenerator expects.
# It's the only contract the client knows: it knows nothing about fetch_orders(),
# read_file() or the specific formats of each source.
#
# The normalized format that all adapters must produce is:
#   {"product": str, "amount": float, "date": "YYYY-MM-DD"}
#
# The chosen format (that will be used throughout the client code) is a
# dictionary with standard keys and date in ISO format. But it could be
# anything: the important thing is that it's UNIQUE and STANDARD for the entire client.

class DataSource(ABC):
    @abstractmethod
    def get_sales(self) -> list[dict]:
        """
        Always returns a list of dictionaries in the standard format:
        [{"product": str, "amount": float, "date": "YYYY-MM-DD"}, ...]
        """
        pass


# ==========================================
# 2. THE ADAPTERS (one for each Adaptee)
# ==========================================
# Each Adapter:
#   - IMPLEMENTS DataSource  → the client treats it as a Target
#   - CONTAINS an instance of the Adaptee → delegates the real work to it
#   - Translates the Adaptee's specific format into the Target's standard format
#
# The conversion logic (dates, cents, keys) that in the problem
# was placed in the ReportGenerator is now isolated here, in a dedicated class
# for each source. This way we respect the Single Responsibility Principle:
# each class has a single responsibility: the adapter only handles translation

class DatabaseAdapter(DataSource):
    """
    Adapter for CompanyDatabase.
    The DB already uses the standard format, so no translation is needed:
    the adapter simply delegates the call.
    It exists anyway to uniform the interface towards the client.
    """
    def __init__(self):
        self._adaptee = CompanyDatabase()

    def get_sales(self) -> list[dict]:
        # The DB format already matches the Target: direct delegation.
        return self._adaptee.retrieve_sales()


class APIAdapter(DataSource):
    """
    Adapter for ExternalSupplierAPI.
    Translates: English keys → standard keys, date "DD-MM-YYYY" → "YYYY-MM-DD".
    """
    def __init__(self):
        self._adaptee = ExternalSupplierAPI()

    def get_sales(self) -> list[dict]:
        raw_rows = self._adaptee.fetch_orders()
        result = []
        for r in raw_rows:
            # Date format translation: "15-01-2024" → "2024-01-15"
            d, m, y = r["order_date"].split("-")
            result.append({
                "product": r["item_name"],
                "amount":  r["total_eur"],
                "date":    f"{y}-{m}-{d}",
            })
        return result


class CSVAdapter(DataSource):
    """
    Adapter for CSVParser.
    Translates: tuples with 5 fields → standard dict, cents → euros, 3 date fields → ISO string.
    """
    def __init__(self):
        self._adaptee = CSVParser()

    def get_sales(self) -> list[dict]:
        raw_rows = self._adaptee.read_file()
        result = []
        for r in raw_rows:
            # (description, value_in_cents, day, month, year)
            result.append({
                "product": r[0],
                "amount":  r[1] / 100,              # cents → euros
                "date":    f"{r[4]}-{r[3]:02d}-{r[2]:02d}",  # YYYY-MM-DD
            })
        return result


# ==========================================
# 3. THE CLIENT — ReportGenerator
# ==========================================
# Comparison with the version in the problem:
#
#   BEFORE: knew CompanyDatabase, ExternalSupplierAPI, CSVParser,
#           had three elif with different conversion logic for each.
#
#   NOW:    knows only DataSource. One method. One format. Zero elif.
#           Doesn't know or care if the data comes from a DB, an API, or a CSV.
#
# Adding a fifth source tomorrow (e.g. an XML file)?
# Just write XmlAdapter(DataSource) and the ReportGenerator doesn't change by a single line.

class ReportGenerator:
    def generate_report(self, source: DataSource, name: str):
        print(f"\n--- Report from: {name} ---")
        for r in source.get_sales():
            # The format is always the same: direct access to standard keys.
            print(f"  Product: {r['product']:<15} | Amount: €{r['amount']:>8.2f} | Date: {r['date']}")


# ==========================================
# 4. CLIENT CODE
# ==========================================
# The client instantiates the Adapters (knows that different sources exist),
# but passes to the generator only the DataSource interface.
# The Adapter choice could also come from configuration or
# from another factory — in that case the generator would be completely
# unaware of which source it's using.

# Note that the output of both files (with and without Adapter) is identical.
# The difference is that now the code is clean, modular, extensible and respects SOLID principles.

if __name__ == "__main__":
    generator = ReportGenerator()

    sources = [
        (DatabaseAdapter(), "Company Database"),
        (APIAdapter(),      "External Supplier API"),
        (CSVAdapter(),      "Partner CSV File"),
    ]

    for adapter, name in sources:
        generator.generate_report(adapter, name)
