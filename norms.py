# # Regulative environment
# class Norm:
#     def __init__(self, attribute, deontic, aim, condition=None, or_else=None):
#         self.attribute = attribute
#         self.deontic = deontic
#         self.aim = aim
#         self.condition = condition
#         self.or_else = or_else
#         #self.apo = None #indicador Yes or No

#     def __str__(self):
#         norm_str = f"{self.attribute} {self.deontic} {self.aim} {self.condition} "
#         if self.or_else:
#             norm_str += f", then {self.or_else}"
#         return norm_str

# # Example norms
# norm_homeless = Norm("Anyone", "can", "enter the social emergency program", "if they have lost their home")
# norm_min_income = Norm("Anyone with home address and residency in Spain and a bank account", "can", "apply for minimal vital income")

#print(norm_homeless.condition)

from typing import List

# IMPORTANT do not name any other variable as agx
agx = None

class Norm:

    def __init__(self, precondition: str, postcondition: List[str]) -> None:
        self.precondition = precondition
        self.postcondition = postcondition

    def check_precondition(self, ag) -> bool:
        agx = ag
        precondition_holds = eval(self.precondition)
        agx = None
        return precondition_holds
    
    def apply_postcondition(self, ag):
        agx = ag
        for statement in self.postcondition:
            exec(statement)
        agx = None

    def __str__(self) -> str:
        return f"if {self.precondition} then {', '.join(self.postcondition)}"




if __name__ == '__main__':

    # example norm: if an agent's income is less that 50 units, the agent
    # receives 10 units of income
    norm = Norm("agx.income < 50", ["agx.income += 10"])
    print(norm)


    # very stupid agent class that only has income variable
    # only for example purposes
    class DummyAgent:
        def __init__(self, income):
            self.income= income


    alice = DummyAgent(60)
    norm_applies_to_alice = norm.check_precondition(alice)
    print(f"Does the norm apply to alice? {norm_applies_to_alice}\n")

    bob = DummyAgent(40)
    norm_applies_to_bob = norm.check_precondition(bob)
    print(f"Does the norm apply to bob? {norm_applies_to_bob}\n")
    print("Since the norm applies to bob, we are now going to apply the postcondition of the norm to bob.")
    norm.apply_postcondition(bob)
    print(f"Bob's income now is {bob.income}")
