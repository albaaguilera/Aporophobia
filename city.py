

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
    
  gracia = DistrictGrid(
        'Gràcia',
        10,
        10,
        False,
        {'school': [(0, 0), (7, 6)],
         'work': [(3, 1), (7, 3)],
         'leisure': [(3, 2), (7, 4)],
         'grocery':  [(1, 0), (0, 1)],
         'hospital': [(2, 0), (0, 2)]}
    )
    #gracia.locations['houses'] = gracia.generate_tuples(N, (0,9) , (0,9))

  les_corts = DistrictGrid(
        'Les Corts',
        10,
        10,
        False,
        {'school': [(5, 5)],
         'work': [(0, 0), (5, 1)],
         'leisure': [(3, 2), (7, 4)],
         'grocery':  [(1, 0), (0, 1)],
         'hospital': [(2, 0), (0, 2)]}
    )

  sarria_stgervasi = DistrictGrid(
        'Sarrià-Sant Gervasi',
        10,
        10,
        False,
        {'school': [(5, 4)],
         'work' : [( 0, 1)],
         'leisure': [(3, 2), (7, 4)],
         'grocery':  [(1, 0), (0, 0)],
         'hospital': [(2, 0), (0, 2)]}
    )

  eixample = DistrictGrid(
        'Eixample',
        10,
        10,
        False,
        {'school': [(5, 2)],
         'work' : [(2, 2)],
         'leisure': [(3, 2), (7, 4)],
         'grocery':  [(1, 0), (0, 0)],
         'hospital': [(2, 0), (0, 2)]}
    )

  lista_distritos = [gracia, les_corts, eixample, sarria_stgervasi]