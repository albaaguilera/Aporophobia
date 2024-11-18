
import pandas as pd
import numpy as np
from norms import Norm
#income
districtes = ['Gràcia', 'Sarrià-Sant Gervasi', 'Les Corts', 'Eixample']
renda2020 = pd.read_csv("../OpenData/2019_income.csv")
renda2020['Nom_Districte'] = renda2020['Nom_Districte'].replace("L'Eixample", "Eixample")
renda2020 = renda2020[renda2020['Nom_Districte'].isin(districtes)]
renda2020['Import_Euros'] = renda2020['Import_Euros'] / 12

district_wealth = {}
for district in districtes:
    district_wealth[district] = renda2020[renda2020['Nom_Districte'] == district]

#rent
districtes = ['Gràcia', 'Sarrià-Sant Gervasi', 'Les Corts', 'Eixample']    
lloguer2021 = pd.read_csv("../OpenData/2022_rent.csv") #pd.read_csv("OpenData/2021_lloguer_preu_trim.csv")
lloguer2021['Nom_Districte'] = lloguer2021['Nom_Districte'].replace("L'Eixample", "Eixample")
lloguer2021 = lloguer2021[(lloguer2021['Nom_Districte'].isin(districtes)) & (lloguer2021['Lloguer_mitja'] == 'Lloguer mitjà mensual (Euros/mes)')]
lloguer2021['Preu'] = pd.to_numeric(lloguer2021['Preu'])/4

district_rent = {}
for district in districtes:
    district_rent[district] = lloguer2021[lloguer2021['Nom_Districte'] == district]

#age
edat2020 = pd.read_csv("../OpenData/2019_age_by_gender.csv")

edat2020 = edat2020[edat2020['Nom_Districte'].isin(districtes)]
edat2020['Edat'] = edat2020['Edat any a any'].str.extract('(\d+)').astype(int)
total_people = edat2020.groupby(['Nom_Districte'])['Nombre'].sum()
age_counts = edat2020.groupby(['Nom_Districte', 'Edat'])['Nombre'].sum()
age_percentages = age_counts / total_people
age_percentages = age_percentages.reset_index()
probabilidades_por_distrito = age_percentages.groupby('Nom_Districte').apply(lambda x: dict(zip(x.Edat, x.Nombre))).to_dict()


#homeless assignation
homeless_per_district = [297, 32, 43, 34]
prob_homeless = (homeless_per_district / total_people) *100  #variable probabilty to study homeless behaviour, multiplied by the reason considering N_real = 600.000 /N=100. 

#gender
gender_counts = edat2020.groupby(['Nom_Districte', 'Sexe'])['Nombre'].sum()
gender_percentages = gender_counts / total_people
gender_percentages = gender_percentages.reset_index()
probabilidades_por_distrito_gender = gender_percentages.groupby('Nom_Districte').apply(lambda x: dict(zip(x.Sexe, x.Nombre))).to_dict()

#district
def assign_district():
    district_probabilities = total_people / total_people.sum()
    district_selected = np.random.choice(total_people.index, p=district_probabilities)
    return district_selected

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
                SAT_matrix[i][j] = 0.43
            elif need == "food" and action == "go_reception_center":
                SAT_matrix[i][j] = 0.37
            elif need == "food" and action == "beg":
                SAT_matrix[i][j] = 0.36
            elif need == "food" and action == "go_leisure":
                SAT_matrix[i][j] = 0.2
            if status == "unemployed":
                if need == "food" and action == "invest_education":
                    SAT_matrix[i][j] = 0.25
        

            # SHELTER
            if need == "shelter" and action == "go_home":
                SAT_matrix[i][j] = 1.0
            elif need == "shelter" and action == "go_reception_center":
                SAT_matrix[i][j] = 0.4
            elif need == "shelter" and action == "sleep_street":
                SAT_matrix[i][j] = 0.3
            if status == "retired":
                if need == "shelter" and action == "go_hospital":
                    SAT_matrix[i][j] = 0.4
            
            # SLEEP
            if need == "sleep" and action == "go_home":
                SAT_matrix[i][j] = 0.2
            elif need == "sleep" and action == "sleep_street":
                SAT_matrix[i][j] = 0.85
            elif need == "sleep" and action == "go_reception_center":
                SAT_matrix[i][j] = 0.26
            
            # CLOTHING
            if need == "clothing" and action == "go_shopping":
                SAT_matrix[i][j] = 1.0
            elif need == "clothing" and action == "steal_clothes":
                SAT_matrix[i][j] = 0.8
            elif need == "clothing" and action == "beg":
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
            elif need in ["financial security", "employment"] and action =="beg":
                SAT_matrix[i][j] = 1.0
            if status == "employed": 
                if need in ["financial security", "employment"] and action =="invest_education":
                    SAT_matrix[i][j] = 0.5

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
            elif status == "employed":
                if need == "friendship" and action == "go_leisure":
                    SAT_matrix[i][j] = 0.8
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
                    SAT_matrix[i][j] = 0.2
            elif status == "homeless":
                if need == "intimacy" and action == "go_reception_center":
                    SAT_matrix[i][j] = 0.15
                elif need == "intimacy" and action == "go_leisure":
                    SAT_matrix[i][j] = 0.1

            # FREEDOM
            if need == "freedom" and action == "go_home":
                SAT_matrix[i][j] = 0.15
            elif need == "freedom" and action == "go_leisure":
                SAT_matrix[i][j] = 0.7
            elif need == "freedom" and action == "beg":
                SAT_matrix[i][j] = 0.7
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
                    SAT_matrix[i][j] = 0.6
            

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
            elif status == "employed":
                if need == "status" and action == "go_leisure":
                    SAT_matrix[i][j] = 0.7

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

