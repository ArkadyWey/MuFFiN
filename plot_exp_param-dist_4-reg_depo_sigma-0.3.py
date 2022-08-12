from matplotlib import pyplot as plt
import os 
import numpy
from scipy import interpolate

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



# Plot deposition parameter histogram fo all N on same graph
# -----------------------    
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)


#num_nodes_list = [16,25,36,49,64,81,100]
#num_nodes_list = [1,4,9,16,25,36,49,64,81,100]
num_nodes_list = [4,16,36,64,100]
#num_nodes_list = [1,25,100].0
#num_nodes_list = [9]
num_tests = len(num_nodes_list)

num_bins_in_range = 100
num_pts_to_interp = 250


# Must divide by sqrt(N) and make psitive to generate this j, since wasn't done in simulation
ax_parameter_distribution =  utils_plot_exp_param_dist.PlotParameterDistribution(parameter_name="depo",
                                                                        num_nodes_list=num_nodes_list,
                                                                        num_bins_in_range=num_bins_in_range,
                                                                        num_pts_to_interp=num_pts_to_interp,
                                                                        path_results=path_results,
                                                                        ax=ax)


conf = configure.Configure(num_nodes=1,
                           initialisation=initialisation,
                           sigma=sigma)

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$j^{0}$",
                             y_label=r"Probability density",
                             x_left=0.0,
                             x_right=conf.mean+0.1,
                             y_bottom=0.0,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"prob_density__v__depo.svg"))







# Plot deposition parameter with boxes
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
    conf = configure.Configure(num_nodes=1,
                               initialisation=initialisation,
                               sigma=sigma)


    num_bins = 500
    min_val = 0.0
    max_val = conf.mean

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



    # Plot a bar at each scaled B value 
    # with width max distribution we expect from this 
    # edge contribution
    # Height is scaled with tallest bar in j distribution
    # -----
    count_adhe_hori_1 = numpy.load(os.path.join(path_results, "count_adhe_hori_1_N-{}.npy".format(N)))

    num_bins_adhe = N+1
    plot_depo_aprx_v_density = utils_plot_exp_param_dist.Plot_DepoAprx_vs_Density(num_nodes=N,
                                                                                  num_bins=num_bins_adhe,
                                                                                  conf=conf, 
                                                                                  count_adhe_1=count_adhe_hori_1, 
                                                                                  max_height=max(y2))
    
    

    ax.bar(x=plot_depo_aprx_v_density.x_j_aprx_1, 
           height=plot_depo_aprx_v_density.height_adhe_1, 
           width=plot_depo_aprx_v_density.width, 
           bottom=None, 
           align='center', 
           alpha=1.0, 
           data=None, 
           label=r"$N={}$".format(N), 
           fill=False,
           edgecolor=colors[t], 
           linewidth=1.0)


    # Plot dashed line at mean
    for i in range(len(plot_depo_aprx_v_density.x_j_aprx_1)):
        ax.vlines(x=plot_depo_aprx_v_density.x_j_aprx_1[i], 
                  ymin=0.0, 
                  ymax=plot_depo_aprx_v_density.height_adhe_1[i], 
                  color=colors[t], 
                  linewidth=1.0, 
                  linestyle="--", 
                  alpha=1.0)


# Attempt to fit a log-normal distribution
# -------
sigma = conf.sigma/numpy.sqrt(N)
#for i,N in enumerate(num_nodes_list):
#for mu in plot_depo_aprx_v_density.x_j_aprx_1:
mu = numpy.log(conf.mean/2)-(sigma**2)/2
#mu = conf.mu + numpy.log(conf.mean/2/N)
x = numpy.linspace(mu-10, mu+10, 1_0000)
# Normal
# pdf = (numpy.exp(-(x - mu)**2 / (2 * sigma**2))  / (sigma * numpy.sqrt(2 * numpy.pi))) 
# lognormal
pdf = (numpy.exp(-(numpy.log(x) - mu)**2 / (2 * sigma**2))  / (x * sigma * numpy.sqrt(2 * numpy.pi)))/numpy.sqrt(N)
ax.plot(x, pdf, linewidth=1, linestyle="--", label=r"$\sigma={}$".format(sigma), color="tab:red")

# Cleanup graph 
# -------------
plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$j^{0}$",
                             y_label=r"Probability density",
                             x_left=0.0,
                             x_right=conf.mean,
                             y_bottom=0.0,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"prob_density__v__depo__with_approx.svg"))








# Plot mean and standard deviation of each histogram 
# ------
num_nodes_list = [1,4,9,16,25,36,49,64,81,100]
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


conf = configure.Configure(num_nodes=1,
                           initialisation=initialisation,
                           sigma=sigma)

ax.scatter(num_nodes_list,mean_1-conf.mean*conf.get_cdf(x=conf.mean), label=r"mean $j^{0}-\bar{G}$cdf($\bar{G}$)")
ax.scatter(num_nodes_list,sd_1, label=r"std. dev. $j^{0}$")

# Plot guide lines
N_smooth =  numpy.linspace(1,100,500)
#ax.plot(N_smooth, (mean_1[-1]-mean_1[0])*numpy.ones_like(N_smooth), color="tab:blue",ls="--")

ax.plot(N_smooth, (mean_1[-1]-conf.mean*conf.get_cdf(x=conf.mean))*numpy.ones_like(N_smooth), color="tab:blue",ls="--")
ax.plot(N_smooth, 0.6703200460356393*numpy.power(N_smooth,-0.5), color="tab:orange", label=r"$0.670N^{-\frac{1}{2}}$",ls="-")
#print(numpy.exp(-0.40)) = 0.6703200460356393
# Cleanup plot
# Cleanup graph 
# -------------
plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$N$",
                             y_label=None,
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)

print(mean_1[-1])
print(mean_1[0])
plotting.save_fig(fig=fig,fname=os.path.join(path_results,"mean-j_and_std-j__v__N.svg"), format="svg")


#ax.plot(numpy.linspace(1,100,500), (mean_1[-1]-mean_1[0])*numpy.ones_like(numpy.linspace(1,100,500)), color="tab:blue", ls="--")
#ax.plot(numpy.linspace(0,100,1000), 0.1*numpy.power(numpy.linspace(0,100,1000),-0.5)-0.1, color="tab:blue")
#ax.plot(numpy.linspace(0,100,500), 0.498*numpy.power(numpy.linspace(0,100,500),-0.5), color="tab:blue")





# Plot Log Log to check gradient of standard deviation
# -------
plotting.thesisify_pre_ax_creation
fig, ax = plt.subplots(1,1)

x = numpy.linspace(0,5,500)
ax.scatter(numpy.log(num_nodes_list),numpy.log(mean_1), label=r"log(mean $j^{0}$$)$")
ax.scatter(numpy.log(num_nodes_list),numpy.log(sd_1), label=r"log(std. dev. $j^{0}$$)$")
ax.plot(x, -0.5*x + (-0.40*numpy.ones_like(x)), color="tab:orange", label=r"$-\frac{1}{2}$log$(N)-0.40$")

# Cleanup plot
plotting.thesisify_post_plot(ax=ax,x_label=r"log$(N)$")

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"logmean-j_and_logstd-j__v__logN.svg"), format="svg")