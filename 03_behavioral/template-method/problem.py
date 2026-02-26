# ==========================================
# IL PROBLEMA CHE IL TEMPLATE METHOD RISOLVE
# ==========================================
# Abbiamo tre algoritmi (A, B, C) che eseguono una pipeline
# di 4 step su una lista di numeri. Gli step 1 e 4 sono
# IDENTICI in tutti gli algoritmi, mentre gli step 2 e 3
# differiscono.
#
# Senza il pattern, ogni algoritmo reimplementa TUTTI gli
# step — inclusi quelli comuni. Il risultato: duplicazione
# massiccia. Se domani cambia lo step 1, dobbiamo modificare
# TUTTE le classi.

from typing import Any


# ==========================================
# LE CLASSI — ogni algoritmo è a sé stante
# ==========================================
# Nessuna classe base, nessuna condivisione di codice.
# step1() e step4() sono copia-incollati identici ovunque.

class AlgoritmoA:
    """Ordina i dati e raddoppia ogni valore."""

    def esegui(self, dati: list[int]) -> list[int]:

        # --- step 1: validazione e caricamento (COMUNE) ---
        print(f"[AlgoritmoA] Step 1 — Validazione e caricamento")
        if not dati:
            print("  ⚠️ Lista vuota, nulla da elaborare")
            return []
        dati_lavoro = dati.copy()
        print(f"  Dati ricevuti: {dati_lavoro}")

        # --- step 2: elaborazione (SPECIFICA A) ---
        print(f"[AlgoritmoA] Step 2 — Ordinamento crescente")
        dati_lavoro.sort()
        print(f"  Risultato: {dati_lavoro}")

        # --- step 3: trasformazione (SPECIFICA A) ---
        print(f"[AlgoritmoA] Step 3 — Raddoppio valori")
        dati_lavoro = [x * 2 for x in dati_lavoro]
        print(f"  Risultato: {dati_lavoro}")

        # --- step 4: output finale (COMUNE) ---
        print(f"[AlgoritmoA] Step 4 — Risultato finale")
        print(f"  ✅ Pipeline completata → {dati_lavoro}")
        print(f"  📊 Elementi: {len(dati_lavoro)}, Somma: {sum(dati_lavoro)}")
        return dati_lavoro


class AlgoritmoB:
    """Inverte l'ordine e somma coppie adiacenti."""

    def esegui(self, dati: list[int]) -> list[int]:

        # --- step 1: validazione e caricamento (COMUNE — COPIA!) ---
        # ↑↑↑ Identico ad AlgoritmoA — codice duplicato!
        print(f"[AlgoritmoB] Step 1 — Validazione e caricamento")
        if not dati:
            print("  ⚠️ Lista vuota, nulla da elaborare")
            return []
        dati_lavoro = dati.copy()
        print(f"  Dati ricevuti: {dati_lavoro}")

        # --- step 2: elaborazione (SPECIFICA B) ---
        print(f"[AlgoritmoB] Step 2 — Inversione ordine")
        dati_lavoro.reverse()
        print(f"  Risultato: {dati_lavoro}")

        # --- step 3: trasformazione (SPECIFICA B) ---
        print(f"[AlgoritmoB] Step 3 — Somma coppie adiacenti")
        risultato = []
        for i in range(0, len(dati_lavoro) - 1, 2):
            risultato.append(dati_lavoro[i] + dati_lavoro[i + 1])
        if len(dati_lavoro) % 2 == 1:
            risultato.append(dati_lavoro[-1])   # elemento dispari rimane
        dati_lavoro = risultato
        print(f"  Risultato: {dati_lavoro}")

        # --- step 4: output finale (COMUNE — COPIA!) ---
        # ↑↑↑ Identico ad AlgoritmoA — codice duplicato!
        print(f"[AlgoritmoB] Step 4 — Risultato finale")
        print(f"  ✅ Pipeline completata → {dati_lavoro}")
        print(f"  📊 Elementi: {len(dati_lavoro)}, Somma: {sum(dati_lavoro)}")
        return dati_lavoro


class AlgoritmoC:
    """Filtra i pari e eleva al quadrato."""

    def esegui(self, dati: list[int]) -> list[int]:

        # --- step 1: validazione e caricamento (COMUNE — COPIA!) ---
        # ↑↑↑ Identico ad A e B — terza copia dello stesso codice!
        print(f"[AlgoritmoC] Step 1 — Validazione e caricamento")
        if not dati:
            print("  ⚠️ Lista vuota, nulla da elaborare")
            return []
        dati_lavoro = dati.copy()
        print(f"  Dati ricevuti: {dati_lavoro}")

        # --- step 2: elaborazione (SPECIFICA C) ---
        print(f"[AlgoritmoC] Step 2 — Filtra solo i pari")
        dati_lavoro = [x for x in dati_lavoro if x % 2 == 0]
        print(f"  Risultato: {dati_lavoro}")

        # --- step 3: trasformazione (SPECIFICA C) ---
        print(f"[AlgoritmoC] Step 3 — Elevamento al quadrato")
        dati_lavoro = [x ** 2 for x in dati_lavoro]
        print(f"  Risultato: {dati_lavoro}")

        # --- step 4: output finale (COMUNE — COPIA!) ---
        # ↑↑↑ Identico ad A e B — terza copia dello stesso codice!
        print(f"[AlgoritmoC] Step 4 — Risultato finale")
        print(f"  ✅ Pipeline completata → {dati_lavoro}")
        print(f"  📊 Elementi: {len(dati_lavoro)}, Somma: {sum(dati_lavoro)}")
        return dati_lavoro


# ==========================================
# IL PROBLEMA: DUPLICAZIONE OVUNQUE
# ==========================================
# Step 1 (validazione) → copiato 3 volte
# Step 4 (output)      → copiato 3 volte
#
# Se domani cambiamo la validazione (es. aggiungiamo un log),
# dobbiamo modificare TUTTE E TRE le classi. E se aggiungiamo
# AlgoritmoD, dobbiamo copiare di nuovo step 1 e step 4.
#
# Inoltre il metodo esegui() contiene sia logica comune che
# logica specifica mescolata insieme — difficile da leggere.


# ==========================================
# UTILIZZO
# ==========================================

if __name__ == "__main__":

    print("=" * 50)
    print("  TEMPLATE METHOD — Il problema (senza pattern)")
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

    # Problema evidente: se vogliamo cambiare il messaggio dello
    # step 1 o il formato dello step 4, dobbiamo toccare TUTTE le classi.
    # E ogni nuova classe richiede di copiare gli stessi blocchi.
