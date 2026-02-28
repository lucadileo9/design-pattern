# Factory Pattern

## Problem

Let's say we have a class `X` that performs certain operations. Later, we realize we need more classes that perform operations similar to those of `X`, but with some differences (e.g. `Y`).

In this case we might be tempted to create an instance of `X` or `Y` directly in our code, but this would force us to modify the code every time we introduce a new class. Moreover, creating instances in multiple places makes the code harder to maintain and test.

With a small number of classes this might be fine, but when the number of classes grows and you observe a recurring pattern of similar behavior, it's time to introduce a pattern that handles the situation more efficiently and maintainably.

Classic example: logistics
- We have a `Truck` class with `load()` and `unload()` methods.
- The company expands and needs new transport systems, e.g. `Ship`, with the same methods but different behaviors (water vs road).
- The client code would need to create instances of `Truck` or `Ship` depending on the case, increasing the risk of errors and maintenance difficulty.
- Adding a new vehicle (e.g. `Airplane`) would require changes to the client code if an appropriate pattern is not used.


## Solution

The solution is the **Factory** pattern. Let's proceed step by step:

- **Product**: we define the product interface (e.g. `A`) with abstract methods. The concrete classes (`X`, `Y`, `Z`) will implement this interface.
- **Factory / Creator**: we define the `Factory` interface with an abstract `create()` method. The concrete classes (`FactoryX`, `FactoryY`, `FactoryZ`) implement `create()` and return instances of concrete products.

Important: the **Creator** is not just for creating objects; it often contains core business logic that relies on the product objects returned by the factory method.

How to use the Creator

- In the client code, instead of instantiating `X`, `Y`, or `Z` directly, you instantiate the corresponding concrete `Factory` (e.g. `FactoryX`) and call `create()` to obtain a product (typed as the interface `A`).
- The client uses the product interface without knowing its concrete implementation.

Example (logistics)

- Common interface: `TransportVehicle` with `load()` and `unload()`.
- Concrete classes: `Truck`, `Ship`, `Airplane` implement `TransportVehicle`.
- We define the `TransportVehicleFactory` interface with `create()`.
- Concrete implementations: `TruckFactory`, `ShipFactory`, `AirplaneFactory`, each creates its respective `TransportVehicle`.

WARNING: do not confuse with *Simple Factory* — the `TransportVehicleFactory` here is an interface/creator, not a class with a switch-case that directly instantiates different products.

N.B.: there's no need to maintain a list of concrete classes anywhere, because everything is perfectly decoupled. 

## Diagrammi

### Generic diagram

```mermaid
classDiagram
    direction TD

    %% Parte dei Prodotti (L'interfaccia e ciò che viene creato)
    class Product {
        <<interface>>
        +operation()*
    }
    class ConcreteProduct {
        +operation()
    }

    %% Parte dei Creatori (La logica di istanziazione e business)
    class Creator {
        <<abstract>>
        +someOperation()
        +factoryMethod()* Product
    }
    class ConcreteCreator {
        +factoryMethod() Product
    }

    %% Relazioni Gerarchiche
    Product <|.. ConcreteProduct : implements
    Creator <|-- ConcreteCreator : extends

    %% Relazione di Dipendenza (Il cuore del pattern)
    ConcreteCreator ..> ConcreteProduct : instantiates
    Creator ..> Product : uses

    %% Styling Professionale Dark
    style Product fill:#2d3436,stroke:#00cec9,stroke-width:2px,color:#fff
    style Creator fill:#2d3436,stroke:#a29bfe,stroke-width:2px,color:#fff
    style ConcreteProduct fill:#2f3542,stroke:#dfe6e9,color:#fff
    style ConcreteCreator fill:#2f3542,stroke:#dfe6e9,color:#fff
```




### Specific diagram

The best approach is to look at these diagrams after reviewing the code, otherwise they might be a bit difficult to understand. 

