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
initialisation = "6-reg"
num_reps       = 10000
sigma          = 0.3
type_alpha     = "median"

path_results = os.path.join(".","results/results_exp_param-dist_{}_reps-{}_sigma-{}_alpha-{}".format(initialisation,num_reps,sigma,type_alpha))



# Make density v number of edges blocked plot
# --------------------------------
"""
Density plot of number of edges blocked where each bar has width 1. 
Then over the top of each histogram we fit a normal distribution.
"""
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

num_nodes_list = [2,8,18]#[2,18,50]#2*numpy.array([4,16,36,64,100])
colors = ["tab:blue","tab:orange","tab:green","tab:red","tab:purple"]
# Get number of each number of edges blocked
for t,N in enumerate(num_nodes_list):
    
    count_adhe_hori_1 = numpy.load(os.path.join(path_results, "count_adhe_1_N-{}.npy".format(N)))

    # Bin number of edges blocked 
    bincount_adhe_hori_1 = numpy.bincount(list(count_adhe_hori_1.astype(dtype=int)))
    
    # Get probability density of each bin
    # --------
    width = 1.0
    height_adhe_hori_1 = bincount_adhe_hori_1/sum(bincount_adhe_hori_1)/width

    conf = configure.Configure(num_nodes=N,
                               initialisation=initialisation,
                               sigma=sigma, type_alpha=type_alpha)

    num_bins_adhe = 3*N+1
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


# Fit binomial distribution and normal
# --------------------
for i,N in enumerate(num_nodes_list):
    p = conf.get_cdf(x=conf.mean)
    n = 3*N
    ks = list(range(n+1))
    bs = []
    for k in ks:
        b = (math.comb(n, k) * p**k * (1-p)**(n-k))
        bs.append(b)

    ax.scatter(ks,bs, marker=".")

    mu_normal = n*p
    sigma_normal = numpy.sqrt(n*p*(1-p))
    x = numpy.linspace(mu_normal-30, mu_normal+30, 1_000)
    pdf = (numpy.exp(-(x - mu_normal)**2 / (2 * sigma_normal**2))  / (sigma_normal * numpy.sqrt(2 * numpy.pi))) 
    ax.plot(x, pdf, linewidth=2)

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$b^{0}$",
                             y_label=r"Probability density",
                             x_left=-1.0,
                             x_right=100.0,
                             y_bottom=0.0,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"prob_density__v__adhe.svg"), format="svg")




# Make density v number of edges blocked plot
# Only horizontal edges
# --------------------------------
"""
Density plot of number of edges blocked where each bar has width 1. 
Then over the top of each histogram we fit a normal distribution.
"""
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

num_nodes_list = [2,18,50]#2*numpy.array([4,16,36,64,100])
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
                               sigma=sigma, type_alpha=type_alpha)
                            

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


# Fit binomial distribution and normal
# --------------------
for i,N in enumerate(num_nodes_list):
    p = conf.get_cdf(x=conf.mean)
    n = N
    ks = list(range(n+1))
    bs = []
    for k in ks:
        b = (math.comb(n, k) * p**k * (1-p)**(n-k))
        bs.append(b)

    ax.scatter(ks,bs, marker=".")

    mu_normal = n*p
    sigma_normal = numpy.sqrt(n*p*(1-p))
    x = numpy.linspace(mu_normal-30, mu_normal+30, 1_000)
    pdf = (numpy.exp(-(x - mu_normal)**2 / (2 * sigma_normal**2))  / (sigma_normal * numpy.sqrt(2 * numpy.pi))) 
    ax.plot(x, pdf, linewidth=2)

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$b^{0}_{H}$",
                             y_label=r"Probability density",
                             x_left=-1.0,
                             x_right=40.0,
                             y_bottom=0.0,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"prob_density__v__adhe_hori.svg"), format="svg")



# Make density v number of edges blocked plot
# Only diagonal edges
# --------------------------------
"""
Density plot of number of edges blocked where each bar has width 1. 
Then over the top of each histogram we fit a normal distribution.
"""
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

num_nodes_list = [2,18,50]#2*numpy.array([4,16,36,64,100])
colors = ["tab:blue","tab:orange","tab:green","tab:red","tab:purple"]
# Get number of each number of edges blocked
for t,N in enumerate(num_nodes_list):
    
    count_adhe_hori_1 = numpy.load(os.path.join(path_results, "count_adhe_not_hori_1_N-{}.npy".format(N)))

    # Bin number of edges blocked 
    bincount_adhe_hori_1 = numpy.bincount(list(count_adhe_hori_1.astype(dtype=int)))
    
    # Get probability density of each bin
    # --------
    width = 1.0
    height_adhe_hori_1 = bincount_adhe_hori_1/sum(bincount_adhe_hori_1)/width

    conf = configure.Configure(num_nodes=N,
                               initialisation=initialisation,
                               sigma=sigma, type_alpha=type_alpha)
                            

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


# Fit binomial distribution and normal
# --------------------
for i,N in enumerate(num_nodes_list):
    p = conf.get_cdf(x=conf.mean)
    n = 2*N
    ks = list(range(n+1))
    bs = []
    for k in ks:
        b = (math.comb(n, k) * p**k * (1-p)**(n-k))
        bs.append(b)

    ax.scatter(ks,bs, marker=".")

    mu_normal = n*p
    sigma_normal = numpy.sqrt(n*p*(1-p))
    x = numpy.linspace(mu_normal-30, mu_normal+30, 1_000)
    pdf = (numpy.exp(-(x - mu_normal)**2 / (2 * sigma_normal**2))  / (sigma_normal * numpy.sqrt(2 * numpy.pi))) 
    ax.plot(x, pdf, linewidth=2)

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$b^{0}_{D}$",
                             y_label=r"Probability density",
                             x_left=-1.0,
                             x_right=40.0,
                             y_bottom=0.0,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"prob_density__v__adhe_diag.svg"), format="svg")






