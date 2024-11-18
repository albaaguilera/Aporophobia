import mesa
import numpy as np
from data import probabilidades_por_distrito, district_wealth, needs_list, actions_dict, prob_homeless, district_rent, SAT_matrices
from data import probabilidades_por_distrito_gender
from typing import Dict, List
from copy import deepcopy
import random 

class Apo_Agent(mesa.Agent):
    needs: Dict[str, List[str]] #Diccionari needs principal definit, res del nested de dins.
    sat: Dict[str, List[List[float]]] #Diccionari sat matrices deppending on status

    def __init__(self, unique_id, model, district, needs: Dict[str, List[str]], sat:  Dict[str, List[List[float]]]): #
        super().__init__(unique_id, model)
        self.home = None
        self.age = None
        self.district = district
        self.wealth = 0 
        self.income = None
        self.depth = 0  
        self.status = None
        self.gender = None
        self.needs = deepcopy(needs)
        self.nsl = {}
        self.urg = {}
        self.sat = None
        self.max_score_idx = 0
        self.chosenaction = None
        self.last_actions = []

    def initialize_nsl(self):
        for category in self.needs:
            mean, variance = self.needs[category]['mean and var']
            nsl_values = np.random.normal(mean, np.sqrt(variance), len(self.needs[category]['needs']))
            nsl_values = np.clip(nsl_values, 0.6, 0.8)
            #nsl_values = np.minimum(np.clip(nsl_values, 0.6, 1.0), 1.0)  # Clip values to the desired range
            urg_values = 1 - nsl_values

            self.nsl[category] = nsl_values.tolist()
            self.urg[category] = urg_values.tolist()

    def decide_action(self):
        actions_list = actions_dict[self.status]
        reception_agents = self.model.districts[self.district].check_number_of_agents_reception()
        total_agents = len(self.model.schedule.agents)
        last_actions = self.last_actions[-3:]  # Get last 5 actions

        # Check if "invest_education" was chosen in the last 5 steps or less
        if "invest_education" in last_actions:
            actions_list = [action for action in actions_list if action != "invest_education"]
            actions_to_remove = ["invest_education"]
            indices_to_remove = [actions_list.index(action) for action in actions_to_remove if action in actions_list]
            sat_copy = deepcopy(self.sat)  # Create a copy of self.sat
            sat_copy = [[row[i] for i in range(len(row)) if i not in indices_to_remove] for row in sat_copy]
            scores = []        
            for action in actions_list:
                score = 0
                for category, category_data in self.needs.items():
                    weight = category_data['weight']
                    for need, urgency in zip(category_data['needs'], self.urg[category]):
                        j = actions_list.index(action)
                        i = needs_list.index(need)

                        score += sat_copy[i][j] * urgency * weight
                scores.append(score)

        #restriction on spending-money actions
        elif self.wealth <= 0:
            actions_to_remove = ["go_shopping", "go_grocery", "go_leisure", "invest_education"]
            indices_to_remove = [actions_list.index(action) for action in actions_to_remove if action in actions_list]
            #print(str(indices_to_remove) + str(self.status))
            actions_list = [action for action in actions_list if action not in actions_to_remove]
            sat_copy = deepcopy(self.sat)  # Create a copy of self.sat
            sat_copy = [[row[i] for i in range(len(row)) if i not in indices_to_remove] for row in sat_copy]
            #print("SAT Matrix2:")
            #for row in sat_copy:
                #print(row)
            scores = []        
            for action in actions_list:
                score = 0
                for category, category_data in self.needs.items():
                    weight = category_data['weight']
                    for need, urgency in zip(category_data['needs'], self.urg[category]):
                        j = actions_list.index(action)
                        i = needs_list.index(need)

                        score += sat_copy[i][j] * urgency * weight
                scores.append(score)
        
        #spatial restriction in the reception center
        elif reception_agents > total_agents // 10:
            indices_to_remove = [actions_list.index(action) for action in ["go_reception_center"] if action in actions_list]
            sat_copy = deepcopy(self.sat)  # Create a copy of self.sat
            sat_copy = [[row[i] for i in range(len(row)) if i not in indices_to_remove] for row in sat_copy]
            #print("SAT Matrix2:")
            #for row in sat_copy:
                #print(row)
            scores = []        
            for action in actions_list:
                score = 0
                for category, category_data in self.needs.items():
                    weight = category_data['weight']
                    for need, urgency in zip(category_data['needs'], self.urg[category]):
                        j = actions_list.index(action)
                        i = needs_list.index(need)

                        score += sat_copy[i][j] * urgency * weight
                scores.append(score)
        else:
            scores = []
            for action in actions_list:
                score = 0
                for category, category_data in self.needs.items():
                    weight = category_data['weight']
                    for need, urgency in zip(category_data['needs'], self.urg[category]):
                        j = actions_list.index(action)
                        i = needs_list.index(need)

                        score += self.sat[i][j] * urgency * weight
                scores.append(score)

        self.max_score_idx = scores.index(max(scores))
        max_score_action = actions_list[self.max_score_idx]

        self.last_actions.append(max_score_action)

        return max_score_action
    
    def update_nsl_and_urg(self):
        for category in self.needs:
            decay = self.needs[category]['decaying'][self.status]
            for i in range(len(self.nsl[category])):
                #print("NEED " + str(self.nsl[category][i]) + " DECAY = " +str(decay[i]))
                self.nsl[category][i] = self.nsl[category][i] * decay[i] 
                self.urg[category][i] = 1 - self.nsl[category][i]
    
        #update nsl values with the corresponding proportion of the SAT column of the action (with maximum value 1)
        for category, category_data in self.needs.items():
            for i, need in enumerate(category_data['needs']):
                j = self.max_score_idx
                leisure_agents = self.model.districts[self.district].check_number_of_agents_leisure()  # Get agents at the leisure position
                if leisure_agents < 2:
                    # Set the sat values to 0 for family and friendship needs in the and go_leisure column
                    self.sat[8][actions_dict[self.status].index("go_leisure")] = 0.0
                    self.sat[9][actions_dict[self.status].index("go_leisure")] = 0.0
                    #print("SAT" + str(self.sat[3][actions_dict[self.status].index("go_hospital")]))
                self.nsl[category][i] = min(self.nsl[category][i] + 0.7* self.sat[i][j], 1.0000)


    def assign_income(self):
        district_income_data = district_wealth[self.district]
        income = district_income_data['Import_Euros'].tolist()
        income_probs = income / district_income_data['Import_Euros'].sum()
        prob = income_probs.tolist()
        self.income = np.random.choice(income, p=prob)
        self.wealth = self.income
    
    def assign_rent(self):
        district_rent_data = district_rent[self.district]
        rent = district_rent_data['Preu'].tolist()
        rent_probs = rent / district_rent_data['Preu'].sum()
        prob = rent_probs.tolist()
        rent_sample = np.random.choice(rent, p=rent_probs)
        return rent_sample

    def assign_age_and_status(self):
        probabilidades_edades = probabilidades_por_distrito[self.district]
        self.age = np.random.choice(list(probabilidades_edades.keys()), p=list(probabilidades_edades.values()))
        if self.age <= 16:
            self.status = "student"
        elif 16 < self.age <=22:
            self.status = np.random.choice(["student", "employed", "unemployed"], p=[0.3, 0.4, 0.3]) #un 30% de prob d'estar en atur
        elif 22 < self.age <= 67:
            self.status = np.random.choice([ "employed", "unemployed"], p=[0.7, 0.3]) #POSAR PROBABILITATS AQUÍ!0.7 0.3
        else: self.status = "retired"
    
    def assign_homeless(self):
        """if self.status == 'unemployed' and self.gender == 'man': #need to fix, some probability of having a homeless woman 10%
            prob = prob_homeless[self.district]
            #self.status = np.random.choice(["homeless", "unemployed"], p= [prob, 1-prob]) #arreglar probabilitat
            self.status = np.random.choice(["homeless", "unemployed"], p= [0.5, 0.5]) # For the cluster submission
            self.age = int(np.random.normal(44, 5))"""
        prob = prob_homeless[self.district]
        if random.random() <= prob:
            self.status = "homeless"
            self.age = int(np.random.normal(44, 5))
            self.gender = 'man' 

    def assign_gender(self):
        probabilidades_genero = probabilidades_por_distrito_gender[self.district]
        genero_seleccionado = np.random.choice(list(probabilidades_genero.keys()), p=list(probabilidades_genero.values()))
        if genero_seleccionado == 'Dona':
            self.gender = "woman"
        elif genero_seleccionado == 'Home':
            self.gender = "man"
        
    def go_work(self):
        self.model.districts[self.district].place_agent(self, self.random.choice(self.model.districts[self.district].locations['work']))
    
    def go_leisure(self):
        self.model.districts[self.district].place_agent(self, self.random.choice(self.model.districts[self.district].locations['leisure']))
        if self.status != ["homeless", "student"]:
            self.wealth -= 4
        elif self.status == "student":
            if random.random() < 0.05:
                self.wealth -= 0.5

    def go_home(self):
        self.model.districts[self.district].place_agent(self, self.home)

    def go_study(self):
        self.model.districts[self.district].place_agent(self, self.random.choice(self.model.districts[self.district].locations['school']))

    def go_grocery(self):
        self.model.districts[self.district].place_agent(self, self.random.choice(self.model.districts[self.district].locations['grocery']))
        if self.status == "student":
            if random.random() < 0.2:
                self.wealth -= 2
        else: self.wealth -= 5

    def go_hospital(self):
        self.model.districts[self.district].place_agent(self, self.random.choice(self.model.districts[self.district].locations['hospital']))

    def go_shopping(self):
        self.model.districts[self.district].place_agent(self, self.random.choice(self.model.districts[self.district].locations['shopping']))
        self.wealth -= 10 

    #DEFINIR LA RESTA D'ACCIONS
    def steal_food(self):
        self.model.districts[self.district].place_agent(self, self.random.choice(self.model.districts[self.district].locations['grocery']))
        # afegir component random que posi l'agent a la presó
    
    def steal_clothes(self):
        self.model.districts[self.district].place_agent(self, self.random.choice(self.model.districts[self.district].locations['shopping']))

    def go_reception_center(self):
        self.model.districts[self.district].place_agent(self, self.random.choice(self.model.districts[self.district].locations['reception center']))

    def sleep_street(self):
        #self.model.districts[self.district].place_agent(self, self.model.districts[self.district].generate_tuples(2, (0,9), (0,9)))
        self.model.districts[self.district].place_agent(self, (1, 1))
    
    def invest_education(self):
        self.wealth -= 50
        if self.status == "unemployed":
            if random.random() < 0.2:  # Adjust the probability as desired
                self.status = "employed"
                self.sat = SAT_matrices[self.status]

    def beg(self):
        if random.random() < 0.5:
            self.wealth += 2
    
    def go_prison(self):
        self.model.districts[self.district].place_agent(self, self.random.choice(self.model.districts[self.district].locations['prison']))
        for i in range(1,3,1):
                        self.nsl['belonging'][i] = 0.0 
                        self.nsl['esteem'][i] = 0.0
        
        #self.depth += 500

    #STEP
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

        if 8 <= time < 17: 
            self.update_nsl_and_urg()
            getattr(self, self.decide_action())() 
            self.chosenaction = self.decide_action()
            #print("NSL " + str(self.nsl["physiological"]) + " decides " + str(self.chosenaction))
            #print("NSL " + str(self.nsl["physiological"][3]))
            #print(" At time " + str(time + 8) + " the agent " + str(self.status) + " and district " + str(self.district) + " decides " + str((self.chosenaction))+ " to the position " + str(self.pos) + " with nsl " + str(self.nsl))
        
        # Personalized sleep nsl
        if 17 <= time <= 23:
            self.nsl['physiological'][2] = min(np.clip(np.random.normal(0.95, np.sqrt(0.1)), 0.9, 1.0), 1.0)

        # Turn wealth strictly positive by creating depth
        if self.model.schedule.time != 0: 
            if self.wealth < 0:   #and self.status != "homeless": 
                self.depth += abs(self.wealth)
                self.wealth = 0 

        # Eviction for depth
        if self.depth >= 3000:
            self.status = "homeless"
            self.sat = SAT_matrices[self.status]
            self.home = None
