"""
Iterator Pattern - ESEMPIO REALE: Organigramma aziendale
=========================================================
Scenario: una grande azienda ha un organigramma gerarchico (un albero).
A seconda del contesto, vogliamo attraversarlo in modi diversi:

  - Pre-order (DFS): si visita il manager *prima* del suo team.
    → Utile per: report top-down, stampe gerarchiche.

  - BFS (breadth-first): si visita livello per livello.
    → Utile per: organigrammi visivi, analisi per fascia gerarchica.

  - Post-order: si visita il team *prima* del manager.
    → Utile per: calcoli bottom-up (es. headcount cumulativo per team).

OGNI algoritmo di attraversamento è incapsulato nel proprio Iterator.
Il client usa sempre la stessa interfaccia: has_next() + next().
Cambiare strategia = cambiare solo il parametro passato a create_iterator().
E ovviamente il client non sa nulla di stack, queue, o ricorsione: interagisce solo con l'iteratore.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from collections import deque


# ── Interfacce ───────────────────────────────────────────────────────────────

class Iterator(ABC):
    """Interfaccia comune per tutti gli iteratori."""

    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self) -> "Employee":
        pass


class Aggregate(ABC):
    """Interfaccia comune per le strutture iterabili."""

    @abstractmethod
    def create_iterator(self, strategy: str = "preorder") -> Iterator:
        pass


# ── Struttura dati ───────────────────────────────────────────────────────────

class Employee:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.level = 0               # profondità nell'albero (0 = CEO)
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
        raise ValueError(f"Strategia sconosciuta: '{strategy}'")


# ── Iteratori concreti ───────────────────────────────────────────────────────

class PreOrderIterator(Iterator):
    """
    DFS pre-order: visita il nodo prima dei suoi figli (stack esplicito).
    Utile per produrre un output gerarchico top-down dall'organigramma.
    """

    def __init__(self, root: Employee):
        self._stack: list[Employee] = [root]

    def has_next(self) -> bool:
        return len(self._stack) > 0

    def next(self) -> Employee:
        node = self._stack.pop()
        # Figli in ordine inverso → pop() li restituisce nell'ordine originale
        for child in reversed(node.reports):
            self._stack.append(child)
        return node


class BFSIterator(Iterator):
    """
    Breadth-first search: visita livello per livello (coda FIFO).
    Utile per analizzare la struttura per fascia gerarchica.
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
    DFS post-order: visita i figli prima del nodo padre.
    Costruisce la sequenza completa in anticipo tramite DFS ricorsivo,
    poi la espone uno alla volta tramite has_next() / next().
    Utile per calcoli bottom-up (aggregati, costi, headcount).
    """

    def __init__(self, root: Employee):
        self._nodes: list[Employee] = []
        self._build(root)
        self._index = 0

    def _build(self, node: Employee) -> None:
        for child in node.reports:
            self._build(child)
        self._nodes.append(node)    # nodo aggiunto DOPO i figli

    def has_next(self) -> bool:
        return self._index < len(self._nodes)

    def next(self) -> Employee:
        node = self._nodes[self._index]
        self._index += 1
        return node


# ── Codice client ────────────────────────────────────────────────────────────

INDENT = "  "


def main():
    # Costruzione dell'organigramma (top-down, così i livelli sono calcolati correttamente)
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
    # Vista 1 — Pre-order: gerarchia top-down
    # Il client usa has_next() + next(); non sa nulla di stack o DFS.
    # ─────────────────────────────────────────────────────────────────────────
    print(f"{'─' * 52}")
    print(f"  {org.name} — Vista gerarchica  [pre-order]")
    print(f"{'─' * 52}")

    iterator = org.create_iterator("preorder")
    while iterator.has_next():
        emp = iterator.next()
        indent = INDENT * emp.level
        marker = "▸ " if emp.reports else "  "
        print(f"{indent}{marker}{emp.name}  [{emp.role}]")

    # ─────────────────────────────────────────────────────────────────────────
    # Vista 2 — BFS: per livello gerarchico
    # Stessa interfaccia, algoritmo completamente diverso interno.
    # ─────────────────────────────────────────────────────────────────────────
    level_labels = {0: "Executive", 1: "C-Suite", 2: "Management", 3: "Team"}
    current_level = -1

    print(f"\n{'─' * 52}")
    print(f"  {org.name} — Per livello gerarchico  [BFS]")
    print(f"{'─' * 52}")

    iterator = org.create_iterator("bfs")
    while iterator.has_next():
        emp = iterator.next()
        if emp.level != current_level:
            current_level = emp.level
            label = level_labels.get(current_level, f"Livello {current_level}")
            print(f"\n  ┌─ {label} ─┐")
        print(f"  │  - {emp.name}  ({emp.role})")

    # ─────────────────────────────────────────────────────────────────────────
    # Vista 3 — Post-order: foglie prima, radice per ultima
    # Utile per calcoli bottom-up: quando processiamo un manager,
    # tutti i suoi riporti diretti sono già stati processati.
    # ─────────────────────────────────────────────────────────────────────────
    print(f"\n{'─' * 52}")
    print(f"  {org.name} — Processiamo bottom-up  [post-order]")
    print(f"{'─' * 52}\n")

    headcount: dict[str, int] = {}     # headcount cumulativo per ogni nodo

    iterator = org.create_iterator("postorder")
    while iterator.has_next():
        emp = iterator.next()
        # Quando arriviamo qui, i figli sono già stati inseriti in headcount
        team_size = 1 + sum(headcount[r.name] for r in emp.reports)
        headcount[emp.name] = team_size

        indent = INDENT * emp.level
        if emp.reports:
            print(f"{indent}▸ {emp.name}  [{emp.role}]  → team totale: {team_size} persone")
        else:
            print(f"{indent}  {emp.name}  [{emp.role}]")

    # Il client non ha mai toccato stack, queue, o ricorsione.
    # Ha usato solo has_next() + next() con tre strategie diverse,
    # ognuna incapsulata nel proprio Iterator.


if __name__ == "__main__":
    main()
