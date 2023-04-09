

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


class CityModel(Model):
    """A model representing a city as a collection of districts.

    Attributes
    ----------
    name : str
    districts : Dict[str, DistrictGrid]

    See Also
    --------
    mesa.model.Model

    """
    name: str
    districts: Dict[str, DistrictGrid]

    def __init__(self, name: str, districts: Collection[DistrictGrid]) -> None:
        """Generate a new city model.

        Parameters
        ----------
        name : str
        districts : Collection[DistrictGrid]

        """
        self.name = name
        self.districts = {dist.name: dist for dist in districts}


if __name__ == '__main__':
    
    # crear dos districtes
    ciutat_vella = DistrictGrid(
        'Ciutat Vella',
        10,
        10,
        False,
        {'escola': [(0, 0), (7, 6)],
         'hospital': [(5, 5)]}
    )

    les_corts = DistrictGrid(
        'Les Corts',
        7,
        7,
        False,
        {'escola': [(5, 5)],
         'hospital': [(3, 1), (7, 3)]}
    )

    # crear la ciutat amb els dos districtes
    barcelona = CityModel('Barcelona', [ciutat_vella, les_corts])

    # on estan els hospitals de Les Corts
    print("Els hospitals de Les Corts:")
    print(barcelona.districts['Les Corts'].locations['hospital'])

    print("Escoles a Ciutat Vella:")
    print(barcelona.districts['Ciutat Vella'].locations['escola'])

    # posar una nova escola a ciutat vella
    barcelona.districts['Ciutat Vella'].add_location('escola', 4, 3)
    print("Noves escoles a Ciuta Vella:")
    print(barcelona.districts['Ciutat Vella'].locations['escola'])

    pass
