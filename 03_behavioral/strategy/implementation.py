# ==========================================
# STRATEGY PATTERN — SOLUTION
# ==========================================
# Each algorithm becomes a separate class that implements
# the same interface (Strategy). The Context maintains a
# reference to the current strategy and delegates execution to it.
#
# Adding an algorithm D → create a new class.
# The Context and the existing strategies are not touched.

from abc import ABC, abstractmethod


# ==========================================
# STRATEGY — common interface
# ==========================================
# Declares the method that all strategies must implement.
# The Context only knows this interface.

class Strategy(ABC):
    """Common interface for all algorithms."""

    @abstractmethod
    def execute(self, data: list[int]) -> None:
        """Executes the algorithm on the data provided by the Context."""
        ...


# ==========================================
# CONCRETE STRATEGIES — one algorithm per class
# ==========================================
# Each strategy is isolated in its own class.
# It knows nothing about the other strategies or the Context.

class StrategyA(Strategy):
    """Algorithm A: sums all elements."""

    def execute(self, data: list[int]) -> None:
        result = sum(data)
        print(f"Strategy A (sum): {result}")


class StrategyB(Strategy):
    """Algorithm B: finds the maximum."""

    def execute(self, data: list[int]) -> None:
        result = max(data)
        print(f"Strategy B (maximum): {result}")


class StrategyC(Strategy):
    """Algorithm C: counts even elements."""

    def execute(self, data: list[int]) -> None:
        result = sum(1 for x in data if x % 2 == 0)
        print(f"Strategy C (count even): {result}")


# ==========================================
# CONTEXT — delegates to the current strategy
# ==========================================
# The Context does not know the details of the algorithms.
# It only knows the strategy has an execute() method — polymorphism.

class Context:
    """Maintains a reference to a Strategy and delegates work to it."""

    def __init__(self, data: list[int], strategy: Strategy):
        self.data = data
        self._strategy = strategy

    def set_strategy(self, strategy: Strategy) -> None:
        """Changes the strategy at runtime — the Context does not change."""
        self._strategy = strategy

    def execute_operation(self) -> None:
        """Delegates execution to the current strategy."""
        self._strategy.execute(self.data)


# ==========================================
# USAGE
# ==========================================
# The client chooses the strategy (an object, not a string).
# The Context delegates without if/elif. Adding StrategyD
# does not require touching anything existing.

if __name__ == "__main__":

    data = [3, 7, 2, 8, 4, 1, 6]

    print("=" * 45)
    print("  STRATEGY PATTERN — each algorithm is a class")
    print("=" * 45)

    # --- The client creates the context with an initial strategy ---
    context = Context(data, StrategyA())
    context.execute_operation()                # uses Strategy A

    # --- Changing strategy at runtime ---
    context.set_strategy(StrategyB())
    context.execute_operation()                # uses Strategy B

    context.set_strategy(StrategyC())
    context.execute_operation()                # uses Strategy C


    # ADVANTAGES over problem.py:
    # 1. Each algorithm is isolated in its own class → individually testable.
    # 2. The Context is simple: it delegates and that's it, zero if/elif.
    # 3. Adding StrategyD does not modify anything existing → OCP respected.
    # 4. The client passes objects (type-safe), not magic strings.

    # It's important to note that the execution and result are the same; what changes
    # is the code structure, which is now more modular, extensible, and maintainable.