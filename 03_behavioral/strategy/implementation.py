# ==========================================
# STRATEGY PATTERN — SOLUZIONE
# ==========================================
# Ogni algoritmo diventa una classe separata che implementa
# la stessa interfaccia (Strategia). Il Contesto mantiene un
# riferimento alla strategia corrente e le delega l'esecuzione.
#
# Aggiungere un algoritmo D → creare una nuova classe.
# Il Contesto e le strategie esistenti non vengono toccati.

from abc import ABC, abstractmethod


# ==========================================
# STRATEGY — interfaccia comune
# ==========================================
# Dichiara il metodo che tutte le strategie devono implementare.
# Il Contesto conosce solo questa interfaccia.

class Strategia(ABC):
    """Interfaccia comune per tutti gli algoritmi."""

    @abstractmethod
    def esegui(self, dati: list[int]) -> None:
        """Esegue l'algoritmo sui dati forniti dal Contesto."""
        ...


# ==========================================
# STRATEGIE CONCRETE — un algoritmo per classe
# ==========================================
# Ogni strategia è isolata nella propria classe.
# Non sa nulla delle altre strategie né del Contesto.

class StrategiaA(Strategia):
    """Algoritmo A: somma tutti gli elementi."""

    def esegui(self, dati: list[int]) -> None:
        risultato = sum(dati)
        print(f"Strategia A (somma): {risultato}")


class StrategiaB(Strategia):
    """Algoritmo B: trova il massimo."""

    def esegui(self, dati: list[int]) -> None:
        risultato = max(dati)
        print(f"Strategia B (massimo): {risultato}")


class StrategiaC(Strategia):
    """Algoritmo C: conta gli elementi pari."""

    def esegui(self, dati: list[int]) -> None:
        risultato = sum(1 for x in dati if x % 2 == 0)
        print(f"Strategia C (conta pari): {risultato}")


# ==========================================
# CONTESTO — delega alla strategia corrente
# ==========================================
# Il Contesto non conosce i dettagli degli algoritmi.
# Sa solo che la strategia ha un metodo esegui() — polimorfismo.

class Contesto:
    """Mantiene un riferimento a una Strategia e le delega il lavoro."""

    def __init__(self, dati: list[int], strategia: Strategia):
        self.dati = dati
        self._strategia = strategia

    def imposta_strategia(self, strategia: Strategia) -> None:
        """Cambia strategia a runtime — il Contesto non cambia."""
        self._strategia = strategia

    def esegui_operazione(self) -> None:
        """Delega l'esecuzione alla strategia corrente."""
        self._strategia.esegui(self.dati)


# ==========================================
# UTILIZZO
# ==========================================
# Il client sceglie la strategia (un oggetto, non una stringa).
# Il Contesto delega senza if/elif. Aggiungere StrategiaD
# non richiede di toccare nulla di esistente.

if __name__ == "__main__":

    dati = [3, 7, 2, 8, 4, 1, 6]

    print("=" * 45)
    print("  STRATEGY PATTERN — ogni algoritmo è una classe")
    print("=" * 45)

    # --- Il client crea il contesto con una strategia iniziale ---
    contesto = Contesto(dati, StrategiaA())
    contesto.esegui_operazione()                # usa Strategia A

    # --- Cambio strategia a runtime ---
    contesto.imposta_strategia(StrategiaB())
    contesto.esegui_operazione()                # usa Strategia B

    contesto.imposta_strategia(StrategiaC())
    contesto.esegui_operazione()                # usa Strategia C


    # VANTAGGI rispetto al problem.py:
    # 1. Ogni algoritmo è isolato nella propria classe → testabile singolarmente.
    # 2. Il Contesto è semplice: delega e basta, zero if/elif.
    # 3. Aggiungere StrategiaD non modifica nulla di esistente → OCP rispettato.
    # 4. Il client passa oggetti (type-safe), non stringhe magiche.

    # è importante notare che l'esecuzione e il risultato è lo stesso, quel che cambia
    # è la struttura del codice, che ora è più modulare, estensibile e manutenibile.