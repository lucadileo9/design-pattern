# ==========================================
# IL SOTTOSISTEMA — tre servizi complessi
# ==========================================
# Ogni classe ha la propria interfaccia, i propri metodi,
# il proprio protocollo (prima login, poi richiesta dati).
# In un sistema reale sarebbero librerie o microservizi esterni.

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
        # Nota: il metodo si chiama diversamente da X (autenticazione, non login)
        print(f"[Y] Autenticazione con API key '{api_key[:8]}...'... OK.")
        return True

    def fetch_metriche_y(self) -> dict:
        # Nota: ritorna le stesse chiavi ma con valori diversi (prezzi medi)
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
# IL PROBLEMA: IL CLIENT ORCHESTRATORE
# ==========================================
# Il client deve conoscere OGNI sottosistema, OGNI metodo,
# e l'ORDINE corretto delle operazioni. È lui il "collante".
#
# Problemi evidenti:
#  1. Se X cambia il nome di un metodo (es. login_x → connect_x),
#     questo codice si rompe.
#  2. Se aggiungiamo un quarto sottosistema, dobbiamo modificare qui.
#  3. Ogni client che vuole fare un report deve ripetere TUTTA questa logica.
#  4. Se ci si dimentica un passaggio (es. il login), il sistema fallisce.

def codice_client():
    print("Client: devo generare un report. Preparo tutto manualmente...\n")

    # --- Passo 1: Login al servizio inventario ---
    x = ServizioInventarioX()
    x.login_x("admin", "password123")

    # --- Passo 2: Recupero dati inventario ---
    inventario = x.richiedi_dati_x()

    # --- Passo 3: Autenticazione al servizio analytics ---
    y = ServizioAnalyticsY()
    y.autenticazione_y("ak-93jf82hd-prod-key")

    # --- Passo 4: Recupero dati vendite ---
    metriche = y.fetch_metriche_y()

    # --- Passo 5: Fusione dati (logica in mano al client!) ---
    # Il client deve sapere che le chiavi sono le stesse nei due dict.
    # Se un sottosistema cambia le chiavi, si rompe tutto.
    dati_fusi = {}
    for prodotto in inventario:
        dati_fusi[prodotto] = {
            "quantita": inventario[prodotto],
            "prezzo":   metriche.get(prodotto, 0.0),
        }

    # --- Passo 6: Generazione report ---
    z = MotoreReportZ()
    z.inizializza_z("Report Inventario + Vendite")
    for prodotto, valori in dati_fusi.items():
        z.aggiungi_riga_z(prodotto, valori["quantita"], valori["prezzo"])
    z.finalizza_z()

    # --- Passo 7: Pulizia (facile da dimenticare!) ---
    x.logout_x()
    y.disconnetti_y()


# ==========================================
# UTILIZZO
# ==========================================
# Se un altro modulo dell'app vuole generare lo stesso report,
# deve copiare tutto questo codice. Qualsiasi modifica a X, Y o Z
# obbliga a cambiare TUTTI i punti dove questa logica è duplicata.
if __name__ == "__main__":
    codice_client()
