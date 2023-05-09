for r in {0..1000}; do 

echo Running for r-$r

python3 run_preprocess_2D.py --path_results "/home/user/projects/papers/2023_homogenisation/figures/results_ensemble-preprocess/r-$r"; 

done

echo Calculating statistics...

python3 run_ensemble-preprocess-stats.py