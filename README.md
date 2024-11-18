# An Agent-Based Model for Poverty and Discrimination Policy-Making

The aim of this project is to study the effect of aporophobic and non-aporophobic regulatory policies using an agent-based model (ABM). This simulation is populated by autonomous decision-making agents built from real demographic data. In particular, we extract data from [Open Data Barcelona portal](https://opendata-ajuntament.barcelona.cat/), filtering for four different Barcelona districts. This study seeks to analyze the effect of norms, labelled as aporophobic or non-aporophobic by legal experts, on the levels of poverty and inequality. 

This repository is based on methods from Aguilera et al. (2024) [1].

## Structure
The Github repository is structured in three main folders containing: 

1. **Model Formulation**: main code files, *data.py* initializes the agents' profiles and policies, city creates the physical environment, *model.py* and *agent.py* describe the individual step and action deliberation of the agents and *norms.py* defines the functioning of the policies affecting the simulation.
   - **model**
   - **agent**
   - **city**
   - **data**
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
To run this project, you’ll need:

- Python 3.7
- Required packages in requirements.txt

## Contact

For questions or collaborations, please reach out to the project maintainer, Alba Aguilera (aaguilera@iiia.csic.es).

## References

1. Aguilera, A., Montes, N., Curto, G., Sierra, C., & Osman, N. (2024) *Can Poverty Be Reduced by Acting on Discrimination? An Agent-based Model for Policy Making*. IFAAMAS, DOI: [https://dl.acm.org/doi/10.5555/3635637.3662848]([(https://www.ifaamas.org/Proceedings/aamas2024/pdfs/p22.pdf))



