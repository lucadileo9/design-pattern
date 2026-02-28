# ==========================================
# THE PROBLEM THAT THE ABSTRACT FACTORY SOLVES
# ==========================================
# The Factory Method handled ONE single type of product.
# Now imagine having TWO types of related products: A and B.
# As in the Factory Method we use X, Y, Z — but now they're not single products,
# they're FAMILIES: each family has its own variant of A and B,
# and variants of the same family MUST be used together.
#
#   Family X:  ProductAX  +  ProductBX   ✅ compatible
#   Family Y:  ProductAY  +  ProductBY   ✅ compatible
#   ProductAX  +  ProductBY              ❌ incompatible!
#
# Without Abstract Factory, it's the CLIENT that must manually manage
# this compatibility — with all the risks that entails.

# ==========================================
# CONCRETE PRODUCTS — type A (one per family)
# ==========================================
# Not even a common interface: each class exposes its own method
# with a different name, making interchangeability impossible.

class ProductAX:
    def specific_operation_ax(self) -> str:
        return "Result from Product A of family X"

class ProductAY:
    def specific_operation_ay(self) -> str:
        return "Result from Product A of family Y"

class ProductAZ:
    def specific_operation_az(self) -> str:
        return "Result from Product A of family Z"

# ==========================================
# CONCRETE PRODUCTS — type B (one per family)
# ==========================================

class ProductBX:
    def behavior_bx(self) -> str:
        return "Result from Product B of family X"

class ProductBY:
    def behavior_by(self) -> str:
        return "Result from Product B of family Y"

class ProductBZ:
    def behavior_bz(self) -> str:
        return "Result from Product B of family Z"

# ==========================================
# THE PROBLEM: THE CLIENT THAT MANAGES EVERYTHING
# ==========================================
class ClientApplication:
    def execute_logic(self, family: str):
        print(f"Client: building products for family '{family}'")

        # PROBLEM 1: the client knows ALL concrete classes of both types.
        # PROBLEM 2: it must remember which variants are compatible with each other.
        #             If it gets it wrong (e.g. AX with BY), nobody warns — silent bug.
        # PROBLEM 3: adding family W means modifying this block.
        if family == "X":
            a = ProductAX()
            b = ProductBX()
            result_a = a.specific_operation_ax()   # different method name!
            result_b = b.behavior_bx()              # different method name!
        elif family == "Y":
            a = ProductAY()
            b = ProductBY()
            result_a = a.specific_operation_ay()
            result_b = b.behavior_by()
        elif family == "Z":
            a = ProductAZ()
            b = ProductBZ()
            result_a = a.specific_operation_az()
            result_b = b.behavior_bz()
        else:
            raise ValueError(f"Family '{family}' unknown!")

        print(f"  → {result_a}")
        print(f"  → {result_b}")

# ==========================================
# USAGE
# ==========================================
# Visible problems:
#  • The client depends on 6 concrete classes (AX, AY, AZ, BX, BY, BZ).
#  • Compatibility between A and B is guaranteed ONLY by the programmer's discipline.
#  • Adding family W requires touching this file.
if __name__ == "__main__":
    app = ClientApplication()
    app.execute_logic("X")
    app.execute_logic("Y")
    app.execute_logic("Z")

    # Nothing prevents making this mistake — the code runs just the same:
    # a = ProductAX()
    # b = ProductBY()   ← wrong family! silent bug.