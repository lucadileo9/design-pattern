# Behavioral Patterns

Behavioral patterns deal with **communication and the distribution of responsibilities between objects**: they define how objects interact with each other, how they exchange information, and how tasks are assigned, making the system more flexible and decoupled.

---

## 1. Observer

**Intent**: define a one-to-many dependency between objects, so that when one object changes state, all its dependents are notified and updated automatically.

**Typical usage**: event-driven systems, automatic UI updates on data changes, push notifications — whenever a change in one object must propagate to others without the object knowing its dependents.

Reference: [Full explanation](./observer/README.md)

---

## 2. Iterator

**Intent**: provide a standard way to sequentially access the elements of a collection without exposing its internal structure.

**Typical usage**: traversal of complex data structures (trees, graphs, lists of lists) where you want to hide the iteration logic from the client, while also supporting different traversal modes (e.g., pre-order, post-order).

Reference: [Full explanation](./iterator/README.md)

---

## 3. Strategy

**Intent**: define a family of interchangeable algorithms, encapsulate each one in a dedicated class, and make them swappable at runtime, without modifying the context that uses them.

**Typical usage**: runtime selection of the most suitable algorithm (sorting, payment, compression, routing) — when you want to add new variants without touching existing code (Open/Closed Principle).

Reference: [Full explanation](./strategy/README.md)

---

## 4. Template Method

**Intent**: define the skeleton of an algorithm in an abstract class, delegating to subclasses the implementation of only the variable steps, without altering the overall structure.

**Typical usage**: pipelines with a fixed flow but interchangeable steps (data import, report generation, ETL processes) — when multiple variants share the same sequence of steps but differ in some of them.

Reference: [Full explanation](./template-method/README.md)

---

## 5. Command

**Intent**: encapsulate a request as an object, parameterizing clients with different operations and supporting undoable operations (undo/redo).

**Typical usage**: operation queues, undo/redo systems, macros, job schedulers — when you want to decouple the invoker of an operation from the one that executes it.

*To be completed...*

---

## 6. Chain of Responsibility

**Intent**: pass a request along a chain of handlers, where each one decides whether to handle it or pass it to the next one.

**Typical usage**: HTTP middleware, layered validation, hierarchical approval systems — when multiple objects can handle a request and the correct handler is not known in advance.

*To be completed...*

---

## Real cases where I used these patterns:
**Strategy**:
 - In a project to create a distributed computing system where I had different work splitting and work assignment algorithms. I created a SplittingStrategy interface and an AssignmentStrategy one, and then different concrete classes for each specific algorithm. This way the system was very flexible and I could easily add new algorithms without modifying existing code. However, I didn't use a proper Context class, but instead treated the JobManager class that contained the two strategies as a context class, delegating the execution of the strategies to it.