# ==========================================
# CONTESTO
# ==========================================
# Abbiamo un GeneratoreReport che sa come formattare e stampare dati.
# Lavora bene con i dati che arrivano dal database interno dell'azienda,
# perché è stato scritto insieme ad esso — stesso team, stesso formato.
#
# Il problema emerge quando dobbiamo integrare NUOVE sorgenti dati:
# una REST API di un fornitore esterno e un file CSV di un partner.
# Nessuna delle due restituisce dati nel formato che il generatore si aspetta.
#
# Non possiamo modificare le sorgenti (codice esterno / librerie di terze parti).
# Quindi modifichiamo il GeneratoreReport per gestire tutti i formati.
# Questo è l'errore che l'Adapter pattern evita.


# ==========================================
# LE SORGENTI DATI (che non si possono toccare)
# ==========================================
# Simulano codice esterno: librerie, API, sistemi legacy.
# Ognuna restituisce dati in un formato diverso e incompatibile.

class DatabaseAziendale:
    """Sorgente interna. Restituisce una lista di dizionari con chiavi standard."""
    def recupera_vendite(self) -> list[dict]:
        return [
            {"prodotto": "Widget A", "importo": 1500.0, "data": "2024-01-15"},
            {"prodotto": "Widget B", "importo": 890.0,  "data": "2024-01-16"},
        ]

class APIFornitoreEsterno:
    """
    REST API di un fornitore. Restituisce una lista di dizionari
    ma con chiavi in inglese e nomi completamente diversi.
    Non possiamo cambiare il formato: è definito dal fornitore.
    """
    def fetch_orders(self) -> list[dict]:
        return [
            {"item_name": "Gadget X", "total_eur": 3200.0, "order_date": "15-01-2024"},
            {"item_name": "Gadget Y", "total_eur": 210.5,  "order_date": "16-01-2024"},
        ]

class ParserCSV:
    """
    Legge file CSV di un partner commerciale.
    Restituisce una lista di tuple (non dizionari), con la data in formato diverso.
    """
    def leggi_file(self) -> list[tuple]:
        # (descrizione, valore_in_centesimi, giorno, mese, anno)
        return [
            ("Componente Z", 75000, 15, 1, 2024),
            ("Componente W", 42500, 16, 1, 2024),
        ]


# ==========================================
# IL PROBLEMA: IL CLIENT CHE GESTISCE TUTTO
# ==========================================
class GeneratoreReport:
    """
    Questo era un componente semplice e pulito.
    Sapeva fare una cosa sola: formattare e stampare righe di report.
    Dopo aver integrato le nuove sorgenti, è diventato un mostro.
    """

    def genera_report(self, sorgente: str):
        print(f"\n--- Report da: {sorgente} ---")

        # PROBLEMA 1: il GeneratoreReport conosce i dettagli interni
        #             di OGNI sorgente dati. È accoppiato a tutte.
        # PROBLEMA 2: ogni nuovo formato richiede un nuovo elif qui dentro,
        #             modificando una classe che "funzionava già".
        # PROBLEMA 3: la logica di traduzione (es. centesimi→euro, date)
        #             è sepolta qui nel mezzo, invisibile e non riusabile.

        if sorgente == "database":
            db = DatabaseAziendale()
            righe = db.recupera_vendite()
            for r in righe:
                # Il formato del DB è già quello giusto: accesso diretto.
                print(f"  Prodotto: {r['prodotto']:<15} | Importo: €{r['importo']:>8.2f} | Data: {r['data']}")

        elif sorgente == "api":
            api = APIFornitoreEsterno()
            righe = api.fetch_orders()
            for r in righe:
                # Dobbiamo tradurre: chiavi diverse, formato data diverso (gg-mm-aaaa → aaaa-mm-gg)
                parti_data = r["order_date"].split("-")
                data_convertita = f"{parti_data[2]}-{parti_data[1]}-{parti_data[0]}"
                print(f"  Prodotto: {r['item_name']:<15} | Importo: €{r['total_eur']:>8.2f} | Data: {data_convertita}")

        elif sorgente == "csv":
            parser = ParserCSV()
            righe = parser.leggi_file()
            for r in righe:
                # Dobbiamo tradurre: tuple → campi, centesimi → euro, data da 3 campi separati
                prodotto    = r[0]
                importo_eur = r[1] / 100
                data        = f"{r[4]}-{r[3]:02d}-{r[2]:02d}"
                print(f"  Prodotto: {prodotto:<15} | Importo: €{importo_eur:>8.2f} | Data: {data}")

        else:
            raise ValueError(f"Sorgente '{sorgente}' non supportata!")
        # Se domani arriva una quarta sorgente (es. un file XML, o un WebSocket),
        # dobbiamo tornare qui e aggiungere un altro elif.
        # Ogni modifica rischia di rompere i casi che già funzionavano.


# ==========================================
# UTILIZZO
# ==========================================
# I problemi visibili:
#  • GeneratoreReport dipende direttamente da DatabaseAziendale,
#    APIFornitoreEsterno e ParserCSV — tre classi esterne.
#  • Aggiungere una nuova sorgente = modificare GeneratoreReport.
#  • La logica di conversione (date, centesimi, chiavi) è dispersa
#    in un unico metodo lungo e difficile da testare.
if __name__ == "__main__":
    generatore = GeneratoreReport()
    generatore.genera_report("database")
    generatore.genera_report("api")
    generatore.genera_report("csv")