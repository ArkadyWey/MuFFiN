from matplotlib import pyplot as plt
import os 
import numpy 
import scipy.interpolate as interpolate

import configure
import utils_plot_exp_param_dist


import sys
sys.path.append("/home/user/utils_python")
import plotting


# Parameters 
# -----
type_clog      = "deposit"
initialisation = "4-reg"
num_nodes      = 4

path_fulls = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/poly/esbl_prep/init-{}/N-{}/fulls_init-{}_N-{}".format(initialisation,num_nodes,initialisation,num_nodes)) # paper


# Load variables
# -----
# Average
perm_prep_4       = numpy.load(os.path.join(path_fulls, "perm_prep_4.npy")) # [r_max+1,k,m,n]
depo_prep_3       = numpy.load(os.path.join(path_fulls, "depo_prep_3.npy")) # [r_max+1,k,m]

hist_perm, hist_perm_bin_edges = numpy.histogram(a=perm_prep_4[:,0,0,0], bins=10, range=None, density=None, weights=None)
hist_depo, hist_depo_bin_edges = numpy.histogram(a=depo_prep_3[:,0,0],   bins=10, range=None, density=None, weights=None)


# Plot permeability and deposition parameter values on one axis 
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

print(hist_perm)
ax.hist(hist_perm, hist_perm_bin_edges)

plt.show()
#ax.show()


sigma = 0.3 
type_alpha = "mean"
initialisation = "4-reg"

path_results = "/home/user/projects/papers/2023_homogenisation/figures/poly/esbl_prep/init-4-reg/N-4/fulls_init-4-reg_N-4"


# Plot histogram clearer method
# -----------------------    
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)
num_nodes_list = [4]
colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink"]
for t, N in enumerate(num_nodes_list):

    # Plot parameter distribution
    # ----------------------------
    # Get parameters
    # --------
    conf = configure.Configure(num_nodes=N,
                               initialisation=initialisation,
                               sigma=sigma, type_alpha=type_alpha)


    num_bins = 100
    min_val = 0.0
    max_val = conf.mean*2

    # Get parameter to histogram
    # ------
    param_effe_1     = numpy.load(os.path.join(path_results, "perm_prep_4_N-{}.npy".format(N)))

    # Get bin edges of histogram
    # ------
    bin_edges = utils_plot_exp_param_dist.GetBinEdges(num_bins=num_bins,
                                                      min_val=min_val, 
                                                      max_val=max_val)
    
    # Plot histogram
    # ------
    count_param_1, bins_param, _ignored = ax.hist(x=param_effe_1, 
                                                  bins=bin_edges.bin_edges, 
                                                  density=True, 
                                                  align='mid', 
                                                  label=r"$N={}$".format(num_nodes_list[t]), 
                                                  alpha=0.4, color=colors[t])
   
    
    # Interpolate histogram
    # ------
    bin_centres = numpy.linspace(start=min_val, stop=max_val, num=num_bins, endpoint=True)
    spl = interpolate.splrep(bin_centres, count_param_1, k=3)
    x2 = numpy.linspace(bin_centres[0], bin_centres[-1], 10*num_bins)
    y2 = interpolate.splev(x2, spl)
    ax.plot(x2,y2,color=colors[t], 
                  linewidth=2.0, 
                  linestyle="-", 
                  alpha=1.0)