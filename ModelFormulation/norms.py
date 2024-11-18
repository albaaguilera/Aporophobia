from typing import List

agx = None

class Norm:

    def __init__(self, precondition: str, postcondition: List[str]) -> None:
        self.precondition = precondition
        self.postcondition = postcondition

    def check_precondition(self, ag) -> bool:
        agx = ag
        precondition_holds = eval(self.precondition)
        agx = None
        return precondition_holds
    
    def apply_postcondition(self, ag):
        agx = ag
        for statement in self.postcondition:
            exec(statement)
        agx = None

    def __str__(self) -> str:
        return f"if {self.precondition} then {', '.join(self.postcondition)}"

#SAT
needs_list = ["food", "shelter", "sleep", "health", "clothing", "financial security", "employment", "education", "family", "friendship", "intimacy", "freedom", "status", "self-esteem"]
actions_dict = {
        'retired': ["go_home", "go_grocery", "go_hospital", "go_shopping", "go_leisure", "steal_food", "steal_clothes", "go_prison"],
        'employed': ["go_home", "go_grocery", "go_hospital", "go_shopping", "go_leisure", "steal_food", "steal_clothes", "go_prison"], #"go_work",
        'unemployed': ["go_home", "go_grocery", "go_hospital", "go_shopping", "go_leisure", "steal_food", "steal_clothes", "go_prison", "invest_education"],
        'student': ["go_home", "go_grocery", "go_hospital", "go_shopping", "go_leisure", "steal_food", "steal_clothes", "go_prison"], #"go_study",
        'homeless': ["go_grocery","go_hospital", "go_shopping", "go_leisure", "invest_education", "sleep_street", "beg", "steal_food", "steal_clothes", "go_reception_center", "go_prison"]
        }

SAT_matrices = {}

