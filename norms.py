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
