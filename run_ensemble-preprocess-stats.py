import numpy
import os 

path_results = "/home/user/projects/papers/2023_homogenisation/figures/results_ensemble-preprocess/"

r_max = 20000

perm_prep_4 = [] # [r_max+1,k,m,n] 
depo_prep_3 = [] # [r_max+1,k,m]


# Collect results in lists
for r in range(r_max+1):
    path_results_r = os.path.join(path_results,"r-{}".format(r))

    perm_prep_3 = numpy.load(os.path.join(path_results_r, "perm_prep_3.npy"))
    depo_prep_2 = numpy.load(os.path.join(path_results_r, "depo_prep_2.npy"))

    perm_prep_4.append(perm_prep_3)
    depo_prep_3.append(depo_prep_2)

# Convert lists to numpy arrays
perm_prep_4 = numpy.array(perm_prep_4)
depo_prep_3 = numpy.array(depo_prep_3)

# Calculate statistics
perm_prep_av_3 = numpy.mean(a=perm_prep_4, axis=0)
depo_prep_av_2 = numpy.mean(a=depo_prep_3, axis=0)

perm_prep_sd_3 = numpy.std(a=perm_prep_4, axis=0)
depo_prep_sd_2 = numpy.std(a=depo_prep_3, axis=0)


# Save statistics
path_results = "/home/user/projects/papers/2023_homogenisation/figures/results_ensemble-preprocess/stats"
if not os.path.exists(path_results):
    os.mkdir(path_results)

# Save means
numpy.save(file=os.path.join(path_results,"perm_prep_av_3.npy"), arr=perm_prep_av_3, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_results,"depo_prep_av_2.npy"), arr=depo_prep_av_2, allow_pickle=True, fix_imports=True)

# Save stds
numpy.save(file=os.path.join(path_results,"perm_prep_sd_3.npy"), arr=perm_prep_sd_3, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_results,"depo_prep_sd_2.npy"), arr=depo_prep_sd_2, allow_pickle=True, fix_imports=True)