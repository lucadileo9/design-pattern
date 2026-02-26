# Facade Pattern

## Problema

Ipotizziamo di trovarci in una situazione già di default abbastanza complessa, con la necessità di interagire con tante classi e oggetti diversi, ognuno con la propria interfaccia e modalità di utilizzo. Per eseguire una semplice operazione potremmo dover fare:

- operazione A su classe `X` (es. un login)
- operazione B su classe `X` (es. una richiesta di dati)
- operazione C su classe `Y` (es. un altro login)
- operazione D su classe `Y` (es. una richiesta di dati)
- operazione E: fondere i dati ottenuti da `X` e `Y`
- operazione F: passare i dati alla classe `Z` (es. un sistema di visualizzazione)

Gestire tutto questo lato client è scomodo, difficile da mantenere e da capire. Se volessimo cambiare una delle classi o aggiungere una nuova operazione, dovremmo modificare tutto il codice client, con un alto rischio di introdurre bug.

Un'analogia reale potrebbe essere quella dell'organizzzzione di una festa di laurea in un hotel, siccome per organizzare il tutto dovremmo:
- prenotare la sala con il responsabile dell'hotel
- prenotare il catering con il responsabile del catering
- prenotare la musica con il responsabile della musica
- prenotare i fiori con il responsabile dei fiori

Ovviamente è poco realizzabile, e nel caso in cui volessimo cambiare qualcosa (ad esempio il catering) dovremmo contattare innanzitutto il responsabile del catering, ma anche (ipoteticamente) il responsabile della sala e/o della musica, per assicurarci che tutto sia compatibile e che non ci siano problemi di coordinamento.

## Soluzione

La soluzione è introdurre un oggetto **Facade** che nasconda la complessità del sistema sottostante, fornendo un'interfaccia semplificata al client.

Nel nostro esempio, il **Facade** si occuperà di eseguire tutte le operazioni (A, B, C, D, E, F) in modo trasparente: il client chiama un'unica operazione (es. `execute()`) e il Facade gestisce tutto il resto. Se un'operazione interna cambia, si modifica solo il Facade — il codice client rimane invariato.

Nell'analogia della festa di laurea, il Facade è il **Wedding Planner**: noi gli diciamo cosa vogliamo, lui coordina sala, catering, musica e fiori. Se vogliamo cambiare il catering, lo diciamo solo a lui.

> **N.B.**: il Facade non introduce nuove funzionalità o comportamenti. La complessità del sistema sottostante non sparisce — viene semplicemente nascosta dietro un'interfaccia più semplice e gestibile.

**N.B.**: Una buona Facade non dovrebbe impedire l'accesso al sottosistema complesso. Se un "client esperto" avesse bisogno di un controllo granulare che la Facade non offre, dovrebbe comunque poter interagire direttamente con le classi originali (X, Y o Z). La Facade è una comodità, non una prigione

## Diagrammi

### Diagramma generico

```mermaid
classDiagram
    class Client {
        <<codice applicativo>>
    }
    class Facade {
        -subsystemA
        -subsystemB
        -subsystemC
        +operation()
    }
    class SubsystemA {
        +operationA1()
        +operationA2()
    }
    class SubsystemB {
        +operationB1()
        +operationB2()
        +operationB3()
    }
    class SubsystemC {
        +operationC1()
        +operationC2()
    }

    Client --> Facade : usa
    Facade *-- SubsystemA : crea e coordina
    Facade *-- SubsystemB : crea e coordina
    Facade *-- SubsystemC : crea e coordina

    note for Facade "Espone un metodo semplice.\nOrchestra internamente A → B → C.\nGestisce errori e rollback."
    note for Client "Conosce SOLO la Facade.\nNon sa che A, B, C esistono."
```

### Diagramma specifico