```mermaid
%%{init: {"layout": "elk"}}%%
classDiagram
    direction TD

    %% Gerarchia PRODOTTI
    class DatabaseConnection {
        <<interface>>
        +open()*
        +query(sql)*
    }
    class MySQLConnection {
        +connection_string: str
        +open()
        +query(sql)
    }
    class MongoDBConnection {
        +uri: str
        +open()
        +query(sql)
    }
    
    %% Gerarchia CREATORI
    class DatabaseManager {
        <<abstract>>
        +create_database()* DatabaseConnection
        +initialize_system()
    }
    class ProductionMySQLManager {
        +create_database() DatabaseConnection
    }
    class CloudMongoManager {
        +create_database() DatabaseConnection
    }

    %% Relazioni di Ereditarietà
    DatabaseConnection <|-- MySQLConnection : implements
    DatabaseConnection <|-- MongoDBConnection : implements
    DatabaseManager <|-- ProductionMySQLManager : extends
    DatabaseManager <|-- CloudMongoManager : extends

    %% Dependency and Creation relationships
    DatabaseManager ..> DatabaseConnection : uses
    ProductionMySQLManager ..> MySQLConnection : creates
    CloudMongoManager ..> MongoDBConnection : creates

    %% Styling
    style DatabaseConnection fill:#1e272e,stroke:#0fbcf9,stroke-width:2px,color:#fff
    style DatabaseManager fill:#1e272e,stroke:#05c46b,stroke-width:2px,color:#fff
    style MySQLConnection fill:#2f3542,stroke:#ced4da,color:#fff
    style MongoDBConnection fill:#2f3542,stroke:#ced4da,color:#fff
```
### Sequence diagram


```mermaid
%%{init: {"layout": "elk"}}%%
graph 
    %% Note Styles Definition
    classDef note style fill:#2f3640,stroke:#fbc531,stroke-width:2px,stroke-dasharray: 5 5,color:#fbc531,font-style:italic;
    classDef action style fill:#2d3436,stroke:#0fbcf9,color:#fff;
    classDef logic style fill:#2d3436,stroke:#05c46b,color:#fff;

    subgraph Client_Space [Client Environment]
        direction TB
        A[Start] --> B[Instantiate ProductionMySQLManager]
        
        %% NOTE 1
        N1{{<b>NOTE 1: DB Choice</b><br/>At this exact point the Client<br/>decides which database to use.<br/>Changing this line changes<br/>the entire system behavior.}}
        B -.-> N1
    end

    subgraph Manager_Logic [Base DatabaseManager]
        direction TB
        C[Call initialize_system] --> D["db = self.create_database()"]
        
        %% NOTE 2
        N2{{<b>NOTE 2: Abstraction</b><br/>The method returns a<br/>'DatabaseConnection' object. The Manager<br/>doesn't know if it's MySQL or Mongo,<br/>only that it respects the interface.}}
        D -.-> N2
    end

    subgraph Operation [Polymorphic Usage]
        direction TB
        H[db.open] --> I[db.query]
        
        %% NOTE 3
        N3{{<b>NOTE 3: Polymorphism</b><br/>These methods called in the DatabaseManager work<br/>regardless of the chosen DB because<br/>all classes derive from the<br/>same abstract base class.}}
        I -.-> N3
    end

    %% Links between blocks
    B --> C
    D --> H

    %% Class Assignment
    class B,H,I action;
    class C,D logic;
    class N1,N2,N3 note;

```

### Advantages

Adopting the Factory Method offers significant structural benefits for software maintainability:

- **Decoupling**: avoids tight coupling between the class that uses the product (creator) and the concrete product classes.
- **Single Responsibility Principle**: moves creation code to a single point in the program, making it easier to manage.
- **Open/Closed Principle**: allows introducing new products without modifying existing client code.


### Svantaggi

Nonostante i benefici, ci sono aspetti critici da considerare:

- **Aumento della complessità**: il numero di sottoclassi può aumentare, rendendo il codice più articolato.
- **Rischio di over-engineering**: su progetti molto semplici il pattern può complicare inutilmente l'architettura.

