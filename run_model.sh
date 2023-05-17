#!/bin/bash

# sbatch options
#SBATCH --job-name=aporo_model_runs
#SBATCH --time=00-24:00:00
#SBATCH --mem-per-cpu=2G

#SBATCH --output=/home/nmontes/logs/%x-%j.log
#SBATCH --error=/home/nmontes/logs/%x-%j.err
#SBATCH --mail-user=nmontes@iiia.csic.es

# You must carefully match tasks, cpus, nodes,
# and cpus-per-task for your job. See docs.
#SBATCH --tasks=1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=20
#SBATCH --tasks-per-node=1

/home/nmontes/.conda/envs/aporo/bin/python run_model.py
