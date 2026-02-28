"""
Iterator Pattern - REAL EXAMPLE: Corporate Org Chart
=========================================================
Scenario: a large company has a hierarchical org chart (a tree).
Depending on the context, we want to traverse it in different ways:

  - Pre-order (DFS): visit the manager *before* their team.
    → Useful for: top-down reports, hierarchical printouts.

  - BFS (breadth-first): visit level by level.
    → Useful for: visual org charts, analysis by hierarchical tier.

  - Post-order: visit the team *before* the manager.
    → Useful for: bottom-up calculations (e.g., cumulative headcount per team).

EACH traversal algorithm is encapsulated in its own Iterator.
The client always uses the same interface: has_next() + next().
Changing strategy = changing only the parameter passed to create_iterator().
And of course the client knows nothing about stacks, queues, or recursion: it only interacts with the iterator.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from collections import deque


# ── Interfaces ───────────────────────────────────────────────────────────────

class Iterator(ABC):
    """Common interface for all iterators."""

    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self) -> "Employee":
        pass


class Aggregate(ABC):
    """Common interface for iterable structures."""

    @abstractmethod
    def create_iterator(self, strategy: str = "preorder") -> Iterator:
        pass


# ── Data Structure ───────────────────────────────────────────────────────────

class Employee:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.level = 0               # depth in the tree (0 = CEO)
        self.reports: list[Employee] = []

    def add_report(self, employee: "Employee") -> None:
        employee.level = self.level + 1
        self.reports.append(employee)


class Organization(Aggregate):
    def __init__(self, name: str, ceo: Employee):
        self.name = name
        self.ceo = ceo

    def create_iterator(self, strategy: str = "preorder") -> Iterator:
        if strategy == "preorder":
            return PreOrderIterator(self.ceo)
        if strategy == "bfs":
            return BFSIterator(self.ceo)
        if strategy == "postorder":
            return PostOrderIterator(self.ceo)
        raise ValueError(f"Unknown strategy: '{strategy}'")


# ── Concrete Iterators ───────────────────────────────────────────────────────

class PreOrderIterator(Iterator):
    """
    DFS pre-order: visits the node before its children (explicit stack).
    Useful for producing a top-down hierarchical output from the org chart.
    """

    def __init__(self, root: Employee):
        self._stack: list[Employee] = [root]

    def has_next(self) -> bool:
        return len(self._stack) > 0

    def next(self) -> Employee:
        node = self._stack.pop()
        # Children in reverse order → pop() returns them in original order
        for child in reversed(node.reports):
            self._stack.append(child)
        return node


class BFSIterator(Iterator):
    """
    Breadth-first search: visits level by level (FIFO queue).
    Useful for analyzing the structure by hierarchical tier.
    """

    def __init__(self, root: Employee):
        self._queue: deque[Employee] = deque([root])

    def has_next(self) -> bool:
        return len(self._queue) > 0

    def next(self) -> Employee:
        node = self._queue.popleft()
        for child in node.reports:
            self._queue.append(child)
        return node


class PostOrderIterator(Iterator):
    """
    DFS post-order: visits children before the parent node.
    Builds the complete sequence in advance via recursive DFS,
    then exposes it one at a time via has_next() / next().
    Useful for bottom-up calculations (aggregates, costs, headcount).
    """

    def __init__(self, root: Employee):
        self._nodes: list[Employee] = []
        self._build(root)
        self._index = 0

    def _build(self, node: Employee) -> None:
        for child in node.reports:
            self._build(child)
        self._nodes.append(node)    # node added AFTER children

    def has_next(self) -> bool:
        return self._index < len(self._nodes)

    def next(self) -> Employee:
        node = self._nodes[self._index]
        self._index += 1
        return node


# ── Client Code ──────────────────────────────────────────────────────────────

INDENT = "  "


def main():
    # Building the org chart (top-down, so levels are calculated correctly)
    ceo = Employee("Laura Rossi", "CEO")

    cto = Employee("Marco Bianchi", "CTO")
    cfo = Employee("Anna Conti", "CFO")
    coo = Employee("Luca Ferrari", "COO")
    ceo.add_report(cto)
    ceo.add_report(cfo)
    ceo.add_report(coo)

    dev_lead   = Employee("Sara Esposito", "Dev Lead")
    infra_lead = Employee("Giorgio Ricci", "Infra Lead")
    cto.add_report(dev_lead)
    cto.add_report(infra_lead)

    finance_mgr = Employee("Marta Lombardi", "Finance Manager")
    cfo.add_report(finance_mgr)

    ops_mgr = Employee("Paolo Gallo", "Ops Manager")
    coo.add_report(ops_mgr)

    dev_lead.add_report(Employee("Chiara Marini",   "Senior Developer"))
    dev_lead.add_report(Employee("Filippo Romano",  "Junior Developer"))
    dev_lead.add_report(Employee("Elena Greco",     "Senior Developer"))
    infra_lead.add_report(Employee("Andrea Russo",  "DevOps Engineer"))
    finance_mgr.add_report(Employee("Carla Bruno",  "Financial Analyst"))
    ops_mgr.add_report(Employee("Roberto Moretti",  "Operations Analyst"))
    ops_mgr.add_report(Employee("Giulia Colombo",   "Operations Analyst"))

    org = Organization("TechCorp Italia", ceo)

    # ─────────────────────────────────────────────────────────────────────────
    # View 1 — Pre-order: top-down hierarchy
    # The client uses has_next() + next(); it knows nothing about stacks or DFS.
    # ─────────────────────────────────────────────────────────────────────────
    print(f"{'─' * 52}")
    print(f"  {org.name} — Hierarchical view  [pre-order]")
    print(f"{'─' * 52}")

    iterator = org.create_iterator("preorder")
    while iterator.has_next():
        emp = iterator.next()
        indent = INDENT * emp.level
        marker = "▸ " if emp.reports else "  "
        print(f"{indent}{marker}{emp.name}  [{emp.role}]")

    # ─────────────────────────────────────────────────────────────────────────
    # View 2 — BFS: by hierarchical level
    # Same interface, completely different internal algorithm.
    # ─────────────────────────────────────────────────────────────────────────
    level_labels = {0: "Executive", 1: "C-Suite", 2: "Management", 3: "Team"}
    current_level = -1

    print(f"\n{'─' * 52}")
    print(f"  {org.name} — By hierarchical level  [BFS]")
    print(f"{'─' * 52}")

    iterator = org.create_iterator("bfs")
    while iterator.has_next():
        emp = iterator.next()
        if emp.level != current_level:
            current_level = emp.level
            label = level_labels.get(current_level, f"Level {current_level}")
            print(f"\n  ┌─ {label} ─┐")
        print(f"  │  - {emp.name}  ({emp.role})")

    # ─────────────────────────────────────────────────────────────────────────
    # View 3 — Post-order: leaves first, root last
    # Useful for bottom-up calculations: when we process a manager,
    # all their direct reports have already been processed.
    # ─────────────────────────────────────────────────────────────────────────
    print(f"\n{'─' * 52}")
    print(f"  {org.name} — Processing bottom-up  [post-order]")
    print(f"{'─' * 52}\n")

    headcount: dict[str, int] = {}     # cumulative headcount for each node

    iterator = org.create_iterator("postorder")
    while iterator.has_next():
        emp = iterator.next()
        # When we get here, children have already been inserted in headcount
        team_size = 1 + sum(headcount[r.name] for r in emp.reports)
        headcount[emp.name] = team_size

        indent = INDENT * emp.level
        if emp.reports:
            print(f"{indent}▸ {emp.name}  [{emp.role}]  → total team: {team_size} people")
        else:
            print(f"{indent}  {emp.name}  [{emp.role}]")

    # The client never touched stacks, queues, or recursion.
    # It used only has_next() + next() with three different strategies,
    # each encapsulated in its own Iterator.


if __name__ == "__main__":
    main()
