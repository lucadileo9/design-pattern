# Pattern Comparisons

> When to use one pattern instead of another?

Design patterns often overlap in intent or structure. This guide highlights the key differences between patterns that are frequently confused, helping you pick the right one for each situation.

---

## Creational Patterns

### Factory Method vs Abstract Factory

| Aspect | Factory Method | Abstract Factory |
|---|---|---|
| **Scope** | Creates **one** product | Creates **families** of related products |
| **Mechanism** | Inheritance — subclass overrides a creation method | Composition — the client receives a factory object |
| **When to add a product** | Add a new subclass of the creator | Add a new method to the factory interface (all concrete factories must implement it) |
| **Typical use** | A framework defines the skeleton, the app customizes what gets created | A UI toolkit that must produce buttons, text fields, and menus that are visually consistent |

**Rule of thumb**: if you need a single object, start with Factory Method. If you need a coordinated set of objects, use Abstract Factory.

### Factory Method vs Singleton

| Aspect | Factory Method | Singleton |
|---|---|---|
| **Goal** | Decide *which* object to create at runtime | Guarantee *one and only one* instance of a class |
| **Number of instances** | Multiple (one per call) | Exactly one (global) |
| **Typical combination** | Often used together — the factory can be a singleton | The singleton instance is usually created lazily |

---

## Structural Patterns

### Adapter vs Facade

| Aspect | Adapter | Facade |
|---|---|---|
| **Intent** | Make an **existing** interface compatible with **another existing** interface | Provide a **new, simplified** interface over a complex subsystem |
| **Direction** | 1-to-1 — wraps a single class | 1-to-many — wraps an entire subsystem |
| **Existing interfaces** | Both interfaces already exist; we just bridge them | The simplified interface is new; the subsystem interfaces already exist |
| **Analogy** | A power plug adapter between EU and US sockets | A hotel reception desk that handles rooms, restaurant, and spa behind the scenes |

### Adapter vs Composite

| Aspect | Adapter | Composite |
|---|---|---|
| **Structure** | Wraps a **single** object to change its interface | Organizes objects in a **tree** (part-whole hierarchy) |
| **Goal** | Interface compatibility | Uniform treatment of individual and composite objects |
| **Recursion** | No | Yes — a composite contains other components (leaves or composites) |

### Facade vs Composite

| Aspect | Facade | Composite |
|---|---|---|
| **Structure** | A flat wrapper over several subsystems | A recursive tree structure |
| **Client view** | Sees one simplified entry point | Sees a uniform interface for both leaves and branches |
| **Use case** | Simplify a complex API | Represent hierarchies (file systems, org charts, UI widget trees) |

---

## Behavioral Patterns

### Strategy vs Template Method

This is one of the most common comparisons, since both deal with *varying an algorithm*.

| Aspect | Strategy | Template Method |
|---|---|---|
| **Mechanism** | **Composition** — inject a strategy object | **Inheritance** — subclass overrides abstract steps |
| **Flexibility** | Behavior can change **at runtime** (swap the strategy) | Behavior is fixed **at compile time** (class hierarchy) |
| **Granularity** | Replaces the **entire** algorithm | Replaces only **specific steps** within a fixed skeleton |
| **Number of classes** | One context + N strategy classes | One abstract class + N concrete subclasses |
| **Coupling** | Low — context and strategy are independent | Higher — subclass is tightly coupled to the base class |
| **When to use** | When you need to switch algorithms dynamically, or when the algorithms are completely different | When algorithms share most of their structure and only differ in a few steps |

**Rule of thumb**: if the algorithms share 80 % of their code, use Template Method. If they are substantially different, use Strategy.

### Observer vs Strategy

| Aspect | Observer | Strategy |
|---|---|---|
| **Relationship** | One-to-**many** (one subject, many observers) | One-to-**one** (one context, one strategy at a time) |
| **Communication** | The subject **pushes** notifications to observers | The context **delegates** execution to the strategy |
| **Goal** | Decouple a state change from its side effects | Decouple an algorithm from the code that uses it |

