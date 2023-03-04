
import pandas as pd
import mesa
import numpy as np
import matplotlib.pyplot as plt
from Apo_model_agent import Apo_Agent, Apo_Model
from typing import Dict, List, Tuple
from matplotlib.colors import ListedColormap

income = pd.read_csv('C:/Users/albaa/Escriptori/MasterModelitzacio/JAE/pythonmesa/mesa/2020_atles_renda_bruta_persona.csv')
monthly_wealth = np.array(income['Import_Renda_Bruta_€']) / 12

# Define the color map using a list of colors
color_list = ["lightgrey", "orange", "red"]
wealth_cmap = ListedColormap(color_list)

def agent_portrayal(agent):
    # Map the agent's wealth to an index in the color map
    wealth_index = int(agent.wealth / (max(monthly_wealth) - min(monthly_wealth)) * (len(color_list) - 1))
    
    # Set the portrayal properties
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5,
                 "Layer": 0,
                 "Color": wealth_cmap(wealth_index)}
    
    if agent.wealth <= 1000:
        portrayal["r"] = 0.2
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
    else:
        portrayal["r"] = 0.2
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1    
    return portrayal

grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = mesa.visualization.ModularServer(
    Apo_Model, [grid], "Aporophobia Model", {"N": 5, "width": 10, "height": 10, "wealth_list": monthly_wealth}
)
server.port = 8521  # The default
server.launch()