# ==========================================
# CONCRETE PRODUCTS (X, Y, Z)
# ==========================================
# In this scenario there's often not even a formal common interface,
# which makes everything even more fragile.

class ProductX:
    def specific_operation_x(self):
        return "Result from Product X"

class ProductY:
    def different_operation_y(self):
        return "Result from Product Y"

class ProductZ:
    def operation_z(self):
        return "Result from Product Z"

# ==========================================
# THE PROBLEM: THE COUPLED CLIENT
# ==========================================
class ClientApplication:
    def execute_logic(self, product_type):
        print(f"Client: I'm trying to create a product of type {product_type}")
        
        # --- START OF THE DISASTER ---
        # The client must know all concrete classes.
        # If we add "ProductW", we must modify this file and this function.
        if product_type == "X":
            product = ProductX()
            result = product.specific_operation_x()
        elif product_type == "Y":
            product = ProductY()
            result = product.different_operation_y()
        elif product_type == "Z":
            product = ProductZ()
            result = product.operation_z()
        else:
            raise Exception("Unknown product type!")
        # --- END OF THE DISASTER ---

        print(f"Result obtained: {result}")

# ==========================================
# USAGE
# ==========================================
# As we can see there's too much logic in the execute_logic() section, despite
# having similar behaviors there's a lot of repeated code (DRY)
# Moreover, if we want to add a new product type, we must modify this function,
# which violates the Open/Closed principle.
if __name__ == "__main__":
    app = ClientApplication()
    
    # For each new product type, the client must be informed
    # and the code above must be changed.
    app.execute_logic("X")
    app.execute_logic("Y")
    app.execute_logic("Z")