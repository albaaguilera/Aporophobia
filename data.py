
import pandas as pd
import numpy as np

districtes = ['Gràcia', 'Sarrià-Sant Gervasi', 'Les Corts', 'Eixample']
renda2020 = pd.read_csv("OpenData/2020_renda_neta_mitjana_per_persona.csv")
renda2020['Nom_Districte'] = renda2020['Nom_Districte'].replace("L'Eixample", "Eixample")
renda2020 = renda2020[renda2020['Nom_Districte'].isin(districtes)]
pd.unique(renda2020['Nom_Districte'])
renda2020['Import_Euros'] = renda2020['Import_Euros'] / 12
district_wealth = {}
for district in districtes:
    district_wealth[district] = renda2020[renda2020['Nom_Districte'] == district]

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
prob_homeless = homeless_per_district / total_people * 100

gender_counts = edat2020.groupby(['Nom_Districte', 'Sexe'])['Nombre'].sum()
gender_percentages = gender_counts / total_people
gender_percentages = gender_percentages.reset_index()
probabilidades_por_distrito_gender = gender_percentages.groupby('Nom_Districte').apply(lambda x: dict(zip(x.Sexe, x.Nombre))).to_dict()

def assign_district():
    district_probabilities = total_people / total_people.sum()
    district_selected = np.random.choice(total_people.index, p=district_probabilities)
    return district_selected

renda2020 = pd.read_csv("OpenData/2020_renda_neta_mitjana_per_persona.csv")
renda2020['Nom_Districte'] = renda2020['Nom_Districte'].replace("L'Eixample", "Eixample")
renda2020 = renda2020[renda2020['Nom_Districte'].isin(districtes)]
renda2020['Import_Euros'] = renda2020['Import_Euros'] / 12
district_wealth = {}
for district in districtes:
    district_wealth[district] = renda2020[renda2020['Nom_Districte'] == district]

#SAT
    needs_list = ["food", "shelter", "sleep", "clothing", "health", "financial security", "employment", "education", "family", "friendship", "intimacy", "freedom", "status", "self-esteem"]
    actions_dict = {
        'retired': ["go_home", "go_grocery", "go_hospital", "go_shopping", "go_leisure"],
        'employed': ["go_home", "go_grocery", "go_work", "go_hospital", "go_shopping", "go_leisure"],
        'unemployed': ["go_home", "go_grocery", "go_school", "go_hospital", "go_shopping", "go_leisure"],
        'student': ["go_home", "go_grocery","go_school", "go_hospital", "go_shopping", "go_leisure"],
        'homeless': ["go_grocery","go_hospital", "go_shopping", "go_leisure", "invest_high_education"]
        }
    
    SAT_matrices = {}

# Loop through each status category in actions_dict
for status, actions in actions_dict.items():
    # Initialize the SAT matrix with zeros
    SAT_matrix = [[0.0 for _ in range(len(actions))] for _ in range(len(needs_list))]
    for i, need in enumerate(needs_list):
        for j, action in enumerate(actions):
            # Assign specific SAT values based on need-action pairs
            if need == "food" and action == "go_home":
                if status == "retired":
                    SAT_matrix[i][j] = 0.8
                elif status == "student":
                    SAT_matrix[i][j] = 0.7
                else:
                    SAT_matrix[i][j] = 0.5
            elif need == "food" and action == "go_grocery":
                SAT_matrix[i][j] = 0.9

            elif need == "health" and action == "go_hospital":
                if status == "retired":
                    SAT_matrix[i][j] = 0.9
                else:
                    SAT_matrix[i][j] = 0.6
            elif need == "friendship" and action == "go_leisure":
                if status == "student":
                    SAT_matrix[i][j] = 0.8
                else:
                    SAT_matrix[i][j] = 0.4
            else:
                # Assign a default SAT value of 0.5 for all other pairs
                SAT_matrix[i][j] = 0.5
    # Add the SAT matrix to the dictionary with the status category as the key
    SAT_matrices[status] = SAT_matrix


needs = {
    'physiological': {
        'needs': ['food', 'shelter', 'sleep', 'health'],
        'weight': 0.9,
        'decaying': [ 0.8,  0.5,  0.7,  0.3 ],
        'initial':  0.9
    },
    'safety': {
        'needs': ['clothing', 'financial security', 'employment', 'education'],
        'weight': 0.6,
        'decaying': [ 0.5,  0.6,  0.5,  0.5 ],
        'initial':  0.8
    },
    'belonging': {
        'needs': ['family', 'friendship', 'intimacy'],
        'weight': 0.4,
        'decaying': [ 0.3,  0.4,  0.2 ],
        'initial':  0.8
    },
    'esteem': {
        'needs': ['freedom', 'status', 'self-esteem'],
        'weight': 0.2,
        'decaying': [ 0.2,  0.1,  0.3],
        'initial':  0.7
    }
}

#needs.items()