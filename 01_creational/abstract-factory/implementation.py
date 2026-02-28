from abc import ABC, abstractmethod

# ==========================================
# 1. PRODUCT INTERFACES (A and B)
# ==========================================
# The fundamental difference from the Factory Method is this:
# we don't have ONE single product interface, but TWO (or more).
# Each product type represents a "dimension" of the family.
# All concrete ProductA speak the same language (operation()),
# and the same applies to all ProductB (collaborate()).

class ProductA(ABC):
    @abstractmethod
    def operation(self) -> str:
        """Main functionality of type A product."""
        pass

class ProductB(ABC):
    @abstractmethod
    def collaborate(self, a: ProductA) -> str:
        """
        Product B can interact with Product A of the same family.
        Note that the parameter is the abstract interface, not the concrete class:
        B doesn't know if it's collaborating with AX, AY, or AZ.
        """
        pass

# ==========================================
# 2. CONCRETE PRODUCTS — Family X
# ==========================================

class ProductAX(ProductA):
    def operation(self) -> str:
        return "Result from Product A of family X"

class ProductBX(ProductB):
    def collaborate(self, a: ProductA) -> str:
        # BX accepts the abstract interface, doesn't know if a is AX, AY, or AZ
        return f"Product B (X) collaborates with → {a.operation()}"

# ==========================================
# 3. CONCRETE PRODUCTS — Family Y
# ==========================================

class ProductAY(ProductA):
    def operation(self) -> str:
        return "Result from Product A of family Y"

class ProductBY(ProductB):
    def collaborate(self, a: ProductA) -> str:
        return f"Product B (Y) collaborates with → {a.operation()}"

# ==========================================
# 4. CONCRETE PRODUCTS — Family Z
# ==========================================

class ProductAZ(ProductA):
    def operation(self) -> str:
        return "Result from Product A of family Z"

class ProductBZ(ProductB):
    def collaborate(self, a: ProductA) -> str:
        return f"Product B (Z) collaborates with → {a.operation()}"

# ==========================================
# 5. THE ABSTRACT FACTORY
# ==========================================
# This is the real difference from the Factory Method:
# instead of a single factory_method(), here we declare ONE creation
# method FOR EACH product type in the family.
#
# Each concrete factory will therefore be responsible for creating
# an entire consistent family — not a single object.

class AbstractFactory(ABC):
    @abstractmethod
    def create_product_a(self) -> ProductA:
        pass

    @abstractmethod
    def create_product_b(self) -> ProductB:
        pass

# ==========================================
# 6. CONCRETE FACTORIES (one per family)
# ==========================================
# Each concrete factory implements BOTH creation methods
# and guarantees that the returned products belong to the same family.
# It's structurally impossible to get AX with BY from this factory.

class FactoryX(AbstractFactory):
    def create_product_a(self) -> ProductA:
        return ProductAX()

    def create_product_b(self) -> ProductB:
        return ProductBX()

class FactoryY(AbstractFactory):
    def create_product_a(self) -> ProductA:
        return ProductAY()

    def create_product_b(self) -> ProductB:
        return ProductBY()

class FactoryZ(AbstractFactory):
    def create_product_a(self) -> ProductA:
        return ProductAZ()

    def create_product_b(self) -> ProductB:
        return ProductBZ()

# ==========================================
# 7. CLIENT CODE
# ==========================================
# The client receives an AbstractFactory and works only with the abstract
# interfaces ProductA and ProductB. It never names AX, BY, or any
# concrete class: compatibility is guaranteed by the factory itself.

def client_code(factory: AbstractFactory):
    print("Client: I don't know which family was passed to me, but I know how to use it.")
    # We ask the factory for the entire family — always consistent
    a = factory.create_product_a()
    b = factory.create_product_b()

    print(f"  ProductA → {a.operation()}")
    print(f"  ProductB → {b.collaborate(a)}")

if __name__ == "__main__":
    print("--- Family X ---")
    client_code(FactoryX())

    print("\n--- Family Y ---")
    client_code(FactoryY())

    print("\n--- Family Z ---")
    client_code(FactoryZ())