# Plot mean and standard deviation of blocked edge count.
# -----------------------
"""
Plot mean and standard deviation of the distributions above. 
Use this to inform what the parameters of the normal distributions 
are that we fit the distributions above to.
"""
num_nodes_list = [2,8,18]#2*numpy.array([1,4,9,16,25,36,49,64,81,100])
num_tests = len(num_nodes_list)

plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

# Get mean and standard deviation for each N

# All edges 
# ---------
mean_1 = numpy.zeros(shape=num_tests)
sd_1   = numpy.zeros(shape=num_tests)
for t in range(num_tests):
    N = num_nodes_list[t]
    n = int(numpy.sqrt(N/2))

    count_adhe_1 = numpy.load(os.path.join(path_results, "count_adhe_1_N-{}.npy".format(N)))
    mean_1[t]   = numpy.mean(a=count_adhe_1, axis=0)
    sd_1[t]     = numpy.std( a=count_adhe_1, axis=0)
    
# Plot scatter for distribution means
ax.scatter(num_nodes_list, mean_1, label=r"mean $b^{0}$")
ax.scatter(num_nodes_list, sd_1,   label=r"std. dev. $b^{0}$")

# Plot guide lines
N_smooth = numpy.linspace(1,max(num_nodes_list),500)
#ax.plot(N_smooth, N_smooth/2, color="tab:blue", ls=":", label=r"$\frac{N}{2}$")
ax.plot(N_smooth, 3*N_smooth*conf.get_cdf(x=conf.mean), color="tab:blue", ls="--", label=r"$3N$cdf($\bar{G}$)")
ax.plot(N_smooth, numpy.sqrt(3*N_smooth*conf.get_cdf(x=conf.mean)*(1-conf.get_cdf(x=conf.mean))), color="tab:orange", ls="--", label=r"($3N$cdf($\bar{G}$)($1-$cdf($\bar{G}$)))$^{\frac{1}{2}}$")



# Horizontal edges 
# ---------
mean_1 = numpy.zeros(shape=num_tests)
sd_1   = numpy.zeros(shape=num_tests)
for t in range(num_tests):
    N = num_nodes_list[t]
    n = int(numpy.sqrt(N/2))

    count_adhe_1 = numpy.load(os.path.join(path_results, "count_adhe_hori_1_N-{}.npy".format(N)))
    mean_1[t]   = numpy.mean(a=count_adhe_1, axis=0)
    sd_1[t]     = numpy.std( a=count_adhe_1, axis=0)
    
# Plot scatter for distribution means
ax.scatter(num_nodes_list, mean_1, label=r"mean $b^{0}_{H}$"     , marker="+")
ax.scatter(num_nodes_list, sd_1,   label=r"std. dev. $b^{0}_{H}$", marker="+")

# Plot guide lines
N_smooth = numpy.linspace(1,max(num_nodes_list),500)
#ax.plot(N_smooth, N_smooth/2, color="tab:blue", ls=":", label=r"$\frac{N}{2}$")
ax.plot(N_smooth, N_smooth*conf.get_cdf(x=conf.mean), color="tab:green", ls="--", label=r"$N$cdf($\bar{G}$)")
ax.plot(N_smooth, numpy.sqrt(N_smooth*conf.get_cdf(x=conf.mean)*(1-conf.get_cdf(x=conf.mean))), color="tab:red", ls="--", label=r"$(N$cdf($\bar{G}$)($1-$cdf($\bar{G}$))$^{\frac{1}{2}}$")


# Diagonal edges
# ---------
mean_1 = numpy.zeros(shape=num_tests)
sd_1   = numpy.zeros(shape=num_tests)
for t in range(num_tests):
    N = num_nodes_list[t]
    n = int(numpy.sqrt(N/2))

    count_adhe_1 = numpy.load(os.path.join(path_results, "count_adhe_not_hori_1_N-{}.npy".format(N)))
    mean_1[t]   = numpy.mean(a=count_adhe_1, axis=0)
    sd_1[t]     = numpy.std( a=count_adhe_1, axis=0)
    
# Plot scatter for distribution means
ax.scatter(num_nodes_list, mean_1, label=r"mean $b^{0}_{D}$"     , marker="x")
ax.scatter(num_nodes_list, sd_1,   label=r"std. dev. $b^{0}_{D}$", marker="x")

# Plot guide lines
N_smooth = numpy.linspace(1,max(num_nodes_list),500)
#ax.plot(N_smooth, N_smooth/2, color="tab:blue", ls=":", label=r"$\frac{N}{2}$")
ax.plot(N_smooth, 2*N_smooth*conf.get_cdf(x=conf.mean), color="tab:purple", ls="--", label=r"$2N$cdf($\bar{G}$)")
ax.plot(N_smooth, numpy.sqrt(2*N_smooth*conf.get_cdf(x=conf.mean)*(1-conf.get_cdf(x=conf.mean))), color="tab:brown", ls="--", label=r"$(2N$cdf($\bar{G}$)($1-$cdf($\bar{G}$))$^{\frac{1}{2}}$")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$N$",
                             y_label=None,
                             x_left=-5.0,
                             x_right=205.0,
                             y_bottom=-10.0,
                             y_top=310.0)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"mean-b_and_std-b__v__N.svg"), format="svg")