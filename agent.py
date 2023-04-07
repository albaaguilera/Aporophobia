import mesa
import numpy as np
from data import probabilidades_por_distrito, district_wealth, actions_list, needs_list
from typing import Collection, Dict, List, Tuple
import math 

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
        self.needs = needs
        self.nsl = {category: [self.needs[category]['initial']] * len(self.needs[category]['needs']) for category in self.needs}
        self.urg = {category: [1-self.needs[category]['initial']] * len(self.needs[category]['needs']) for category in self.needs}
        self.sat = sat

    def update_nsl_and_urg(self):
        for category in self.needs:
            decay = self.needs[category]['decaying']
            for i in range(len(self.nsl[category])):
                self.nsl[category][i] *= decay[i]
                #print(self.nsl)
                self.urg[category][i] = 1 - self.nsl[category][i]
    
    def decide_action(self):
        scores = []
        for action in actions_list:
            score = 0
            for category, category_data in self.needs.items():
                weight = category_data['weight']
                for need, urgency in zip(category_data['needs'], self.urg[category]):
                    i =  actions_list.index(action)
                    j =  needs_list.index(need)
                    #cambios lele
                    #for status in ['retired', 'employed', 'unemployed', 'student']:
                        #sat_matrix = self.sat[status]

                    #sat = sat_matrix[j][i]
                    sat = self.sat[j][i]
                    score += sat * urgency * weight
            scores.append(score)

        max_score_idx = scores.index(max(scores))
        max_score_action = actions_list[max_score_idx]

        #update nsl values with the corresponding proportion of the SAT column of the action (with maximum value 1)
        for category, category_data in self.needs.items():
            for i, need in enumerate(category_data['needs']):
                j = max_score_idx
                self.nsl[category][i] = min(self.nsl[category][i] + 0.2* self.sat[i][j], 1.0000)
                #self.nsl[category][i] += 0.2* self.sat[i][j] #sense límit a 1

        return max_score_action

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
            self.status = np.random.choice(["student", "employed", "unemployed"], p=[0.4, 0.3, 0.3]) #un 30% de prob d'estar en atur
        elif 22 < self.age <= 67:
            self.status = np.random.choice([ "employed", "unemployed"])
        else: self.status = "retired"

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

    def step(self):
        #print(self.needs['physiological']['weight'])

        time = self.model.schedule.time % 24

        #Segons el temps i l'status, manipulo els nsl values 
        #if 0 <= time < 8: 
        #    if self.status == ''

        #Every step we update the nsl and urg scores

        #self.get_scores()
        #print(self.get_scores())
        #Decide action with the highest score and Update nsl values related with that action with SAT.

        if 8 <= time < 15: 
            self.update_nsl_and_urg()
            getattr(self, self.decide_action())() 
            chosenaction = self.decide_action()
            #print(chosenaction)
            #getattr(self, chosen_action)()   # és com fer agent.chosenaction
            print(" At time " + str(time + 8) + " the agent " + str(self.status) + " decides " + str((chosenaction))+ " to the position " + str(self.pos) + " with nsl " + str(self.nsl))

        #print(self.nsl)
        #print(self.urg)
        #print(self.sat)