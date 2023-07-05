import mesa 
from city import DistrictGrid, gracia, sarria_stgervasi, eixample, les_corts
from typing import Collection, Dict
from agent import Apo_Agent
from data import assign_district, SAT_matrices, needs, all_norms
from norms import Norm
import numpy as np
import random 

N = 5
T = 3000

class CityModel(mesa.Model):
    name: str
    districts: Dict[str, DistrictGrid]
    
    def __init__(self, name: str, districts: Collection[DistrictGrid], N, norms: Collection[Norm] = []) -> None:
        self.num_agents = N
        self.name = name
        self.districts = {dist.name: dist for dist in districts}
        self.schedule = mesa.time.RandomActivation(self)
        self.norms = norms 

        statuses = ["retired", "homeless", "student", "unemployed", "employed"]
        ages = [72, 43, 18, 37, 53]
        for i in range(self.num_agents):
            ag = Apo_Agent(i, self, district = assign_district(), needs = needs, sat = SAT_matrices) 
            ag.initialize_nsl()
            ag.assign_gender()
            ag.assign_age_and_status()
            ag.assign_homeless()
            #TRIAL
            ag.age = ages[i % len(ages)]
            ag.status = statuses[i % len(statuses)]

            ag.sat = SAT_matrices[ag.status] 
            if ag.status != ["homeless"]: 
                ag.home = self.districts[ag.district].locations['houses'][i]
            if ag.status in ["employed", "unemployed"]:
                ag.assign_income()
            elif ag.status == "homeless": ag.wealth = 500
            elif ag.status == "student": ag.wealth = 1000
            self.schedule.add(ag)
            
        self.datacollector = mesa.DataCollector(
        model_reporters={"Agent Positions": lambda m: [a.pos for a in m.schedule.agents]},
        agent_reporters={
                "physiological": lambda a: [a.nsl['physiological'][i] for i in range(len(a.nsl['physiological']))],
                "safety": lambda a: [a.nsl['safety'][i] for i in range(len(a.nsl['safety']))],
                "belonging": lambda a: [a.nsl['belonging'][i] for i in range(len(a.nsl['belonging']))],
                "esteem": lambda a: [a.nsl['esteem'][i] for i in range(len(a.nsl['esteem']))],
                "wealth": lambda a: a.wealth,  # Add the wealth and decided actions attribute to collect
                "actions": lambda a: a.chosenaction,
                "status": lambda a: a.status
            })


    def step(self):
        
        #what time is it?
        time = self.schedule.time % 24
        #print("Són les " + str(time + 8))

        # Place agents at the beginning
        if time == 0: 
            for agent in self.schedule.agents:
                #print("aqui "+ str(agent.sat) + "status " + agent.status)
                if agent.status != "homeless":
                    self.districts[agent.district].place_agent(agent, agent.home)

        # Schedule agents to go to work or school in the morning 
        if 0 < time < 8:
            for agent in self.schedule.agents:
                if agent.status == "student": 
                    agent.go_study()
                    #for i in range(1,4,1):
                    agent.nsl['safety'][3] = min(agent.nsl['safety'][3] + 0.3, 1.0) #education is increased
                        #agent.nsl['esteem'][1] += 0.3
                elif agent.status == "employed":
                    agent.go_work()
                    for i in range(1,3,1):
                        agent.nsl['safety'][i] = min(agent.nsl['safety'][i] + 0.3, 1.0) #finan  and employ increased 
                        agent.nsl['esteem'][1] = min(agent.nsl['esteem'][1] + 0.3, 1.0) #status increased
                        
                elif agent.status == "homeless":
                    pass
                elif agent.home == None: 
                    pass
                else:  #agent.status == "Unemployed" or "Retired"  AIXÒ HO HAURE DE CANVIAR MÉS ENDAVANT
                    agent.go_home()
            #fix nsl values when they go work 
            

       # Schedule agents to sleep
        if 17 <= time <= 23:
            for agent in self.schedule.agents:
                if agent.home == None: agent.go_reception_center()    #arreglar això, decisio autonoma pels homeless
                elif agent.status == "homeless": 
                    if random.random() < 0.6:
                        agent.go_reception_center()
                        agent.nsl['physiological'][2] = min(agent.nsl['physiological'][2] + 0.4, 1.0)
                    else: 
                        agent.sleep_street()
                        agent.nsl['physiological'][2] = min(agent.nsl['physiological'][2] + 0.2, 1.0)

                else:
                    agent.go_home()
                    agent.nsl['physiological'][2] = min(agent.nsl['physiological'][2] + 0.5, 1.0)
                    #agent.nsl['physiological'][2] = np.clip(np.random.normal(0.95, np.sqrt(0.1)), 0.9, 1.0)
                    #agent.nsl['physiological'][1] = 1
                    #agent.nsl['physiological'][0] = 1
        
        # some agents losing or getting a job every month
        
        if self.schedule.time % 720 == 0:
            a = random.random()
            if a < 0.1:
                selected_agent = random.choice(self.schedule.agents)
                if selected_agent.status == "employed":
                    selected_agent.status = "unemployed"
                    selected_agent.sat = SAT_matrices[selected_agent.status]
            elif 0.1 <= a < 0.2:
                selected_agent = random.choice(self.schedule.agents)
                if selected_agent.status == "unemployed":
                    selected_agent.status = "employed"
                    selected_agent.sat = SAT_matrices[selected_agent.status]
            else:
                pass
        

        # when a month has passed, mensuality is given to the agents and they also pay rent
        if self.schedule.time % 720 == 0:
            for agent in self.schedule.agents:
                if agent.status == 'employed':
                    agent.wealth += agent.income
                    agent.wealth -= agent.assign_rent()    #QUANTITAT FIXA DE LLOGUER, AGAFAR DE LES DADES OPENDATA FALTA SEGONS DISTRICTE NO?
                elif agent.status == 'retired':
                    agent.wealth += 1100
                    agent.wealth -= agent.assign_rent()    #QUANTITAT FIXA DE LLOGUER, AGAFAR DE LES DADES OPENDATA
                elif agent.status == 'student':
                    agent.wealth += 700
                    #agent.wealth -= agent.assign_rent()   #considerem que students no pagan rent
                else: pass
        
        # when a year has passed, agents grow old
        if self.schedule.time % 8064 == 0:
            for agent in self.schedule.agents:
                agent.age += 1
                
        for i in range(self.num_agents):
            agent = self.schedule.agents[i]
            #print( "Position of "+ str(agent.unique_id) +" at time " + str(time + 8) + " is " + str(agent.pos) + " in district " + str(agent.district) + " with age " + str(agent.age) + " status " + str(agent.status) + " and gender " + str(agent.gender) + " and wealth " + str(agent.wealth) + " and depth " + str(agent.depth))

        #print("Number of leisure agents:", gracia.check_number_of_agents())
        self.datacollector.collect(self)
        self.schedule.step()


if __name__ == '__main__':

    lista_distritos = [gracia, les_corts, eixample, sarria_stgervasi] 
    
    #GENERATE HOUSES FOR N AGENTS
    for district in lista_distritos:
        district.locations['houses'] = district.generate_tuples(N, (0, 9), (0, 9))
    
    barcelona = CityModel('Barcelona', lista_distritos, N, all_norms)

    for i in range(T):
        barcelona.step()
   

nsl_wealth = barcelona.datacollector.get_agent_vars_dataframe()
nsl_wealth.to_csv(r'C:/Users/albaa/Escriptori/MasterModelitzacio/JAE/pythonmesa/mesa/aporophobia/con_norms/nsl_wealth.csv', index=False, header=True)

