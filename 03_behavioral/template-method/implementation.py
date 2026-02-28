# ==========================================
# TEMPLATE METHOD — SOLUTION
# ==========================================
# We define an abstract class (BaseAlgorithm) that contains the
# "template method" — execute() — which calls the 4 steps in order.
#
# The COMMON steps (1 and 4) are implemented in the base class.
# The SPECIFIC steps (2 and 3) are declared abstract: each
# subclass implements them in its own way.
#
# Result: zero duplication. If step 1 changes, it's modified
# in ONE single place. Adding AlgorithmD → only new step 2 and 3.

from abc import ABC, abstractmethod


# ==========================================
# ABSTRACT CLASS — the "template"
# ==========================================
# The execute() method defines the SKELETON of the algorithm:
# the order of steps is fixed and non-overridable.
# Subclasses can only customize the abstract steps.

class BaseAlgorithm(ABC):
    """
    Abstract class that defines the template method.
    
    - execute()  → template method (do NOT override!)
    - step1()    → common, implemented here
    - step2()    → abstract, each subclass implements it
    - step3()    → abstract, each subclass implements it
    - step4()    → common, implemented here
    """

    def execute(self, data: list[int]) -> list[int]:
        """
        Template method: defines the structure of the algorithm.
        Calls the steps in order — subclasses do NOT touch
        this method, only the abstract steps.
        """
        working_data = self._step1(data)
        if working_data is None:
            return []
        working_data = self._step2(working_data)
        working_data = self._step3(working_data)
        self._step4(working_data)
        return working_data

    # --- COMMON steps (implemented here, only once) ---

    def _step1(self, data: list[int]) -> list[int] | None:
        """Validation and loading — common to all algorithms."""
        name = self.__class__.__name__
        print(f"[{name}] Step 1 — Validation and loading")
        if not data:
            print("  ⚠️ Empty list, nothing to process")
            return None
        working_data = data.copy()
        print(f"  Data received: {working_data}")
        return working_data

    def _step4(self, working_data: list[int]) -> None:
        """Final output — common to all algorithms."""
        name = self.__class__.__name__
        print(f"[{name}] Step 4 — Final result")
        print(f"  ✅ Pipeline completed → {working_data}")
        print(f"  📊 Elements: {len(working_data)}, Sum: {sum(working_data)}")

    # --- ABSTRACT steps (implemented by subclasses) ---

    @abstractmethod
    def _step2(self, data: list[int]) -> list[int]:
        """Processing — specific to each algorithm."""
        ...

    @abstractmethod
    def _step3(self, data: list[int]) -> list[int]:
        """Transformation — specific to each algorithm."""
        ...


# ==========================================
# CONCRETE CLASSES — only the specific steps
# ==========================================
# Each subclass implements ONLY step2 and step3.
# Step 1 and 4 are inherited for free — zero duplication.

class AlgorithmA(BaseAlgorithm):
    """Sorts data and doubles every value."""

    def _step2(self, data: list[int]) -> list[int]:
        print(f"[AlgorithmA] Step 2 — Ascending sort")
        result = sorted(data)
        print(f"  Result: {result}")
        return result

    def _step3(self, data: list[int]) -> list[int]:
        print(f"[AlgorithmA] Step 3 — Doubling values")
        result = [x * 2 for x in data]
        print(f"  Result: {result}")
        return result


class AlgorithmB(BaseAlgorithm):
    """Reverses order and sums adjacent pairs."""

    def _step2(self, data: list[int]) -> list[int]:
        print(f"[AlgorithmB] Step 2 — Reversing order")
        result = list(reversed(data))
        print(f"  Result: {result}")
        return result

    def _step3(self, data: list[int]) -> list[int]:
        print(f"[AlgorithmB] Step 3 — Summing adjacent pairs")
        result = []
        for i in range(0, len(data) - 1, 2):
            result.append(data[i] + data[i + 1])
        if len(data) % 2 == 1:
            result.append(data[-1])
        print(f"  Result: {result}")
        return result


class AlgorithmC(BaseAlgorithm):
    """Filters even numbers and squares them."""

    def _step2(self, data: list[int]) -> list[int]:
        print(f"[AlgorithmC] Step 2 — Filter only even numbers")
        result = [x for x in data if x % 2 == 0]
        print(f"  Result: {result}")
        return result

    def _step3(self, data: list[int]) -> list[int]:
        print(f"[AlgorithmC] Step 3 — Squaring")
        result = [x ** 2 for x in data]
        print(f"  Result: {result}")
        return result


# ==========================================
# USAGE
# ==========================================
# The client uses ALL algorithms through the same
# interface (BaseAlgorithm.execute). It knows nothing about
# the internal steps — it only knows the pipeline is executed.

if __name__ == "__main__":

    print("=" * 50)
    print("  TEMPLATE METHOD — Solution (with pattern)")
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

    # Advantages:
    # 1. Steps 1 and 4 → defined ONCE in the base class
    # 2. Each subclass implements ONLY what distinguishes it
    # 3. Adding AlgorithmD → new class with only step2 and step3
    # 4. La struttura dell'algoritmo (l'ordine degli step) è garantita
    #    dal template method — le sotto-classi non possono alterarla
    # OVviamente nulla vieta di riscrivere anche metodi comuni nel caso in
    # cui l'algoritmo lo richieda. Ossia segnare il metodo come astratto ma 
    # dando un'implementazione di default che le sotto-classi possono sovrascrivere.
