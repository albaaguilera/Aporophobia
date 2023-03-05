from mesa.space import MultiGrid
from mesa.model import Model

from typing import Collection, Dict, List, Tuple


class DistrictGrid(MultiGrid):
    """A grid representing a district with buildings of different types.

    Attributes
    ----------
    name : str
    locations : Dict[str, List[Tuple[int, int]]]
        Map of locations of buildings.

    """
    name: str
    locations: Dict[str, List[Tuple[int, int]]]
    __busy_positions: List[Tuple[int, int]]
       
    def __init__(self, name: str, width: int, height: int, torus: bool, \
    locations: Dict[str, List[Tuple[int, int]]]) -> None:
        """Create a new district grid.

        Parameters
        ----------
        name : str
        width : int
        height : int
        torus : bool
        locations : Dict[str, List[Tuple[int, int]]]
            Map of locations.

        Raises
        ------
        ValueError
            if the locations are not consistent.
        
        See Also
        --------
        mesa.space.MultiGrid

        """
        super().__init__(width, height, torus)
        self.name = name
        self.__busy_positions = []
        self.__check_consistent_locations(width, height, locations)
        self.locations = locations


    def __check_consistent_locations(
        self,
        width: int,
        height: int,
        locations: Dict[str, List[Tuple[int, int]]]
    ) -> None:
        """Check that the locations are consistent with grid size and among
        themselves."""
        for l in locations.values():
            for x, y in l:
                if x<0 or x>width or y<0 or y>height:
                    raise ValueError(f"position ({x, y}) outside of grid \
                    dimensions")
                if (x, y) in self.__busy_positions:
                    raise ValueError(f"position ({x, y}) is already busy")
                self.__busy_positions.append((x, y))

    def has_any_building(self, x: int, y: int) -> bool:
        """Check if some location has a building of any type.

        Parameters
        ----------
        x : int
        y : int

        Returns
        -------
        bool
        
        """
        return (x, y) in self.__busy_positions
    
    def has_building(self, type: str, x: int, y: int) -> bool:
        """Check if some location has a building of a given type.

        Parameters
        ----------
        type : str
        x : int
        y : int

        Returns
        -------
        bool
        
        """
        return (x, y) in self.locations[type]
    
    def add_location(self, type: str, x: int, y:int) -> None:
        """Set a location as containing a building of some type.

        Parameters
        ----------
        type : str
        x : int
        y : int

        Raises
        ------
        ValueError
            If the input location is already busy.
            
        """
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