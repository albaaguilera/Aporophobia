# An Agent-Based Model (ABM) for Poverty and Discrimination Policy-Making
-----
## Description

The Aporophobia Agent-Based Model (AABM) is a multiagent system simulation designed to represent the daily lives of citizens influenced by legal norms.These individuals are created based on real-life demographic data from certain districts within a city, while the norms reflect real-world policies inforced in that city. For this initial version of the model, we choose 4 districts within Barcelona.  In particular, we extract data from [Open Data Barcelona portal](https://opendata-ajuntament.barcelona.cat/), filtering for four different Barcelona districts. 

On the other hand, aporophobia is a term coined by Adela Cortina in 2017, refering to the rejection of the poor. This discrimination against a minority has been officially recalled as an aggravating factor for hate crimes ([2021](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2019-7771)).  This study seeks to analyze the effect of norms, labelled either as aporophobic or non-aporophobic by legal experts on poverty and inequality, into the behaviour and economy of the agents. By using this social simulation, we are able to examine the impact that aporophobia, within the legal framework, has on poverty and inequality levels. These insights can then inform the development of a new generation of policy-making for poverty reduction.   

The AABM is built using Python's Agent-Based Model (ABM) library Mesa, used for building, analyzing and visualizing ABMs ([Mesa](https://mesa.readthedocs.io/en/stable/)). The city is constructed as a virtual grid with different locations associated to buildings. The agents represent citizens with a unique personal profile including attributes like gender, age, status, etc. Additionally, the agents are programmed to make autonomous decision with a methodology inspired by the Needs-based Model (Dignum et al., [Needs-based Model](https://simassocc.org/)), which allows agent to decide on their actions based on their personal profile and needs. 

To assess the poverty and inequality levels resulting from the implemented policies, statistical samples of the resulting wealth distributions and computed Gini Coefficients are utilized. These metrics are a valuable indicator of the outcomes of the policies under examination.

This repository is based on methods from *Aguilera et al*. (2024) [1], *Nieves et al*. (2023) [2].

## Structure
The Github repository is structured in three main folders containing: 

1. **Model Formulation**: main code files, *data.py* initializes the agents' profiles and policies, city creates the physical environment, *model.py* and *agent.py* describe the individual step and action deliberation of the agents and *norms.py* defines the functioning of the policies affecting the simulation.
   - **data**
   - **city**
   - **model**
   - **agent**
   - **norms**
3. **Open Data**: demographic datasets required to initialize the simulation.
   - 2018_age_by_gender.csv
   - 2019_income.csv
   - 2022_rent.csv
   - 2021_unemployment_by_gender.csv
5. **Results**: submission scripts to the cluster, zip folder with the output of the simulation and analysis of it through wealth distributions and gini computation.
   - **run_cluster.ssh**
   - **run_cluster.py**
   - **resultatssimulacionscluster.zip**
   - **cluster.ipnyb**

There is a ![UML diagram](diagram.mmd) to illustrate the dependencies between the different code files in Model Formulation. 

## Getting Started 
To use the AABM, clone the repository into your local file system:

.. code-block:: bash

    git clone https://github.com/aaguilera/Aporophobia-ABM.git


## Contact

For questions or collaborations, please reach out to the project maintainer, Alba Aguilera (aaguilera@iiia.csic.es).

## References

1. Aguilera, A., Montes, N., Curto, G., Sierra, C., & Osman, N. (2024) *Can Poverty Be Reduced by Acting on Discrimination? An Agent-based Model for Policy Making*. IFAAMAS, DOI: [https://dl.acm.org/doi/10.5555/3635637.3662848]([(https://www.ifaamas.org/Proceedings/aamas2024/pdfs/p22.pdf))
2. Montes, N., Curto, G., Osman, N., & Sierra, C. (2023). An Agent-Based Model for Poverty and Discrimination Policy-Making. arXiv preprint arXiv:2303.13994.



