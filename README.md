# Design Patterns — Personal Encyclopedia
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Course](https://img.shields.io/badge/Course-Software%20Development%20Methodologies-green)
![UNIMORE](https://img.shields.io/badge/University-UNIMORE-004990?style=flat)

A practical and personal encyclopedia of the most common design patterns in object-oriented programming.

---

## Objective

This repository was created as a personal study and reference tool to understand, implement, and master fundamental design patterns. Each pattern is:

- **Isolated**: a self-contained micro-project
- **Explained**: with clear and precise descriptions, real-world analogies, and UML diagrams
- **Demonstrated**: with a didactic implementation and a concrete example inspired by real-world scenarios
- **Contextualized**: with cases where the pattern was applied first-hand

---

## Repository Structure

```
design-pattern/
├── README.md                         # This file
├── docs/                             # Supporting documentation
│   ├── glossary.md                  # Design pattern terminology
│   ├── comparison.md                # Comparisons between similar patterns
│   └── resources.md                 # Resources and useful links
│
├── 01_creational/                    # Creational Patterns
│   ├── README.md
│   ├── singleton/
│   ├── factory/
│   └── abstract-factory/
│
├── 02_structural/                    # Structural Patterns
│   ├── README.md
│   ├── adapter/
│   ├── facade/
│   └── composite/
│
└── 03_behavioral/                    # Behavioral Patterns
    ├── README.md
    ├── observer/
    ├── iterator/
    ├── strategy/
    └── template-method/
```

---

## How Each Pattern is Documented

Each pattern folder follows a standard structure:

### `README.md`
1. **Problem**: what concrete problem the pattern solves, with a real-world analogy
2. **Solution**: how the pattern addresses the problem, with a description of the actors
3. **Diagram**: UML generated with Mermaid (generic + specific for the example)

### `problem.py`
Naïve implementation of the problem, without applying the pattern — to understand what we want to avoid.

### `implementation.py`
Didactic implementation of the pattern: commented code, clear structure, demonstrative output.

### `real_example.py`
Concrete example inspired by a real-world scenario (e-commerce, data pipelines, enterprise systems), showing how the pattern is applied in practice.

---

## Categories

### Creational Patterns — [`01_creational/`](./01_creational/)

They deal with **object creation**, providing flexible mechanisms to separate creation from the object's own responsibility.

| Pattern | Intent |
|---|---|
| [Singleton](./01_creational/singleton/) | A single global instance |
| [Factory Method](./01_creational/factory/) | Delegates creation to subclasses |
| [Abstract Factory](./01_creational/abstract-factory/) | Families of related objects |

### Structural Patterns — [`02_structural/`](./02_structural/)

They deal with the **composition of classes and objects**, explaining how to assemble them into larger structures while maintaining flexibility.

| Pattern | Intent |
|---|---|
| [Adapter](./02_structural/adapter/) | Converts incompatible interfaces |
| [Facade](./02_structural/facade/) | Simplified interface to a complex subsystem |
| [Composite](./02_structural/composite/) | Part-whole tree structures |

### Behavioral Patterns — [`03_behavioral/`](./03_behavioral/)

They deal with **communication between objects**, defining how they interact and how responsibilities are distributed.

| Pattern | Intent |
|---|---|
| [Observer](./03_behavioral/observer/) | Automatic notification to dependents on state change |
| [Iterator](./03_behavioral/iterator/) | Uniform traversal of collections |
| [Strategy](./03_behavioral/strategy/) | Interchangeable algorithms at runtime |
| [Template Method](./03_behavioral/template-method/) | Fixed algorithm skeleton, variable steps in subclasses |

---

## Technologies

- **Language**: Python 3.x
- **Diagrams**: Mermaid
- **Documentation**: Markdown

---

## Notes

> **Work in Progress**: this repository is constantly evolving. Patterns are added and improved progressively.

**Author**: lucadileo9
