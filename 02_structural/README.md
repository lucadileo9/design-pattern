# Structural Patterns

Structural patterns deal with the **composition of classes and objects**: how to assemble them into larger structures while maintaining flexibility, reusability, and readability. Rather than intervening in object creation, they focus on how objects relate to and collaborate with each other.
In fact, they often don't introduce new functionality or specify particular behaviors, but simply organize and structure existing code in a more efficient and maintainable way.

---

## 1. Adapter

**Intent**: convert the interface of a class into another one expected by the client, allowing classes with incompatible interfaces to work together.

**Typical use**: integrating external libraries, legacy code, or third-party APIs without modifying them, adapting their output to the format expected by the system.

Reference: [Full explanation](./adapter/README.md)

---

## 2. Facade

**Intent**: provide a simplified interface to a complex subsystem, hiding the internal complexity from the client.

**Typical use**: orchestrating multiple services or modules (e.g. payments, shipping, notifications) through a single access point, reducing coupling between the client and the subsystems.

Reference: [Full explanation](./facade/README.md)

---

## 3. Composite

**Intent**: compose objects into tree structures allowing the client to uniformly treat individual objects and compositions.

**Typical use**: recursive hierarchical structures such as menus, file systems, e-commerce categories, org charts — where you want to apply the same operation to a single element or an entire branch.

Reference: [Full explanation](./composite/README.md)

---

## 4. Decorator

**Intent**: add responsibilities to an object dynamically, without modifying its class. A flexible alternative to inheritance for extending behavior.

**Typical use**: adding cross-cutting functionality (logging, caching, validation) to existing objects in a composable way.

*To be completed...*

---

## 5. Proxy

**Intent**: provide a surrogate or placeholder for another object, controlling access to it.

**Typical use**: lazy loading, access control, caching, logging — whenever you want to intercept or wrap calls to a real object.

*To be completed...*

---

## Real-world cases where I used these patterns:
**Facade**:
- In an integration project between multiple services accessed via API (Teams, Telegram, Notion), I created a Facade that handled orchestrating all the calls to the various services, hiding the complexity from the client.
- In a project to create a distributed computing system (in Java using RMI) I created a Facade class JobManager that handled job management; specifically, using the classes it was initialized with, it took the job, split it into smaller tasks (using the strategy it was initialized with), determined the distribution of tasks across workers (using the strategy it was initialized with), and finally delegated task execution to another class (a dedicated class that performed the RMI calls).