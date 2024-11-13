# An Agent-Based Model for Poverty and Discrimination Policy-Making

The aim of this project is to study the effect of aporophobic and non-aporophobic regulatory policies using an agent-based model (ABM). This simulation is populated by autonomous decision-making agents built from real demographic data. In particular, we extract data from [Open Data Barcelona portal](https://opendata-ajuntament.barcelona.cat/), filtering for four different Barcelona districts. This study seeks to analyze the effect of norms, labelled as aporophobic or non-aporophobic by legal experts, on the levels of poverty and inequality. 

The Github repository is structured in three main folders containing: 

1. **Model Formulation**: main code files.
   - **model**
   - **agent**
   - **city**
   - **data**: input of the simulation, reads and treats demographic data and fills the SATS and NSL initial parameters depending on status.
   - **norms**
3. **Open Data**: input of the simulation, demographic datasets required to initialize the simulation.
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

For questions or collaborations, please reach out to the project maintainer, Alba Aguilera.


