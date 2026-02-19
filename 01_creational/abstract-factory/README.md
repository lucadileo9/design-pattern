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


##  Diagrammi

### Diagramma generico delle classi

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




### Diagramma delle classi

La cosa migliore è guardare questi diagramma dopo aver visto il codice, altrimenti potrebbe essere un po' difficile da capire. 

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
    DatabaseConnection <|-- MySQLConnection : implementa
    DatabaseConnection <|-- MongoDBConnection : implementa
    DatabaseManager <|-- ProductionMySQLManager : estende
    DatabaseManager <|-- CloudMongoManager : estende

    %% Relazione di Dipendenza e Creazione
    DatabaseManager ..> DatabaseConnection : usa
    ProductionMySQLManager ..> MySQLConnection : crea
    CloudMongoManager ..> MongoDBConnection : crea

    %% Styling
    style DatabaseConnection fill:#1e272e,stroke:#0fbcf9,stroke-width:2px,color:#fff
    style DatabaseManager fill:#1e272e,stroke:#05c46b,stroke-width:2px,color:#fff
    style MySQLConnection fill:#2f3542,stroke:#ced4da,color:#fff
    style MongoDBConnection fill:#2f3542,stroke:#ced4da,color:#fff
```
### Diagramma di esecuzione


```mermaid
%%{init: {"layout": "elk"}}%%
graph 
    %% Definizione Stili Note
    classDef note style fill:#2f3640,stroke:#fbc531,stroke-width:2px,stroke-dasharray: 5 5,color:#fbc531,font-style:italic;
    classDef action style fill:#2d3436,stroke:#0fbcf9,color:#fff;
    classDef logic style fill:#2d3436,stroke:#05c46b,color:#fff;

    subgraph Client_Space [Ambiente Client]
        direction TB
        A[Inizio] --> B[Istanzia ProductionMySQLManager]
        
        %% NOTA 1
        N1{{<b>NOTA 1: Scelta del DB</b><br/>In questo preciso punto il Client<br/>decide quale database usare.<br/>Cambiando questa riga, cambia<br/>l'intero comportamento del sistema.}}
        B -.-> N1
    end

    subgraph Manager_Logic [DatabaseManager Base]
        direction TB
        C[Chiama initialize_system] --> D["db = self.create_database()"]
        
        %% NOTA 2
        N2{{<b>NOTA 2: Astrazione </b><br/> Il metodo ritorna un oggetto<br/>'DatabaseConnection'. Il Manager<br/>non sa se è MySQL o Mongo,<br/>sa solo che rispetta l'interfaccia.}}
        D -.-> N2
    end

    subgraph Operation [Utilizzo Polimorfico]
        direction TB
        H[db.open] --> I[db.query]
        
        %% NOTA 3
        N3{{<b>NOTA 3: Polimorfismo</b><br/>Questi metodi chiamati nel DataBaseManager funzionano a<br/>prescindere dal DB scelto perché<br/>tutte le classi derivano dalla<br/>stessa classe base astratta.}}
        I -.-> N3
    end

    %% Collegamenti tra i blocchi
    B --> C
    D --> H

    %% Assegnazione Classi
    class B,H,I action;
    class C,D logic;
    class N1,N2,N3 note;

```

### ✅ Vantaggi
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

### Quando usarlo?
Dovreste optare per l'Abstract Factory nelle seguenti circostanze:
- **Sistemi Multi-Piattaforma o Multi-Ambiente**: Quando il sistema deve supportare diverse famiglie di prodotti (es. interfacce utente per Windows, macOS e Linux) e volete che tutti i componenti siano coerenti tra loro.

- **Dipendenze tra Prodotti**: Quando avete un insieme di oggetti correlati progettati per essere utilizzati insieme e volete forzare questo vincolo a livello architettonico.


- **Configurazione Dinamica**: Quando un'applicazione deve scegliere una famiglia di prodotti in base alla configurazione corrente o alle impostazioni dell'ambiente.
