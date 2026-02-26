# ==========================================
# TEMPLATE METHOD — Esempio reale: Pipeline di Importazione Dati
# ==========================================
# Un sistema deve importare dati da sorgenti diverse (CSV, SQL).
# Il flusso è sempre lo stesso: leggi → pulisci → salva.
# Ma il COME si legge cambia in base alla sorgente.
#
# La classe base (ImportatoreDati) definisce il template method
# importa() che garantisce l'ordine: leggi_sorgente() → pulisci_dati() → salva_nel_db().
# Le sotto-classi implementano SOLO leggi_sorgente() — il resto
# lo ereditano gratis. Aggiungere un JSONImporter domani → una
# sola classe nuova, zero modifiche al flusso esistente.

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


# ==========================================
# MODELLO DATI
# ==========================================

@dataclass
class Record:
    """Un singolo record importato (es. una riga di log)."""
    timestamp: str
    livello: str        # INFO, WARNING, ERROR
    messaggio: str
    sorgente: str = ""  # compilato durante l'importazione


# ==========================================
# CLASSE ASTRATTA — il "template"
# ==========================================
# importa() è il template method: definisce il flusso rigido
# leggi → pulisci → salva. Le sotto-classi NON toccano questo
# metodo — implementano solo leggi_sorgente().

class ImportatoreDati(ABC):
    """
    Classe base: definisce la pipeline di importazione.

    Template method: importa()
        1. leggi_sorgente()  → ASTRATTO (ogni formato lo implementa)
        2. pulisci_dati()    → COMUNE (rimuove duplicati, normalizza)
        3. salva_nel_db()    → COMUNE (simula il salvataggio)
    """

    def __init__(self, nome_sorgente: str):
        self.nome_sorgente = nome_sorgente

    def importa(self) -> list[Record]:
        """
        Template method — l'ordine è fisso e non sovrascrivibile.
        Le sotto-classi personalizzano SOLO leggi_sorgente().
        """
        print(f"\n{'='*50}")
        print(f"  Pipeline: {self.nome_sorgente}")
        print(f"{'='*50}")

        # Step 1 — lettura (ASTRATTO)
        records = self._leggi_sorgente()

        # Step 2 — pulizia (COMUNE)
        records = self._pulisci_dati(records)

        # Step 3 — salvataggio (COMUNE)
        self._salva_nel_db(records)

        return records

    # --- Step ASTRATTO (implementato dalle sotto-classi) ---

    @abstractmethod
    def _leggi_sorgente(self) -> list[Record]:
        """Legge i dati dalla sorgente specifica. Ogni formato è diverso."""
        ...

    # --- Step COMUNI (implementati qui, una sola volta) ---

    def _pulisci_dati(self, records: list[Record]) -> list[Record]:
        """
        Pulizia comune a TUTTE le sorgenti:
        - rimuove record con messaggio vuoto
        - normalizza il livello in maiuscolo
        - rimuove duplicati (stesso timestamp + messaggio)
        """
        nome = self.__class__.__name__
        print(f"\n[{nome}] Step 2 — Pulizia dati")
        print(f"  Record ricevuti: {len(records)}")

        # Normalizza livello
        for r in records:
            r.livello = r.livello.strip().upper()

        # Rimuovi record con messaggio vuoto
        prima = len(records)
        records = [r for r in records if r.messaggio.strip()]
        rimossi_vuoti = prima - len(records)

        # Rimuovi duplicati
        visti: set[tuple[str, str]] = set()
        unici: list[Record] = []
        for r in records:
            chiave = (r.timestamp, r.messaggio)
            if chiave not in visti:
                visti.add(chiave)
                unici.append(r)
        rimossi_duplicati = len(records) - len(unici)
        records = unici

        print(f"  Rimossi {rimossi_vuoti} vuoti, {rimossi_duplicati} duplicati")
        print(f"  Record puliti: {len(records)}")
        return records

    def _salva_nel_db(self, records: list[Record]) -> None:
        """
        Salvataggio comune a TUTTE le sorgenti.
        (Simulato — in produzione sarebbe un INSERT nel DB.)
        """
        nome = self.__class__.__name__
        print(f"\n[{nome}] Step 3 — Salvataggio nel DB")

        if not records:
            print("  ⚠️ Nessun record da salvare")
            return

        for r in records:
            icona = {"INFO": "ℹ️", "WARNING": "⚠️", "ERROR": "❌"}.get(r.livello, "❓")
            print(f"  {icona} [{r.timestamp}] {r.livello}: {r.messaggio}")

        print(f"\n  ✅ {len(records)} record salvati da '{self.nome_sorgente}'")


