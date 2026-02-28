# ==========================================
# THE PROBLEM THAT TEMPLATE METHOD SOLVES
# ==========================================
# We have three algorithms (A, B, C) that execute a pipeline
# of 4 steps on a list of numbers. Steps 1 and 4 are
# IDENTICAL across all algorithms, while steps 2 and 3
# differ.
#
# Without the pattern, each algorithm reimplements ALL the
# steps — including the common ones. The result: massive
# duplication. If tomorrow step 1 changes, we must modify
# ALL the classes.

from typing import Any


# ==========================================
# THE CLASSES — each algorithm is standalone
# ==========================================
# No base class, no code sharing.
# step1() and step4() are copy-pasted identically everywhere.

class AlgorithmA:
    """Sorts data and doubles every value."""

    def execute(self, data: list[int]) -> list[int]:

        # --- step 1: validation and loading (COMMON) ---
        print(f"[AlgorithmA] Step 1 — Validation and loading")
        if not data:
            print("  ⚠️ Empty list, nothing to process")
            return []
        working_data = data.copy()
        print(f"  Data received: {working_data}")

        # --- step 2: processing (SPECIFIC A) ---
        print(f"[AlgorithmA] Step 2 — Ascending sort")
        working_data.sort()
        print(f"  Result: {working_data}")

        # --- step 3: transformation (SPECIFIC A) ---
        print(f"[AlgorithmA] Step 3 — Doubling values")
        working_data = [x * 2 for x in working_data]
        print(f"  Result: {working_data}")

        # --- step 4: final output (COMMON) ---
        print(f"[AlgorithmA] Step 4 — Final result")
        print(f"  ✅ Pipeline completed → {working_data}")
        print(f"  📊 Elements: {len(working_data)}, Sum: {sum(working_data)}")
        return working_data


class AlgorithmB:
    """Reverses order and sums adjacent pairs."""

    def execute(self, data: list[int]) -> list[int]:

        # --- step 1: validation and loading (COMMON — COPY!) ---
        # ↑↑↑ Identical to AlgorithmA — duplicated code!
        print(f"[AlgorithmB] Step 1 — Validation and loading")
        if not data:
            print("  ⚠️ Empty list, nothing to process")
            return []
        working_data = data.copy()
        print(f"  Data received: {working_data}")

        # --- step 2: processing (SPECIFIC B) ---
        print(f"[AlgorithmB] Step 2 — Reversing order")
        working_data.reverse()
        print(f"  Result: {working_data}")

        # --- step 3: transformation (SPECIFIC B) ---
        print(f"[AlgorithmB] Step 3 — Summing adjacent pairs")
        result = []
        for i in range(0, len(working_data) - 1, 2):
            result.append(working_data[i] + working_data[i + 1])
        if len(working_data) % 2 == 1:
            result.append(working_data[-1])   # odd element remains
        working_data = result
        print(f"  Result: {working_data}")

        # --- step 4: final output (COMMON — COPY!) ---
        # ↑↑↑ Identical to AlgorithmA — duplicated code!
        print(f"[AlgorithmB] Step 4 — Final result")
        print(f"  ✅ Pipeline completed → {working_data}")
        print(f"  📊 Elements: {len(working_data)}, Sum: {sum(working_data)}")
        return working_data


class AlgorithmC:
    """Filters even numbers and squares them."""

    def execute(self, data: list[int]) -> list[int]:

        # --- step 1: validation and loading (COMMON — COPY!) ---
        # ↑↑↑ Identical to A and B — third copy of the same code!
        print(f"[AlgorithmC] Step 1 — Validation and loading")
        if not data:
            print("  ⚠️ Empty list, nothing to process")
            return []
        working_data = data.copy()
        print(f"  Data received: {working_data}")

        # --- step 2: processing (SPECIFIC C) ---
        print(f"[AlgorithmC] Step 2 — Filter only even numbers")
        working_data = [x for x in working_data if x % 2 == 0]
        print(f"  Result: {working_data}")

        # --- step 3: transformation (SPECIFIC C) ---
        print(f"[AlgorithmC] Step 3 — Squaring")
        working_data = [x ** 2 for x in working_data]
        print(f"  Result: {working_data}")

        # --- step 4: final output (COMMON — COPY!) ---
        # ↑↑↑ Identical to A and B — third copy of the same code!
        print(f"[AlgorithmC] Step 4 — Final result")
        print(f"  ✅ Pipeline completed → {working_data}")
        print(f"  📊 Elements: {len(working_data)}, Sum: {sum(working_data)}")
        return working_data


# ==========================================
# THE PROBLEM: DUPLICATION EVERYWHERE
# ==========================================
# Step 1 (validation) → copied 3 times
# Step 4 (output)     → copied 3 times
#
# If tomorrow we change the validation (e.g., add a log),
# we must modify ALL THREE classes. And if we add
# AlgorithmD, we must copy step 1 and step 4 again.
#
# Moreover, the execute() method contains both common logic
# and specific logic mixed together — hard to read.


# ==========================================
# USAGE
# ==========================================

if __name__ == "__main__":

    print("=" * 50)
    print("  TEMPLATE METHOD — The problem (without pattern)")
    print("=" * 50)

    data = [3, 7, 2, 8, 4, 1, 6]

    print("\n--- AlgorithmA ---")
    a = AlgorithmA()
    a.execute(data)

    print("\n--- AlgorithmB ---")
    b = AlgorithmB()
    b.execute(data)

    print("\n--- AlgorithmC ---")
    c = AlgorithmC()
    c.execute(data)

    # Obvious problem: if we want to change the step 1 message
    # or the step 4 format, we have to touch ALL the classes.
    # And every new class requires copying the same blocks.
