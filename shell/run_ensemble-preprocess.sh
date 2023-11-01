#!/bin/bash

# Local
path_start=/home/user/projects/papers/2023_homogenisation/figures/results_ensemble-preprocess

# Remote
#path_start="/scratch/wey/2023_homogenisation/figures/results_ensemble-preprocess"

declare -i num_nodes=4
initialisation=4-reg
declare -i r_max=50

#for r in $vals; do 
for ((r=0;r<=${r_max};r+=1)); do

echo "Running for r-${r} of r_max-${r_max}"

path_add_sim=_init-${initialisation}_N-${num_nodes}
path_add_rep=/r-${r} 

path_sim=${path_start}${path_add_sim}
path_rep=${path_start}${path_add_sim}${path_add_rep}

python3 run_preprocess_2D.py --path_results $path_rep --num_nodes $num_nodes --initialisation $initialisation; 

done

echo Calculating statistics...

python3 run_ensemble-preprocess-stats.py --path_results ${path_sim} --num_nodes $num_nodes --initialisation $initialisation --r_max ${r_max}

