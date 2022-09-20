from matplotlib import pyplot as plt
import os 
import numpy

import utils_plot_exp_param_dist


# Parameters 
# -----
path_results = os.path.join(".","results/results_experiment_param-dist_structure-comparison")

if not os.path.exists(path_results):
    os.mkdir(path_results)

parameter_name = "depo"

# Paths to param experiment results for each structure
path_results_square_struc = os.path.join(".","results_experiment_param-dist_square-structure_reps-50k")
path_results_hexag_struc = os.path.join("."," results_experiment_param-dist_hexag-structure_reps-5k")
path_results_rand_struc = os.path.join(".","  results_experiment_param-dist_random-structure_reps-50k")

paths_results = [
    path_results_square_struc,
    path_results_hexag_struc,
    path_results_rand_struc
]

# Each structure will have a different color and marker
colors = ["tab:blue", "tab:orange", "tab:green"]
markers = ["s","h",(6, 2, 0)] 

# Each structure was trialed for different numbers of nodes
num_nodes_list_square_struc = [1,4,9,16,25,36,49,64,81,100]
num_nodes_list_hexag_struc = [2, 8,18,32,50,72,98,128]
num_nodes_list_rand_struc = [4,9,16,25,36,49,64,81,100]
num_nodes_lists = [num_nodes_list_square_struc, 
                   num_nodes_list_hexag_struc,
                   num_nodes_list_rand_struc]

# Each structure needs its own labels in plot
labels_mean = [r"mean $j^{0}$ - 4-lattice", r"mean $j^{0}$ - 6-lattice", r"mean $j^{0}$ - 6-random"]
labels_sd = [r"std. dev. $j^{0}$ - 4-lattice", r"std. dev. $j^{0}$ - 6-lattice", r"std. dev. $j^{0}$ - 6-random"]

sd_constants_and_powers = [[0.406,-0.5],[0.684, -0.5],[0.779, -1.0/3.0]]  # first index is constant out front, second is power
labels_sd_fit = [r"$0.406N^{-\frac{1}{2}}$", 
                 r"$0.684N^{-\frac{1}{2}}$",
                 r"$0.779N^{-\frac{1}{3}}$"
                ]

# For guidelines, need smooth x axis
N_smooth = numpy.linspace(1,200,1000) # For guide lines




# Make mean and SD plots using plotting class
# -----------------------
fig_mean, ax_mean = plt.subplots(1,1)
fig_sd, ax_sd = plt.subplots(1,1)

plot_parameter_mean_and_sd = utils_plot_exp_param_dist.PlotParameterMeanAndSD(parameter_name=parameter_name,
                                                                     paths_results=paths_results,
                                                                     num_nodes_lists=num_nodes_lists,
                                                                     markers=markers,
                                                                     labels_mean=labels_mean,
                                                                     colors=colors,
                                                                     N_smooth=N_smooth,
                                                                     labels_sd=labels_sd,
                                                                     sd_constants_and_powers=sd_constants_and_powers,
                                                                     labels_sd_fit=labels_sd_fit,
                                                                     ax_mean=ax_mean,
                                                                     ax_sd=ax_sd)


plot_parameter_mean_and_sd.ax_mean.set_xlabel(r"$N$")
plot_parameter_mean_and_sd.ax_mean.legend()

plot_parameter_mean_and_sd.ax_sd.set_xlabel(r"$N$")
plot_parameter_mean_and_sd.ax_sd.legend()

fig_mean.savefig(fname=os.path.join(path_results,"compare__mean-j__v__N.svg"), format="svg")
fig_sd.savefig(fname=os.path.join(path_results,"compare__sd-j__v__N.svg"), format="svg")