from mesa.space import MultiGrid

from typing import Dict, List, Tuple

class CityGrid(MultiGrid):
    """A grid representing a city with buildings.

    Attributes
    ----------
    locations : Dict[str, List[Tuple[int, int]]]
        Map of locations of buildings.

    """
    locations: Dict[str, List[Tuple[int, int]]]
    __busy_positions: List[Tuple[int, int]]
       
    def __init__(self, width: int, height: int, torus: bool, \
    locations: Dict[str, List[Tuple[int, int]]]) -> None:
        """Create a new city grid.

        Parameters
        ----------
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


    def is_busy(self, x: int, y: int) -> bool:
        """Check if some locations has a building of any type.

        Parameters
        ----------
        x : int
        y : int

        Returns
        -------
        bool
        
        """
        return (x, y) in self.__busy_positions
    

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
