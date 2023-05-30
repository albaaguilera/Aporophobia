from model import CityModel, lista_distritos, all_norms
import itertools
import matplotlib.pyplot as plt

# Script parameters
N = 5000000
T = 5000
M = 500

# Power set
def powerset(s):
    power_set = []
    for r in range(len(s)+1):
        for subset in itertools.combinations(s, r):
            power_set.append(list(subset))
    return power_set

# Loop model
for config in range(M):
    for norm in powerset(all_norms):
        barcelona = CityModel('Barcelona', lista_distritos, N, all_norms)
        for i in range(T):
            barcelona.step()

#Data Collectors
positions = barcelona.datacollector.get_model_vars_dataframe()
nsl_wealth = barcelona.datacollector.get_agent_vars_dataframe()

final_wealth = nsl_wealth.xs(max(nsl_wealth.index.get_level_values('Step')), level='Step')['wealth']

#Final Wealth Distribution
plt.hist(final_wealth, bins=30)
plt.xlabel('Wealth')
plt.ylabel('Frequency')
plt.title('Distribution of Agent Wealth')
plt.show()

# NSL Evolution of just one need: food
nsl_wealth['physiological'] = nsl_wealth['physiological'].apply(lambda x: x[0])
nsl_wealth_pivot = nsl_wealth['physiological'].unstack(level=1)
plt.figure(figsize=(10, 6))
for agent_id in nsl_wealth_pivot.columns:
    plt.plot(nsl_wealth_pivot.index, nsl_wealth_pivot[agent_id], label=f"Agent {agent_id}")

plt.xlabel('Step')
plt.ylabel('Physiological Need - Food')
plt.title('Evolution of Physiological Need - Food')
plt.legend()
plt.show()

# NSL Distribution of the global values for: food
food_nsl_values = nsl_wealth['physiological'].values.flatten()
plt.figure(figsize=(10, 6))
plt.hist(food_nsl_values, bins=20, edgecolor='black')
plt.xlabel('NSL Value for Food')
plt.ylabel('Frequency')
plt.title('Distribution of NSL Values for Food')
plt.show()

# Save data into csv
nsl_wealth.to_csv(r'"C:/Users/albaa/Downloads/nsl_wealth.csv"', index=False, header=True)