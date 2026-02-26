# ==========================================
# IL PROBLEMA CHE LO STRATEGY RISOLVE
# ==========================================
# Abbiamo una classe Contesto che deve eseguire un'operazione,
# ma quell'operazione può essere svolta in modi diversi
# (algoritmo A, B, C…).
#
# Senza il pattern Strategy, il Contesto contiene TUTTA la
# logica di tutti gli algoritmi, selezionati con if/elif.
# Aggiungere un nuovo algoritmo → modificare il Contesto.


# ==========================================
# IL CONTESTO — un "coltellino svizzero" sovraccarico
# ==========================================
# Conosce TUTTI gli algoritmi. Ogni nuovo algoritmo richiede
# di modificare questa classe.

class Contesto:
    """Contesto che esegue l'operazione in base al tipo richiesto."""

    def __init__(self, dati: list[int]):
        self.dati = dati

    def esegui(self, tipo_algoritmo: str) -> None:
        """
        Il client sceglie l'algoritmo passando una stringa.
        Il Contesto deve conoscere ogni possibile algoritmo
        e implementarlo internamente — tutto in un unico metodo.
        """

        # --- INIZIO DEL DISASTRO ---
        # Ogni algoritmo è un ramo if/elif. Se ne aggiungiamo
        # uno nuovo, dobbiamo modificare QUESTO metodo.

        if tipo_algoritmo == "A":
            # Algoritmo A: somma tutti gli elementi
            risultato = sum(self.dati)
            print(f"Algoritmo A (somma): {risultato}")

        elif tipo_algoritmo == "B":
            # Algoritmo B: trova il massimo
            risultato = max(self.dati)
            print(f"Algoritmo B (massimo): {risultato}")

        elif tipo_algoritmo == "C":
            # Algoritmo C: conta gli elementi pari
            risultato = sum(1 for x in self.dati if x % 2 == 0)
            print(f"Algoritmo C (conta pari): {risultato}")

        else:
            raise ValueError(f"Algoritmo '{tipo_algoritmo}' sconosciuto!")

        # --- FINE DEL DISASTRO ---
        # Se domani serve un algoritmo D (es. media, prodotto, filtro),
        # bisogna aggiungere un altro elif QUI e sperare di non
        # rompere nulla degli algoritmi esistenti.


# ==========================================
# UTILIZZO
# ==========================================
# Il client deve conoscere le stringhe "A", "B", "C" e il
# Contesto deve implementarli tutti. Entrambi sono fragili.

if __name__ == "__main__":

    contesto = Contesto([3, 7, 2, 8, 4, 1, 6])

    print("=" * 45)
    print("  SENZA STRATEGY — if/elif nel Contesto")
    print("=" * 45)

    contesto.esegui("A")    # somma
    contesto.esegui("B")    # massimo
    contesto.esegui("C")    # conta pari

    # Se proviamo un algoritmo non previsto → errore
    try:
        contesto.esegui("D")
    except ValueError as e:
        print(f"\nErrore: {e}")

    # PROBLEMI:
    # 1. Il Contesto è un unico blocco monolitico con tutti gli algoritmi.
    # 2. Aggiungere un algoritmo D richiede di modificare esegui() → viola OCP.
    # 3. Impossibile testare un algoritmo in isolamento.
    # 4. Il client usa stringhe magiche ("A", "B") → fragile e senza type-safety.
