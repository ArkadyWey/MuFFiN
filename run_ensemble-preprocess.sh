for r in {0..20000}; do 

echo Running for r-$r

# Local
#python3 run_preprocess_2D.py --path_results "/home/user/projects/papers/2023_homogenisation/figures/results_ensemble-preprocess/r-$r"; 

# Remote
python3 run_preprocess_2D.py --path_results "/scratch/wey/2023_homogenisation/figures/results_ensemble-preprocess/r-$r"; 

done

echo Calculating statistics...

python3 run_ensemble-preprocess-stats.py