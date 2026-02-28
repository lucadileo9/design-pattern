# ==========================================
# TEMPLATE METHOD — Real Example: Data Import Pipeline
# ==========================================
# A system must import data from different sources (CSV, SQL).
# The flow is always the same: read → clean → save.
# But HOW the reading is done changes based on the source.
#
# The base class (DataImporter) defines the template method
# import_data() that guarantees the order: read_source() → clean_data() → save_to_db().
# Subclasses implement ONLY read_source() — the rest
# is inherited for free. Adding a JSONImporter tomorrow → one
# new class, zero modifications to the existing flow.

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


# ==========================================
# DATA MODEL
# ==========================================

@dataclass
class Record:
    """A single imported record (e.g., a log row)."""
    timestamp: str
    level: str          # INFO, WARNING, ERROR
    message: str
    source: str = ""    # filled during import


# ==========================================
# ABSTRACT CLASS — the "template"
# ==========================================
# import_data() is the template method: defines the rigid flow
# read → clean → save. Subclasses do NOT touch this
# method — they only implement read_source().

class DataImporter(ABC):
    """
    Base class: defines the import pipeline.

    Template method: import_data()
        1. read_source()   → ABSTRACT (each format implements it)
        2. clean_data()    → COMMON (removes duplicates, normalizes)
        3. save_to_db()    → COMMON (simulates saving)
    """

    def __init__(self, source_name: str):
        self.source_name = source_name

    def import_data(self) -> list[Record]:
        """
        Template method — the order is fixed and non-overridable.
        Subclasses customize ONLY read_source().
        """
        print(f"\n{'='*50}")
        print(f"  Pipeline: {self.source_name}")
        print(f"{'='*50}")

        # Step 1 — reading (ABSTRACT)
        records = self._read_source()

        # Step 2 — cleaning (COMMON)
        records = self._clean_data(records)

        # Step 3 — saving (COMMON)
        self._save_to_db(records)

        return records

    # --- ABSTRACT step (implemented by subclasses) ---

    @abstractmethod
    def _read_source(self) -> list[Record]:
        """Reads data from the specific source. Each format is different."""
        ...

    # --- COMMON steps (implemented here, only once) ---

    def _clean_data(self, records: list[Record]) -> list[Record]:
        """
        Cleaning common to ALL sources:
        - removes records with empty message
        - normalizes level to uppercase
        - removes duplicates (same timestamp + message)
        """
        name = self.__class__.__name__
        print(f"\n[{name}] Step 2 — Data cleaning")
        print(f"  Records received: {len(records)}")

        # Normalize level
        for r in records:
            r.level = r.level.strip().upper()

        # Remove records with empty message
        before = len(records)
        records = [r for r in records if r.message.strip()]
        removed_empty = before - len(records)

        # Remove duplicates
        seen: set[tuple[str, str]] = set()
        unique: list[Record] = []
        for r in records:
            key = (r.timestamp, r.message)
            if key not in seen:
                seen.add(key)
                unique.append(r)
        removed_duplicates = len(records) - len(unique)
        records = unique

        print(f"  Removed {removed_empty} empty, {removed_duplicates} duplicates")
        print(f"  Clean records: {len(records)}")
        return records

    def _save_to_db(self, records: list[Record]) -> None:
        """
        Saving common to ALL sources.
        (Simulated — in production this would be a DB INSERT.)
        """
        name = self.__class__.__name__
        print(f"\n[{name}] Step 3 — Saving to DB")

        if not records:
            print("  ⚠️ No records to save")
            return

        for r in records:
            icon = {"INFO": "ℹ️", "WARNING": "⚠️", "ERROR": "❌"}.get(r.level, "❓")
            print(f"  {icon} [{r.timestamp}] {r.level}: {r.message}")

        print(f"\n  ✅ {len(records)} records saved from '{self.source_name}'")


# ==========================================
# CONCRETE CLASSES — only the reading changes
# ==========================================

class CSVImporter(DataImporter):
    """Reads logs from a CSV file (simulated with strings)."""

    def __init__(self, csv_content: str):
        super().__init__("file_log.csv")
        self._content = csv_content

    def _read_source(self) -> list[Record]:
        print(f"\n[CSVImporter] Step 1 — Reading CSV file")
        print(f"  📄 Parsing '{self.source_name}'...")

        records: list[Record] = []
        rows = self._content.strip().split("\n")

        for i, row in enumerate(rows):
            # Skip header
            if i == 0:
                print(f"  Header: {row}")
                continue

            parts = row.split(",")
            if len(parts) >= 3:
                record = Record(
                    timestamp=parts[0].strip(),
                    level=parts[1].strip(),
                    message=parts[2].strip(),
                    source="CSV"
                )
                records.append(record)

        print(f"  Rows read: {len(records)}")
        return records


class SQLImporter(DataImporter):
    """Reads logs from a SQL database (simulated with a list of tuples)."""

    def __init__(self, query_results: list[tuple[str, str, str]]):
        super().__init__("external_db.logs")
        self._results = query_results

    def _read_source(self) -> list[Record]:
        print(f"\n[SQLImporter] Step 1 — SQL database query")
        print(f"  🗄️ Connecting to '{self.source_name}'...")
        print(f"  🗄️ Executing: SELECT timestamp, level, message FROM logs")

        records: list[Record] = []
        for row in self._results:
            record = Record(
                timestamp=row[0],
                level=row[1],
                message=row[2],
                source="SQL"
            )
            records.append(record)

        print(f"  Rows read: {len(records)}")
        print(f"  🗄️ Connection closed")
        return records


# ==========================================
# USAGE
# ==========================================

if __name__ == "__main__":

    print("=" * 50)
    print("  TEMPLATE METHOD — Data Import Pipeline")
    print("=" * 50)

    # --- Scenario 1: import from CSV ---
    # Includes: an empty message and a duplicate (will be removed)
    csv_data = """timestamp,level,message
2026-02-26 10:00:01,info,Server startup
2026-02-26 10:00:05,warning,Memory at 85%
2026-02-26 10:00:12,error,DB connection failed
2026-02-26 10:00:12,error,DB connection failed
2026-02-26 10:00:20,info,
2026-02-26 10:00:30,info,Connection retry succeeded"""

    csv_importer = CSVImporter(csv_data)
    csv_importer.import_data()

    # --- Scenario 2: import from SQL ---
    # Includes: an empty message (will be removed)
    sql_data = [
        ("2026-02-26 11:00:00", "INFO", "Deploy completed"),
        ("2026-02-26 11:05:00", "warning", "CPU at 92%"),
        ("2026-02-26 11:10:00", "ERROR", "External API timeout"),
        ("2026-02-26 11:15:00", "info", "  "),
        ("2026-02-26 11:20:00", "INFO", "Auto-scaling activated"),
    ]

    sql_importer = SQLImporter(sql_data)
    sql_importer.import_data()

    # The key point: both importers use the SAME
    # pipeline (import_data → read → clean → save). Only the
    # reading differs. Adding a JSONImporter requires
    # only a new class with _read_source() — the rest
    # is inherited from the base class without duplication.
