# --- SOLUTION WITH SINGLETON ---

class SharedFundSingleton:
    _instance = None  # Static field to store the unique instance

    def __new__(cls):
        # If the instance doesn't exist yet, we create it
        if cls._instance is None:
            print("\n--- Creation of the ONLY shared fund for the entire trip ---")
            cls._instance = super(SharedFundSingleton, cls).__new__(cls)
            cls._instance.money = 100  # One-time initialization
        return cls._instance  # We always return the same instance

    def pay_ice_cream(self, amount):
        self.money -= amount
        print(f"Paid {amount}€. Remaining shared fund: {self.money}€")

# Student A tries to create the fund
fund_a = SharedFundSingleton()
fund_a.pay_ice_cream(10)

# Student B tries to create the fund
# They won't receive a new object, but the one created by student A!
fund_b = SharedFundSingleton()
fund_b.pay_ice_cream(10)

print(f"Object identity A: {id(fund_a)}")
print(f"Object identity B: {id(fund_b)}")
print(f"Both see the correct balance: {fund_a.money}€")
# Now the balance is 80€ because both drew from the same source!