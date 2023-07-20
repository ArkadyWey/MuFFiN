import numpy
import os 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-pr",    "--path_results",  type=str, help="Path to results")
parser.add_argument("-rm",    "--r_max",         type=int, help="Number of repeated simulations")
parser.add_argument("-N",     "--num_nodes",     type=int, help="Number of nodes in cell")
parser.add_argument("-init",  "--initialisation",type=str, help="Structure of cell")
args = parser.parse_args()
path_results   = args.path_results
r_max          = args.r_max 
initialisation = args.initialisation
num_nodes      = args.num_nodes

perm_prep_4 = [] # [r_max+1,k,m,n] 
depo_prep_3 = [] # [r_max+1,k,m]
delt_6      = [] # [r_max+1,k,i,j,r,m]
cond_tabl_6 = [] # [r_max+1,k,i,j,r,m]


# Collect results in lists
for r in range(r_max+1):
    path_results_r = os.path.join(path_results,"r-{}".format(r))
    
    perm_prep_3 = numpy.load(os.path.join(path_results_r, "perm_prep_3.npy"))
    depo_prep_2 = numpy.load(os.path.join(path_results_r, "depo_prep_2.npy"))
    delt_5      = numpy.load(os.path.join(path_results_r, "delt_5.npy"))
    cond_tabl_5 = numpy.load(os.path.join(path_results_r, "cond_tabl_5.npy"))

    perm_prep_4.append(perm_prep_3)
    depo_prep_3.append(depo_prep_2)
    delt_6.append(delt_5)
    cond_tabl_6.append(cond_tabl_5)

    if r==0:
        conc_max_or_tot_1 = numpy.load(os.path.join(path_results_r, "conc_max_or_tot_1.npy"))
    else: 
        pass

# Convert lists to numpy arrays
perm_prep_4 = numpy.array(perm_prep_4)
depo_prep_3 = numpy.array(depo_prep_3)
delt_6      = numpy.array(delt_6)
cond_tabl_6 = numpy.array(cond_tabl_6)

# Calculate statistics
perm_prep_av_3 = numpy.mean(a=perm_prep_4, axis=0)
depo_prep_av_2 = numpy.mean(a=depo_prep_3, axis=0)
delt_av_5      = numpy.mean(a=delt_6,      axis=0)
cond_tabl_av_5 = numpy.mean(a=cond_tabl_6, axis=0)

perm_prep_sd_3 = numpy.std(a=perm_prep_4, axis=0)
depo_prep_sd_2 = numpy.std(a=depo_prep_3, axis=0)
delt_sd_5      = numpy.std(a=delt_6,      axis=0)
cond_tabl_sd_5 = numpy.std(a=cond_tabl_6, axis=0)

# Save statistics
#path_results = "/home/user/projects/papers/2023_homogenisation/figures/results_ensemble-preprocess/stats"
path_stats = os.path.join(path_results,"stats_init-{}_N-{}".format(initialisation,num_nodes))
if not os.path.exists(path_stats):
    os.mkdir(path_stats)

# Save x axis 
numpy.save(file=os.path.join(path_stats,"conc_max_or_tot_1.npy"), arr=conc_max_or_tot_1, allow_pickle=True, fix_imports=True)

# Save means
numpy.save(file=os.path.join(path_stats,"perm_prep_av_3.npy"), arr=perm_prep_av_3, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_stats,"depo_prep_av_2.npy"), arr=depo_prep_av_2, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_stats,"delt_av_5.npy"),      arr=delt_av_5,      allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_stats,"cond_tabl_av_5.npy"), arr=cond_tabl_av_5, allow_pickle=True, fix_imports=True)


# Save stds
numpy.save(file=os.path.join(path_stats,"perm_prep_sd_3.npy"), arr=perm_prep_sd_3, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_stats,"depo_prep_sd_2.npy"), arr=depo_prep_sd_2, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_stats,"delt_sd_5.npy"),      arr=delt_sd_5,      allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_stats,"cond_tabl_sd_5.npy"), arr=cond_tabl_sd_5, allow_pickle=True, fix_imports=True)


# Save entire results (for distributions)
path_fulls = os.path.join(path_results,"fulls_init-{}_N-{}".format(initialisation,num_nodes))
if not os.path.exists(path_fulls):
    os.mkdir(path_fulls)

numpy.save(file=os.path.join(path_fulls,"perm_prep_4.npy"), arr=perm_prep_4, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_fulls,"depo_prep_3.npy"), arr=depo_prep_3, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_fulls,"delt_6.npy"),      arr=delt_6,      allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_fulls,"cond_tabl_6.npy"), arr=cond_tabl_6, allow_pickle=True, fix_imports=True)
