import mesa
import numpy as np
from data import probabilidades_por_distrito, district_wealth, needs_list, actions_dict, prob_homeless
from data import probabilidades_por_distrito_gender
from typing import Dict, List
from copy import deepcopy
# from norms import norm_homeless

class Apo_Agent(mesa.Agent):
    needs: Dict[str, List[str]] #Diccionari needs principal definit, res del nested de dins.
    sat: Dict[str, List[List[float]]] #Diccionari sat matrices deppending on status

    def __init__(self, unique_id, model, district, needs: Dict[str, List[str]], sat:  Dict[str, List[List[float]]]): #
        super().__init__(unique_id, model)
        self.home = None
        self.age = None
        self.district = district
        self.wealth = None 
        self.status = None
        self.gender = None
        self.needs = deepcopy(needs)
        self.nsl = {category: [self.needs[category]['initial']] * len(self.needs[category]['needs']) for category in self.needs}
        self.urg = {category: [1-self.needs[category]['initial']] * len(self.needs[category]['needs']) for category in self.needs}
        self.sat = None
        self.max_score_idx = 0
        # self.norms = norm_homeless #[norm_homeless, norm_min_income]

    def decide_action(self):
        scores = []
        actions_list = actions_dict[self.status]  # Access actions from the actions_dict based on status
        for action in actions_list:
            score = 0
            for category, category_data in self.needs.items():
                weight = category_data['weight']
                for need, urgency in zip(category_data['needs'], self.urg[category]):
                    i = actions_list.index(action)
                    j = needs_list.index(need)
                    sat = self.sat[j][i]  
                    score += sat * urgency * weight
            scores.append(score)

        self.max_score_idx = scores.index(max(scores))
        max_score_action = actions_list[self.max_score_idx]

        return max_score_action
    
    def update_nsl_and_urg(self):
        for category in self.needs:
            decay = self.needs[category]['decaying']
            for i in range(len(self.nsl[category])):
                self.nsl[category][i] *= decay[i]
                #print(self.nsl)
                self.urg[category][i] = 1 - self.nsl[category][i]
    
        #update nsl values with the corresponding proportion of the SAT column of the action (with maximum value 1)
        for category, category_data in self.needs.items():
            for i, need in enumerate(category_data['needs']):
                j = self.max_score_idx
                self.nsl[category][i] = min(self.nsl[category][i] + 0.2* self.sat[i][j], 1.0000)
                #self.nsl[category][i] += 0.2* self.sat[i][j] #sense límit a 1

    def assign_income(self):
        district_income_data = district_wealth[self.district]
        income = district_income_data['Import_Euros'].tolist()
        income_probs = income / district_income_data['Import_Euros'].sum()
        prob = income_probs.tolist()
        self.wealth = np.random.choice(income, p=prob)

    def assign_age_and_status(self):
        probabilidades_edades = probabilidades_por_distrito[self.district]
        self.age = np.random.choice(list(probabilidades_edades.keys()), p=list(probabilidades_edades.values()))
        if self.age <= 16:
            self.status = "student"
        elif 16 < self.age <=22:
            self.status = np.random.choice(["student", "employed", "unemployed"], p=[0.4, 0.3, 0.3]) #un 30% de prob d'estar en atur
        elif 22 < self.age <= 67:
            self.status = np.random.choice([ "employed", "unemployed"]) #POSAR PROBABILITATS AQUÍ!
        else: self.status = "retired"
    
    def assign_homeless(self):
        if self.status == 'unemployed' and self.gender == 'man': #need to fix, some probability of having a homeless woman 10%
            prob = prob_homeless[self.district]
            self.status = np.random.choice(["homeless", "unemployed"], p= [prob, 1-prob])
            self.age = int(np.random.normal(44, 5))

    def assign_gender(self):
        probabilidades_genero = probabilidades_por_distrito_gender[self.district]
        genero_seleccionado = np.random.choice(list(probabilidades_genero.keys()), p=list(probabilidades_genero.values()))
        if genero_seleccionado == 'Dones':
            self.gender = "woman"
        elif genero_seleccionado == 'Homes':
            self.gender = "man"
        
    def go_work(self):
        self.model.districts[self.district].place_agent(self, self.random.choice(self.model.districts[self.district].locations['work']))
    
    def go_leisure(self):
        self.model.districts[self.district].place_agent(self, self.random.choice(self.model.districts[self.district].locations['leisure']))

    def go_home(self):
        self.model.districts[self.district].place_agent(self, self.home)

    def go_school(self):
        self.model.districts[self.district].place_agent(self, self.random.choice(self.model.districts[self.district].locations['school']))

    def go_grocery(self):
        self.model.districts[self.district].place_agent(self, self.random.choice(self.model.districts[self.district].locations['grocery']))

    def go_hospital(self):
        self.model.districts[self.district].place_agent(self, self.random.choice(self.model.districts[self.district].locations['hospital']))

    def go_shopping(self):
        self.model.districts[self.district].place_agent(self, self.random.choice(self.model.districts[self.district].locations['shopping']))

    def step(self):
        #print(self.needs['physiological']['weight'])
        time = self.model.schedule.time % 24

        # Norms implementation
        for norm in self.model.norms:
            # check that the norm applies to the agent
            norm_applies = norm.check_precondition(self)
            # if the norm applies, apply post-condition
            if norm_applies:
                norm.apply_postcondition(self)

        #print(self.norms.aim)
        """
        for norm in self.norms:
            if self.status == "Employed": #if norm.condition():  #Should be if norm.condition() but condition should be written in a boolean way with the model parameters
                if norm.deontic == "must":
                    print("Mandatory action " + str(norm.aim()))
                elif norm.deontic == "can":
                    #agent.actions_dict[agent.status].append(norm.aim)
                    print(self.actions_dict[self.status])
                else: pass
                    #elif norm.deontic == "must not":
                        #agent.unavailable_actions.append(norm.aim)
        """
        if 8 <= time < 15: 
            self.update_nsl_and_urg()
            getattr(self, self.decide_action())() 
            chosenaction = self.decide_action()
            print(" At time " + str(time + 8) + " the agent " + str(self.status) + " decides " + str((chosenaction))+ " to the position " + str(self.pos) + " with nsl " + str(self.nsl))

        #print(self.nsl)
        #print(self.urg)
        #print(self.sat)