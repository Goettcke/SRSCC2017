#!/bin/bash



INTERVALS=(0 100000 200000 300000 400000 500000 600000 
             700000 800000 900000 1000000 1100000 1200000 1300000 1400000 1485838)

for (( i=0; i<${#INTERVALS[*]}-1; ++i)); do
    sbatch run.sh ${INTERVALS[$i]} ${INTERVALS[$(( $i+1 ))]} ${1:-"default.ini"}
done
