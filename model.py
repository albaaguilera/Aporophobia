import mesa 
from city import DistrictGrid, gracia, sarria_stgervasi, eixample, les_corts
from typing import Collection, Dict
from agent import Apo_Agent
from data import assign_district, SAT_matrices, needs, all_norms
from norms import Norm
import numpy as np
import random 

N = 5

class CityModel(mesa.Model):
    name: str
    districts: Dict[str, DistrictGrid]
    
    def __init__(self, name: str, districts: Collection[DistrictGrid], N, norms: Collection[Norm] = []) -> None:
        self.num_agents = N
        self.name = name
        self.districts = {dist.name: dist for dist in districts}
        self.schedule = mesa.time.RandomActivation(self)
        self.norms = norms 

        # Create agents
        for i in range(self.num_agents):
            ag = Apo_Agent(i, self, district = assign_district(), needs = needs, sat = SAT_matrices) 
            ag.initialize_nsl()
            ag.assign_gender()
            ag.assign_age_and_status()
            ag.assign_homeless()
            ag.sat = SAT_matrices[ag.status] 
            if ag.status != "homeless": 
                ag.home = self.districts[ag.district].locations['houses'][i]
                ag.assign_income()
            self.schedule.add(ag)
            
        self.datacollector = mesa.DataCollector(
        model_reporters={"Agent Positions": lambda m: [a.pos for a in m.schedule.agents]},
        agent_reporters={
                "physiological": lambda a: [a.nsl['physiological'][i] for i in range(len(a.nsl['physiological']))],
                "safety": lambda a: [a.nsl['safety'][i] for i in range(len(a.nsl['safety']))],
                "belonging": lambda a: [a.nsl['belonging'][i] for i in range(len(a.nsl['belonging']))],
                "esteem": lambda a: [a.nsl['esteem'][i] for i in range(len(a.nsl['esteem']))],
                "wealth": lambda a: a.wealth,  # Add the wealth and decided actions attribute to collect
                "actions": lambda a: a.chosenaction
            })

    def step(self):

        #what time is it?
        time = self.schedule.time % 24
        print("Són les " + str(time + 8))

        # Place agents at the beginning
        if time == 0: 
            for agent in self.schedule.agents:
                if agent.status != "homeless":
                    self.districts[agent.district].place_agent(agent, agent.home)

        # Schedule agents to go to work or school in the morning 
        if 0 < time < 8:
            for agent in self.schedule.agents:
                if agent.status == "student": 
                    agent.go_study()
                elif agent.status == "employed":
                    agent.go_work()
                elif agent.status == "homeless":
                    pass
                elif agent.home == None: 
                    pass
                else:  #agent.status == "Unemployed" or "Retired"  AIXÒ HO HAURE DE CANVIAR MÉS ENDAVANT
                    agent.go_home()

       # Schedule agents to sleep
        if 17 <= time <= 23:
            for agent in self.schedule.agents:
                if agent.home == None: agent.go_reception_center()    #arreglar això, decisio autonoma pels homeless
                elif agent.status == "homeless": 
                    if random.random() < 0.6:
                        agent.go_reception_center()
                    else: agent.sleep_street()
                else:
                    agent.go_home()
                    #agent.nsl['physiological'][2] = np.clip(np.random.normal(0.95, np.sqrt(0.1)), 0.9, 1.0)
                    #agent.nsl['physiological'][1] = 1
                    #agent.nsl['physiological'][0] = 1
        
        # some employed agents losing their jobs 
        if random.random() < 0.3:
            selected_agent = random.choice(self.schedule.agents)
            if selected_agent.status == "employed":
                selected_agent.status = "unemployed"


        # when a month has passed, mensuality is given to the agents and they also pay rent
        if self.schedule.time % 720 == 0:
            for agent in self.schedule.agents:
                if agent.status == 'employed':
                    agent.wealth += agent.monthly_income
                    agent.wealth -= agent.assign_rent()    #QUANTITAT FIXA DE LLOGUER, AGAFAR DE LES DADES OPENDATA FALTA SEGONS DISTRICTE NO?
                elif agent.status == 'retired':
                    agent.wealth += 1100
                    agent.wealth -= agent.assign_rent()    #QUANTITAT FIXA DE LLOGUER, AGAFAR DE LES DADES OPENDATA
                elif agent.status == 'student':
                    agent.wealth *= 500
                    agent.wealth -= agent.assign_rent()   #QUANTITAT FIXA DE LLOGUER, AGAFAR DE LES DADES OPENDATA
                else: pass
        
        # when a year has passed, agents grow old
        if self.schedule.time % 8064 == 0:
            for agent in self.schedule.agents:
                agent.age += 1
                
        for i in range(self.num_agents):
            agent = self.schedule.agents[i]
            print( "Position of "+ str(agent.unique_id) +" at time " + str(time + 8) + " is " + str(agent.pos) + " in district " + str(agent.district) + " with age " + str(agent.age) + " status " + str(agent.status) + " and gender " + str(agent.gender) + " and wealth " + str(agent.wealth) + " and depth " + str(agent.depth))

        #print("Number of leisure agents:", gracia.check_number_of_agents())

        self.datacollector.collect(self)
        self.schedule.step()


if __name__ == '__main__':

    lista_distritos = [gracia, les_corts, eixample, sarria_stgervasi] 
    
    #GENERATE HOUSES FOR N AGENTS
    for district in lista_distritos:
        district.locations['houses'] = district.generate_tuples(N, (0, 9), (0, 9))
        #print("Busy positions leisure" + str(district.get_busy_positions()))
    
    barcelona = CityModel('Barcelona', lista_distritos, N, all_norms)
    # pass

    for i in range(23):
        barcelona.step()
   

nsl_wealth = barcelona.datacollector.get_agent_vars_dataframe()
nsl_wealth.to_csv(r'C:/Users/albaa/Escriptori/MasterModelitzacio/JAE/pythonmesa/mesa/aporophobia/con_norms/nsl_wealth.csv', index=False, header=True)

