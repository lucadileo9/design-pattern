# Simple Factory Pattern

Il simple factory pattern è un design pattern creazionale che fornisce un'interfaccia per creare oggetti in una superclasse, ma consente alle sottoclassi di alterare il tipo di oggetti che verranno creati. In altre parole, il simple factory pattern delega la responsabilità della creazione degli oggetti a una classe separata, chiamata factory, che decide quale classe concreta istanziare in base a determinate condizioni o parametri.
Quindi è parecchio diversa (e più semplice) rispetto al factory method.

Continuando con l'esempio della logistica, potremmo avere una classe `MezzoDiTrasportoFactory` che si occupa SOLO di creare istanze di `Camion`, `Nave` e `Aereo` in base a determinate condizioni o parametri.
Di conseguenza il costruttore di `MezzoDiTrasportoFactory` potrebbe solamente prendere un parametro che indica quale tipo di mezzo di trasporto creare, avere quindi un giga switch-case o if-else che decide quale classe concreta istanziare e restituire l'istanza creata. In questo modo, se in futuro dovessimo introdurre una nuova classe concreta, basterà aggiungere una nuova condizione al metodo `create()` della classe Factory, senza dover modificare il nostro codice principale.

## Limiti
Il simple factory pattern è semplice da implementare e può essere utile in situazioni in cui la logica di creazione degli oggetti è relativamente semplice e non richiede una grande flessibilità. Tuttavia, presenta alcuni limiti:
- Se la logica di creazione degli oggetti diventa complessa, la classe factory può diventare difficile da mantenere e testare.
- Se il numero di classi concrete cresce, la classe factory può diventare un "god class" che conosce tutte le classi concrete, violando il principio di Open/Closed.
- Non supporta bene l'estensione, poiché ogni volta che si aggiunge una nuova classe concreta, è necessario modificare la classe factory, il che può portare a errori e rendere il codice meno manutenibile.
- Non è adatto per situazioni in cui la creazione degli oggetti richiede una logica complessa o dipende da molte variabili, poiché la classe factory potrebbe diventare troppo complicata e difficile da gestire.