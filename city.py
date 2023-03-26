

from mesa.space import MultiGrid
from typing import Collection, Dict, List, Tuple
import random
import numpy as np
import pandas as pd
N = 5

class DistrictGrid(MultiGrid):
    name: str
    locations: Dict[str, List[Tuple[int, int]]]
    __busy_positions: List[Tuple[int, int]]
       
    def __init__(self, name: str, width: int, height: int, torus: bool, \
    locations: Dict[str, List[Tuple[int, int]]]) -> None:
        super().__init__(width, height, torus)
        self.name = name
        self.__busy_positions = []
        self.__check_consistent_locations(width, height, locations)
        self.locations = locations
        print(self.__busy_positions)
    
    def __check_consistent_locations(
        self,
        width: int,
        height: int,
        locations: Dict[str, List[Tuple[int, int]]]
    ) -> None:
        for l in locations.values():
            for x, y in l:
                if x<0 or x>width or y<0 or y>height:
                    raise ValueError(f"position ({x, y}) outside of grid \
                    dimensions")
                if (x, y) in self.__busy_positions:
                    raise ValueError(f"position ({x, y}) is already busy")
                self.__busy_positions.append((x, y))

    def has_any_building(self, x: int, y: int) -> bool:
        return (x, y) in self.__busy_positions
    
    def has_building(self, type: str, x: int, y: int) -> bool:
        return (x, y) in self.locations[type]
    
    def add_location(self, type: str, x: int, y:int) -> None:
        if (x, y) in self.__busy_positions:
            raise ValueError(f"position ({x, y}) is already busy")
        try:
            self.locations[type].append((x, y))
        except KeyError:
            self.locations[type] = [(x, y)]
        self.__busy_positions.append((x, y))
    
    def generate_tuples(self, N, x_range, y_range):
        tuples = list()
        while len(tuples) < N:
            x = random.randint(x_range[0], x_range[1])
            y = random.randint(y_range[0], y_range[1])
            t = (x, y)
            if t in self.__busy_positions:
                continue
            if t in tuples:
                continue
            tuples.append(t)
        return tuples

    def move_agent(self, agent, new_location):
        self.locations[agent.location].remove(agent)
        agent.location = new_location
        self.locations[new_location].append(agent)
