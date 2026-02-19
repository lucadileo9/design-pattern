from abc import ABC, abstractmethod

# ==========================================
# 1. INTERFACCE DEI PRODOTTI (A e B)
# ==========================================
# La differenza fondamentale rispetto al Factory Method è questa:
# non abbiamo UN'unica interfaccia di prodotto, ma DUE (o più).
# Ogni tipo di prodotto rappresenta una "dimensione" della famiglia.
# Tutti i ProdottoA concreti parlano la stessa lingua (operazione()),
# e lo stesso vale per tutti i ProdottoB (collabora()).

class ProdottoA(ABC):
    @abstractmethod
    def operazione(self) -> str:
        """Funzionalità principale del prodotto di tipo A."""
        pass

class ProdottoB(ABC):
    @abstractmethod
    def collabora(self, a: ProdottoA) -> str:
        """
        Il prodotto B può interagire con il prodotto A della stessa famiglia.
        Notare che il parametro è l'interfaccia astratta, non la classe concreta:
        B non sa se sta collaborando con AX, AY o AZ.
        """
        pass

# ==========================================
# 2. PRODOTTI CONCRETI — Famiglia X
# ==========================================

class ProdottoAX(ProdottoA):
    def operazione(self) -> str:
        return "Risultato del Prodotto A della famiglia X"

class ProdottoBX(ProdottoB):
    def collabora(self, a: ProdottoA) -> str:
        # BX accetta l'interfaccia astratta, non sa se a è AX, AY o AZ
        return f"Prodotto B (X) collabora con → {a.operazione()}"

# ==========================================
# 3. PRODOTTI CONCRETI — Famiglia Y
# ==========================================

class ProdottoAY(ProdottoA):
    def operazione(self) -> str:
        return "Risultato del Prodotto A della famiglia Y"

class ProdottoBY(ProdottoB):
    def collabora(self, a: ProdottoA) -> str:
        return f"Prodotto B (Y) collabora con → {a.operazione()}"

# ==========================================
# 4. PRODOTTI CONCRETI — Famiglia Z
# ==========================================

class ProdottoAZ(ProdottoA):
    def operazione(self) -> str:
        return "Risultato del Prodotto A della famiglia Z"

class ProdottoBZ(ProdottoB):
    def collabora(self, a: ProdottoA) -> str:
        return f"Prodotto B (Z) collabora con → {a.operazione()}"

# ==========================================
# 5. LA ABSTRACT FACTORY
# ==========================================
# Questa è la vera differenza rispetto al Factory Method:
# invece di un solo factory_method(), qui dichiariamo UN metodo
# di creazione PER OGNI tipo di prodotto della famiglia.
#
# Ogni factory concreta sarà quindi responsabile di creare
# un'intera famiglia coerente — non un singolo oggetto.

class AbstractFactory(ABC):
    @abstractmethod
    def create_prodotto_a(self) -> ProdottoA:
        pass

    @abstractmethod
    def create_prodotto_b(self) -> ProdottoB:
        pass

# ==========================================
# 6. FACTORY CONCRETE (una per famiglia)
# ==========================================
# Ogni factory concreta implementa ENTRAMBI i metodi di creazione
# e garantisce che i prodotti restituiti appartengano alla stessa famiglia.
# È strutturalmente impossibile ottenere AX con BY da questa factory.

class FactoryX(AbstractFactory):
    def create_prodotto_a(self) -> ProdottoA:
        return ProdottoAX()

    def create_prodotto_b(self) -> ProdottoB:
        return ProdottoBX()

class FactoryY(AbstractFactory):
    def create_prodotto_a(self) -> ProdottoA:
        return ProdottoAY()

    def create_prodotto_b(self) -> ProdottoB:
        return ProdottoBY()

class FactoryZ(AbstractFactory):
    def create_prodotto_a(self) -> ProdottoA:
        return ProdottoAZ()

    def create_prodotto_b(self) -> ProdottoB:
        return ProdottoBZ()

# ==========================================
# 7. CODICE CLIENT
# ==========================================
# Il client riceve una AbstractFactory e lavora solo con le interfacce
# astratte ProdottoA e ProdottoB. Non nomina mai AX, BY o qualsiasi
# classe concreta: la compatibilità è garantita dalla factory stessa.

def codice_client(factory: AbstractFactory):
    print("Client: Non so quale famiglia mi è stata passata, ma so come usarla.")
    # Chiediamo alla factory l'intera famiglia — sempre coerente
    a = factory.create_prodotto_a()
    b = factory.create_prodotto_b()

    print(f"  ProdottoA → {a.operazione()}")
    print(f"  ProdottoB → {b.collabora(a)}")

if __name__ == "__main__":
    print("--- Famiglia X ---")
    codice_client(FactoryX())

    print("\n--- Famiglia Y ---")
    codice_client(FactoryY())

    print("\n--- Famiglia Z ---")
    codice_client(FactoryZ())