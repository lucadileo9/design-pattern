# Abstract Factory Pattern

## Problema

Innanzitutto è importante analizzare questo design pattern solo dopo aver analizzato e capito il Factory Method, perché è un'estensione di quest'ultimo. 
Infatti tale pattern si pone come obiettivo quello di risolvere un problema più complesso, ovvero quando abbiamo più famiglie di prodotti da creare. Nell'esempio del Factory Method, avevamo un solo tipo di classe, simili tra loro: `X`, `Y`, `Z`. Quindi quel che facemmo fu creare un'interfaccia comune `A` e poi una factory per ogni classe concreta, così da usare le factory per creare oggetti di tipo `A` senza conoscere la classe concreta.
Ora invece immaginiamo di avere più famiglie di classi, ad esempio `X1`, `Y1`, `Z1` che appartengono alla famiglia 1, e `X2`, `Y2`, `Z2` che appartengono alla famiglia 2. Il problema è che se usassimo il Factory Method, avremmo bisogno di una factory per ogni classe concreta, quindi 6 factory: `FactoryX1`, `FactoryY1`, `FactoryZ1`, `FactoryX2`, `FactoryY2`, `FactoryZ2`. Questo porterebbe a un numero esponenziale di factory.

Per ritornare all'esempio classico della logistica, immaginiamo di avere sempre i mezzi di trasporto `Camion`, `Nave`, `Aereo`, ma ora abbiamo due famiglie che li dividono ulteriormente: i mezzi elettrici (`CamionElettrico`, `NaveElettrica`, `AereoElettrico`) e i mezzi a combustione (`CamionCombustione`, `NaveCombustione`, `AereoCombustione`). Se usassimo il Factory Method, avremmo bisogno di 6 factory per creare questi mezzi, il che è inefficiente e difficile da mantenere.

N.B.: tipicamente i vari prodotti di una famiglia sono progettati per lavorare insieme, come ad esempio un database con un driver specifico o un logger specifico e così via. 

## Soluzione

La soluzione a questo problema è il pattern **Abstract Factory**. In questo pattern, invece di avere una factory per ogni classe concreta, abbiamo una factory astratta che definisce un'interfaccia per creare famiglie di oggetti correlati. Poi, per ogni famiglia di prodotti, creiamo una factory concreta che implementa questa interfaccia.

Spiegato per fasi abbiamo:
- **Product**: definiamo l'interfaccia del prodotto (es. `A`) con metodi astratti. Le classi concrete (`X1`, `Y1`, `Z1`, `X2`, `Y2`, `Z2`) implementeranno questa interfaccia.
- **Abstract Factory**: definiamo l'interfaccia `AbstractFactory` con metodi astratti per creare OGNI tipo di prodotto, ad esempio `create_X()`, `create_Y()`, `create_Z()`. Le classi concrete (`FactoryFamiglia1`, `FactoryFamiglia2`) implementano questi metodi e restituiscono istanze dei prodotti concreti della rispettiva famiglia.

Di conseguenza quel che succede è che io con ogni factory concreta creo un'intera famiglia di prodotti, e il client può scegliere quale famiglia usare semplicemente istanziando la factory concreta corrispondente.

Come usare l'Abstract Factory

- Nel codice client, invece di istanziare direttamente i prodotti concreti, si istanzia la factory concreta corrispondente alla famiglia di prodotti desiderata (es. `FactoryFamiglia1`) e si chiama i metodi per creare i prodotti (es. `create_X()`, `create_Y()`, `create_Z()`).
- Il client utilizza l'interfaccia dei prodotti senza conoscere la loro implementazione concreta, e può facilmente cambiare la famiglia di prodotti semplicemente cambiando la factory concreta istanziata.

