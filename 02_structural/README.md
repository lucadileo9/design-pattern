# Pattern Strutturali

I pattern strutturali si occupano della **composizione di classi e oggetti**: come assemblarli in strutture più grandi mantenendo flessibilità, riusabilità e leggibilità. Anziché intervenire sulla creazione degli oggetti, si concentrano su come questi si relazionano e collaborano tra loro.
Spessi infatti essi non introducono nuove funzionalità né specificano determinati comportamenti, ma si limitano a organizzare e strutturare il codice esistente in modo più efficiente e manutenibile. 

---

## 1. Adapter

**Intento**: convertire l'interfaccia di una classe in un'altra attesa dal client, permettendo a classi con interfacce incompatibili di lavorare insieme.

**Utilizzo tipico**: integrare librerie esterne, codice legacy o API di terze parti senza modificarli, adattando il loro output al formato atteso dal sistema.

Riferimento: [Spiegazione completa](./adapter/README.md)

---

## 2. Facade

**Intento**: fornire un'interfaccia semplificata a un sottosistema complesso, nascondendo la complessità interna al client.

**Utilizzo tipico**: orchestrare più servizi o moduli (es. pagamenti, spedizioni, notifiche) attraverso un unico punto di accesso, riducendo l'accoppiamento tra il client e i sottosistemi.

Riferimento: [Spiegazione completa](./facade/README.md)

---

## 3. Composite

**Intento**: comporre oggetti in strutture ad albero permettendo al client di trattare uniformemente singoli oggetti e composizioni.

**Utilizzo tipico**: strutture gerarchiche ricorsive come menu, file system, categorie e-commerce, organigrammi — dove si vuole applicare la stessa operazione a un elemento singolo o a un intero ramo.

Riferimento: [Spiegazione completa](./composite/README.md)

---

## 4. Decorator

**Intento**: aggiungere responsabilità a un oggetto dinamicamente, senza modificarne la classe. Alternativa flessibile all'ereditarietà per estendere il comportamento.

**Utilizzo tipico**: aggiunta di funzionalità trasversali (logging, caching, validazione) a oggetti esistenti in modo componibile.

*Da completare...*

---

## 5. Proxy

**Intento**: fornire un surrogato o segnaposto per un altro oggetto, controllando l'accesso a esso.

**Utilizzo tipico**: lazy loading, controllo degli accessi, caching, logging — ogni volta che si vuole intercettare o wrappare le chiamate a un oggetto reale.

*Da completare...*

---

## Casi reali in cui ho usato questi pattern:
**Facade**: 
- In un progetto di integrazione tra più servizi a cui accedevo tramite API (teams, telegram, notion), ho creato un Facade che si occupava di orchestrare tutte le chiamate ai vari servizi, nascondendo la complessità al client. 
- In un progetto di creazione di un sistema di calcolo distribuito (in java usando RMI) ho creato una classe Facade JobManager che si occupava della gestione del job, in particolare usando le classi con cui veniva inizializzato prendeva il job lo divideva in delle task più piccole (usando la strategia con cui era stato inizializzato), stabiliva la distrivuzione delle task sui vari worker (usando la strategia con cui era stato inizializzato) e infine delegava ad un'altra task l'esecuzione delle task (classe dedicata che eseguiva le chiamate RMI).