import mesa
import numpy as np
from data import probabilidades_por_distrito, district_wealth

class Apo_Agent(mesa.Agent):
    def __init__(self, unique_id, model, district):
        super().__init__(unique_id, model)
        self.home = None
        self.age = None
        self.district = district
        self.wealth = None 
        self.status = None
        self.gender = None

    def assign_income(self):
        district_income_data = district_wealth[self.district]
        income = district_income_data['Import_Euros'].tolist()
        income_probs = income / district_income_data['Import_Euros'].sum()
        prob = income_probs.tolist()
        self.wealth = np.random.choice(income, p=prob)

    def assign_age_and_status(self):
        probabilidades_edades = probabilidades_por_distrito[self.district]
        edades = list(probabilidades_edades.keys())
        probabilidades = list(probabilidades_edades.values())
        self.age = np.random.choice(edades, p=probabilidades)

        if self.age <= 16:
            self.status = "student"
        elif 16 < self.age <=22:
            self.status = np.random.choice(["student", "employed", "unemployed"])
        elif 22 < self.age <= 67:
            self.status = np.random.choice([ "employed", "unemployed"])
        else: self.status = ["retired"]

    def go_work(self):
        self.model.districts[self.district].place_agent(self, self.random.choice(self.model.districts[self.district].locations['work']))
    
    def go_leisure(self):
        self.model.districts[self.district].place_agent(self, self.random.choice(self.model.districts[self.district].locations['leisure']))

    def go_home(self):
        self.model.districts[self.district].place_agent(self, self.home)

    def go_school(self):
        self.model.districts[self.district].place_agent(self, self.random.choice(self.model.districts[self.district].locations['school']))
    
    def step(self):
        #print("Position of "+ str(self.unique_id) +" is " + str(self.pos))
        print(self.wealth)