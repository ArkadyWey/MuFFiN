from matplotlib import pyplot as plt
import os 
import numpy

import utils_param_dist

# Parameters 
# -----
path_results = os.path.join(".","results/results_experiment_param-dist_random-structure_reps-50k")

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
ax_parameter_distribution =  utils_param_dist.PlotParameterDistribution(parameter_name="depo",
                                                                        num_nodes_list=num_nodes_list,
                                                                        num_bins_in_range=num_bins_in_range,
                                                                        num_pts_to_interp=num_pts_to_interp,
                                                                        path_results=path_results,
                                                                        ax=ax)

ax.set_xlabel(r"$j^{0}$")
ax.set_ylabel(r"Probability density")
ax.set_xlim(left=0.0,right=2.0)
ax.set_ylim(bottom=0.0)

ax.legend()

plt.savefig(fname=os.path.join(path_results,"prob_density__v__depo.svg"), format="svg")






# Plot mean and standard deviation of each histogram 
# ------
num_nodes_list = [4,9,16,25,36,49,64,81,100]
num_tests = len( num_nodes_list)

# Get mean and standard deviation at each N
mean_1 = numpy.zeros(shape=num_tests)
sd_1 = numpy.zeros(shape=num_tests)
for t in range(num_tests):
    N = num_nodes_list[t]

    depo_effe_2 = -numpy.load(os.path.join(path_results, "depo_effe_2_N-{}.npy".format(N)))

    mean_1[t] = numpy.mean(a=depo_effe_2/numpy.sqrt(N), axis=1)
    sd_1[t]   = numpy.std(a=depo_effe_2/numpy.sqrt(N), axis=1)

# Plot scatter of means and SDs
fig, ax = plt.subplots(1,1)

# Mean minus first mean
ax.scatter(num_nodes_list,mean_1-mean_1[0], label=r"mean $j^{0}$-mean $j^{0}_{N=1}$")
ax.scatter(num_nodes_list,sd_1, label=r"std. dev. $j^{0}$")

# Plot guide lines
N_smooth =  numpy.linspace(1,100,500)
ax.plot(N_smooth, (mean_1[-1]-mean_1[0])*numpy.ones_like(N_smooth), color="tab:blue",ls="--")
ax.plot(N_smooth, numpy.exp(-0.25)*numpy.power(N_smooth,-1.0/3.0), color="tab:orange", label=r"$0.779N^{-\frac{1}{3}}$",ls="-")
#print(numpy.exp(-0.25))

# Cleanup plot
ax.set_xlabel(r"$N$")
ax.legend()

#print(mean_1[-1])
#print(mean_1[0])
plt.savefig(fname=os.path.join(path_results,"mean-j_and_std-j__v__N.svg"), format="svg")



# Plot Log Log to check gradient of standard deviation
# -------
fig, ax = plt.subplots(1,1)


ax.scatter(numpy.log(num_nodes_list),numpy.log(mean_1), label=r"$log($mean $j^{0}$$)$")
ax.scatter(numpy.log(num_nodes_list),numpy.log(sd_1), label=r"$log$(std. dev. $j^{0}$$)$")
ax.plot( numpy.linspace(1,5,500), -1/3*numpy.linspace(1,5,500) + (-0.25*numpy.ones_like(numpy.linspace(1,5,500))), color="tab:orange", label=r"$-\frac{1}{3}log(N)-0.25$")

# Cleanup plot
ax.set_xlabel(r"$log(N)$")
ax.legend()

plt.savefig(fname=os.path.join(path_results,"logmean-j_and_logstd-j__v__logN.svg"), format="svg")