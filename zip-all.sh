#!/bin/bash

#SBATCH --account sdusscsa1_slim
#SBATCH --nodes 1
#SBATCH --time 23:59:00
#SBATCH -o slurm-dump/zip-all-slurm.%N.%j.out # stdout
#SBATCH -e slurm-dump/zip-all-slurm.%N.%j.err # stderr

for folder in "$@"; do
    zip "$folder.zip" -r "$folder"
done

wait