```mermaid
classDiagram
    class CheckoutFacade {
        -_catalog: CatalogService
        -_payment: PaymentService
        -_shipping: ShippingService
        -_notifications: NotificationService
        +complete_order(items, email, address, card) OrderResult
    }

    class CatalogService {
        -_stock: dict
        +check_availability(product_id, qty) bool
        +reserve_stock(product_id, qty)
        +release_stock(product_id, qty)
    }

    class PaymentService {
        +process_payment(card_number, amount) Optional~str~
    }

    class ShippingService {
        +create_shipment(address, n_items) str
    }

    class NotificationService {
        +send_confirmation(email, order_id, total, tracking)$
        +send_error(email, reason)$
    }

    class CartItem {
        <<dataclass>>
        +product_id: str
        +name: str
        +quantity: int
        +unit_price: float
        +subtotal: float
    }

    class OrderResult {
        <<dataclass>>
        +success: bool
        +order_id: Optional~str~
        +tracking_code: Optional~str~
        +total: float
        +message: str
    }

    CheckoutFacade *-- CatalogService
    CheckoutFacade *-- PaymentService
    CheckoutFacade *-- ShippingService
    CheckoutFacade *-- NotificationService

    CheckoutFacade ..> CartItem : riceve
    CheckoutFacade ..> OrderResult : restituisce
```

### Diagramma di sequenza

```mermaid
sequenceDiagram
    actor Client
    participant Facade as CheckoutFacade
    participant Catalog as CatalogService
    participant Payment as PaymentService
    participant Shipping as ShippingService
    participant Email as NotificationService

    Client ->>+ Facade: complete_order(items, email, address, card)

    Note over Facade: Passo 1 — Verifica disponibilità
    loop per ogni item nel carrello
        Facade ->> Catalog: check_availability(product_id, qty)
        Catalog -->> Facade: bool
    end

    Note over Facade: Passo 2 — Riserva stock
    loop per ogni item
        Facade ->> Catalog: reserve_stock(product_id, qty)
    end

    Note over Facade: Passo 3 — Pagamento
    Facade ->> Payment: process_payment(card, total)

    alt pagamento accettato
        Payment -->> Facade: transaction_id

        Note over Facade: Passo 4 — Spedizione
        Facade ->> Shipping: create_shipment(address, n_items)
        Shipping -->> Facade: tracking_code

        Note over Facade: Passo 5 — Conferma
        Facade ->> Email: send_confirmation(email, order_id, total, tracking)
        Facade ->>- Client: OrderResult(success=True)

    else pagamento rifiutato
        Payment -->> Facade: None
        Note over Facade: ↩ ROLLBACK
        loop per ogni item riservato
            Facade ->> Catalog: release_stock(product_id, qty)
        end
        Facade ->> Email: send_error(email, reason)
        Facade -->> Client: OrderResult(success=False)
    end
```
Come si può vedere, il client chiama un unico metodo `complete_order()`, tutta la complessità è nascosta all'interno del Facade, che si occupa di orchestrare le chiamate ai vari servizi e gestire errori e rollback in caso di problemi.

### Vantaggi

Il Facade è uno degli strumenti migliori per combattere il "codice a spaghetti":

- **Riduzione dell'accoppiamento**: il client non conosce le classi del sottosistema. Se si vuole sostituire la `Classe X` con una nuova versione o libreria, sarà necessario modificare solo il Facade — il client rimarrà intatto e ignaro del cambiamento.
- **Semplicità d'uso**: riduce drasticamente la curva di apprendimento. Invece di imparare 10 API diverse, gli sviluppatori devono conoscere solo i 2-3 metodi esposti dal Facade.
- **Migliore organizzazione a livelli**: nelle architetture moderne, il Facade funge da "punto di ingresso" per un intero modulo, definendo chiaramente cosa è pubblico e cosa è un dettaglio di implementazione privato.
- **Prevenzione di errori**: automatizzando l'ordine corretto delle chiamate (prima A, poi B, poi C), il Facade evita che il client dimentichi un passaggio critico (es. effettuare il login prima di richiedere i dati).


### Svantaggi

Se usato male, il Facade può introdurre problemi:

- **Rischio "God Object"**: se il sottosistema è enorme, il Facade rischia di diventare una classe gigantesca che fa troppe cose e "sa" troppo, violando il Single Responsibility Principle.
- **Barriera all'accesso (se mal progettato)**: un incapsulamento troppo rigido potrebbe impedire ai client avanzati di eseguire operazioni specifiche che il Facade non ha previsto.
- **Manutenzione del Facade stesso**: ogni volta che il sottosistema cambia in modo radicale, il Facade va aggiornato — diventa un ulteriore strato di codice da mantenere e testare.
- **Falsa sensazione di semplicità**: nascondere la complessità non significa eliminarla. Se il sottosistema è inefficiente, il Facade darà solo l'illusione che tutto funzioni bene, rendendo il debugging più difficile per chi non conosce i dettagli interni.