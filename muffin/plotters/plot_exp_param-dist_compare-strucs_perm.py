from matplotlib import pyplot as plt
import os 
import numpy

import multiscale_models.utils_plot_exp_param_dist as utils_plot_exp_param_dist

import sys
sys.path.append("/home/user/utils_python")
import plotting


# Parameters 
# -----
path_results = os.path.join(".","results/results_experiment_param-dist_structure-comparison")

if not os.path.exists(path_results):
    os.mkdir(path_results)

parameter_name = "perm"

# Paths to param experiment results for each structure
path_results_square_struc = os.path.join(".","results/results_exp_param-dist_4-reg_reps-10000_sigma-0.3_alpha-mean")
#path_results_hexag_struc = os.path.join(".","results/results_exp_param-dist_6-reg_reps-10000_sigma-0.3_alpha-mean")
#path_results_rand_struc = os.path.join(".","results/results_exp_param-dist_6-ireg_reps-10000_sigma-0.3_alpha-mean")
path_results_hexag_struc = os.path.join(".","results/results_exp_param-dist_6-reg_reps-10000_sigma-0.3_alpha-mean")
path_results_rand_struc = os.path.join(".","results/results_exp_param-dist_6-ireg_reps-10000_sigma-0.3_alpha-mean")
#path_results_hexag_struc = os.path.join(".","results/results_exp_param-dist_6-rand_reps-1001_sigma-0.3_alpha-mean") #fixed connectivity 
#path_results_rand_struc =  os.path.join(".","results/results_exp_param-dist_6-rand_reps-1002_sigma-0.3_alpha-mean") #random connectivity
#path_results_rand_struc = os.path.join(".","results/results_exp_param-dist_6-ireglikereg_reps-10000_sigma-0.3_alpha-mean")
#path_results_rand_struc = os.path.join(".","results/results_exp_param-dist_6-ireglikereg_reps-105_sigma-0.3_alpha-mean")


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
num_nodes_list_hexag_struc = [2,8,18,32,50,72,98,128,162,200]
#num_nodes_list_hexag_struc = [4,9,16]
#num_nodes_list_rand_struc = [8,18,32,50]
num_nodes_list_rand_struc = [4,9,16,25,36,49,64,81,100]
#num_nodes_list_rand_struc =  [8,18,32,50]
num_nodes_lists = [num_nodes_list_square_struc, 
                   num_nodes_list_hexag_struc,
                   num_nodes_list_rand_struc]

# Each structure needs its own labels in plot
labels_mean = [r"$\mathbb{E}[k^{11}]$ - 4-regular", r"$\mathbb{E}[k^{11}]$ - 6-regular", r"$\mathbb{E}[k^{11}]$ - 6-irregular"]
labels_sd = [r"$\mathbb{S}[k^{11}]$ - 4-regular", r"$\mathbb{S}[k^{11}]$ - 6-regular", r"$\mathbb{S}[k^{11}]$ - 6-irregular"]

sd_constants_and_powers = [[0.498,-0.5],[0.577, -0.5],[1.1, -0.5]]  # first index is constant out front, second is power
labels_sd_fit = [r"$0.498N^{-\frac{1}{2}}$", 
                 r"$0.577N^{-\frac{1}{2}}$",
                 r"$1.100N^{-\frac{1}{2}}$"
                ]

# For guidelines, need smooth x axis
N_smooth = numpy.linspace(1,200,1000) # For guide lines




# Make mean and SD plots using plotting class
# -----------------------
plotting.thesisify_pre_ax_creation()
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

ax_mean.plot(N_smooth, 1.7246083823764355*numpy.ones_like(N_smooth), label=r"$\bar{k}_4$")
ax_mean.plot(N_smooth, 2.6587931103444693*numpy.ones_like(N_smooth), label=r"$\bar{k}_6$")

# Cleanup graph 
# ----
plotting.thesisify_post_plot(ax=plot_parameter_mean_and_sd.ax_mean,
                             x_label=r"$N$",
                             y_label=None,
                             x_left=-5.0,
                             x_right=None,
                             y_bottom=0.0,
                             y_top=None)

plotting.save_fig(fig=fig_mean,fname=os.path.join(path_results,"compare__mean-k__v__N.svg"))

# Cleanup graph 
# ----
plotting.thesisify_post_plot(ax=plot_parameter_mean_and_sd.ax_sd,
                             x_label=r"$N$",
                             y_label=None,
                             x_left=-5.0,
                             x_right=None,
                             y_bottom=0.0,
                             y_top=None)

plotting.save_fig(fig=fig_sd,fname=os.path.join(path_results,"compare__sd-k__v__N.svg"))