#print(SAT_matrices['employed'])

# Needs
needs = {
    'physiological': {
        'needs': ['food', 'shelter', 'sleep', 'health'],
        'weight': 0.85,
        'decaying': {
            'retired': [0.825, 0.92, 0.91, 0.88],
            'employed': [0.822, 0.95, 0.93, 0.9993],
            'unemployed': [0.822, 0.95, 0.94, 0.9993],
            'homeless': [0.82, 0.90, 0.92, 0.999],
            'student': [0.81, 0.95, 0.96, 0.9995]
        },
        'mean and var': (0.7, 0.2)
    },
    'safety': {
        'needs': ['clothing', 'financial security', 'employment', 'education'],
        'weight': 0.8,
        'decaying': {
            'retired': [0.9988, 0.995, 0.999, 0.998],
            'employed': [0.9982, 0.999, 0.9992, 0.998],
            'unemployed': [0.9983, 0.991, 0.995, 0.991],
            'homeless': [0.9983, 0.999, 0.99, 0.995],
            'student': [0.998, 0.993, 0.997, 0.991]
        },
        'mean and var': (0.8, 0.4)
    },
    'belonging': {
        'needs': ['family', 'friendship', 'intimacy'],
        'weight': 0.75,
        'decaying': {
            'retired': [0.8, 0.97, 0.98],
            'employed': [0.91, 0.85, 0.98],
            'unemployed': [0.91, 0.87, 0.98],
            'homeless': [0.91, 0.995, 0.98],
            'student': [0.95, 0.85, 0.9]
        },
        'mean and var': (0.6, 0.4)
    },
    'esteem': {
        'needs': ['freedom', 'status', 'self-esteem'],
        'weight': 0.7,
        'decaying': {
            'retired': [0.99, 0.99, 0.99],
            'employed': [0.94, 0.99, 0.98],
            'unemployed': [0.99, 0.99, 0.97],
            'homeless': [0.99, 0.99, 0.99],
            'student': [0.9, 0.99, 0.8]
        },
        'mean and var': (0.7, 0.4)
    }
}

#Norms

all_norms = [
        #Norm("agx.status == \"unemployed\" and agx.model.schedule.time % 720 == 0", ["agx.wealth += 700"]), #ATUR (s'ha d'afegir que hagi cotitzat)
        #Norm("agx.status == \"homeless\" and agx.model.schedule.time % 720 == 0", ["agx.status = \"unemployed\"", "agx.sat = SAT_matrices[agx.status]"]),   #Projecte de norma (no en vigor) 
        #Norm("agx.chosenaction in [\"steal_food\", \"steal_clothes\", \"sleep_street\"] and agx.wealth > 0", ["agx.wealth -= 500"]),
        #Norm("agx.chosenaction in [\"steal_food\", \"steal_clothes\", \"sleep_street\"] and agx.wealth <= 0", ["agx.go_prison()", "agx.wealth -= 500"]), #consequencies preso? 
        #Norm("agx.wealth <= 0 and agx.model.schedule.time % 720 == 0" , ["agx.home = None", "agx.status = \"homeless\"", "agx.sat = SAT_matrices[agx.status]"]),  #Eviction for rent
        #Norm("agx.wealth <= 0 and agx.model.schedule.time % 720 == 0", ["agx.wealth += 735"]), #minimal vital income
        
    ]

#Norm("agx.status == \"homeless\"", ["agx.go_reception_center()"]), #Ja feta en les propies available actions: puc fer que no estigui available l'acció com a contranorma.
#Norm("agx.chosenaction == \"sleep_street\" and agx.wealth > 0", ["agx.wealth -= 500"]),  # Multa dormir si tenen diners (randomly?)
#Norm("agx.chosenaction == \"sleep_street\" and agx.wealth <= 0", ["agx.go_prison()"]),  # Multa dormir si no tenen diners (consequencies presó?)
