from matplotlib import pyplot as plt
import os 
import numpy
from scipy import interpolate
import math

import configure
import utils_plot_exp_param_dist

import sys
sys.path.append("/home/user/utils_python")
import plotting

# Parameters 
# -----
initialisation = "4-reg"
num_reps       = 10000
sigma          = 0.3

path_results = os.path.join(".","results/results_exp_param-dist_{}_reps-{}_sigma-{}".format(initialisation,num_reps,sigma))



# Plot histograms with all bars same width
# ----------------------------------------
num_nodes_list = [1,4,16,36,64,100]
num_tests = len(num_nodes_list)
fig, ax = plt.subplots(1,1)

num_bins_in_range = 100
num_pts_to_interp = 200

ax_parameter_distribution =  utils_plot_exp_param_dist.PlotParameterDistribution(parameter_name="perm",
                                                                        num_nodes_list=num_nodes_list,
                                                                        num_bins_in_range=num_bins_in_range,
                                                                        num_pts_to_interp=num_pts_to_interp,
                                                                        path_results=path_results,
                                                                        ax=ax)

ax.set_xlabel(r"$k^{00}$")
ax.set_ylabel(r"Probability density")
ax.set_xlim(left=0.5,right=3.0)
ax.set_ylim(bottom=0.0)
ax.legend()

plt.savefig(fname=os.path.join(path_results,"prob_density__v__perm.svg"), format="svg")






# Plot histogram clearer method
# -----------------------    
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)
num_nodes_list = [1,4,16,36,64,100]
colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink"]
for t, N in enumerate(num_nodes_list):

    # Plot parameter distribution
    # ----------------------------
    # Get parameters
    # --------
    conf = configure.Configure(num_nodes=N,
                               initialisation=initialisation,
                               sigma=sigma)


    num_bins = 500
    min_val = 0.0
    max_val = conf.mean*2

    # Get parameter to histogram
    # ------
    param_effe_1     = numpy.load(os.path.join(path_results, "perm_effe_1_N-{}.npy".format(N)))

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


# Cleanup graph 
# ----
plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$k^{00}$",
                             y_label=r"Probability density",
                             x_left=0.0,
                             x_right=2*conf.mean,
                             y_bottom=0.0,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"prob_density__v__perm__with_approx.svg"))






# Plot mean and standard deviation of each histogram 
# ------------------------------------
num_nodes_list = [1,4,9,16,25,36,49,64,81,100]
num_tests = len(num_nodes_list)

plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

# Get mean and standard deviation for each N
# -------
mean_1 = numpy.zeros(shape=num_tests)
sd_1 = numpy.zeros(shape=num_tests)
for t in range(num_tests):
    N = num_nodes_list[t]

    perm_effe_2 = numpy.load(os.path.join(path_results, "perm_effe_1_N-{}.npy".format(N)))
    mean_1[t] = numpy.mean(a=perm_effe_2, axis=0)
    sd_1[t]   = numpy.std(a=perm_effe_2, axis=0)


# Plot scatter for distribution means
# -------
conf = configure.Configure(num_nodes=N,
                           initialisation=initialisation,
                           sigma=sigma)
ax.scatter(num_nodes_list,mean_1-conf.mean, label=r"mean $k^{00}-\bar{G}$")
ax.scatter(num_nodes_list,sd_1, label=r"std. dev. $k^{00}$")

# Plot guide lines
# ------
N_smooth = numpy.linspace(1,100,500)
ax.plot(N_smooth, 0.498*numpy.power(N_smooth,-0.5), color="tab:orange", label=r"$0.498N^{-\frac{1}{2}}$",ls="-")
ax.plot(N_smooth, (mean_1[-1]-conf.mean)*numpy.ones_like(N_smooth), color="tab:blue", ls="--")


# Cleanup graph 
# ----
plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$N$",
                             y_label=None,
                             x_left=-5.0,
                             x_right=105.0,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"mean-k_and_std-k__v__N.svg"), format="svg")






# Plot Log Log to check gradient of standard deviation
# -------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

N_smoother = numpy.linspace(0.01,5,500)
ax.scatter(numpy.log(num_nodes_list),numpy.log(mean_1), label=r"log(mean $k^{00}$$)$")
ax.scatter(numpy.log(num_nodes_list),numpy.log(sd_1), label=r"log(std. dev. $k^{00}$$)$")
ax.plot(N_smoother, -0.5*N_smoother + (numpy.log(0.498)*numpy.ones_like(N_smoother)), color="tab:orange", label=r"$-\frac{1}{2}log(N)-0.697$")

# Cleanup graph 
# -------------
plotting.thesisify_post_plot(ax=ax,
                             x_label=r"log$(N)$",
                             y_label=None,
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"logmean-k_and_logstd-k__v__logN.svg"), format="svg")







# Plot histogram for N=1 (outside to get bins for pdf)
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)
perm_effe_2 = numpy.load(os.path.join(path_results, "perm_effe_1_N-1.npy"))
count, bins_1, ignored = ax.hist(x=perm_effe_2[:], bins=75, density=True, align='mid', label=r"$N=1$", alpha=0.4)

# ...and compare with log-normal distribution that edges are drawn from 
# # -----

conf = configure.Configure(num_nodes=N,
                           initialisation=initialisation,
                           sigma=sigma)
mu    = conf.mu
sigma = conf.sigma
x     = numpy.linspace(min(bins_1), max(bins_1), 1_000)
pdf   = conf.get_pdf(x=x) 
ax.plot(x, pdf, linewidth=2, color='r', label=r"$G$")

# Find proportion of GF above mean
x   = conf.mean
cdf = conf.get_cdf(x=x) # proportion up to mean


ax.vlines(x=conf.mean, 
          ymin=0.0, 
          ymax=1.0, 
          color="tab:red", 
          linewidth=2.0, 
          linestyle="--", 
          alpha=1.0, 
          label="mean")

ax.vlines(x=conf.median, 
          ymin=0.0, 
          ymax=1.0, 
          color="black", 
          linewidth=2.0, 
          linestyle=":", 
          alpha=1.0,
          label="median")

# Cleanup graph 
# ------
plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$k^{00}$",
                             y_label=r"Probability density",
                             x_left=0.0,
                             x_right=4.0,
                             y_bottom=0.0,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"prob_density__v__perm_N=1.svg"), format="svg")