Esempio (logistica)
- Interfaccia comune: `MezzoDiTrasporto` con `carica()` e `scarica()`.
- Classi concrete: `CamionElettrico`, `NaveElettrica`, `AereoElettrico` per la famiglia elettrica, e `CamionCombustione`, `NaveCombustione`, `AereoCombustione` per la famiglia a combustione, tutte implementano `MezzoDiTrasporto`.
- Definiamo l'interfaccia `MezzoDiTrasportoFactory` con metodi `create_Camion()`, `create_Nave()`, `create_Aereo()`.
- Implementazioni concrete: `FactoryElettrica`, `FactoryCombustione`, ciascuna crea i rispettivi mezzi di trasporto della famiglia. 


## Diagrammi

### Diagramma generico

```mermaid
%%{init: {"layout": "elk"}}%%
classDiagram
    direction TB

    %% --- GERARCHIA PRODOTTI A ---
    class AbstractProductA {
        <<interface>>
        +operationA()*
    }
    class ConcreteProductA1 {
        +operationA()
    }
    class ConcreteProductA2 {
        +operationA()
    }

    %% --- GERARCHIA PRODOTTI B ---
    class AbstractProductB {
        <<interface>>
        +operationB()*
    }
    class ConcreteProductB1 {
        +operationB()
    }
    class ConcreteProductB2 {
        +operationB()
    }

    %% --- GERARCHIA FACTORY ---
    class AbstractFactory {
        <<interface>>
        +createProductA()* AbstractProductA
        +createProductB()* AbstractProductB
    }

    class ConcreteFactory1 {
        +createProductA() AbstractProductA
        +createProductB() AbstractProductB
    }

    class ConcreteFactory2 {
        +createProductA() AbstractProductA
        +createProductB() AbstractProductB
    }

    %% Relazioni Prodotti
    AbstractProductA <|.. ConcreteProductA1
    AbstractProductA <|.. ConcreteProductA2
    AbstractProductB <|.. ConcreteProductB1
    AbstractProductB <|.. ConcreteProductB2

    %% Relazioni Factory
    AbstractFactory <|.. ConcreteFactory1
    AbstractFactory <|.. ConcreteFactory2

    %% Relazioni di Creazione (DIPENDENZE)
    ConcreteFactory1 ..> ConcreteProductA1 : "crea"
    ConcreteFactory1 ..> ConcreteProductB1 : "crea"
    ConcreteFactory2 ..> ConcreteProductA2 : "crea"
    ConcreteFactory2 ..> ConcreteProductB2 : "crea"

    %% Styling
    style AbstractFactory fill:#1e272e,stroke:#05c46b,stroke-width:2px,color:#fff
    style AbstractProductA fill:#1e272e,stroke:#0fbcf9,stroke-width:2px,color:#fff
    style AbstractProductB fill:#1e272e,stroke:#0fbcf9,stroke-width:2px,color:#fff
    
    style ConcreteFactory1 fill:#2d3436,stroke:#ced4da,color:#fff
    style ConcreteFactory2 fill:#2d3436,stroke:#ced4da,color:#fff
```




### Diagramma specifico

La cosa migliore è guardare questi diagramma dopo aver visto il codice, altrimenti potrebbe essere un po' difficile da capire. 

