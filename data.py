
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


def assign_district():
    district_probabilities = total_people / total_people.sum()
    district_selected = np.random.choice(total_people.index, p=district_probabilities)
    return district_selected

probabilidades_edades = probabilidades_por_distrito['Gràcia']

# duplicado
districtes = ['Gràcia', 'Sarrià-Sant Gervasi', 'Les Corts', 'Eixample']
edat2020 = pd.read_csv("OpenData/2020_ine_edat_any_a_any_per_sexe.csv")
edat2020 = edat2020[edat2020['Nom_Districte'].isin(districtes)]
edat2020['Edat'] = edat2020['Edat_any_a_any'].str.extract('(\d+)').astype(int)
total_people = edat2020.groupby(['Nom_Districte'])['Nombre'].sum()
age_counts = edat2020.groupby(['Nom_Districte', 'Edat'])['Nombre'].sum()
age_percentages = age_counts / total_people
age_percentages = age_percentages.reset_index()
probabilidades_por_distrito = age_percentages.groupby('Nom_Districte').apply(lambda x: dict(zip(x.Edat, x.Nombre))).to_dict()

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
    needs_list = ["food", "shelter", "sleep", "clothing", "health", "financial security", "employment", "family", "friendship", "intimacy", "freedom", "status", "self-esteem"]
    actions_list = ["go_home", "go_grocery", "go_work", "go_hospital", "go_shopping", "go_leisure"]
    """
    #1ERA MANERA 
    # Initialize the matrix with zeros
    SAT_matrix = [[0.0 for _ in range(len(actions_list))] for _ in range(len(needs_list))]
    for i, n in enumerate(needs_list):
        for j, a in enumerate(actions_list):
            if n == "food" and a == "go_home":
                SAT_matrix[i][j] = 0.8
            elif n == "food" and a == "go_grocery":
                SAT_matrix[i][j] = 0.9
            else:
                # Assign a default SAT value of 0.5 for all other pairs
                SAT_matrix[i][j] = 0.5
                """
    #2na manera
    SAT_values = [
        [0.8, 0.9, 0.4, 0.9, 0.1, 0.1],
        [0.9, 0.1, 0.6, 0.2, 0.3, 0.3],
        [0.2, 0.2, 0.1, 0.2, 0.1, 0.1],
        [0.1, 0.1, 0.2, 0.1, 0.9, 0.3],
        [0.3, 0.1, 0.1, 0.8, 0.1, 0.1],
        [0.1, 0.1, 0.9, 0.1, 0.1, 0.1],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.3, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.4, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    ]

    # Create a matrix of SAT values
    SAT_matrix = np.array(SAT_values)

    def get_SAT(n, a):  #to get a certain value with a cerrtain string need or action
        i = needs_list.index(n)
        j = actions_list.index(a)
        return SAT_matrix[i][j]

# Dictionary of Sat matrices for each STATUS
SAT_retired = [
        [0.8, 0.9, 0.4, 0.9, 0.1, 0.1],
        [0.9, 0.2, 0.6, 0.2, 0.3, 0.3],
        [0.2, 0.1, 0.1, 0.2, 0.1, 0.1],
        [0.1, 0.3, 0.2, 0.1, 0.9, 0.3],
        [0.3, 0.1, 0.1, 0.8, 0.1, 0.1],
        [0.1, 0.1, 0.9, 0.1, 0.1, 0.1],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.9, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.9, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.9, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.9, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.9, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    ]

SAT_student = [
        [0.8, 0.9, 0.4, 0.9, 0.1, 0.1],
        [0.9, 0.2, 0.6, 0.2, 0.3, 0.3],
        [0.2, 0.1, 0.1, 0.2, 0.1, 0.1],
        [0.1, 0.3, 0.2, 0.1, 0.9, 0.3],
        [0.3, 0.1, 0.1, 0.8, 0.1, 0.1],
        [0.1, 0.1, 0.9, 0.1, 0.1, 0.1],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.9, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.9, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.9, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.9, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.9, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    ]
SAT_employed = [
        [0.8, 0.9, 0.4, 0.9, 0.1, 0.1],
        [0.9, 0.2, 0.6, 0.2, 0.3, 0.3],
        [0.2, 0.1, 0.1, 0.2, 0.1, 0.1],
        [0.1, 0.3, 0.2, 0.1, 0.9, 0.3],
        [0.3, 0.1, 0.1, 0.8, 0.1, 0.1],
        [0.1, 0.1, 0.9, 0.1, 0.1, 0.1],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.9, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.9, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.9, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.9, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.9, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    ]
SAT_unemployed = [
        [0.8, 0.9, 0.4, 0.9, 0.1, 0.1],
        [0.9, 0.2, 0.6, 0.2, 0.3, 0.3],
        [0.2, 0.1, 0.1, 0.2, 0.1, 0.1],
        [0.1, 0.3, 0.2, 0.1, 0.9, 0.3],
        [0.3, 0.1, 0.1, 0.8, 0.1, 0.1],
        [0.1, 0.1, 0.9, 0.1, 0.1, 0.1],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.9, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.9, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.9, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.9, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.9, 0.5, 0.5, 0.5, 0.5],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    ]

SAT_matrices = {
    'retired': np.array(SAT_retired),
    'student': np.array(SAT_student),
    'employed': np.array(SAT_employed),
    'unemployed': np.array(SAT_unemployed)
}

SAT_matrices['retired']

needs = {
    'physiological': {
        'needs': ['food', 'shelter', 'sleep', 'health'],
        'weight': 0.9,
        'decaying': [ 0.8,  0.5,  0.7,  0.3 ],
        'initial':  0.9
    },
    'safety': {
        'needs': ['clothing', 'financial security', 'employment'],
        'weight': 0.6,
        'decaying': [ 0.5,  0.6,  0.5 ],
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

needs.items()