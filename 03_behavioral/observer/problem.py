# ==========================================
# IL PROBLEMA CHE L'OBSERVER RISOLVE
# ==========================================
# Un negoziante (Negozio) riceve periodicamente nuovi prodotti.
# Alcuni clienti sono interessati a prodotti specifici e vogliono
# sapere quando arrivano.
#
# Senza il pattern Observer, ogni cliente deve fare POLLING:
# chiedere ripetutamente al negozio "È arrivato il mio prodotto?".
# Il negozio viene bombardato di richieste, e i clienti sprecano
# tempo a controllare continuamente.


import time


# ==========================================
# IL NEGOZIO — non sa nulla dei clienti
# ==========================================
# Il negozio gestisce i propri prodotti. Non ha nessun meccanismo
# per avvisare i clienti: sono LORO a dover controllare.

class Negozio:
    """Il negozio: gestisce il magazzino, ma non avvisa nessuno."""

    def __init__(self, nome: str):
        self.nome = nome
        self.prodotti_disponibili: list[str] = []

    def aggiungi_prodotto(self, prodotto: str) -> None:
        """Aggiunge un prodotto al magazzino — nessuna notifica."""
        self.prodotti_disponibili.append(prodotto)
        print(f"[{self.nome}] Nuovo prodotto in magazzino: '{prodotto}'")

    def ha_prodotto(self, prodotto: str) -> bool:
        """Il cliente deve chiamare questo metodo per controllare."""
        return prodotto in self.prodotti_disponibili


# ==========================================
# IL CLIENTE — deve fare polling manualmente
# ==========================================
# Il cliente vuole un prodotto specifico. L'unico modo per
# sapere se è arrivato è chiedere ripetutamente al negozio.

class Cliente:
    """Un cliente che aspetta un prodotto specifico."""

    def __init__(self, nome: str, prodotto_desiderato: str):
        self.nome = nome
        self.prodotto_desiderato = prodotto_desiderato

    def controlla_disponibilita(self, negozio: Negozio) -> bool:
        """
        POLLING: il cliente chiede attivamente al negozio.
        Deve farlo ripetutamente, sperando che il prodotto sia arrivato.
        """
        disponibile = negozio.ha_prodotto(self.prodotto_desiderato)
        if disponibile:
            print(f"  [{self.nome}] Evvai! '{self.prodotto_desiderato}' è disponibile!")
        else:
            print(f"  [{self.nome}] '{self.prodotto_desiderato}' non c'è ancora...")
        return disponibile


# ==========================================
# SIMULAZIONE DEL POLLING
# ==========================================
# Ogni cliente controlla il negozio continuamente.
# Il negozio viene bombardato di richieste inutili.
# Se ci sono 100 clienti, il carico diventa insostenibile.

if __name__ == "__main__":

    negozio = Negozio("Elettronica Express")

    mario = Cliente("Mario", "PlayStation 6")
    giulia = Cliente("Giulia", "iPhone 20")
    luca = Cliente("Luca", "PlayStation 6")

    print("=" * 50)
    print("  POLLING — i clienti controllano ripetutamente")
    print("=" * 50)

    # --- Turno 1: nessun prodotto ancora ---
    print("\n--- Turno 1: i clienti controllano ---")
    mario.controlla_disponibilita(negozio)      # niente
    giulia.controlla_disponibilita(negozio)     # niente
    luca.controlla_disponibilita(negozio)       # niente

    # --- Il negozio riceve un prodotto ---
    print("\n--- Il negozio riceve merce ---")
    negozio.aggiungi_prodotto("PlayStation 6")

    # --- Turno 2: i clienti controllano DI NUOVO ---
    print("\n--- Turno 2: i clienti controllano ---")
    mario.controlla_disponibilita(negozio)      # trovato!
    giulia.controlla_disponibilita(negozio)     # niente (vuole iPhone)
    luca.controlla_disponibilita(negozio)       # trovato!

    # --- Il negozio riceve un altro prodotto ---
    print("\n--- Il negozio riceve altra merce ---")
    negozio.aggiungi_prodotto("iPhone 20")

    # --- Turno 3: TUTTI devono controllare ancora ---
    print("\n--- Turno 3: i clienti controllano ---")
    mario.controlla_disponibilita(negozio)      # già trovato prima, spreco
    giulia.controlla_disponibilita(negozio)     # finalmente!
    luca.controlla_disponibilita(negozio)       # già trovato prima, spreco

    # PROBLEMI:
    # 1. Ogni cliente deve controllare OGNI volta, anche quando non
    #    serve 
    # 2. Il negozio riceve N richieste per turno (con 100 clienti = 100
    #    richieste ripetute ad ogni turno).
    # 3. Se il negozio aggiunge un prodotto tra un turno e l'altro,
    #    i clienti se ne accorgono solo al turno successivo (ritardo).
    # 4. Il client (il main) deve orchestrare manualmente il polling.
    # Da notare inoltre che il negozio viene costantemente interrogato,
    # quindi viene costantemente disturbato, non potendo ad esempio
    # concentrarsi su altre attività
