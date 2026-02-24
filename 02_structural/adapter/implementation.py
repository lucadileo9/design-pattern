from abc import ABC, abstractmethod

# ==========================================
# LE SORGENTI DATI — invariate rispetto al problema
# ==========================================
# Queste classi non si toccano. Sono codice esterno, librerie di terze parti,
# o sistemi legacy: non abbiamo il controllo sul loro formato di output.
# Il punto dell'Adapter è proprio non doverle modificare.

class DatabaseAziendale:
    def recupera_vendite(self) -> list[dict]:
        return [
            {"prodotto": "Widget A", "importo": 1500.0, "data": "2024-01-15"},
            {"prodotto": "Widget B", "importo": 890.0,  "data": "2024-01-16"},
        ]

class APIFornitoreEsterno:
    def fetch_orders(self) -> list[dict]:
        return [
            {"item_name": "Gadget X", "total_eur": 3200.0, "order_date": "15-01-2024"},
            {"item_name": "Gadget Y", "total_eur": 210.5,  "order_date": "16-01-2024"},
        ]

class ParserCSV:
    def leggi_file(self) -> list[tuple]:
        # (descrizione, valore_in_centesimi, giorno, mese, anno)
        return [
            ("Componente Z", 75000, 15, 1, 2024),
            ("Componente W", 42500, 16, 1, 2024),
        ]


# ==========================================
# 1. IL TARGET (interfaccia che il client conosce)
# ==========================================
# Definiamo il formato standard che il GeneratoreReport si aspetta.
# È l'unico contratto che il client conosce: non sa nulla di fetch_orders(),
# leggi_file() o dei formati specifici di ciascuna sorgente.
#
# Il formato normalizzato che tutti gli adapter devono produrre è:
#   {"prodotto": str, "importo": float, "data": "AAAA-MM-GG"}
#
# Il formato scelto (che verrà usato in tutto il codice del client) è un 
# dizionario con chiavi italiane e data in formato ISO. Ma potrebbe essere
# qualsiasi cosa: l'importante è che sia UNICO e STANDARD per tutto il client.

class SorgenteDati(ABC):
    @abstractmethod
    def get_vendite(self) -> list[dict]:
        """
        Restituisce sempre una lista di dizionari nel formato standard:
        [{"prodotto": str, "importo": float, "data": "AAAA-MM-GG"}, ...]
        """
        pass


# ==========================================
# 2. GLI ADAPTER (uno per ogni Adaptee)
# ==========================================
# Ogni Adapter:
#   - IMPLEMENTA SorgenteDati  → il client lo tratta come un Target
#   - CONTIENE un'istanza dell'Adaptee → delega il lavoro reale ad esso
#   - Traduce il formato specifico dell'Adaptee in quello standard del Target
#
# La logica di conversione (date, centesimi, chiavi) che nel problema
# era messa nel GeneratoreReport ora è isolata qui, in una classe dedicata
# per ogni sorgente. Così facendo rispettiamo il Single Responsibility Principle:
# ogni classe ha una sola responsabilità: l'adapter si occupa solo di tradurre

class DatabaseAdapter(SorgenteDati):
    """
    Adapter per DatabaseAziendale.
    Il DB già usa il formato standard, quindi non serve traduzione:
    l'adapter si limita a delegare la chiamata.
    Esiste comunque per uniformare l'interfaccia verso il client.
    """
    def __init__(self):
        self._adaptee = DatabaseAziendale()

    def get_vendite(self) -> list[dict]:
        # Il formato del DB coincide già con il Target: delega diretta.
        return self._adaptee.recupera_vendite()


class APIAdapter(SorgenteDati):
    """
    Adapter per APIFornitoreEsterno.
    Traduce: chiavi inglesi → chiavi italiane, data "GG-MM-AAAA" → "AAAA-MM-GG".
    """
    def __init__(self):
        self._adaptee = APIFornitoreEsterno()

    def get_vendite(self) -> list[dict]:
        righe_grezze = self._adaptee.fetch_orders()
        risultato = []
        for r in righe_grezze:
            # Traduzione del formato data: "15-01-2024" → "2024-01-15"
            g, m, a = r["order_date"].split("-")
            risultato.append({
                "prodotto": r["item_name"],
                "importo":  r["total_eur"],
                "data":     f"{a}-{m}-{g}",
            })
        return risultato


class CSVAdapter(SorgenteDati):
    """
    Adapter per ParserCSV.
    Traduce: tuple con 5 campi → dict standard, centesimi → euro, 3 campi data → stringa ISO.
    """
    def __init__(self):
        self._adaptee = ParserCSV()

    def get_vendite(self) -> list[dict]:
        righe_grezze = self._adaptee.leggi_file()
        risultato = []
        for r in righe_grezze:
            # (descrizione, valore_in_centesimi, giorno, mese, anno)
            risultato.append({
                "prodotto": r[0],
                "importo":  r[1] / 100,              # centesimi → euro
                "data":     f"{r[4]}-{r[3]:02d}-{r[2]:02d}",  # AAAA-MM-GG
            })
        return risultato


# ==========================================
# 3. IL CLIENT — GeneratoreReport
# ==========================================
# Confronto con la versione nel problema:
#
#   PRIMA: conosceva DatabaseAziendale, APIFornitoreEsterno, ParserCSV,
#          aveva tre elif con logica di conversione diversa per ognuna.
#
#   ORA:   conosce solo SorgenteDati. Un metodo. Un formato. Zero elif.
#          Non sa né vuole sapere se i dati vengono da un DB, un'API o un CSV.
#
# Aggiungere una quinta sorgente domani (es. un file XML)?
# Si scrive XmlAdapter(SorgenteDati) e il GeneratoreReport non cambia di una riga.

class GeneratoreReport:
    def genera_report(self, sorgente: SorgenteDati, nome: str):
        print(f"\n--- Report da: {nome} ---")
        for r in sorgente.get_vendite():
            # Il formato è sempre lo stesso: accesso diretto alle chiavi standard.
            print(f"  Prodotto: {r['prodotto']:<15} | Importo: €{r['importo']:>8.2f} | Data: {r['data']}")


# ==========================================
# 4. CODICE CLIENT
# ==========================================
# Il client istanzia gli Adapter (sa che esistono sorgenti diverse),
# ma passa al generatore solo l'interfaccia SorgenteDati.
# La scelta dell'Adapter potrebbe anche venire da configurazione o
# da un'altra factory — in quel caso il generatore sarebbe completamente
# ignaro persino di quale sorgente sta usando.

# Da notare che l'output dei due file (con e senza Adapter) è identico.
# La differenza è che ora il codice è pulito, modulare, estendibile e rispetta i principi SOLID.

if __name__ == "__main__":
    generatore = GeneratoreReport()

    sorgenti = [
        (DatabaseAdapter(), "Database Aziendale"),
        (APIAdapter(),      "API Fornitore Esterno"),
        (CSVAdapter(),      "File CSV Partner"),
    ]

    for adapter, nome in sorgenti:
        generatore.genera_report(adapter, nome)
