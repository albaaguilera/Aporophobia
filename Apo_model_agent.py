import mesa
from city import CityGrid

locs = {
    'school': [(0, 1), (3, 3)],
    'hospital': [(1, 1)],
    'leisure': [(2, 4), (5, 5)],
    'houses': [(2, 3), (5, 3), (1, 2), (3, 4), (5, 6)],
    'work' : [(1, 0), (6, 6)]
}

class Apo_Agent(mesa.Agent):
    """An agent with BCN income."""
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 0
        self.home = None
        self.age = None
    
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.location, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.location = new_position
    
    def go_to_work(self):
        self.model.grid.move_agent(self, self.random.choice(self.model.locs['work']))

    def go_to_leisure(self):
        self.model.grid.move_agent(self, self.random.choice(self.model.locs['leisure']))
        
    def go_home(self):
        self.model.grid.move_agent(self, self.model.locs['houses'][self.unique_id])
    
    def step(self):
        print("Position of "+ str(self.unique_id) +" is " + str(self.pos))

class Apo_Model(mesa.Model):
    def __init__(self, N, width, height, wealth_list):
        self.num_agents = N
        self.locs = locs
        self.grid = CityGrid(width, height, False, locs) 
        self.wealth_list = wealth_list
        self.time_of_day = "morning"
        
        # Scheduler
        self.schedule = mesa.time.RandomActivation(self)
        
        # Create agents
        for i in range(self.num_agents):
            ag = Apo_Agent(i, self)
            self.schedule.add(ag)
            ag.wealth = 0 #wealth_list[i]
            ag.home = self.locs['houses'][i]
            #self.grid.place_agent(ag, ag.home)
            #ag.age = self.
            
        # Initialize data collector
        self.datacollector = mesa.DataCollector(
            model_reporters={"Agent Positions": lambda m: [a.pos for a in m.schedule.agents]}, agent_reporters= {"Wealth": lambda a: a.wealth})

    def step(self):
        time = self.schedule.time % 24
        if time == 0: 
            for agent in self.schedule.agents:
                self.grid.place_agent(agent, agent.home)
        # Schedule agents to go to work in the morning
        if 0 < time < 8:
            for agent in self.schedule.agents:
                agent.go_to_work()
        
        # Schedule agents to go to leisure locations in the afternoon
        if 8 <= time < 16:
            for agent in self.schedule.agents:
                agent.go_to_leisure()
        
        # Schedule agents to go home at night
        else:
            for agent in self.schedule.agents:
                agent.go_home()

        #when a month has passed, mensuality is given to the agents

        if self.schedule.time % 672 == 0:
            for agent in self.schedule.agents:
                agent.wealth += self.wealth_list[agent.unique_id]

        # Collect agent positions
        self.datacollector.collect(self)
        print(time)
        self.schedule.step()
        