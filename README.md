# Design Patterns — Enciclopedia Personale
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Course](https://img.shields.io/badge/Course-Software%20Development%20Methodologies-green)
![UNIMORE](https://img.shields.io/badge/University-UNIMORE-004990?style=flat)

Un'enciclopedia pratica e personale dei design pattern più comuni nella programmazione orientata agli oggetti.

---

## Obiettivo

Questo repository nasce come strumento di studio e riferimento personale per capire, implementare e padroneggiare i design pattern fondamentali. Ogni pattern è:

- **Isolato**: un micro-progetto autocontenuto
- **Spiegato**: con descrizioni chiare e precise, analogie con il mondo reale e diagrammi UML
- **Dimostrato**: con un'implementazione didattica e un esempio concreto ispirato a scenari reali
- **Contestualizzato**: con casi in cui il pattern è stato applicato in prima persona

---

## Struttura del Repository

```
design-pattern/
├── README.md                         # Questo file
├── docs/                             # Documentazione di supporto
│   ├── glossary.md                  # Terminologia dei design pattern
│   ├── comparison.md                # Confronti tra pattern simili
│   └── resources.md                 # Risorse e link utili
│
├── 01_creational/                    # Pattern Creazionali
│   ├── README.md
│   ├── singleton/
│   ├── factory/
│   └── abstract-factory/
│
├── 02_structural/                    # Pattern Strutturali
│   ├── README.md
│   ├── adapter/
│   ├── facade/
│   └── composite/
│
└── 03_behavioral/                    # Pattern Comportamentali
    ├── README.md
    ├── observer/
    ├── iterator/
    ├── strategy/
    └── template-method/
```

---

## Come è Documentato Ogni Pattern

Ogni cartella di pattern segue una struttura standard:

### `README.md`
1. **Problema**: quale problema concreto risolve il pattern, con analogia reale
2. **Soluzione**: come il pattern affronta il problema, con descrizione degli attori
3. **Diagramma**: UML generato con Mermaid (generico + specifico per l'esempio)

### `problem.py`
Implementazione naïve del problema, senza applicare il pattern — per capire cosa si vuole evitare.

### `implementation.py`
Implementazione didattica del pattern: codice commentato, struttura chiara, output dimostrativo.

### `real_example.py`
Esempio concreto ispirato a uno scenario reale (e-commerce, pipeline dati, sistemi aziendali), che mostra come il pattern si applica in pratica.

---

## Categorie

### Pattern Creazionali — [`01_creational/`](./01_creational/)

Si occupano della **creazione di oggetti**, fornendo meccanismi flessibili per separare la creazione dalla responsabilità dell'oggetto stesso.

| Pattern | Intento |
|---|---|
| [Singleton](./01_creational/singleton/) | Una sola istanza globale |
| [Factory Method](./01_creational/factory/) | Delega la creazione alle sottoclassi |
| [Abstract Factory](./01_creational/abstract-factory/) | Famiglie di oggetti correlati |

### Pattern Strutturali — [`02_structural/`](./02_structural/)

Si occupano della **composizione di classi e oggetti**, spiegando come assemblarli in strutture più grandi mantenendo flessibilità.

| Pattern | Intento |
|---|---|
| [Adapter](./02_structural/adapter/) | Converte interfacce incompatibili |
| [Facade](./02_structural/facade/) | Interfaccia semplificata a un sottosistema complesso |
| [Composite](./02_structural/composite/) | Strutture ad albero parte-tutto |

### Pattern Comportamentali — [`03_behavioral/`](./03_behavioral/)

Si occupano della **comunicazione tra oggetti**, definendo come interagiscono e come vengono distribuite le responsabilità.

| Pattern | Intento |
|---|---|
| [Observer](./03_behavioral/observer/) | Notifica automatica ai dipendenti al cambio di stato |
| [Iterator](./03_behavioral/iterator/) | Attraversamento uniforme di collezioni |
| [Strategy](./03_behavioral/strategy/) | Algoritmi intercambiabili a runtime |
| [Template Method](./03_behavioral/template-method/) | Scheletro fisso dell'algoritmo, passi variabili nelle sottoclassi |

---

## Tecnologie

- **Linguaggio**: Python 3.x
- **Diagrammi**: Mermaid
- **Documentazione**: Markdown

---

## Note

> **Work in Progress**: il repository è in costante evoluzione. I pattern vengono aggiunti e migliorati progressivamente.

**Autore**: lucadileo9
