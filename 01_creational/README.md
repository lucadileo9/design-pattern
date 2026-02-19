# Pattern Creazionali

Questi modelli affrontano il problema della creazione di oggetti. Quando la creazione diretta (tramite `new`) potrebbe portare a complessità o dipendenze indesiderate, i pattern creazionali offrono meccanismi flessibili per separare la creazione dalla responsabilità dell'oggetto stesso.

---

## 1. Singleton

**Intento**: garantire che una classe abbia una sola istanza e fornire un punto di accesso globale a essa.

**Utilizzo tipico**: gestione di risorse condivise (connessioni a database, logger, configurazioni globali).

Riferimento: [Spiegazione completa](./singleton/README.md)

---

## 2. Factory Method

**Intento**: definire un'interfaccia per creare un oggetto, delegando alle sottoclassi la decisione su quale classe specifica istanziare.

**Utilizzo tipico**: quando il sistema non può anticipare il tipo esatto di oggetti da creare o vuole delegare la responsabilità della creazione.

Riferimento: [Spiegazione completa](./factory/README.md)

---

## 3. Abstract Factory

**Intento**: fornire un'interfaccia per creare famiglie di oggetti correlati o dipendenti senza specificare le loro classi concrete.

**Utilizzo tipico**: creazione di interfacce utente multitema o sistemi che devono supportare diverse varianti di prodotti in modo coerente.

Riferimento: [Spiegazione completa](./abstract_factory/README.md)

---

## 4. Builder

**Intento**: separare la costruzione di un oggetto complesso dalla sua rappresentazione, permettendo processi di costruzione step-by-step.

**Utilizzo tipico**: creazione di oggetti con molti parametri opzionali o quando il processo di costruzione è complesso.

*Da completare...*

---

## 5. Prototype

**Intento**: creare nuovi oggetti clonando un prototipo esistente invece di crearne da zero.

**Utilizzo tipico**: quando la creazione di un nuovo oggetto è più costosa della clonazione, o quando si vuole evitare le sottoclassi.

*Da completare...*


## Casi reali in cui ho usato questi pattern:
**Singleton**: 
 - Ho fatto un'applicazione che interagiva tramite python con microsft teams, notion e un bot telegram. Ho usato un singleton per gestire l'avvio bot, siccome dovevo essere sicuro che quando le varie api chiamavano il bot, questo fosse già stato avviato, e sopratutto che non venisse avviato più di una volta e che si trattasse effettivamente sempre della stessa istanza.
