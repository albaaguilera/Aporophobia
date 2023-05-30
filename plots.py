
# PLOTS FOR THE FIRST TRIAL WITH 5 AGENTS

# EVOLUTION OF NSL OF A CERTAIN CATEGORY

import matplotlib.pyplot as plt
import pandas as pd
import ast

# Import data
nsl_wealth = pd.read_csv("C:/Users/albaa/Escriptori/MasterModelitzacio/JAE/pythonmesa/mesa/aporophobia/con_norms/nsl_wealth.csv")

#Choose category
category = 'physiological'

nsl_wealth[category] = nsl_wealth[category].apply(ast.literal_eval)

belonging_needs = ['family', 'friendship', 'intimacy']
physiological_needs = ['food', 'shelter', 'sleep', 'health']

# Plot the evolution of the first value for each physiological need
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

for i, need in enumerate(physiological_needs):
    row = i // 2
    col = i % 2
    ax = axs[row, col]

    # Extract the first value of each list for all agents
    first_values = nsl_wealth[category].apply(lambda x: x[i])

    # Plot the evolution of the first value for each agent
    for agent_id in range(5):
        agent_first_values = first_values[agent_id::5]  
        ax.plot(range(len(agent_first_values)), agent_first_values, label=f'Agent {agent_id+1}')

    ax.set_ylabel(f'NSL {need.capitalize()}')
    ax.set_title(f'NSL\'s evolution of {need.capitalize()} Need')
    ax.legend()

    ax.set_xticks(range(0, len(agent_first_values), 8))  
    ax.set_xticklabels(range(8, 8 + len(agent_first_values), 8))  

    # Add labels every 24 ticks (1 day)
    day_labels = range(1, len(agent_first_values) // 24 + 1)
    for tick_pos, day_label in zip(range(0, len(agent_first_values), 24), day_labels):
        ax.text(tick_pos, -0.1, f'{day_label} day', transform=ax.get_xaxis_transform(), ha='center', va= 'baseline')

    ax.set_xlabel("Model hour", labelpad=10)

plt.tight_layout()
plt.show()


# DISTRIBUTION OF ACTIONS
nsl_wealth = nsl_wealth.dropna(subset=["actions"])

action_counts = nsl_wealth["actions"].value_counts()
plt.bar(action_counts.index, action_counts.values)
plt.xlabel("Actions")
plt.ylabel("Frequency")
plt.title("Distribution of Actions")
plt.xticks(rotation=90)
plt.show()

# EVOLUTION OF WEALTH 



# DISTRIBUTION OF FINAL WEALTH



