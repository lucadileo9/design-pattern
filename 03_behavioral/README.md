# Pattern Comportamentali

I pattern comportamentali si occupano della **comunicazione e della distribuzione delle responsabilità tra oggetti**: definiscono come gli oggetti interagiscono tra loro, come si scambiano informazioni e come vengono assegnati i compiti, rendendo il sistema più flessibile e disaccoppiato.

---

## 1. Observer

**Intento**: definire una dipendenza uno-a-molti tra oggetti, in modo che quando un oggetto cambia stato tutti i suoi dipendenti vengano notificati e aggiornati automaticamente.

**Utilizzo tipico**: sistemi event-driven, aggiornamento automatico di UI al cambio di dati, notifiche push — ogni volta che un cambiamento in un oggetto deve propagarsi ad altri senza che l'oggetto conosca i suoi dipendenti.

Riferimento: [Spiegazione completa](./observer/README.md)

---

## 2. Iterator

**Intento**: fornire un modo standard per accedere sequenzialmente agli elementi di una collezione senza esporne la struttura interna.

**Utilizzo tipico**: attraversamento di strutture dati complesse (alberi, grafi, liste di liste) in cui si vuole nascondere al client la logica di iterazione, supportando anche modalità di visita diverse (es. pre-ordine, post-ordine).

Riferimento: [Spiegazione completa](./iterator/README.md)

---

## 3. Strategy

**Intento**: definire una famiglia di algoritmi intercambiabili, incapsulare ciascuno in una classe dedicata e renderli sostituibili a runtime, senza modificare il contesto che li usa.

**Utilizzo tipico**: selezione a runtime dell'algoritmo più adatto (ordinamento, pagamento, compressione, routing) — quando si vuole aggiungere nuove varianti senza toccare il codice esistente (Open/Closed Principle).

Riferimento: [Spiegazione completa](./strategy/README.md)

---

## 4. Template Method

**Intento**: definire lo scheletro di un algoritmo in una classe astratta, delegando alle sottoclassi l'implementazione dei soli passi variabili, senza alterare la struttura generale.

**Utilizzo tipico**: pipeline con flusso fisso ma step intercambiabili (importazione dati, generazione report, processi ETL) — quando più varianti condividono la stessa sequenza di passaggi ma differiscono in alcuni di essi.

Riferimento: [Spiegazione completa](./template-method/README.md)

---

## 5. Command

**Intento**: incapsulare una richiesta come oggetto, parametrizzando i client con operazioni diverse e supportando operazioni annullabili (undo/redo).

**Utilizzo tipico**: code di operazioni, sistemi undo/redo, macro, job scheduler — quando si vuole disaccoppiare chi invoca un'operazione da chi la esegue.

*Da completare...*

---

## 6. Chain of Responsibility

**Intento**: passare una richiesta lungo una catena di handler, dove ciascuno decide di gestirla o di passarla al successivo.

**Utilizzo tipico**: middleware HTTP, validazione a strati, sistemi di approvazione gerarchica — quando più oggetti possono gestire una richiesta e il gestore corretto non è noto a priori.

*Da completare...*

---

## Casi reali in cui ho usato questi pattern:
**Strategy**:
 - In un progetto di creazione di un sistema di calcolo distribuito in cui avevo diversi algoritmi di splitting del lavoro e assegnazione del lavoro. Ho creato un'interfaccia SplittingStrategy e una di AssignmentStrategy, e poi diverse classi concrete per ogni algoritmo specifico. In questo modo il sistema era molto flessibile e potevo facilmente aggiungere nuovi algoritmi senza modificare il codice esistente. Tuttavia non ho usato una vera e propria classe Conetxt, ma ho trattato la classe JobManager che conteneva le due strategie come una classe contesto, delegando a essa l'esecuzione delle strategie.