#!/bin/bash

#
#SBATCH --account sdusscsa1_slim
#SBATCH --nodes 1
#SBATCH --time 23:59:00

./main.py $1 $2 4 $3
