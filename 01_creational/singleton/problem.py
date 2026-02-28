# --- PROBLEMATIC CODE (WITHOUT SINGLETON) ---

class SharedFund:
    def __init__(self):
        self.money = 100  # Initial trip budget
        print("Opened a new shared fund!")

    def pay_ice_cream(self, amount):
        self.money -= amount
        print(f"Paid {amount}€. Remaining in this fund: {self.money}€")

# Student A wants to pay for ice cream
fund_student_a = SharedFund()
fund_student_a.pay_ice_cream(10)

# Student B wants to pay for ice cream
# PROBLEM: Student B creates a NEW fund instead of using the same one!
fund_student_b = SharedFund()
fund_student_b.pay_ice_cream(10)

print(f"Student A sees in fund: {fund_student_a.money}€")
print(f"Student B sees in fund: {fund_student_b.money}€")
# Result: The money was not deducted from the same source. We have an inconsistency.