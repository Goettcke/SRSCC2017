#!/bin/bash

#SBATCH --account sdusscsa1_slim
#SBATCH --nodes 1
#SBATCH --time 23:59:00
#SBATCH -o slurm-dump/slurm.%N.%j.out # stdout
#SBATCH -e slurm-dump/slurm.%N.%j.err # stderr

set -o xtrace

rm -f *.pyc
rm -rf *.zip
rm -f slurm-dump/*
rm -rf output*sample
mkdir -p stash
mv output* stash
rm -rf stash/output*
rm -rf stash
