# Aporophobia

An agent-based model to study the relationship between institutional aporophobia and poverty.

The uploaded files in the citymodel branch describe a district/partitioned grid with a number of agents N with ages X proportional to real data of each district extracted from OpenData BCN. The corresponding houses locations are randomly generated. 

The uploaded files with Needs Model implementation message describe the Needs model method, the agent class holds a needs class dictionary, SAT values, and NSL values stored in the data.py file. The action in the time step t is decided taking the maximum score of [1] in the Needs Model paper. 

