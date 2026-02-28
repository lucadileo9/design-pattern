# Creational Patterns

These patterns address the problem of object creation. When direct creation (via `new`) could lead to unwanted complexity or dependencies, creational patterns offer flexible mechanisms to separate creation from the object's own responsibility.

---

## 1. Singleton

**Intent**: ensure that a class has only one instance and provide a global access point to it.

**Typical usage**: managing shared resources (database connections, loggers, global configurations).

Reference: [Full explanation](./singleton/README.md)

---

## 2. Factory Method

**Intent**: define an interface for creating an object, delegating to subclasses the decision of which specific class to instantiate.

**Typical usage**: when the system cannot anticipate the exact type of objects to create or wants to delegate creation responsibility.

Reference: [Full explanation](./factory/README.md)

---

## 3. Abstract Factory

**Intent**: provide an interface for creating families of related or dependent objects without specifying their concrete classes.

**Typical usage**: creating multi-theme user interfaces or systems that need to support different product variants in a consistent way.

Reference: [Full explanation](./abstract_factory/README.md)

---

## 4. Builder

**Intent**: separate the construction of a complex object from its representation, allowing step-by-step construction processes.

**Typical usage**: creating objects with many optional parameters or when the construction process is complex.

*To be completed...*

---

## 5. Prototype

**Intent**: create new objects by cloning an existing prototype instead of building from scratch.

**Typical usage**: when creating a new object is more expensive than cloning, or when you want to avoid subclassing.

*To be completed...*


## Real cases where I used these patterns:
**Singleton**: 
 - I built an application that interacted via Python with Microsoft Teams, Notion, and a Telegram bot. I used a Singleton to manage the bot startup, since I needed to be sure that when the various APIs called the bot, it had already been started, and especially that it wouldn't be started more than once and that it was always the same instance.
