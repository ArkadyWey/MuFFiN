from matplotlib import pyplot as plt
import os 
import numpy

import utils_plot_exp_param_dist


# Parameters 
# -----
path_results = os.path.join(".","results/results_exp_param-dist_6-reg_reps-5000")

#path_results = os.path.join(".","results_experiment_permdist_reps-50k")

#num_nodes_list = [2,8,18,32,50,72,98,128,162,200]
num_nodes_list = [2,18,50,98]
num_tests = len(num_nodes_list)


# Plot permeability histogram fo all N on same graph
# -----    
fig, ax = plt.subplots(1,1)

num_bins_in_range = 250
num_pts_to_interp = 300

ax_parameter_distribution =  utils_plot_exp_param_dist.PlotParameterDistribution(parameter_name="perm",
                                                                        num_nodes_list=num_nodes_list,
                                                                        num_bins_in_range=num_bins_in_range,
                                                                        num_pts_to_interp=num_pts_to_interp,
                                                                        path_results=path_results,
                                                                        ax=ax)

ax.set_xlabel(r"$k^{00}$")
ax.set_ylabel(r"Probability density")
ax.set_xlim(left=1.5,right=4.0)
ax.set_ylim(bottom=0.0)
ax.legend()

plt.savefig(fname=os.path.join(path_results,"prob_density__v__perm.svg"), format="svg")





# Plot mean and standard deviation of each histogram 
# ------
num_nodes_list = [2,8,18,32,50,72,98,128,162]
num_tests = len(num_nodes_list)

fig, ax = plt.subplots(1,1)

# Get mean and standard deviation for each N
mean_1 = numpy.zeros(shape=num_tests)
sd_1 = numpy.zeros(shape=num_tests)
for t in range(num_tests):
    N = num_nodes_list[t]

    perm_effe_2 = numpy.load(os.path.join(path_results, "perm_effe_1_N-{}.npy".format(N)))
    mean_1[t] = numpy.mean(a=perm_effe_2, axis=0)
    
    sd_1[t]   = numpy.std(a=perm_effe_2, axis=0)

print(mean_1)

# Plot scatter for distribution means
#ax.scatter(num_nodes_list,mean_1-mean_1[0], label=r"mean $k^{00}-k^{00}_{N=1}$")
ax.scatter(num_nodes_list,mean_1-2.77982, label=r"mean $k^{00}-\bar{k}_6$")
ax.scatter(num_nodes_list,sd_1, label=r"std. dev. $k^{00}$")

# Plot guide lines
N_smooth = numpy.linspace(1,200,1000)
# square grid fit
#ax.plot(N_smooth, 0.498*numpy.power(N_smooth,-0.5), color="tab:orange", label=r"square grid fit",ls="--")
# random fit
#ax.plot(N_smooth, 1.1*numpy.power(N_smooth,-0.5), color="tab:orange", label=r"random fit",ls=":")
# new fit
ax.plot(N_smooth, 0.561*numpy.power(N_smooth,-0.5), color="tab:orange", label=r"$0.561N^{-\frac{1}{2}}$",ls="-")
#ax.plot(N_smooth, (-0.07469260409119505)*numpy.ones_like(N_smooth), color="tab:blue", ls="--", label=r"square grid mean")
ax.plot(N_smooth, (mean_1[-1]-2.77982)*numpy.ones_like(N_smooth), color="tab:blue", ls="--")

#ax.scatter(num_nodes_list,mean_1-1.72461, label=r"mean-$k^{00}_{N=1}$")
#ax.scatter(num_nodes_list,mean_1-2.77982, label=r"mean-$k^{00}_{N=1}$")
#ax.plot(numpy.linspace(0,100,1000), 0.1*numpy.power(numpy.linspace(0,100,1000),-0.5)-0.1, color="tab:blue")
#ax.plot(numpy.linspace(0,100,500), 0.498*numpy.power(numpy.linspace(0,100,500),-0.5), color="tab:blue")

ax.set_xlabel(r"$N$")

ax.legend()

plt.savefig(fname=os.path.join(path_results,"mean-k_and_std-k__v__N.svg"), format="svg")






# Plot Log Log to check gradient of standard deviation
# -------
fig, ax = plt.subplots(1,1)

N_smoother = numpy.linspace(0.01,5,500)
ax.scatter(numpy.log(num_nodes_list),numpy.log(mean_1), label=r"$log($mean $k^{00}$$)$")
ax.scatter(numpy.log(num_nodes_list),numpy.log(sd_1), label=r"$log$(std. dev. $k^{00}$$)$")
#ax.plot(N_smoother, -0.5*N_smoother + (numpy.log(0.498)*numpy.ones_like(N_smoother)), color="tab:orange", ls="--", label=r"square grid fit")
#ax.plot(N_smoother, -0.5*N_smoother + (0.2*numpy.ones_like(N_smoother)), color="tab:orange", label=r"new fit")
ax.plot(N_smoother, -0.5*N_smoother + (-0.577*numpy.ones_like(N_smoother)), color="tab:orange", label=r"new fit")
#ax.plot(N_smoother, -0.5*N_smoother + (numpy.log(1.1)*numpy.ones_like(N_smoother)), color="tab:orange", label=r"new fit")
# Cleanup plot
ax.set_xlabel(r"$log(N)$")
ax.legend()

plt.savefig(fname=os.path.join(path_results,"logmean-k_and_logstd-k__v__logN.svg"), format="svg")