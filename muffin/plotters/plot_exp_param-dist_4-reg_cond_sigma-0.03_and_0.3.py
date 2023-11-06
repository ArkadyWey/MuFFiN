from matplotlib import pyplot as plt
import os 
import numpy
from scipy import interpolate
import math
import scipy

import muffin.configure as configure
import muffin.utils.utils_plot_exp_param_dist as utils_plot_exp_param_dist

import sys
sys.path.append("/home/user/utils_python")
import plotting

# Parameters 
# -----
initialisation = "4-reg"
num_reps       = 10000
type_alpha     = "mean"
N              = 1

path_results = os.path.join(".","results/results_exp_cond-pdf_{}_reps-{}_alpha-{}".format(initialisation,num_reps,type_alpha))
# Make results directories 
# --------
if not os.path.exists(path_results):
    os.makedirs(path_results)


plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

sigmas = [0.03,0.3]
colors = ["tab:blue","tab:orange"]
labels = [r"$\bar{G}_{\mathrm{N}}$",r"$\bar{G}_{\mathrm{W}}$"]
for s,sigma in enumerate(sigmas):
    conf = configure.Configure(num_nodes=N,
                               initialisation=initialisation,
                               sigma=sigma, 
                               type_alpha=type_alpha)
    mu    = conf.mu
    sigma = conf.sigma

    x     = numpy.linspace(0.0, 4, 1_000)
    pdf   = conf.get_pdf(x=x) 
    #ax.plot(x, pdf, linewidth=2, label=r"$G_{{ij}}^{{r,0}}|_{{\sigma={}}}$".format(sigma))
    ax.plot(x, pdf, linewidth=2)

    # Find proportion of GF above mean
    x   = conf.mean
    cdf = conf.get_cdf(x=x) # proportion up to mean

#ax.vlines(x=conf.median, 
#          ymin=0.0, 
#          ymax=8.5, 
#          color="tab:blue", 
#          linewidth=2.0, 
#          linestyle="--", 
#          alpha=1.0,
#          label=r"$\bar{G}|_{\sigma=0.03}$")

    ax.vlines(x=conf.mean, 
              ymin=0.0, 
              ymax=8.5, 
              linewidth=2.0, 
              color=colors[s],
              linestyle="--", 
              alpha=1.0, 
              label=labels[s])  

# Cleanup graph 
# ------
plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$G_{ij}^{r, 0}$",
                             y_label=r"Probability density",
                             x_left=0.0,
                             x_right=4.0,
                             y_bottom=0.0,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"prob_density__v__G_init.svg"), format="svg")


plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)
sigmas = [0.03,0.3]
colors = ["tab:blue","tab:orange"]
labels = [r"$\bar{G}_{\mathrm{N}}$",r"$\bar{G}_{\mathrm{W}}$"]
labels_1 = [r"$\mathrm{cdf}(\bar{G}_{\mathrm{N}})$",r"$\mathrm{cdf}(\bar{G}_{\mathrm{W}})$"]
mu = 0.5
for s,sigma in enumerate(sigmas):
    conf = configure.Configure(num_nodes=N,
                               initialisation=initialisation,
                               sigma=sigma, 
                               type_alpha=type_alpha)
    mu    = conf.mu
    sigma = conf.sigma

    x     = numpy.linspace(0.0, 4.0, 1_000)
    pdf   = conf.get_pdf(x=x) 

    ## Find proportion of GF above mean
    #x   = conf.mean
    #cdf = conf.get_cdf(x=x) # proportion up to mean
    cdf = 0.5*(1 + scipy.special.erf( (numpy.log(x) - mu)/(sigma*numpy.sqrt(2))  ))

    ax.plot(x, cdf, linewidth=2, color=colors[s])

    x_to_mean = numpy.linspace(-0.1,conf.mean,1_000)
    ax.plot(x_to_mean, conf.get_cdf(conf.mean)*numpy.ones_like(x_to_mean), linewidth=2, color=colors[s],label=labels_1[s],linestyle=":")


    ax.vlines(x=conf.mean, 
              ymin=0.0, 
              ymax=1.1, 
              linewidth=2.0, 
              color=colors[s],
              linestyle="--", 
              alpha=1.0,
              label=labels[s]) 

# Cleanup graph 
# ------
plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$G_{ij}^{r, 0}$",
                             y_label=r"Cumulative density",
                             x_left=-0.1,
                             x_right=4.0,
                             y_bottom=0.0,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"cdf__v__G_init.svg"), format="svg")