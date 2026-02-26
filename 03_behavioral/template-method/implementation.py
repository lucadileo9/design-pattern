# ==========================================
# TEMPLATE METHOD — SOLUZIONE
# ==========================================
# Definiamo una classe astratta (AlgoritmoBase) che contiene il
# "metodo template" — esegui() — il quale chiama i 4 step in ordine.
#
# Gli step COMUNI (1 e 4) sono implementati nella classe base.
# Gli step SPECIFICI (2 e 3) sono dichiarati astratti: ogni
# sotto-classe li implementa a modo suo.
#
# Risultato: zero duplicazione. Se cambia lo step 1, si modifica
# UN solo punto. Aggiungere AlgoritmoD → solo step 2 e 3 nuovi.

from abc import ABC, abstractmethod


# ==========================================
# CLASSE ASTRATTA — il "template"
# ==========================================
# Il metodo esegui() definisce lo SCHELETRO dell'algoritmo:
# l'ordine degli step è fisso e non sovrascrivibile.
# Le sotto-classi possono personalizzare solo gli step astratti.

class AlgoritmoBase(ABC):
    """
    Classe astratta che definisce il template method.
    
    - esegui()  → metodo template (NON sovrascrivere!)
    - step1()   → comune, implementato qui
    - step2()   → astratto, ogni sotto-classe lo implementa
    - step3()   → astratto, ogni sotto-classe lo implementa
    - step4()   → comune, implementato qui
    """

    def esegui(self, dati: list[int]) -> list[int]:
        """
        Template method: definisce la struttura dell'algoritmo.
        Chiama gli step in ordine — le sotto-classi NON toccano
        questo metodo, ma solo gli step astratti.
        """
        dati_lavoro = self._step1(dati)
        if dati_lavoro is None:
            return []
        dati_lavoro = self._step2(dati_lavoro)
        dati_lavoro = self._step3(dati_lavoro)
        self._step4(dati_lavoro)
        return dati_lavoro

    # --- Step COMUNI (implementati qui, una sola volta) ---

    def _step1(self, dati: list[int]) -> list[int] | None:
        """Validazione e caricamento — comune a tutti gli algoritmi."""
        nome = self.__class__.__name__
        print(f"[{nome}] Step 1 — Validazione e caricamento")
        if not dati:
            print("  ⚠️ Lista vuota, nulla da elaborare")
            return None
        dati_lavoro = dati.copy()
        print(f"  Dati ricevuti: {dati_lavoro}")
        return dati_lavoro

    def _step4(self, dati_lavoro: list[int]) -> None:
        """Output finale — comune a tutti gli algoritmi."""
        nome = self.__class__.__name__
        print(f"[{nome}] Step 4 — Risultato finale")
        print(f"  ✅ Pipeline completata → {dati_lavoro}")
        print(f"  📊 Elementi: {len(dati_lavoro)}, Somma: {sum(dati_lavoro)}")

    # --- Step ASTRATTI (implementati dalle sotto-classi) ---

    @abstractmethod
    def _step2(self, dati: list[int]) -> list[int]:
        """Elaborazione — specifica per ogni algoritmo."""
        ...

    @abstractmethod
    def _step3(self, dati: list[int]) -> list[int]:
        """Trasformazione — specifica per ogni algoritmo."""
        ...


# ==========================================
# CLASSI CONCRETE — solo gli step specifici
# ==========================================
# Ogni sotto-classe implementa SOLO step2 e step3.
# Step 1 e 4 li eredita gratis — zero duplicazione.

class AlgoritmoA(AlgoritmoBase):
    """Ordina i dati e raddoppia ogni valore."""

    def _step2(self, dati: list[int]) -> list[int]:
        print(f"[AlgoritmoA] Step 2 — Ordinamento crescente")
        risultato = sorted(dati)
        print(f"  Risultato: {risultato}")
        return risultato

    def _step3(self, dati: list[int]) -> list[int]:
        print(f"[AlgoritmoA] Step 3 — Raddoppio valori")
        risultato = [x * 2 for x in dati]
        print(f"  Risultato: {risultato}")
        return risultato


class AlgoritmoB(AlgoritmoBase):
    """Inverte l'ordine e somma coppie adiacenti."""

    def _step2(self, dati: list[int]) -> list[int]:
        print(f"[AlgoritmoB] Step 2 — Inversione ordine")
        risultato = list(reversed(dati))
        print(f"  Risultato: {risultato}")
        return risultato

    def _step3(self, dati: list[int]) -> list[int]:
        print(f"[AlgoritmoB] Step 3 — Somma coppie adiacenti")
        risultato = []
        for i in range(0, len(dati) - 1, 2):
            risultato.append(dati[i] + dati[i + 1])
        if len(dati) % 2 == 1:
            risultato.append(dati[-1])
        print(f"  Risultato: {risultato}")
        return risultato


class AlgoritmoC(AlgoritmoBase):
    """Filtra i pari e eleva al quadrato."""

    def _step2(self, dati: list[int]) -> list[int]:
        print(f"[AlgoritmoC] Step 2 — Filtra solo i pari")
        risultato = [x for x in dati if x % 2 == 0]
        print(f"  Risultato: {risultato}")
        return risultato

    def _step3(self, dati: list[int]) -> list[int]:
        print(f"[AlgoritmoC] Step 3 — Elevamento al quadrato")
        risultato = [x ** 2 for x in dati]
        print(f"  Risultato: {risultato}")
        return risultato


# ==========================================
# UTILIZZO
# ==========================================
# Il client usa TUTTI gli algoritmi attraverso la stessa
# interfaccia (AlgoritmoBase.esegui). Non sa nulla degli
# step interni — sa solo che la pipeline viene eseguita.

if __name__ == "__main__":

    print("=" * 50)
    print("  TEMPLATE METHOD — Soluzione (con pattern)")
    print("=" * 50)

    dati = [3, 7, 2, 8, 4, 1, 6]

    print("\n--- AlgoritmoA ---")
    a = AlgoritmoA()
    a.esegui(dati)

    print("\n--- AlgoritmoB ---")
    b = AlgoritmoB()
    b.esegui(dati)

    print("\n--- AlgoritmoC ---")
    c = AlgoritmoC()
    c.esegui(dati)

    # Vantaggi:
    # 1. Step 1 e 4 → definiti UNA sola volta nella classe base
    # 2. Ogni sotto-classe implementa SOLO ciò che la distingue
    # 3. Aggiungere AlgoritmoD → nuova classe con solo step2 e step3
    # 4. La struttura dell'algoritmo (l'ordine degli step) è garantita
    #    dal template method — le sotto-classi non possono alterarla
    # OVviamente nulla vieta di riscrivere anche metodi comuni nel caso in
    # cui l'algoritmo lo richieda. Ossia segnare il metodo come astratto ma 
    # dando un'implementazione di default che le sotto-classi possono sovrascrivere.
