# Regulative environment
class Norm:
    def __init__(self, attribute, deontic, aim, condition=None, or_else=None):
        self.attribute = attribute
        self.deontic = deontic
        self.aim = aim
        self.condition = condition
        self.or_else = or_else
        #self.apo = None #indicador Yes or No

    def __str__(self):
        norm_str = f"{self.attribute} {self.deontic} {self.aim} {self.condition} "
        if self.or_else:
            norm_str += f", then {self.or_else}"
        return norm_str

# Example norms
norm_homeless = Norm("Anyone", "can", "enter the social emergency program", "if they have lost their home")
norm_min_income = Norm("Anyone with home address and residency in Spain and a bank account", "can", "apply for minimal vital income")

#print(norm_homeless.condition)