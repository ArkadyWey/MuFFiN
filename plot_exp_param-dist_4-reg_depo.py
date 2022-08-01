from matplotlib import pyplot as plt
import os 
import numpy
from scipy import interpolate

import configure
import utils_plot_exp_param_dist


# Parameters 
# -----
path_results = os.path.join(".","results/results_exp_param-dist_4-reg_reps-10000_sigma-0.03")

#num_nodes_list = [16,25,36,49,64,81,100]
#num_nodes_list = [1,4,9,16,25,36,49,64,81,100]
#num_nodes_list = [4,16,36,64,100]
#num_nodes_list = [1,25,100].0
num_nodes_list = [9]
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
beta = 0.04
#ax.vlines(x=0*1.6494/4,ymin=0,ymax=30, color="tab:orange") # 1.7264 1.6488 1.6570 1.6494
#ax.vlines(x=1*1.6494/4,ymin=0,ymax=30, color="tab:orange") # 1.7264 1.6488 1.6570
#ax.vlines(x=2*1.6494/4,ymin=0,ymax=30, color="tab:orange") # 1.7264 1.6488 1.6570
#ax.vlines(x=3*1.6494/4,ymin=0,ymax=30, color="tab:orange") # 1.7264 1.6488 1.6570
#ax.vlines(x=4*1.6494/4,ymin=0,ymax=30, color="tab:orange") # 1.7264 1.6488 1.6570

ax.vlines(x=0*1.6494/9,ymin=0,ymax=30, color="tab:green")  # 1.7264
ax.vlines(x=1*1.6494/9,ymin=0,ymax=30, color="tab:green")  # 1.7264
ax.vlines(x=2*1.6494/9,ymin=0,ymax=30, color="tab:green")  # 1.7264
ax.vlines(x=3*1.6494/9,ymin=0,ymax=30, color="tab:green")  # 1.7264
ax.vlines(x=4*1.6494/9,ymin=0,ymax=30, color="tab:green")  # 1.7264
ax.vlines(x=5*1.6494/9,ymin=0,ymax=30, color="tab:green")  # 1.7264
ax.vlines(x=6*1.6494/9,ymin=0,ymax=30, color="tab:green")  # 1.7264
ax.vlines(x=7*1.6494/9,ymin=0,ymax=30, color="tab:green")  # 1.7264
ax.vlines(x=8*1.6494/9,ymin=0,ymax=30, color="tab:green")  # 1.7264
ax.vlines(x=9*1.6494/9,ymin=0,ymax=30, color="tab:green")  # 1.7264
#
#ax.vlines(x=0* 1.7264/16,ymin=0, ymax=35, color="tab:red")  # 1.7264
#ax.vlines(x=1* 1.7264/16,ymin=0, ymax=35, color="tab:red")  # 1.7264
#ax.vlines(x=2* 1.7264/16,ymin=0, ymax=35, color="tab:red")  # 1.7264
#ax.vlines(x=3* 1.7264/16,ymin=0, ymax=35, color="tab:red")  # 1.7264
#ax.vlines(x=4* 1.7264/16,ymin=0, ymax=35, color="tab:red")  # 1.7264
#ax.vlines(x=5* 1.7264/16,ymin=0, ymax=35, color="tab:red")  # 1.7264
#ax.vlines(x=6* 1.7264/16,ymin=0, ymax=35, color="tab:red")  # 1.7264
#ax.vlines(x=7* 1.7264/16,ymin=0, ymax=35, color="tab:red")  # 1.7264
#ax.vlines(x=8* 1.7264/16,ymin=0, ymax=35, color="tab:red")  # 1.7264
#ax.vlines(x=9* 1.7264/16,ymin=0, ymax=35, color="tab:red")  # 1.7264
#ax.vlines(x=10*1.7264/16,ymin=0,ymax=35, color="tab:red")  # 1.7264
#ax.vlines(x=11*1.7264/16,ymin=0,ymax=35, color="tab:red")  # 1.7264
#ax.vlines(x=12*1.7264/16,ymin=0,ymax=35, color="tab:red")  # 1.7264
#ax.vlines(x=13*1.7264/16,ymin=0,ymax=35, color="tab:red")  # 1.7264
#ax.vlines(x=14*1.7264/16,ymin=0,ymax=35, color="tab:red")  # 1.7264
#ax.vlines(x=15*1.7264/16,ymin=0,ymax=35, color="tab:red")  # 1.7264
#ax.vlines(x=16*1.7264/16,ymin=0,ymax=35, color="tab:red")  # 1.7264


ax.set_xlabel(r"$j^{0}$")
ax.set_ylabel(r"Probability density")
#ax.set_xlim(left=0.0,right=0.5)
ax.set_ylim(bottom=0.0)

ax.legend()

plt.savefig(fname=os.path.join(path_results,"prob_density__v__depo.svg"), format="svg")