### Observer vs Iterator

| Aspect | Observer | Iterator |
|---|---|---|
| **Model** | **Push** — the subject notifies observers when something happens | **Pull** — the client asks for the next element when it wants one |
| **Control** | The subject controls timing | The client controls timing |
| **Use case** | Event-driven systems, UI, reactive programming | Traversing collections, lazy evaluation, data pipelines |

---

## Cross-Category Comparisons

### Factory Method (Creational) vs Strategy (Behavioral)

Both rely on polymorphism, but with different goals:

| Aspect | Factory Method | Strategy |
|---|---|---|
| **What varies** | *Which object* is created | *Which algorithm* is executed |
| **Mechanism** | Subclass overrides a factory method | Client injects a strategy object |
| **Result** | A new object of the correct type | The same context behaves differently |

### Composite (Structural) vs Iterator (Behavioral)

Often used together:

| Aspect | Composite | Iterator |
|---|---|---|
| **Focus** | **Structure** — how objects are organized in a tree | **Traversal** — how to visit the elements of a structure |
| **Relationship** | Defines the tree | Walks the tree |
| **Typical combination** | A Composite tree + an Iterator that traverses it in different orders (DFS, BFS, level-order) |

---

## Complete Summary Table

| | **Singleton** | **Factory Method** | **Abstract Factory** | **Adapter** | **Facade** | **Composite** | **Observer** | **Iterator** | **Strategy** | **Template Method** |
|---|---|---|---|---|---|---|---|---|---|---|
| **Category** | Creational | Creational | Creational | Structural | Structural | Structural | Behavioral | Behavioral | Behavioral | Behavioral |
| **Intent** | Guarantee a single global instance of a class | Delegate object creation to subclasses | Create families of related objects without specifying concrete classes | Make an incompatible interface work with an expected one | Provide a simplified interface to a complex subsystem | Treat individual objects and compositions uniformly in a tree | Notify multiple dependents automatically when state changes | Traverse a collection without exposing its internal structure | Encapsulate interchangeable algorithms, swap at runtime | Define an algorithm skeleton, letting subclasses override specific steps |
| **Core mechanism** | Private constructor + static access point | Inheritance — subclass overrides a creation method | Composition — client receives a factory object | Wraps an existing class, translating its interface | Wraps multiple subsystem classes behind one entry point | Recursive tree — composites contain other components | Subject maintains a list of observers and calls their `update()` | Encapsulates traversal state (`__iter__` / `__next__` in Python) | Context holds a strategy reference and delegates via `execute()` | Base class calls abstract "hook" methods that subclasses implement |
| **Key participants** | Singleton class itself | Creator (abstract), ConcreteCreator, Product | AbstractFactory, ConcreteFactory, AbstractProduct, ConcreteProduct | Target interface, Adapter, Adaptee | Facade, Subsystem classes | Component, Leaf, Composite | Subject (Observable), Observer (Listener) | Iterator, Iterable (Collection) | Strategy interface, ConcreteStrategy, Context | AbstractClass, ConcreteClass |
| **Real example in repo** | Database connection pool | Cross-platform notification system | Cross-platform UI kit (Windows/macOS) | Legacy XML system → JSON interface | Home theater system | File system (files & folders) | Event-driven UI (buttons, forms, listeners) | Corporate org chart traversal | E-commerce payment methods | Data import pipeline (CSV, SQL) |
| **Number of classes** | 1 | 1 abstract + N concrete creators + N products | 1 abstract factory + N concrete factories + M×N products | 1 adapter + 1 adaptee | 1 facade + N subsystems | 1 component interface + N leaf/composite types | 1 subject + N observers | 1 iterator per traversal strategy | 1 context + N strategies | 1 abstract base + N concrete subclasses |
| **Relationship type** | — | One-to-one (creator → product) | One-to-many (factory → product family) | One-to-one (adapter → adaptee) | One-to-many (facade → subsystems) | Part-whole tree (recursive) | One-to-many (subject → observers) | One-to-one (iterator → collection) | One-to-one (context → strategy) | One-to-many (base → subclasses via inheritance) |
| **Polymorphism** | No | Yes — creator subclass decides product type | Yes — factory subclass decides product family | Yes — adapter implements target interface | No — facade is a concrete class | Yes — component interface unifies leaf and composite | Yes — observers share a common interface | Yes — different iterators over the same collection | Yes — strategies share a common interface | Yes — subclasses override abstract steps |
| **Uses inheritance** | No | Yes (core mechanism) | No (uses composition) | Optionally (class adapter) | No | Yes (component hierarchy) | No | Optionally | No (uses composition) | Yes (core mechanism) |
| **Uses composition** | No | Optionally | Yes (core mechanism) | Yes (object adapter) | Yes | Yes (composites hold children) | Yes (subject holds observer list) | Yes (iterator holds collection ref) | Yes (core mechanism) | No |
| **Runtime flexibility** | None — instance is fixed | Low — type is fixed at subclass level | Low — family is fixed at factory level | None — bridge is fixed | None — facade is fixed | Medium — can add/remove nodes | High — add/remove observers anytime | Medium — can switch traversal strategy | **High** — swap strategy at any time | None — algorithm is fixed at compile time |
| **Open/Closed Principle** | N/A | ✅ New creator subclass = new product | ✅ New factory = new product family | ✅ New adapter = new integration | ❌ New subsystem may require facade changes | ✅ New leaf/composite type | ✅ New observer = new reaction | ✅ New iterator = new traversal order | ✅ New strategy = new algorithm | ✅ New subclass = new step variation |
| **Main advantage** | Controlled global access, avoids duplicates | Decouples client from concrete product classes | Ensures consistency within a product family | Reuses legacy code without modification | Reduces complexity for callers | Recursive structures with uniform interface | Loose coupling between subject and reactions | Client doesn't need to know collection internals | Algorithms are isolated, testable, interchangeable | Common code written once — DRY |
| **Main risk** | Global mutable state, hard to test, hidden coupling | Class explosion if many product types | Complex — N factories × M products | Extra indirection layer | Can become a "god object" if it grows | Overly generic interface for leaves | Memory leaks if observers aren't unregistered | Overhead for simple collections | Client must know which strategy to pick | Fragile base class — changes propagate to all subclasses |
| **Common analogy** | A government — only one president at a time | A logistics company — each branch creates its own vehicles | A furniture store — each style (modern, classic) produces a full set | A power plug adapter between EU and US sockets | A hotel reception desk | A folder tree on a computer | A newsletter — publisher sends, subscribers react | A TV remote — next/previous channel without knowing frequencies | A GPS — same destination, different route algorithms | A recipe — fixed steps, but each chef adds their sauce |
| **Frequently combined with** | Factory Method (singleton factory) | Template Method, Singleton | Factory Method (internally) | Facade (adapt then simplify) | Adapter (behind the facade) | Iterator (traverse the tree) | Strategy, Mediator | Composite (traverse a tree) | Factory Method (create strategies), Observer | Strategy (for the variable part), Factory Method |

---

## Quick Decision Guide

| If you need to… | Consider |
|---|---|
| Ensure a single global instance | **Singleton** |
| Decide which class to instantiate at runtime | **Factory Method** |
| Create families of related objects | **Abstract Factory** |
| Make an old class work with a new interface | **Adapter** |
| Simplify access to a complex subsystem | **Facade** |
| Represent a part-whole hierarchy | **Composite** |
| Notify multiple objects of a state change | **Observer** |
| Traverse a collection without exposing internals | **Iterator** |
| Swap algorithms at runtime | **Strategy** |
| Share algorithm structure, vary specific steps | **Template Method** |
