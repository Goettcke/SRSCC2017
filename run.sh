#!/bin/bash

#SBATCH --account sdusscsa1_slim
#SBATCH --nodes 1
#SBATCH --time 23:59:00
#SBATCH -o slurm-dump/slurm.%N.%j.out # stdout
#SBATCH -e slurm-dump/slurm.%N.%j.err # stderr

./main.py $1 $2 4 $3