fig, ax = plt.subplots(1,1)
num_nodes_list = [9]
colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]
for t, N in enumerate(num_nodes_list):

    conf = configure.Configure(num_nodes=N,
                               l1=numpy.sqrt(N),
                               l2=numpy.sqrt(N))

    # Plot real j distribution
    # -----------------------
    depo_effe_1     = numpy.load(os.path.join(path_results, "depo_effe_1_N-{}.npy".format(N)))

    num_bins_depo = 500
    plot_depo_v_density = utils_plot_exp_param_dist.Plot_Depo_vs_Density(num_bins=num_bins_depo,
                                                                         conf=conf)
    
    count_depo_1, bins_depo, _ignored = ax.hist(x=depo_effe_1, 
                                                bins=plot_depo_v_density.bin_edges, 
                                                density=True, 
                                                align='mid', 
                                                label=r"$N={}$".format(num_nodes_list[t]), 
                                                alpha=0.4, color=colors[t])
   
    

    # Interpolate j histograms
    bin_centres = numpy.linspace(start=0.0, stop=conf.mean, num=num_bins_depo, endpoint=True)
    spl = interpolate.splrep(bin_centres, count_depo_1, k=3)
    x2 = numpy.linspace(bin_centres[0], bin_centres[-1], 10*num_bins_depo)
    y2 = interpolate.splev(x2, spl)
    ax.plot(x2,y2,color=colors[t], 
                  linewidth=1.0, 
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

# Cleanup graph 
# -------------
ax.set_xlabel(r"$j^{0}$")
ax.set_ylabel(r"Probability density")
ax.set_xlim(left=0.0,right=conf.mean)
ax.set_ylim(bottom=0.0)

ax.legend()


fig.savefig(fname=os.path.join(path_results,"prob_density__v__j_approx.svg"), format="svg")








# Plot mean and standard deviation of each histogram 
# ------
#num_nodes_list = [1,4,9,16,25,36,49,64,81,100]
#num_nodes_list = [1,25,100]
num_nodes_list = [1,4,9,16,25,36,49,64,81,100]
num_tests = len(num_nodes_list)

# Get mean and standard deviation at each N
mean_1 = numpy.zeros(shape=num_tests)
sd_1 = numpy.zeros(shape=num_tests)
for t in range(num_tests):
    N = num_nodes_list[t]

    depo_effe_2 = -numpy.load(os.path.join(path_results, "depo_effe_1_N-{}.npy".format(N)))

    mean_1[t] = numpy.mean(a=depo_effe_2/numpy.sqrt(N), axis=0)
    sd_1[t]   = numpy.std(a=depo_effe_2/numpy.sqrt(N), axis=0)

# Plot scatter of means and SDs
fig, ax = plt.subplots(1,1)

ax.scatter(num_nodes_list,mean_1-mean_1[0], label=r"mean $j^{0}-j^{0}_{N=1}$")
ax.scatter(num_nodes_list,sd_1, label=r"std. dev. $j^{0}$")

# Plot guide lines
N_smooth =  numpy.linspace(1,100,500)
#ax.plot(N_smooth, (mean_1[-1]-mean_1[0])*numpy.ones_like(N_smooth), color="tab:blue",ls="--")

import configure
expected_j_mean = conf = configure.Configure(num_nodes=1,l1=1,l2=1).mean/2
ax.plot(N_smooth, expected_j_mean*numpy.ones_like(N_smooth), color="tab:blue",ls="--")

ax.plot(N_smooth, 0.4065696597*numpy.power(N_smooth,-0.5), color="tab:orange", label=r"$0.406N^{-\frac{1}{2}}$",ls="-")

# Cleanup plot
ax.set_xlabel(r"$N$")
ax.legend()

print(mean_1[-1])
print(mean_1[0])
plt.savefig(fname=os.path.join(path_results,"mean-j_and_std-j__v__N.svg"), format="svg")


#ax.plot(numpy.linspace(1,100,500), (mean_1[-1]-mean_1[0])*numpy.ones_like(numpy.linspace(1,100,500)), color="tab:blue", ls="--")
#ax.plot(numpy.linspace(0,100,1000), 0.1*numpy.power(numpy.linspace(0,100,1000),-0.5)-0.1, color="tab:blue")
#ax.plot(numpy.linspace(0,100,500), 0.498*numpy.power(numpy.linspace(0,100,500),-0.5), color="tab:blue")





# Plot Log Log to check gradient of standard deviation
# -------
fig, ax = plt.subplots(1,1)


ax.scatter(numpy.log(num_nodes_list),numpy.log(mean_1), label=r"$log($mean $j^{0}$$)$")
ax.scatter(numpy.log(num_nodes_list),numpy.log(sd_1), label=r"$log$(std. dev. $j^{0}$$)$")
ax.plot( numpy.linspace(1,5,500), -0.5*numpy.linspace(1,5,500) + (-0.9*numpy.ones_like(numpy.linspace(1,5,500))), color="tab:orange", label=r"$-\frac{1}{2}log(N)-0.9$")

# Cleanup plot
ax.set_xlabel(r"$log(N)$")
ax.legend()

plt.savefig(fname=os.path.join(path_results,"logmean-j_and_logstd-j__v__logN.svg"), format="svg")





# TODO: 
# Consider checking what distribution the final gistogram is similar too?