# Design Patterns Repository

> A practical and personal encyclopedia of the most common design patterns in object-oriented programming.

---

## Project Goal

This repository was created as a study and reference tool to understand, implement, and master fundamental design patterns. Each pattern is:

* **Isolated**: A self-contained micro-project.
* **Explained**: With clear and concise descriptions.
* **Demonstrated**: Using educational and practical examples.
* **Contextualized**: With real-world analogies.

---

## Repository Structure

```
design-pattern/
├── README.md                    # This file
├── docs/                        # Supporting documentation
│   ├── glossary.md              # Design patterns terminology
│   ├── comparison.md            # Comparisons between similar patterns
│   └── resources.md             # Useful links and resources
│
├── 01_creational/               # Creational Patterns
│   ├── README.md                # Category overview
│   ├── factory/
│   │   ├── README.md            # Pattern explanation
│   │   └── example.py           # Educational implementation
│   ├── singleton/
│   ├── builder/
│   ├── prototype/
│   └── abstract_factory/
│
├── 02_structural/               # Structural Patterns
│   ├── README.md
│   ├── adapter/
│   ├── bridge/
│   ├── composite/
│   ├── decorator/
│   ├── facade/
│   ├── flyweight/
│   └── proxy/
│
└── 03_behavioral/               # Behavioral Patterns
    ├── README.md
    ├── chain_of_responsibility/
    ├── command/
    ├── iterator/
    ├── mediator/
    ├── memento/
    ├── observer/
    ├── state/
    ├── strategy/
    ├── template_method/
    └── visitor/

```

---

## Pattern Documentation Template

Each pattern follows a standardized structure to facilitate learning:

### Pattern README.md

1. **Problem**: What specific problem does the pattern solve?
2. **Solution**: How the pattern addresses the problem.
3. **Diagram**: Visualization using Mermaid UML.
4. **Real-World Analogy**: An example from everyday life.

### example.py

A minimal and educational implementation of the pattern in Python, featuring:

* Clear and commented code.
* Practical usage example.
* Demonstrative output.

---

## How to Use This Repository

### For Studying

Navigate through the categories and read the README for each pattern. Real-world analogies will help you understand the concepts intuitively.

### For Reference

Use the tree structure to quickly find the pattern you need. Every example can be executed independently.

### For Demonstration

Showcase your theoretical and practical knowledge of design patterns with concrete, documented implementations.

---

## Progress Tracker

### Creational Patterns

* [ ] Factory Method
* [ ] Abstract Factory
* [ ] Builder
* [ ] Prototype
* [ ] Singleton

### Structural Patterns

* [ ] Adapter
* [ ] Bridge
* [ ] Composite
* [ ] Decorator
* [ ] Facade
* [ ] Flyweight
* [ ] Proxy

### Behavioral Patterns

* [ ] Chain of Responsibility
* [ ] Command
* [ ] Iterator
* [ ] Mediator
* [ ] Memento
* [ ] Observer
* [ ] State
* [ ] Strategy
* [ ] Template Method
* [ ] Visitor

---

## Technologies

* **Language**: Python 3.x
* **Diagrams**: Mermaid
* **Documentation**: Markdown

---

## Design Pattern Categories

### Creational

These patterns concern **object creation**, providing mechanisms that increase flexibility and code reuse.

### Structural

These patterns concern the **composition of classes and objects**, explaining how to assemble objects and classes into larger structures.

### Behavioral

These patterns concern **communication between objects**, defining how objects interact and distribute responsibilities.

---

## Who Is This Repository For?

* **Students** wanting to learn design patterns.
* **Developers** looking for a quick reference.
* **Candidates** preparing for technical interviews.
* **Anyone** wishing to deepen their knowledge of OOP.

---

## Notes

> **Work in Progress**: This repository is constantly evolving. Patterns are added and improved progressively.

**Author**: lucadileo9

**Version**: 1.0.0 (WIP)
