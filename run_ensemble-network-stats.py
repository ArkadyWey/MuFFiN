import numpy
import os 

path_results = "/home/user/projects/papers/2023_homogenisation/figures/results_ensemble-network/"

r_max = 10

conc_3 = [] # [r_max+1,num_times,num_nodes_with_out]
pres_3 = [] # [r_max+1,num_times,num_nodes_with_out]
volu_3 = [] # [r_max+1,num_times,num_nodes_with_out]
cond_4 = [] # [r_max+1,num_times,num_nodes_with_out,num_nodes_with_outc]
adhe_4 = [] # [r_max+1,num_times,num_nodes_with_out,num_nodes_with_outc]

# Collect results in lists
for r in range(r_max+1):
    path_results_r = os.path.join(path_results,"r-{}".format(r))

    conc_2 = numpy.load(os.path.join(path_results_r, "conc_2.npy"))
    pres_2 = numpy.load(os.path.join(path_results_r, "pres_2.npy"))
    volu_2 = numpy.load(os.path.join(path_results_r, "volu_2.npy"))
    cond_3 = numpy.load(os.path.join(path_results_r, "cond_3.npy"))
    adhe_3 = numpy.load(os.path.join(path_results_r, "adhe_3.npy"))

    conc_3.append(conc_2)
    pres_3.append(pres_2)
    volu_3.append(volu_2)
    cond_4.append(cond_3)
    adhe_4.append(adhe_3)

# Convert lists to numpy arrays
conc_3 = numpy.array(conc_3)
pres_3 = numpy.array(pres_3)
volu_3 = numpy.array(volu_3)
cond_4 = numpy.array(cond_4)
adhe_4 = numpy.array(adhe_4)

# Calculate statistics
conc_av_2 = numpy.mean(a=conc_3, axis=0)
pres_av_2 = numpy.mean(a=pres_3, axis=0)
volu_av_2 = numpy.mean(a=volu_3, axis=0)
cond_av_3 = numpy.mean(a=cond_4, axis=0)
adhe_av_3 = numpy.mean(a=adhe_4, axis=0)

conc_sd_2 = numpy.std(a=conc_3, axis=0)
pres_sd_2 = numpy.std(a=pres_3, axis=0)
volu_sd_2 = numpy.std(a=volu_3, axis=0)
cond_sd_3 = numpy.std(a=cond_4, axis=0)
adhe_sd_3 = numpy.std(a=adhe_4, axis=0)

# Save statistics
path_results = "/home/user/projects/papers/2023_homogenisation/figures/results_ensemble-network/stats"
if not os.path.exists(path_results):
    os.mkdir(path_results)

# Save means
numpy.save(file=os.path.join(path_results,"conc_av_2.npy"), arr=conc_av_2, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_results,"pres_av_2.npy"), arr=pres_av_2, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_results,"volu_av_2.npy"), arr=volu_av_2, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_results,"cond_av_3.npy"), arr=cond_av_3, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_results,"adhe_av_3.npy"), arr=adhe_av_3, allow_pickle=True, fix_imports=True)

# Save stds
numpy.save(file=os.path.join(path_results,"conc_sd_2.npy"), arr=conc_sd_2, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_results,"pres_sd_2.npy"), arr=pres_sd_2, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_results,"volu_sd_2.npy"), arr=volu_sd_2, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_results,"cond_sd_3.npy"), arr=cond_sd_3, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_results,"adhe_sd_3.npy"), arr=adhe_sd_3, allow_pickle=True, fix_imports=True)