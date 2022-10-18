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
for s,sigma in enumerate(sigmas):
    conf = configure.Configure(num_nodes=N,
                               initialisation=initialisation,
                               sigma=sigma, 
                               type_alpha=type_alpha)
    mu    = conf.mu
    sigma = conf.sigma

    x     = numpy.linspace(0.0, 3.5, 1_000)
    pdf   = conf.get_pdf(x=x) 
    ax.plot(x, pdf, linewidth=2, label=r"$G_{{ij}}^{{r,0}}|_{{\sigma={}}}$".format(sigma))

    # Find proportion of GF above mean
    x   = conf.mean
    cdf = conf.get_cdf(x=x) # proportion up to mean

ax.vlines(x=conf.median, 
          ymin=0.0, 
          ymax=8.5, 
          color="tab:blue", 
          linewidth=2.0, 
          linestyle="--", 
          alpha=1.0,
          label=r"$\bar{G}|_{\sigma=0.03}$")

ax.vlines(x=conf.mean, 
          ymin=0.0, 
          ymax=8.5, 
          color="tab:orange", 
          linewidth=2.0, 
          linestyle="--", 
          alpha=1.0, 
          label=r"$\bar{G}|_{\sigma=0.3}$")  


# Cleanup graph 
# ------
plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$G_{ij}^{r, 0}$",
                             y_label=r"Probability density",
                             x_left=0.5,
                             x_right=3.0,
                             y_bottom=0.0,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"prob_density__v__perm_N=1.svg"), format="svg")