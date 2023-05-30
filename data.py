
import pandas as pd
import numpy as np
from norms import Norm
#income
districtes = ['Gràcia', 'Sarrià-Sant Gervasi', 'Les Corts', 'Eixample']
renda2020 = pd.read_csv("OpenData/2020_renda_neta_mitjana_per_persona.csv")
renda2020['Nom_Districte'] = renda2020['Nom_Districte'].replace("L'Eixample", "Eixample")
renda2020 = renda2020[renda2020['Nom_Districte'].isin(districtes)]
renda2020['Import_Euros'] = renda2020['Import_Euros'] / 12

district_wealth = {}
for district in districtes:
    district_wealth[district] = renda2020[renda2020['Nom_Districte'] == district]

#rent
districtes = ['Gràcia', 'Sarrià-Sant Gervasi', 'Les Corts', 'Eixample']
lloguer2021 = pd.read_csv("C:/Users/albaa/Escriptori/MasterModelitzacio/JAE/pythonmesa/mesa/aporophobia/con_norms/OpenData/2021_lloguer_preu_trim.csv") #pd.read_csv("OpenData/2021_lloguer_preu_trim.csv")
lloguer2021['Nom_Districte'] = lloguer2021['Nom_Districte'].replace("L'Eixample", "Eixample")
lloguer2021 = lloguer2021[(lloguer2021['Nom_Districte'].isin(districtes)) & (lloguer2021['Lloguer_mitja'] == 'Lloguer mitjà mensual (Euros/mes)')]
lloguer2021['Preu'] = pd.to_numeric(lloguer2021['Preu'])/4

district_rent = {}
for district in districtes:
    district_rent[district] = lloguer2021[lloguer2021['Nom_Districte'] == district]

#age
edat2020 = pd.read_csv("OpenData/2020_ine_edat_any_a_any_per_sexe.csv")
edat2020 = edat2020[edat2020['Nom_Districte'].isin(districtes)]
edat2020['Edat'] = edat2020['Edat_any_a_any'].str.extract('(\d+)').astype(int)
total_people = edat2020.groupby(['Nom_Districte'])['Nombre'].sum()
age_counts = edat2020.groupby(['Nom_Districte', 'Edat'])['Nombre'].sum()
age_percentages = age_counts / total_people
age_percentages = age_percentages.reset_index()
probabilidades_por_distrito = age_percentages.groupby('Nom_Districte').apply(lambda x: dict(zip(x.Edat, x.Nombre))).to_dict()

#homeless assignation
homeless_per_district = [297, 32, 43, 34]
prob_homeless = homeless_per_district / total_people  #variable probabilty to study homeless behaviour

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
needs_list = ["food", "shelter", "sleep", "clothing", "health", "financial security", "employment", "education", "family", "friendship", "intimacy", "freedom", "status", "self-esteem"]
actions_dict = {
        'retired': ["go_home", "go_grocery", "go_hospital", "go_shopping", "go_leisure", "steal_food", "steal_clothes", "go_prison"],
        'employed': ["go_home", "go_grocery", "go_work", "go_hospital", "go_shopping", "go_leisure", "steal_food", "steal_clothes", "go_prison"],
        'unemployed': ["go_home", "go_grocery", "go_study", "go_hospital", "go_shopping", "go_leisure", "steal_food", "steal_clothes", "go_prison", "invest_high_education"],
        'student': ["go_home", "go_grocery","go_study", "go_hospital", "go_shopping", "go_leisure", "steal_food", "steal_clothes", "go_prison"],
        'homeless': ["go_grocery","go_hospital", "go_shopping", "go_leisure", "invest_high_education", "sleep_street", "beg", "steal_food", "steal_clothes", "go_hospital", "go_reception_center", "go_prison"]
        }
    
SAT_matrices = {}

