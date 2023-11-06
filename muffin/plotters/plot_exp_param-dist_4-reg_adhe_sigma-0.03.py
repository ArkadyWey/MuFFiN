from matplotlib import pyplot as plt
import os 
import numpy
from scipy import interpolate
import math

import muffin.configure as configure
import muffin.utils.utils_plot_exp_param_dist as utils_plot_exp_param_dist

import sys
sys.path.append("/home/user/utils_python")
import plotting


# Parameters 
# -----
initialisation = "4-reg"
num_reps       = 10000
sigma          = 0.03
type_alpha     = "mean"

path_results = os.path.join(".","results/results_exp_param-dist_{}_reps-{}_sigma-{}_alpha-{}".format(initialisation,num_reps,sigma,type_alpha))



# Make density v number of edges blocked plot
# --------------------------------
"""
Density plot of number of edges blocked where each bar has width 1. 
Then over the top of each histogram we fit a normal distribution.
"""
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

num_nodes_list = [4,16,36,64,100]
colors = ["tab:blue","tab:orange","tab:green","tab:red","tab:purple"]
# Get number of each number of edges blocked
for t,N in enumerate(num_nodes_list):
    
    count_adhe_hori_1 = numpy.load(os.path.join(path_results, "count_adhe_hori_1_N-{}.npy".format(N)))

    # Bin number of edges blocked 
    bincount_adhe_hori_1 = numpy.bincount(list(count_adhe_hori_1.astype(dtype=int)))
    
    # Get probability density of each bin
    # --------
    width = 1.0
    height_adhe_hori_1 = bincount_adhe_hori_1/sum(bincount_adhe_hori_1)/width

    conf = configure.Configure(num_nodes=N,
                               initialisation=initialisation,
                               sigma=sigma,
                               type_alpha=type_alpha)

    num_bins_adhe = N+1
    plot_depo_aprx_v_density = utils_plot_exp_param_dist.Plot_DepoAprx_vs_Density(num_nodes=N,
                                                                                  num_bins=num_bins_adhe,
                                                                                  conf=conf, 
                                                                                  count_adhe_1=count_adhe_hori_1, 
                                                                                  max_height=1)
    
    ax.bar(x=plot_depo_aprx_v_density.x_adhe_1, 
           height=height_adhe_hori_1, 
           width=width, 
           bottom=None, 
           align='center', 
           alpha=1.0, 
           data=None, 
           label=r"$N={}$".format(N), 
           fill=False,
           edgecolor=colors[t], 
           linewidth=1.0)


# Reset the color cycle and plot normal over histogram for each N
# ---------------
plt.gca().set_prop_cycle(None)

# Fit normal distribution to each 
# -----------
sigmas = [1,2,3,4,5]
for i,N in enumerate(num_nodes_list):

    mu = N/2
    sigma = sigmas[i]
    x = numpy.linspace(mu-30, mu+30, 1_000)
    pdf = (numpy.exp(-(x - mu)**2 / (2 * sigma**2))  / (sigma * numpy.sqrt(2 * numpy.pi))) 
    ax.plot(x, pdf, linewidth=2)

# Fit binomial distribution
# --------------------
for i,N in enumerate(num_nodes_list):
    ks = list(range(N+1))
    p = conf.get_cdf(x=conf.mean)
    bs = []
    for k in ks:
        b = (math.comb(N, k) * p**k * (1-p)**(N-k))
        bs.append(b)

    ax.scatter(ks,bs, marker=".")

plotting.thesisify_post_plot(ax=ax,

                             x_label=r"$b^{1\parallel}$",
                             y_label=r"Probability density",
                             x_left=-1.0,
                             x_right=70.0,
                             y_bottom=0.0,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"prob_density__v__adhe.svg"), format="svg")







# Plot mean and standard deviation of blocked edge count.
# -----------------------
"""
Plot mean and standard deviation of the distributions above. 
Use this to inform what the parameters of the normal distributions 
are that we fit the distributions above to.
"""
num_nodes_list = [1,4,9,16,25,36,49,64,81,100]
num_tests = len(num_nodes_list)

plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

# Get mean and standard deviation for each N
mean_1 = numpy.zeros(shape=num_tests)
sd_1   = numpy.zeros(shape=num_tests)
for t in range(num_tests):
    N = num_nodes_list[t]

    count_adhe_hori_1 = numpy.load(os.path.join(path_results, "count_adhe_hori_1_N-{}.npy".format(N)))
    mean_1[t]   = numpy.mean(a=count_adhe_hori_1, axis=0)
    sd_1[t]     = numpy.std( a=count_adhe_hori_1, axis=0)
    
# Plot scatter for distribution means
ax.scatter(num_nodes_list, mean_1, label=r"$\mathbb{E}[b^{1\parallel}]$")
ax.scatter(num_nodes_list, sd_1,   label=r"$\mathbb{S}[b^{1\parallel}]$")

# Plot guide lines
N_smooth = numpy.linspace(1,max(num_nodes_list),500)
ax.plot(N_smooth, N_smooth*conf.get_cdf(x=conf.mean), color="tab:blue", ls="-", label=r"$N\mathrm{cdf}(\bar{G})$")
ax.plot(N_smooth, numpy.sqrt(N_smooth*conf.get_cdf(x=conf.mean)*(1-conf.get_cdf(x=conf.mean))), color="tab:orange", ls="-", label=r"$\sqrt{N\mathrm{cdf}(\bar{G})(1-\mathrm{cdf}(\bar{G}))}$")

ax.plot(N_smooth, numpy.sqrt(N_smooth)/2, color="tab:green", ls=":", label=r"$\frac{\sqrt{N}}{2}$")
ax.plot(N_smooth, N_smooth/2, color="tab:blue", ls="--", label=r"$\frac{N}{2}$")

aprx = conf.mean*conf.get_cdf(conf.mean)
rslt = mean_1[-1]
pcnt = aprx/rslt*100
print("pcnt:{}".format(pcnt))

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$N$",
                             y_label=r"Blocked edges statistics",
                             x_left=0.0,
                             x_right=102.0,
                             y_bottom=0.0,
                             y_top=52.0)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"mean-b_and_std-b__v__N.svg"), format="svg")


