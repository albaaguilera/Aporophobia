
import mesa 
from city import DistrictGrid
from typing import Collection, Dict, List, Tuple
from agent import Apo_Agent
from data import assign_district
import data

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
            ag = Apo_Agent(i, self, district = assign_district()) 
            ag.home = self.districts[ag.district].locations['houses'][i]
            ag.assign_age_and_status()
            ag.assign_income()
            self.schedule.add(ag)

        self.datacollector = mesa.DataCollector(
        model_reporters={"Agent Positions": lambda m: [a.pos for a in m.schedule.agents]})

    def step(self):
        time = self.schedule.time % 24
            
        if time == 0: 
            for agent in self.schedule.agents:
                self.districts[agent.district].place_agent(agent, agent.home)

        # Schedule agents to go to work in the morning
        if 0 < time < 8:
            for agent in self.schedule.agents:
                if agent.age < 18: 
                    agent.go_school()
                else:
                    agent.go_work()

        if 8 <= time < 17: 
            for agent in self.schedule.agents:
                agent.go_leisure()

        if 17 <= time <= 23:
            for agent in self.schedule.agents:
                agent.go_home()
          
        #when a month has passed, mensuality is given to the agents
        if self.schedule.time % 672 == 0:
            for agent in self.schedule.agents:
                agent.wealth += agent.wealth
                
        for i in range(self.num_agents):
            agent = self.schedule.agents[i]
            print("Position of "+ str(agent.unique_id) +" at time " + str(time) + " is " + str(agent.pos) + " in district " + str(agent.district) + " with age " + str(agent.age) + " and status " + str(agent.status))

        self.datacollector.collect(self)
        self.schedule.step()
    

if __name__ == '__main__':

    gracia = DistrictGrid(
        'Gràcia',
        10,
        10,
        False,
        {'school': [(0, 0), (7, 6)],
         'work': [(3, 1), (7, 3)],
         'leisure': [(3, 2), (7, 4)]}
    )
    #gracia.locations['houses'] = gracia.generate_tuples(N, (0,9) , (0,9))

    les_corts = DistrictGrid(
        'Les Corts',
        10,
        10,
        False,
        {'school': [(5, 5)],
         'work': [(0, 0), (5, 1)],
         'leisure': [(3, 2), (7, 4)]}
    )

    sarria_stgervasi = DistrictGrid(
        'Sarrià-Sant Gervasi',
        10,
        10,
        False,
        {'school': [(5, 4)],
         'work' : [( 0, 1)],
         'leisure': [(3, 2), (7, 4)]}
    )

    eixample = DistrictGrid(
        'Eixample',
        10,
        10,
        False,
        {'school': [(5, 2)],
         'work' : [(2, 2)],
         'leisure': [(3, 2), (7, 4)]}
    )

    lista_distritos = [gracia, les_corts, eixample, sarria_stgervasi] 

    #GENERATE HOUSES FOR N AGENTS
    for district in lista_distritos:
        district.locations['houses'] = district.generate_tuples(N, (0, 9), (0, 9))

    barcelona = CityModel('Barcelona', lista_distritos, N)
    pass

for i in range(4):
    barcelona.step()