for status, actions in actions_dict.items():
    SAT_matrix = [[0.0 for _ in range(len(actions))] for _ in range(len(needs_list))]
    for i, need in enumerate(needs_list):
        for j, action in enumerate(actions):
            # Assign specific SAT values based on need-action pairs
            # FOOD
            if need == "food" and action == "go_home":
                SAT_matrix[i][j] = 0.2
            elif need == "food" and action == "go_grocery":
                SAT_matrix[i][j] = 1.0
            elif need == "food" and action == "steal_food":
                SAT_matrix[i][j] = 0.6
            elif need == "food" and action == "go_reception_center":
                SAT_matrix[i][j] = 0.8
            elif need == "food" and action == "beg":
                SAT_matrix[i][j] = 0.4

            # SHELTER
            if need == "shelter" and action == "go_home":
                SAT_matrix[i][j] = 1.0
            if need == "shelter" and action == "go_reception_center":
                SAT_matrix[i][j] = 0.8
            

            # SLEEP
            if need == "sleep" and action == "go_home":
                SAT_matrix[i][j] = 0.8
            if need == "sleep" and action == "sleep_street":
                SAT_matrix[i][j] = 0.9
            
            # CLOTHING
            if need == "clothing" and action == "go_shopping":
                SAT_matrix[i][j] = 1.0
            elif need == "clothing" and action == "steal_clothes":
                SAT_matrix[i][j] = 0.3

            # HEALTH
            if need == "health" and action == "go_hospital":
                SAT_matrix[i][j] = 2.0

            # FINANCIAL SECURITY and EMPLOYMENT and EDUCATION
            if need in ["financial security", "employment", "education"] and (action == "go_work" or action == "invest_high_education"):
                SAT_matrix[i][j] = 1.0

            # FAMILY and FRIENDSHIP
            if need == "family" and action == "go_home":
                SAT_matrix[i][j] = 1.0
            if need == "family" and action == "go_leisure":
                SAT_matrix[i][j] = 0.6
            if need == "friendship" and action == "go_leisure":
                SAT_matrix[i][j] = 1.0
            elif need == "friendship" and action == "go_work":
                SAT_matrix[i][j] = 0.3

            # INTIMACY
            if need == "intimacy" and action == "go_home":
                SAT_matrix[i][j] = 1.0
            elif need == "intimacy" and action == "go_leisure":
                SAT_matrix[i][j] = 0.7

            # FREEDOM
            if need == "freedom" and (action == "go_home" or action == "go_leisure"):
                SAT_matrix[i][j] = 0.6
            elif need == "freedom" and action == "go_work":
                SAT_matrix[i][j] = 0.4

            # STATUS
            if need == "status" and action == "go_work":
                SAT_matrix[i][j] = 1.0

            # SELF-ESTEEM
            if need == "self-esteem" and (action == "go_leisure" or action == "go_shopping" or action == "go_work"):
                SAT_matrix[i][j] = 0.3

            # Default value
            if SAT_matrix[i][j] == 0.0:
                SAT_matrix[i][j] = 0.0
    SAT_matrices[status] = SAT_matrix

# Needs
needs = {
    'physiological': {
        'needs': ['food', 'shelter', 'sleep', 'health'],
        'weight': 0.9,
        'decaying': [ 0.4,  0.9,  0.8,  0.99 ],
        #'gamma': [0.8, 0.8, 0.6, 0.5],
        'mean and var': (0.7, 0.2)
    },
    'safety': {
        'needs': ['clothing', 'financial security', 'employment', 'education'],
        'weight': 0.6,
        'decaying': [ 0.9,  0.8,  0.8,  0.7 ],
        'mean and var': (0.8, 0.4)
    },
    'belonging': {
        'needs': ['family', 'friendship', 'intimacy'],
        'weight': 0.4,
        'decaying': [ 0.8,  0.7,  0.9 ],
        'mean and var': (0.6, 0.4)
    },
    'esteem': {
        'needs': ['freedom', 'status', 'self-esteem'],
        'weight': 0.2,
        'decaying': [ 0.89,  0.95,  0.85],
        'mean and var': (0.7, 0.4)
    }
}

#Norms

all_norms = [
        Norm("agx.status == \"unemployed\" and agx.model.schedule.time % 672 == 0", ["agx.wealth += 700"]), #ATUR (s'ha d'afegir que hagi cotitzat)
        #Norm("agx.home == None", ["agx.home == agx.model.districts[agx.district].generate_tuples(1, (0, 9), (0, 9))"]),   #Projecte de norma (no en vigor) 
        Norm("agx.sleep_street() and agx.wealth > 0", ["agx.wealth -= 500"]),  # Multa dormir si tenen diners (randomly?)
        Norm("agx.sleep_street() and agx.wealth <= 0", ["agx.go_prison()"]),  # Multa dormir si no tenen diners
        #Norm("agx.status == \"homeless\"", ["agx.go_reception_center()"]), #Ja feta en les propies available actions
        Norm("agx.wealth <= 0 and agx.model.schedule.time % 672 == 0" , ["agx.home == None"]),  #Eviction for rent
        Norm("agx.wealth <= 0 and agx.model.schedule.time % 672 == 0", ["agx.wealth += 735"]), #minimal vital income
    ]

print(prob_homeless)