# ==========================================
# CLASSI CONCRETE — solo la lettura cambia
# ==========================================

class CSVImporter(ImportatoreDati):
    """Legge log da un file CSV (simulato con stringhe)."""

    def __init__(self, contenuto_csv: str):
        super().__init__("file_log.csv")
        self._contenuto = contenuto_csv

    def _leggi_sorgente(self) -> list[Record]:
        print(f"\n[CSVImporter] Step 1 — Lettura file CSV")
        print(f"  📄 Parsing di '{self.nome_sorgente}'...")

        records: list[Record] = []
        righe = self._contenuto.strip().split("\n")

        for i, riga in enumerate(righe):
            # Salta l'intestazione
            if i == 0:
                print(f"  Intestazione: {riga}")
                continue

            parti = riga.split(",")
            if len(parti) >= 3:
                record = Record(
                    timestamp=parti[0].strip(),
                    livello=parti[1].strip(),
                    messaggio=parti[2].strip(),
                    sorgente="CSV"
                )
                records.append(record)

        print(f"  Righe lette: {len(records)}")
        return records


class SQLImporter(ImportatoreDati):
    """Legge log da un database SQL (simulato con una lista di tuple)."""

    def __init__(self, risultati_query: list[tuple[str, str, str]]):
        super().__init__("db_esterno.logs")
        self._risultati = risultati_query

    def _leggi_sorgente(self) -> list[Record]:
        print(f"\n[SQLImporter] Step 1 — Query database SQL")
        print(f"  🗄️ Connessione a '{self.nome_sorgente}'...")
        print(f"  🗄️ Esecuzione: SELECT timestamp, livello, messaggio FROM logs")

        records: list[Record] = []
        for riga in self._risultati:
            record = Record(
                timestamp=riga[0],
                livello=riga[1],
                messaggio=riga[2],
                sorgente="SQL"
            )
            records.append(record)

        print(f"  Righe lette: {len(records)}")
        print(f"  🗄️ Connessione chiusa")
        return records


# ==========================================
# UTILIZZO
# ==========================================

if __name__ == "__main__":

    print("=" * 50)
    print("  TEMPLATE METHOD — Pipeline di Importazione Dati")
    print("=" * 50)

    # --- Scenario 1: importazione da CSV ---
    # Include: un messaggio vuoto e un duplicato (verranno rimossi)
    csv_data = """timestamp,livello,messaggio
2026-02-26 10:00:01,info,Avvio del server
2026-02-26 10:00:05,warning,Memoria al 85%
2026-02-26 10:00:12,error,Connessione al DB fallita
2026-02-26 10:00:12,error,Connessione al DB fallita
2026-02-26 10:00:20,info,
2026-02-26 10:00:30,info,Retry connessione riuscito"""

    csv_importer = CSVImporter(csv_data)
    csv_importer.importa()

    # --- Scenario 2: importazione da SQL ---
    # Include: un messaggio vuoto (verrà rimosso)
    sql_data = [
        ("2026-02-26 11:00:00", "INFO", "Deploy completato"),
        ("2026-02-26 11:05:00", "warning", "CPU al 92%"),
        ("2026-02-26 11:10:00", "ERROR", "Timeout API esterna"),
        ("2026-02-26 11:15:00", "info", "  "),
        ("2026-02-26 11:20:00", "INFO", "Scaling automatico attivato"),
    ]

    sql_importer = SQLImporter(sql_data)
    sql_importer.importa()

    # Il punto chiave: entrambi gli importer usano la STESSA
    # pipeline (importa → leggi → pulisci → salva). Solo la
    # lettura è diversa. Aggiungere un JSONImporter richiede
    # solo una nuova classe con _leggi_sorgente() — il resto
    # viene ereditato dalla classe base senza duplicazione.