for status, actions in actions_dict.items():
    SAT_matrix = [[0.0 for _ in range(len(actions))] for _ in range(len(needs_list))]
    for i, need in enumerate(needs_list):
        for j, action in enumerate(actions):
            # Assign specific SAT values based on need-action pairs
            # tunegem per diferenciar employed de retired

            # FOOD
            if need == "food" and action == "go_grocery":
                SAT_matrix[i][j] = 1.0
            if need == "food" and action == "go_home":
                SAT_matrix[i][j] = 0.15
            elif need == "food" and action == "steal_food":
                SAT_matrix[i][j] = 0.7
            elif need == "food" and action == "go_reception_center":
                SAT_matrix[i][j] = 0.5
            elif need == "food" and action == "beg":
                SAT_matrix[i][j] = 0.15
            elif need == "food" and action == "go_leisure":
                SAT_matrix[i][j] = 0.4
        

            # SHELTER
            if need == "shelter" and action == "go_home":
                SAT_matrix[i][j] = 1.0
            elif need == "shelter" and action == "go_reception_center":
                SAT_matrix[i][j] = 0.7
            
            # SLEEP
            if need == "sleep" and action == "go_home":
                SAT_matrix[i][j] = 0.2
            elif need == "sleep" and action == "sleep_street":
                SAT_matrix[i][j] = 0.7
            
            # CLOTHING
            if need == "clothing" and action == "go_shopping":
                SAT_matrix[i][j] = 1.0
            elif need == "clothing" and action == "steal_clothes":
                SAT_matrix[i][j] = 0.8

            # HEALTH
            if need == "health" and action == "go_hospital":
                SAT_matrix[i][j] = 1.0
            elif need == "health" and action == "go_grocery":
                SAT_matrix[i][j] = 0.3
            if status == "retired":
                if need == "health" and action == "go_hospital":
                    SAT_matrix[i][j] = 0.9

            # FINANCIAL SECURITY and EMPLOYMENT and EDUCATION
            #if need in ["financial security", "employment", "education"] and (action == "go_work" or action == "invest_education"):
                #SAT_matrix[i][j] = 1.0
            if need in ["financial security", "employment"] and action in ["invest_education", "beg"]:
                SAT_matrix[i][j] = 0.5
            elif need == "education" and action == "invest_education":
                SAT_matrix[i][j] = 1.0

            # FAMILY and FRIENDSHIP
            if need == "family" and action == "go_home":
                SAT_matrix[i][j] = 0.8
            if status != "homeless": 
                if need == "family" and action == "go_leisure":
                    SAT_matrix[i][j] = 0.3
                if need == "friendship" and action == "go_leisure":
                    SAT_matrix[i][j] = 1.0
            elif status == "homeless":
                if need == "friendship" and action == "go_leisure":
                    SAT_matrix[i][j] = 0.4
            #elif need == "friendship" and action == "go_work":
                #SAT_matrix[i][j] = 0.2
            #elif need == "friendship" and action == "go_study":
                #SAT_matrix[i][j] = 0.3

            # INTIMACY
            if need == "intimacy" and action == "go_home":
                SAT_matrix[i][j] = 0.8
            elif need == "intimacy" and action == "go_leisure":
                    SAT_matrix[i][j] = 0.5
            if status == "employed":
                if need == "intimacy" and action == "go_leisure":
                    SAT_matrix[i][j] = 0.7
            elif status == "student":
                if need == "intimacy" and action == "go_leisure":
                    SAT_matrix[i][j] = 0.8
            elif status == "homeless":
                if need == "intimacy" and action == "go_reception_center":
                    SAT_matrix[i][j] = 0.3
                elif need == "intimacy" and action == "go_leisure":
                    SAT_matrix[i][j] = 0.1

            # FREEDOM
            if need == "freedom" and action == "go_home":
                SAT_matrix[i][j] = 0.15
            elif need == "freedom" and action == "go_leisure":
                SAT_matrix[i][j] = 0.7
            elif need == "freedom" and action == "beg":
                SAT_matrix[i][j] = 0.4
            if status != "retired":
                if need == "freedom" and action == "go_leisure":
                    SAT_matrix[i][j] = 0.9
            elif status == "homeless":
                if need == "freedom" and action == "invest_education":
                    SAT_matrix[i][j] = 0.4
                if need == "freedom" and action == "go_leisure":
                    SAT_matrix[i][j] = 0.3
            elif status == "student":
                if need == "freedom" and action == "go_shopping":
                    SAT_matrix[i][j] = 0.5
            

            # STATUS
            if need == "status" and action == "go_work":
                SAT_matrix[i][j] = 0.19
            elif need == "status" and action == "go_leisure":
                SAT_matrix[i][j] = 0.7
            elif need == "status" and action == "beg":
                SAT_matrix[i][j] = 0.6
            elif need == "status" and action == "invest_education":
                    SAT_matrix[i][j] = 0.5
            if status == "homeless":
                if need == "status" and action == "invest_education":
                    SAT_matrix[i][j] = 0.6
            elif status == "unemployed":
                if need == "status" and action == "invest_education":
                    SAT_matrix[i][j] = 0.7
                if need == "status" and action == "go_leisure":
                    SAT_matrix[i][j] = 0.5

            # SELF-ESTEEM
            if need == "self-esteem" and (action == "go_leisure" or action == "go_shopping" or action == "go_work"):
                SAT_matrix[i][j] = 0.5
            if status == "student":
                if need == "self-esteem" and action == "go_shopping":
                    SAT_matrix[i][j] = 0.8
                elif need == "self-esteem" and action == "go_leisure":
                    SAT_matrix[i][j] = 0.6
            elif status != "student":
                if need == "self-esteem" and action == "go_shopping":
                    SAT_matrix[i][j] = 0.6
                if need == "self-esteem" and action == "steal_clothes":
                    SAT_matrix[i][j] = 0.6
            elif status == "employed":
                if need == "self-esteem" and action == "go_leisure":
                    SAT_matrix[i][j] = 0.6
            elif status == "unemployed":
                if need == "self-esteem" and action == "invest_education":
                    SAT_matrix[i][j] = 0.5

    SAT_matrices[status] = SAT_matrix