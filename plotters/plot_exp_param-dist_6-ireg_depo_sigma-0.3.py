from matplotlib import pyplot as plt
import os 
import numpy
from scipy import interpolate

import multiscale_models.configure as configure
import multiscale_models.utils_plot_exp_param_dist as utils_plot_exp_param_dist

import sys
sys.path.append("/home/user/utils_python")
import plotting

# Parameters 
# -----
initialisation = "6-ireg"
num_reps       = 10000
sigma          = 0.3
type_alpha     = "mean"

path_results = os.path.join(".","results/results_exp_param-dist_{}_reps-{}_sigma-{}_alpha-{}".format(initialisation,num_reps,sigma,type_alpha))

#num_nodes_list = [16,25,36,49,64,81,100]
#num_nodes_list = [4,9,16,25,36,49,64,81,100]
num_nodes_list = [4,16,36,64,100]
num_tests = len(num_nodes_list)


# Plot deposition parameter histogram fo all N on same graph
# -----    
fig, ax = plt.subplots(1,1)

num_bins_in_range = 100#201
num_pts_to_interp = 250

# MUST DIVIDE bY SQRT(N) and make psitive to generate this j, since wasn't done in simulation
ax_parameter_distribution =  utils_plot_exp_param_dist.PlotParameterDistribution(parameter_name="depo",
                                                                        num_nodes_list=num_nodes_list,
                                                                        num_bins_in_range=num_bins_in_range,
                                                                        num_pts_to_interp=num_pts_to_interp,
                                                                        path_results=path_results,
                                                                        ax=ax)

ax.set_xlabel(r"$j^{1}$")
ax.set_ylabel(r"Probability density")
#ax.set_xlim(left=0.0,right=2.0)
ax.set_ylim(bottom=0.0)

ax.legend()

plt.savefig(fname=os.path.join(path_results,"prob_density__v__depo__old.svg"), format="svg")



# Plot deposition parameter with single N with boxes
# Better neater plot
# -----------------------    
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)
num_nodes_list = [4,16,36,64,100]
colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink"]
for t, N in enumerate(num_nodes_list):

    # Plot parameter distribution
    # ----------------------------
    # Get parameters
    # --------
    conf = configure.Configure(num_nodes=4,initialisation=initialisation,sigma=sigma,type_alpha=type_alpha)


    num_bins = 100
    min_val = 0.0
    max_val = 4*(1.0/numpy.sqrt(3))*conf.scaled_mean


    # Get parameter to histogram
    # ------
    param_effe_1     = numpy.load(os.path.join(path_results, "depo_effe_1_N-{}.npy".format(N)))

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
    # --------
    bin_centres = numpy.linspace(start=min_val, stop=max_val, num=num_bins, endpoint=True)
    spl = interpolate.splrep(bin_centres, count_param_1, k=3)
    x2 = numpy.linspace(bin_centres[0], bin_centres[-1], 10*num_bins)
    y2 = interpolate.splev(x2, spl)
    ax.plot(x2,y2,color=colors[t], 
                  linewidth=2.0, 
                  linestyle="-", 
                  alpha=1.0)


#N = num_nodes_list[0]
#for i in range(4*N+1):
#    ax.vlines(x=i*(1.0/2.0)*conf.scaled_mean/N, 
#              ymin=0.0, 
#              ymax=1.0, 
#              color="black", 
#              linewidth=2.0, 
#              linestyle=":", 
#              alpha=1.0)


# Cleanup graph 
# -------------
plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$j^{1}$",
                             y_label=r"Probability density",
                             x_left=0.0-0.1,
                             x_right=max_val+0.1,
                             y_bottom=0.0,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"prob_density__v__depo__with_approx.svg"))





# Plot mean and standard deviation of each histogram 
# ------
num_nodes_list = [4,9,16,25,36,49,64,81,100] #2*numpy.linspace(1,10,10,dtype=int)**2
num_tests = len(num_nodes_list)

# Get mean and standard deviation at each N
mean_1 = numpy.zeros(shape=num_tests)
sd_1 = numpy.zeros(shape=num_tests)
for t in range(num_tests):
    N = num_nodes_list[t]

    depo_effe_2 = numpy.load(os.path.join(path_results, "depo_effe_1_N-{}.npy".format(N)))

    mean_1[t] = numpy.mean(a=depo_effe_2, axis=0)
    sd_1[t]   = numpy.std(a=depo_effe_2, axis=0 )

# Plot scatter of means and SDs
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)


conf = configure.Configure(num_nodes=4,initialisation=initialisation,sigma=sigma,type_alpha=type_alpha)

rel = 4.0*conf.mean*conf.get_cdf(x=conf.mean)/numpy.sqrt(3.0)

#ax.scatter(num_nodes_list,mean_1-rel, label=r"mean $j^{1}-\frac{4}{\sqrt{3}}\bar{G}$cdf($\bar{G}$)")
#ax.scatter(num_nodes_list,sd_1, label=r"std. dev. $j^{1}$")
#
## Plot guide lines
#N_smooth =  numpy.linspace(1,num_nodes_list[-1],500)
##ax.plot(N_smooth, (mean_1[-1]-mean_1[0])*numpy.ones_like(N_smooth), color="tab:blue",ls="--")
#
#ax.plot(N_smooth, (mean_1[-1]-rel*numpy.ones_like(N_smooth)), color="tab:blue",ls="--")
#ax.plot(N_smooth, numpy.exp(+0.01)*numpy.power(N_smooth,-0.5), color="tab:orange", label=r"$1.01N^{-\frac{1}{2}}$",ls="-")
#print(numpy.exp(+0.01))



ax.scatter(num_nodes_list,mean_1, label=r"$\mathbb{E}[j^{1}]$")
ax.scatter(num_nodes_list,sd_1, label=r"$\mathbb{S}[j^{1}]$")

# Plot guide lines
N_smooth =  numpy.linspace(1,num_nodes_list[-1],500)
#ax.plot(N_smooth, (mean_1[-1]-mean_1[0])*numpy.ones_like(N_smooth), color="tab:blue",ls="--")

ax.plot(N_smooth, 2.074180794884483*numpy.ones_like(N_smooth), color="tab:blue",ls="-", label=r"$\bar{j}^{1}_{6}$")
ax.plot(N_smooth, mean_1[-1]*numpy.ones_like(N_smooth), color="tab:blue",ls="--", label=r"$\bar{j}^{1}_{N \rightarrow \infty}$")
ax.plot(N_smooth, numpy.exp(+0.01)*numpy.power(N_smooth,-0.5), color="tab:orange", label=r"$1.01N^{-\frac{1}{2}}$",ls="-")
print(numpy.exp(+0.01))


# Cleanup graph 
# -------------
plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$N$",
                             y_label=None,
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"mean-j_and_std-j__v__N.svg"), format="svg")







# Plot Log Log to check gradient of standard deviation
# -------
plotting.thesisify_pre_ax_creation
fig, ax = plt.subplots(1,1)

x = numpy.linspace(0,5,500)
ax.scatter(numpy.log(num_nodes_list),numpy.log(mean_1), label=r"log(mean $j^{1}$$)$")
ax.scatter(numpy.log(num_nodes_list),numpy.log(sd_1), label=r"log(std. dev. $j^{1}$$)$")
ax.plot(x, -0.5*x + (+0.01*numpy.ones_like(x)), color="tab:orange", label=r"$-\frac{1}{2}$log$(N)-0.1$")

# Cleanup graph
# ----------
plotting.thesisify_post_plot(ax=ax,x_label=r"log$(N)$")

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"logmean-j_and_logstd-j__v__logN.svg"), format="svg")