```mermaid
%%{init: {"layout": "elk"}}%%
classDiagram
    direction TB

    %% --- INTERFACCE (PRODOTTI) ---
    class DatabaseConnection {
        <<interface>>
        +open() bool
        +query(sql) str
        +health_check() bool
        +close()
    }

    class Logger {
        <<interface>>
        +info(msg)
        +error(msg)
        +flush()
    }

    %% --- GERARCHIA FACTORY ---
    class InfrastructureFactory {
        <<abstract>>
        +create_database()* DatabaseConnection
        +create_logger()* Logger
    }

    class ProductionFactory {
        +create_database() DatabaseConnection
        +create_logger() Logger
    }

    class CloudFactory {
        +create_database() DatabaseConnection
        +create_logger() Logger
    }

    %% --- CLIENT ---
    class Application {
        -db: DatabaseConnection
        -log: Logger
        +run()
    }

    %% --- RELAZIONI ---
    InfrastructureFactory <|-- ProductionFactory : implementa
    InfrastructureFactory <|-- CloudFactory : implementa
    
    DatabaseConnection <|.. MySQLConnection : implementa
    DatabaseConnection <|.. MongoDBConnection : implementa
    
    Logger <|.. FileLogger : implementa
    Logger <|.. CloudLogger : implementa

    %% Relazioni di Creazione (Vicolo di coerenza)
    ProductionFactory ..> MySQLConnection : "crea"
    ProductionFactory ..> FileLogger : "crea"
    
    CloudFactory ..> MongoDBConnection : "crea"
    CloudFactory ..> CloudLogger : "crea"

    %% Il Client usa solo le astrazioni
    Application o-- InfrastructureFactory : riceve
    Application o-- DatabaseConnection : usa
    Application o-- Logger : usa

    %% Styling
    style InfrastructureFactory fill:#1e272e,stroke:#05c46b,stroke-width:2px,color:#fff
    style DatabaseConnection fill:#1e272e,stroke:#0fbcf9,stroke-width:2px,color:#fff
    style Logger fill:#1e272e,stroke:#ffa502,stroke-width:2px,color:#fff
    style Application fill:#2d3436,stroke:#ef5777,stroke-width:2px,color:#fff
```
### Diagramma di sequenza


```mermaid
%%{init: {"layout": "elk"}}%%
sequenceDiagram
    autonumber
    
    participant Client as Main / EntryPoint
    participant App as Application
    participant Fact as ProductionFactory
    participant DB as MySQLConnection
    participant Log as FileLogger

    Note over Client, Fact: 1. Setup dell'Ambiente
    Client->>Fact: new ProductionFactory()
    Client->>App: new Application(factory)
    
    activate App
    App->>Fact: create_database()
    Fact->>DB: new MySQLConnection(config)
    Fact-->>App: ritorna istanza DB
    
    App->>Fact: create_logger()
    Fact->>Log: new FileLogger(path)
    Fact-->>App: ritorna istanza Logger
    deactivate App

    Note over App, Log: 2. Esecuzione Business Logic
    Client->>App: run()
    activate App
    App->>Log: info("Avvio applicazione")
    App->>DB: open()
    DB-->>App: True
    App->>DB: query("SELECT version()")
    DB-->>App: "[MySQL] Risultato..."
    App->>Log: info("Query eseguita")
    
    App->>DB: close()
    App->>Log: flush()
    deactivate App
    
```

### Vantaggi
L'Abstract Factory offre benefici cruciali per la gestione di sistemi complessi:

- **Compatibilità dei Prodotti**: Garantite che i prodotti ottenuti da una factory siano compatibili tra loro, mantenendo la coerenza all'interno della famiglia di oggetti.


- **Disaccoppiamento**: Si evita un accoppiamento stretto tra il codice client e le classi concrete dei prodotti.


- **Single Responsibility Principle**: Potete estrarre il codice di creazione dei prodotti in un unico posto, rendendo il sistema più facile da supportare e manutenere.



- **Open/Closed Principle**: È possibile introdurre nuove varianti (famiglie) di prodotti senza dover modificare il codice client esistente. Tuttavia... vedi contro 


### Svantaggi
Tuttavia, l'astrazione ha un costo:
- **Complessità Elevata**: Il codice può diventare inutilmente complicato a causa dell'introduzione di numerose nuove interfacce e classi.

- **Rigidità dell'Interfaccia**: Se dovete aggiungere un nuovo tipo di prodotto alla famiglia (ad esempio, aggiungere un "Elicottero" alla vostra logistica), dovrete modificare l'interfaccia della Factory Astratta e tutte le sue implementazioni concrete.


- **Difficoltà Iniziale**: Richiede una pianificazione attenta e una conoscenza approfondita dei principi della programmazione orientata agli oggetti.
