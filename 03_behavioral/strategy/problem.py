# ==========================================
# THE PROBLEM THAT STRATEGY SOLVES
# ==========================================
# We have a Context class that must perform an operation,
# but that operation can be done in different ways
# (algorithm A, B, C…).
#
# Without the Strategy pattern, the Context contains ALL the
# logic for all algorithms, selected with if/elif.
# Adding a new algorithm → modifying the Context.


# ==========================================
# THE CONTEXT — an overloaded "Swiss army knife"
# ==========================================
# Knows ALL the algorithms. Each new algorithm requires
# modifying this class.

class Context:
    """Context that executes the operation based on the requested type."""

    def __init__(self, data: list[int]):
        self.data = data

    def execute(self, algorithm_type: str) -> None:
        """
        The client chooses the algorithm by passing a string.
        The Context must know every possible algorithm
        and implement it internally — all in a single method.
        """

        # --- START OF THE DISASTER ---
        # Each algorithm is an if/elif branch. If we add
        # a new one, we must modify THIS method.

        if algorithm_type == "A":
            # Algorithm A: sums all elements
            result = sum(self.data)
            print(f"Algorithm A (sum): {result}")

        elif algorithm_type == "B":
            # Algorithm B: finds the maximum
            result = max(self.data)
            print(f"Algorithm B (maximum): {result}")

        elif algorithm_type == "C":
            # Algorithm C: counts even elements
            result = sum(1 for x in self.data if x % 2 == 0)
            print(f"Algorithm C (count even): {result}")

        else:
            raise ValueError(f"Algorithm '{algorithm_type}' unknown!")

        # --- END OF THE DISASTER ---
        # If tomorrow we need an algorithm D (e.g., average, product, filter),
        # we must add another elif HERE and hope we don't
        # break any of the existing algorithms.


# ==========================================
# USAGE
# ==========================================
# The client must know the strings "A", "B", "C" and the
# Context must implement them all. Both are fragile.

if __name__ == "__main__":

    context = Context([3, 7, 2, 8, 4, 1, 6])

    print("=" * 45)
    print("  WITHOUT STRATEGY — if/elif in Context")
    print("=" * 45)

    context.execute("A")    # sum
    context.execute("B")    # maximum
    context.execute("C")    # count even

    # If we try an unforeseen algorithm → error
    try:
        context.execute("D")
    except ValueError as e:
        print(f"\nError: {e}")

    # PROBLEMS:
    # 1. The Context is a single monolithic block with all algorithms.
    # 2. Adding an algorithm D requires modifying execute() → violates OCP.
    # 3. Impossible to test an algorithm in isolation.
    # 4. The client uses magic strings ("A", "B") → fragile and without type-safety.
