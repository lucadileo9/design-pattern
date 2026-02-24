# ==========================================
# IL PATTERN FACADE — I sottosistemi restano IDENTICI
# ==========================================
# Le classi X, Y, Z non vengono toccate: la Facade li avvolge
# e offre al client un'interfaccia semplificata.


class ServizioInventarioX:
    """Sottosistema X — gestisce dati di inventario."""
    def login_x(self, user: str, password: str) -> bool:
        print(f"[X] Login di '{user}'... OK.")
        return True

    def richiedi_dati_x(self) -> dict:
        print("[X] Recupero dati inventario...")
        return {"widget_a": 150, "widget_b": 89, "gadget_x": 320}

    def logout_x(self):
        print("[X] Sessione inventario chiusa.")


class ServizioAnalyticsY:
    """Sottosistema Y — fornisce dati di analytics/vendite."""
    def autenticazione_y(self, api_key: str) -> bool:
        print(f"[Y] Autenticazione con API key '{api_key[:8]}...'... OK.")
        return True

    def fetch_metriche_y(self) -> dict:
        print("[Y] Recupero metriche di vendita...")
        return {"widget_a": 45.0, "widget_b": 12.5, "gadget_x": 78.0}

    def disconnetti_y(self):
        print("[Y] Connessione analytics chiusa.")


class MotoreReportZ:
    """Sottosistema Z — generatore di report visuali."""
    def inizializza_z(self, titolo: str):
        print(f"[Z] Inizializzazione report: '{titolo}'")

    def aggiungi_riga_z(self, prodotto: str, quantita: int, prezzo: float):
        totale = quantita * prezzo
        print(f"[Z]   {prodotto:<15} | Qtà: {quantita:>5} | Prezzo: €{prezzo:>7.2f} | Totale: €{totale:>10.2f}")

    def finalizza_z(self):
        print("[Z] Report completato e salvato.")


# ==========================================
# LA FACADE
# ==========================================
# La Facade:
#  - Conosce quali sottosistemi servono e come usarli
#  - Espone al client un metodo semplice e descrittivo
#  - Gestisce internamente l'ordine delle operazioni, la fusione
#    dei dati, e la pulizia delle risorse
#
# Il client non sa nemmeno che X, Y e Z esistono.

class ReportFacade:
    """
    Facade che nasconde la complessità di X, Y e Z.

    Il client chiama UN solo metodo: genera_report().
    Tutto il resto (login, fetch, merge, render, logout) è interno.
    """

    def __init__(self, user_x: str, password_x: str, api_key_y: str):
        # La Facade crea e configura i sottosistemi al suo interno
        self._x = ServizioInventarioX()
        self._y = ServizioAnalyticsY()
        self._z = MotoreReportZ()

        # Credenziali memorizzate privatamente
        self._user_x = user_x
        self._password_x = password_x
        self._api_key_y = api_key_y

    # --------------------------------------------------
    # Metodo pubblico — l'unica cosa che il client vede
    # --------------------------------------------------
    def genera_report(self, titolo: str = "Report Inventario + Vendite"):
        """
        Genera un report completo, orchestrando X → Y → fusione → Z.
        Il client non deve conoscere nessun sottosistema.
        """
        print(f"Facade: avvio generazione report '{titolo}'\n")

        # Passo 1-2: login e dati da X
        self._x.login_x(self._user_x, self._password_x)
        inventario = self._x.richiedi_dati_x()

        # Passo 3-4: autenticazione e dati da Y
        self._y.autenticazione_y(self._api_key_y)
        metriche = self._y.fetch_metriche_y()

        # Passo 5: fusione (logica che prima era nel client)
        dati_fusi = self._fondi_dati(inventario, metriche)

        # Passo 6: generazione report con Z
        self._z.inizializza_z(titolo)
        for prodotto, valori in dati_fusi.items():
            self._z.aggiungi_riga_z(prodotto, valori["quantita"], valori["prezzo"])
        self._z.finalizza_z()

        # Passo 7: pulizia — il client non deve ricordarsene
        self._x.logout_x()
        self._y.disconnetti_y()

        print("\nFacade: report completato con successo.")

    # --------------------------------------------------
    # Metodo privato — la logica di fusione è incapsulata
    # --------------------------------------------------
    @staticmethod
    def _fondi_dati(inventario: dict, metriche: dict) -> dict:
        """Unisce i dati di inventario con le metriche di vendita."""
        risultato = {}
        for prodotto in inventario:
            risultato[prodotto] = {
                "quantita": inventario[prodotto],
                "prezzo":   metriche.get(prodotto, 0.0),
            }
        return risultato


# ==========================================
# CODICE CLIENT — semplice, pulito, disaccoppiato
# ==========================================
# Il client:
#  - Non conosce X, Y, Z
#  - Non deve ricordare l'ordine delle operazioni
#  - Non deve gestire la pulizia delle risorse
#  - Se X cambia API, si aggiorna SOLO la Facade

def codice_client(facade: ReportFacade):
    """Il client riceve la Facade e chiama un solo metodo."""
    facade.genera_report("Report Trimestrale Q3")


# ==========================================
# UTILIZZO
# ==========================================
# Anche qui è importante notare che l'output dell'applicazione è identico a prima, ma il client è molto più semplice e disaccoppiato.
if __name__ == "__main__":
    # Configurazione: il client crea la Facade con le credenziali,
    # poi la usa senza preoccuparsi di nient'altro.
    facade = ReportFacade(
        user_x="admin",
        password_x="password123",
        api_key_y="ak-93jf82hd-prod-key",
    )
    codice_client(facade)
