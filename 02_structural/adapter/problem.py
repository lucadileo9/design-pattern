# ==========================================
# CONTEXT
# ==========================================
# We have a ReportGenerator that knows how to format and print data.
# It works well with data coming from the company's internal database,
# because it was written alongside it — same team, same format.
#
# The problem emerges when we need to integrate NEW data sources:
# a REST API from an external supplier and a CSV file from a partner.
# Neither returns data in the format the generator expects.
#
# We can't modify the sources (external code / third-party libraries).
# So we modify the ReportGenerator to handle all formats.
# This is the mistake that the Adapter pattern avoids.


# ==========================================
# DATA SOURCES (that cannot be touched)
# ==========================================
# They simulate external code: libraries, APIs, legacy systems.
# Each one returns data in a different and incompatible format.

class CompanyDatabase:
    """Internal source. Returns a list of dictionaries with standard keys."""
    def retrieve_sales(self) -> list[dict]:
        return [
            {"product": "Widget A", "amount": 1500.0, "date": "2024-01-15"},
            {"product": "Widget B", "amount": 890.0,  "date": "2024-01-16"},
        ]

class ExternalSupplierAPI:
    """
    REST API from a supplier. Returns a list of dictionaries
    but with English keys and completely different names.
    We can't change the format: it's defined by the supplier.
    """
    def fetch_orders(self) -> list[dict]:
        return [
            {"item_name": "Gadget X", "total_eur": 3200.0, "order_date": "15-01-2024"},
            {"item_name": "Gadget Y", "total_eur": 210.5,  "order_date": "16-01-2024"},
        ]

class CSVParser:
    """
    Reads CSV files from a commercial partner.
    Returns a list of tuples (not dictionaries), with the date in a different format.
    """
    def read_file(self) -> list[tuple]:
        # (description, value_in_cents, day, month, year)
        return [
            ("Component Z", 75000, 15, 1, 2024),
            ("Component W", 42500, 16, 1, 2024),
        ]


# ==========================================
# THE PROBLEM: THE CLIENT THAT MANAGES EVERYTHING
# ==========================================
class ReportGenerator:
    """
    This was a simple and clean component.
    It knew how to do one thing only: format and print report rows.
    After integrating the new sources, it became a monster.
    """

    def generate_report(self, source: str):
        print(f"\n--- Report from: {source} ---")

        # PROBLEM 1: the ReportGenerator knows the internal details
        #             of EVERY data source. It's coupled to all of them.
        # PROBLEM 2: every new format requires a new elif in here,
        #             modifying a class that "was already working".
        # PROBLEM 3: the translation logic (e.g. cents→euros, dates)
        #             is buried here in the middle, invisible and non-reusable.

        if source == "database":
            db = CompanyDatabase()
            rows = db.retrieve_sales()
            for r in rows:
                # The DB format is already the right one: direct access.
                print(f"  Product: {r['product']:<15} | Amount: €{r['amount']:>8.2f} | Date: {r['date']}")

        elif source == "api":
            api = ExternalSupplierAPI()
            rows = api.fetch_orders()
            for r in rows:
                # We must translate: different keys, different date format (dd-mm-yyyy → yyyy-mm-dd)
                date_parts = r["order_date"].split("-")
                converted_date = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"
                print(f"  Product: {r['item_name']:<15} | Amount: €{r['total_eur']:>8.2f} | Date: {converted_date}")

        elif source == "csv":
            parser = CSVParser()
            rows = parser.read_file()
            for r in rows:
                # We must translate: tuples → fields, cents → euros, date from 3 separate fields
                product     = r[0]
                amount_eur  = r[1] / 100
                date        = f"{r[4]}-{r[3]:02d}-{r[2]:02d}"
                print(f"  Product: {product:<15} | Amount: €{amount_eur:>8.2f} | Date: {date}")

        else:
            raise ValueError(f"Source '{source}' not supported!")
        # If tomorrow a fourth source arrives (e.g. an XML file, or a WebSocket),
        # we have to come back here and add another elif.
        # Every modification risks breaking the cases that were already working.


# ==========================================
# USAGE
# ==========================================
# Visible problems:
#  • ReportGenerator depends directly on CompanyDatabase,
#    ExternalSupplierAPI and CSVParser — three external classes.
#  • Adding a new source = modifying ReportGenerator.
#  • The conversion logic (dates, cents, keys) is scattered
#    in a single long method that's hard to test.
if __name__ == "__main__":
    generator = ReportGenerator()
    generator.generate_report("database")
    generator.generate_report("api")
    generator.generate_report("csv")