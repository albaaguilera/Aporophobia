
import mesa 
from city import DistrictGrid, gracia, sarria_stgervasi, eixample, les_corts
from typing import Collection, Dict, List, Tuple
from agent import Apo_Agent
from data import assign_district, SAT_matrix, needs

N = 5

class CityModel(mesa.Model):
    name: str
    districts: Dict[str, DistrictGrid]
    
    def __init__(self, name: str, districts: Collection[DistrictGrid], N) -> None:
        self.num_agents = N
        self.name = name
        self.districts = {dist.name: dist for dist in districts}
        self.schedule = mesa.time.RandomActivation(self)

        # Create agents
        for i in range(self.num_agents):
            ag = Apo_Agent(i, self, district = assign_district(), needs = needs, sat = SAT_matrix) 
            ag.home = self.districts[ag.district].locations['houses'][i]
            ag.assign_age_and_status()
            ag.assign_income()
            self.schedule.add(ag)
            
        self.datacollector = mesa.DataCollector(
        model_reporters={"Agent Positions": lambda m: [a.pos for a in m.schedule.agents]},
        agent_reporters={
                "nsl": lambda a: a.nsl,
                "urg": lambda a: a.urg,
            })

    def step(self):
        time = self.schedule.time % 24
        print("Són les " + str(time + 8))
        if time == 0: 
            for agent in self.schedule.agents:
                self.districts[agent.district].place_agent(agent, agent.home)
                #print(agent.pos)

        # Schedule agents to go to work or school in the morning
        if 0 < time < 8:
        
            for agent in self.schedule.agents:
                #print(agent.pos)
                if agent.status == "Student": 
                    agent.go_school()
                elif agent.status == "Employed":
                    agent.go_work()
                else:  #agent.status == "Unemployed" or "Retired"  AIXÒ HO HAURE DE CANVIAR MÉS ENDAVANT
                    agent.go_home()
        """          
        if 8 <= time < 15: 
            for agent in self.schedule.agents:
                agent.go_leisure()
        """
        if 15 <= time <= 23:
            for agent in self.schedule.agents:
                agent.go_home()
        
        #when a month has passed, mensuality is given to the agents
        if self.schedule.time % 672 == 0:
            for agent in self.schedule.agents:
                agent.wealth += agent.wealth
        
        #when a year has passed, agents grow old
        if self.schedule.time % 8064 == 0:
            for agent in self.schedule.agents:
                agent.age += 1
                
        for i in range(self.num_agents):
            agent = self.schedule.agents[i]
            print( "Position of "+ str(agent.unique_id) +" at time " + str(time + 8) + " is " + str(agent.pos) + " in district " + str(agent.district) + " with age " + str(agent.age) + " and status " + str(agent.status))

        self.datacollector.collect(self)
        self.schedule.step()
    

if __name__ == '__main__':

    lista_distritos = [gracia, les_corts, eixample, sarria_stgervasi] 
    
    #GENERATE HOUSES FOR N AGENTS
    for district in lista_distritos:
        district.locations['houses'] = district.generate_tuples(N, (0, 9), (0, 9))

    barcelona = CityModel('Barcelona', lista_distritos, N)
    pass

for i in range(10):
    barcelona.step()
