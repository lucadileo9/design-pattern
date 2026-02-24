# ==========================================
# COMPOSITE — Esempio reale: Menu di un ristorante
# ==========================================
# Un menu di ristorante ha una struttura ad albero:
#   - Piatti singoli (foglie): "Bruschetta", "Carbonara", ecc.
#   - Sezioni (composite): "Antipasti", "Primi", "Bevande", ecc.
#
# Le sezioni possono contenere piatti o sotto-sezioni
# (es. "Bevande" → "Analcoliche" / "Alcoliche").
#
# Il client vuole poter chiedere a qualsiasi elemento:
#   - mostra()           → stampa la struttura
#   - conta_piatti()     → quanti piatti ci sono
#   - get_prezzo_medio() → prezzo medio dei piatti contenuti
# … senza distinguere tra piatto singolo e sezione intera.

from abc import ABC, abstractmethod


# ==========================================
# COMPONENT — interfaccia comune
# ==========================================

class ComponenteMenu(ABC):
    """Interfaccia comune per piatti e sezioni del menu."""

    def __init__(self, nome: str):
        self.nome = nome

    @abstractmethod
    def mostra(self, indentazione: int = 0) -> None:
        """Stampa l'elemento (e i figli, se presenti)."""
        ...

    @abstractmethod
    def conta_piatti(self) -> int:
        """Numero di piatti (foglie) contenuti."""
        ...

    @abstractmethod
    def get_prezzi(self) -> list[float]:
        """Lista di tutti i prezzi dei piatti contenuti."""
        ...

    def get_prezzo_medio(self) -> float:
        """Prezzo medio calcolato dai prezzi raccolti."""
        prezzi = self.get_prezzi()
        if not prezzi:
            return 0.0
        return sum(prezzi) / len(prezzi)


# ==========================================
# LEAF — singolo piatto
# ==========================================

class Piatto(ComponenteMenu):
    """Foglia: un piatto con nome, prezzo e (opzionale) descrizione."""

    def __init__(self, nome: str, prezzo: float, descrizione: str = ""):
        super().__init__(nome)
        self.prezzo = prezzo
        self.descrizione = descrizione

    def mostra(self, indentazione: int = 0) -> None:
        prefisso = "  " * indentazione
        desc = f"  — {self.descrizione}" if self.descrizione else ""
        print(f"{prefisso}• {self.nome}: €{self.prezzo:.2f}{desc}")

    def conta_piatti(self) -> int:
        return 1

    def get_prezzi(self) -> list[float]:
        return [self.prezzo]


# ==========================================
# COMPOSITE — sezione del menu
# ==========================================

class SezioneMenu(ComponenteMenu):
    """Composite: una sezione che contiene piatti e/o sotto-sezioni."""

    def __init__(self, nome: str):
        super().__init__(nome)
        self._figli: list[ComponenteMenu] = []

    def aggiungi(self, componente: ComponenteMenu) -> None:
        self._figli.append(componente)

    def rimuovi(self, componente: ComponenteMenu) -> None:
        self._figli.remove(componente)

    # --- operazioni dell'interfaccia (delegate ai figli) ---

    def mostra(self, indentazione: int = 0) -> None:
        prefisso = "  " * indentazione
        print(f"{prefisso}📂 {self.nome}")
        for figlio in self._figli:
            figlio.mostra(indentazione + 1)

    def conta_piatti(self) -> int:
        return sum(figlio.conta_piatti() for figlio in self._figli)

    def get_prezzi(self) -> list[float]:
        prezzi: list[float] = []
        for figlio in self._figli:
            prezzi.extend(figlio.get_prezzi())
        return prezzi


# ==========================================
# UTILIZZO — costruzione e navigazione del menu
# ==========================================

if __name__ == "__main__":

    # --- Antipasti ---
    bruschetta = Piatto("Bruschetta", 6.00, "pomodoro, basilico, olio EVO")
    caprese = Piatto("Caprese", 8.50, "mozzarella di bufala, pomodoro")
    tagliere = Piatto("Tagliere misto", 12.00, "salumi e formaggi locali")

    antipasti = SezioneMenu("Antipasti")
    antipasti.aggiungi(bruschetta)
    antipasti.aggiungi(caprese)
    antipasti.aggiungi(tagliere)

    # --- Primi ---
    carbonara = Piatto("Carbonara", 11.00)
    amatriciana = Piatto("Amatriciana", 10.50)
    risotto = Piatto("Risotto ai funghi porcini", 13.00)

    primi = SezioneMenu("Primi Piatti")
    primi.aggiungi(carbonara)
    primi.aggiungi(amatriciana)
    primi.aggiungi(risotto)

    # --- Secondi ---
    tagliata = Piatto("Tagliata di manzo", 18.00, "con rucola e grana")
    branzino = Piatto("Branzino al forno", 16.50)

    secondi = SezioneMenu("Secondi Piatti")
    secondi.aggiungi(tagliata)
    secondi.aggiungi(branzino)

    # --- Bevande con sotto-sezioni ---
    acqua = Piatto("Acqua naturale/frizzante", 2.50)
    cola = Piatto("Cola", 3.50)
    succo = Piatto("Succo di frutta", 3.00)

    analcoliche = SezioneMenu("Analcoliche")
    analcoliche.aggiungi(acqua)
    analcoliche.aggiungi(cola)
    analcoliche.aggiungi(succo)

    birra = Piatto("Birra artigianale 0.4L", 5.50)
    vino_rosso = Piatto("Vino rosso della casa (calice)", 4.50)
    vino_bianco = Piatto("Vino bianco della casa (calice)", 4.50)

    alcoliche = SezioneMenu("Alcoliche")
    alcoliche.aggiungi(birra)
    alcoliche.aggiungi(vino_rosso)
    alcoliche.aggiungi(vino_bianco)

    bevande = SezioneMenu("Bevande")
    bevande.aggiungi(analcoliche)       # sotto-sezione dentro sezione
    bevande.aggiungi(alcoliche)         # sotto-sezione dentro sezione

    # --- Menu completo (radice) ---
    menu = SezioneMenu("Menu Ristorante 'Da Luca'")
    menu.aggiungi(antipasti)
    menu.aggiungi(primi)
    menu.aggiungi(secondi)
    menu.aggiungi(bevande)

    # ---- 1. Mostra l'intero menu ----
    print("=" * 50)
    print("  MENU COMPLETO")
    print("=" * 50)
    menu.mostra()

    # ---- 2. Statistiche (uniformi su foglie e composite) ----
    print(f"\nPiatti totali nel menu:    {menu.conta_piatti()}")
    print(f"Prezzo medio (tutto):      €{menu.get_prezzo_medio():.2f}")
    print(f"Prezzo medio (antipasti):  €{antipasti.get_prezzo_medio():.2f}")
    print(f"Piatti in 'Bevande':       {bevande.conta_piatti()}")
    print(f"Piatti in 'Analcoliche':   {analcoliche.conta_piatti()}")

    # Una foglia funziona esattamente come un composite:
    print(f"\nPrezzo medio 'Carbonara': €{carbonara.get_prezzo_medio():.2f}")
    print(f"Piatti in 'Carbonara':     {carbonara.conta_piatti()}")

    # ---- 3. Rimozione di un piatto ----
    print("\n--- Rimuovo 'Amatriciana' dai Primi ---")
    primi.rimuovi(amatriciana)
    primi.mostra()
    print(f"Nuovo prezzo medio (primi): €{primi.get_prezzo_medio():.2f}")
