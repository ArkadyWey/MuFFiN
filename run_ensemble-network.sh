for r in {0..10}; do 

echo Running for r-$r

# Local
#python3 run_network.py --path_results "/home/user/projects/papers/2023_homogenisation/figures/results_ensemble-network/r-$r"; 

# Remote
python3 run_network.py --path_results "/scratch/2023_homogenisation/figures/results_ensemble-network/r-$r"; 

done

echo Calculating statistics...

python3 run_ensemble-network-stats.py