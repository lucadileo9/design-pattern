# Design Patterns Glossary

> Common terminology used in the context of design patterns

---

## General Terms

### Design Pattern
A reusable solution template for a commonly recurring problem in software design. A pattern is not ready-made code — it's a description of an approach that can be adapted to different situations.

### Gang of Four (GoF)
The four authors — Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides — of the seminal book *"Design Patterns: Elements of Reusable Object-Oriented Software"* (1994), which catalogued 23 fundamental patterns.

### Creational Pattern
A pattern that deals with **object creation**, providing flexible mechanisms to decouple the client from the concrete classes it instantiates. Examples: Singleton, Factory Method, Abstract Factory.

### Structural Pattern
A pattern that deals with **the composition of classes and objects**, explaining how to assemble them into larger, flexible structures. Examples: Adapter, Facade, Composite.

### Behavioral Pattern
A pattern that deals with **communication and responsibility distribution** between objects, defining how they interact and collaborate. Examples: Observer, Iterator, Strategy, Template Method.

---

## OOP & SOLID Principles

### Encapsulation
Bundling data and the methods that operate on that data within a single unit (class), restricting direct access to internal state. Many patterns leverage encapsulation to hide complexity.

### Polymorphism
The ability of different classes to respond to the same method call in different ways. This is the engine behind most design patterns — the client codes against an interface, and the correct behavior is resolved at runtime.

### Abstraction
Exposing only the essential features of an object while hiding implementation details. Interfaces and abstract classes are the primary tools.

### Inheritance
A mechanism where a class (subclass) derives from another (superclass), inheriting its attributes and methods. Used heavily in Template Method; often replaced by composition in patterns like Strategy.

### Composition over Inheritance
A design principle suggesting that classes should achieve polymorphic behavior by containing instances of other classes (composition) rather than inheriting from a base class. Favored by Strategy, Observer, and Adapter.

### Single Responsibility Principle (SRP)
A class should have **one, and only one, reason to change**. Design patterns often help achieve SRP by isolating specific responsibilities (e.g., Strategy isolates algorithm logic from the context).

### Open/Closed Principle (OCP)
Software entities should be **open for extension but closed for modification**. Adding a new `ConcreteStrategy` or a new `ConcreteObserver` doesn't require modifying existing code.

### Liskov Substitution Principle (LSP)
Objects of a subclass should be substitutable for objects of the superclass without altering the correctness of the program. Template Method relies on this: any concrete algorithm can replace the base reference.

### Dependency Inversion Principle (DIP)
High-level modules should not depend on low-level modules; both should depend on abstractions. Factory Method and Abstract Factory are direct applications of DIP.

### Interface Segregation Principle (ISP)
Clients should not be forced to depend on interfaces they do not use. Keeping the `Strategy` or `Observer` interface small and focused is an application of ISP.

---

## Pattern Roles & Participants

### Client
The code that uses the pattern. It typically works with abstractions (interfaces/abstract classes) and is unaware of the concrete implementations.

### Context
In Strategy and similar patterns, the class that maintains a reference to a strategy/behavior object and delegates work to it.

### Subject (Observable)
In the Observer pattern, the object that holds state and notifies registered observers when that state changes.

### Observer (Listener)
In the Observer pattern, an object that registers with a subject to receive notifications. It implements an `update()` or `on_event()` method.

### Creator
In the Factory Method pattern, the abstract class that declares the factory method. Subclasses override it to produce specific products.

### Product
In Factory and Abstract Factory, the object being created. The client interacts with it through an abstract interface.

### Concrete Class
A non-abstract class that provides the actual implementation of an interface or abstract class (e.g., `ConcreteStrategyA`, `CSVImporter`, `CreditCard`).

### Abstract Class / Interface
Defines the contract that concrete classes must fulfill. In Python, this is typically achieved with `abc.ABC` and `@abstractmethod`.

---

## Structural Concepts

### Wrapper
A general term for a class that "wraps" another, adding or modifying behavior. Adapter is a wrapper that changes the interface; Facade is a wrapper that simplifies it.

### Delegation
When an object hands off a task to another object rather than performing it itself. The Context *delegates* to the Strategy; the Facade *delegates* to subsystem classes.

### Coupling
The degree of interdependence between modules. Design patterns generally aim to **reduce coupling** — e.g., Observer decouples the subject from its observers.

### Cohesion
The degree to which the elements of a module belong together. High cohesion (each class does one thing well) is a goal shared by all patterns.

### Tree / Composite Structure
A recursive hierarchy where a node can be either a **leaf** (no children) or a **composite** (contains other nodes). Used in the Composite pattern.

---

## Behavioral Concepts

### Template Method
A method in a base class that defines the **skeleton** of an algorithm, calling abstract "hook" methods that subclasses override. The order of steps is fixed.

### Hook Method
An optional or abstract method within a template method that subclasses can override to customize behavior at specific points.

### Strategy Object
An interchangeable object that encapsulates a specific algorithm. The context holds a reference to it and can swap it at runtime.

### Event / Notification
A message sent from a subject to its observers, typically carrying data about what changed (event type, source, payload).

### Push vs Pull Model
- **Push**: the subject sends data to observers automatically (Observer pattern).
- **Pull**: the client explicitly requests the next element (Iterator pattern).

### Lazy Evaluation
Delaying computation until the result is actually needed. Iterators often leverage lazy evaluation (e.g., Python generators with `yield`).

### Iterator Protocol
In Python, the `__iter__()` and `__next__()` dunder methods that allow an object to be used in `for` loops and other iteration contexts.

---

## Common Anti-Patterns (what patterns help avoid)

### God Class
A class that knows too much or does too much. Strategy and Template Method decompose it into smaller, focused classes.

### Conditional Bloat
Excessive `if/elif/else` or `switch` chains to select behavior. Strategy replaces them with polymorphism.

### Tight Coupling
When a class directly depends on concrete implementations rather than abstractions. Factory Method, Observer, and Adapter all help break tight coupling.

### Code Duplication
Repeating the same logic in multiple places. Template Method eliminates it by extracting common steps into a base class.

### Polling
Repeatedly checking for a condition ("are we there yet?"). Observer eliminates polling by pushing notifications only when the state actually changes.
