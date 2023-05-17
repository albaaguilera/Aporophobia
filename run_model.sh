#!/bin/bash

# sbatch options
#SBATCH --job-name=aporo_model_runs
#SBATCH --time=00-24:00:00
#SBATCH --mem-per-cpu=2G

#SBATCH --output=/home/nmontes/logs/%x-%j.log
#SBATCH --error=/home/nmontes/logs/%x-%j.err
#SBATCH --mail-user=nmontes@iiia.csic.es

for i in {1..$SLURM_JOB_NUM_NODES}
do
    srun --nodes 1 --ntasks 1 --cpus-per-task 20 --exclusive /home/nmontes/.conda/envs/aporo/bin/python run_model.py &
done

wait
