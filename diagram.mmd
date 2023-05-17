classDiagram

    class CityModel {
        +name : str
        +agents : List[Apo_Agent]
        +num_agents : int
        +districts : Dict[str, DistrictGrid]
        +norms : List[Norm]

        +step()
    }

    class DistrictGrid {
        +name : str
        +locations : Dict[str, List[Tuple[int, int]]]

        +has_any_building(int, int): bool
        +has_building(str, int, int): bool
        +add_location(str, int, int)
        +generate_tuples(int, int, int): List[Tuple[int, int]]
        +move_agent(Apo_Agent, Tuple[int, int])
    }

    class Apo_Agent {
        +age : int
        +district : str
        +wealth : float
        +status : str
        +gender : str
        +needs : Dict[str, List[float]]

        +assign_income()
        +assign_age_and_status()
        +assign_homeless()
        +assign_gender()

        +go_work()
        +go_leisure()
        +go_home()
        +go_school()
        +go_grocery()
        +go_hospital()
        +go_shopping()
        +step()
    }

    class Norm {
        +precondition : str
        +postcondition : List[str]

        +check_precondition(Apo_Agent): bool
        +apply_postcondition(Apo_Agent)
    }

    CityModel "1" --> "1...n" DistrictGrid : contains
    CityModel "1" --> "0...n" Apo_Agent : populated by
    Apo_Agent "1" --> "1" DistrictGrid : associated to
    CityModel "1" --> "0...n" Norm : regulated by
