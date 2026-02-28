from abc import ABC, abstractmethod

# ==========================================
# 1. PRODUCT DEFINITION (INTERFACE)
# ==========================================
# As we've seen, the purpose of this class is to define the common interface
# for all products the factory can create. This interface will then be used
# by the client to interact with products without knowing their concrete class.
class Product(ABC):
    @abstractmethod
    def operation(self) -> str:
        """Every product must be able to perform an operation."""
        pass

# ==========================================
# 2. CONCRETE PRODUCTS (X, Y, Z)
# ==========================================
# These classes provide different implementations of the operation() method.

class ProductX(Product):
    def operation(self) -> str:
        return "Result from Product X"

class ProductY(Product):
    def operation(self) -> str:
        return "Result from Product Y"

class ProductZ(Product):
    def operation(self) -> str:
        return "Result from Product Z"

# ==========================================
# 3. THE CREATOR (THE ABSTRACT FACTORY)
# ==========================================
# This is the abstract factory that declares the factory method, which must be implemented
# by the concrete subclasses. The creator may also contain business logic that depends on
# the created products, but it doesn't know the concrete class of the products.
class Creator(ABC):
    @abstractmethod
    def factory_method(self) -> Product:
        """Subclasses will implement this method to create objects."""
        pass

    def execute_business_logic(self):
        """
        Note: The creator's primary responsibility is not just to create products,
        but it often contains business logic that depends on them.
        """
        # We call the factory method to create a Product object.
        product = self.factory_method()
        
        # Now we use the product without knowing exactly which class it is.
        result = product.operation()
        print(f"Creator: I worked with the product and got: {result}")

# ==========================================
# 4. CONCRETE CREATORS
# ==========================================
# Each subclass decides which product to instantiate.
# Note: the point is that the Client will use an abstract factory, instantiate a concrete
# subclass, and call the execute_business_logic() method without knowing which concrete
# product was created. As we can see, the client doesn't care about what happens behind
# the scenes, only about the final result.
# In reality, behind the scenes what happened is that the client executed the function,
# which in turn called the factory method, which created a concrete product (depending on
# which concrete factory was instantiated), then that product executed its operation, and
# here too the operation method was called without knowing which concrete product it was,
# and finally the result was printed.

class CreatorX(Creator):
    def factory_method(self) -> Product:
        return ProductX()

class CreatorY(Creator):
    def factory_method(self) -> Product:
        return ProductY()

class CreatorZ(Creator):
    def factory_method(self) -> Product:
        return ProductZ()

# ==========================================
# 5. CLIENT CODE
# ==========================================
# The client works with creators through their base interface.

def client_code(creator: Creator):
    print("Client: I don't know who created the product for me, but I know how to use it.")
    creator.execute_business_logic()

if __name__ == "__main__":
    # To run this example:
    # python example.py
    print("--- Starting with Creator X ---")
    client_code(CreatorX())
    
    print("\n--- Starting with Creator Y ---")
    client_code(CreatorY())
    
    print("\n--- Starting with Creator Z ---")
    client_code(CreatorZ())