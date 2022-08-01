from matplotlib import pyplot as plt
import os 
import numpy

import utils_plot_exp_param_dist

# Parameters 
# -----
path_results = os.path.join(".","results/results_exp_param-dist_4-reg_reps-10000_sigma-0.3")

#num_nodes_list = [1,4,9,16,25,36,49,64,81,100]
#num_nodes_list = [4,16,36,64,100]
#num_nodes_list = [4,16,36,64]
num_nodes_list = [1,4,16,36,64,100]
num_tests = len(num_nodes_list)


# Plot histograms with all bars same width
# ----------------------------------------
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



# Plot mean and standard deviation of each histogram 
# ------
#num_nodes_list = [1,4,9,16,25,36,49,64,81,100]
#num_nodes_list = [1,4,9,16,25,36,49,64,81]
num_nodes_list = [1,25,100]
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


# Plot scatter for distribution means
ax.scatter(num_nodes_list,mean_1-mean_1[0], label=r"mean $k^{00}-\bar{k}_4$")
ax.scatter(num_nodes_list,sd_1, label=r"std. dev. $k^{00}$")

# Plot guide lines
N_smooth = numpy.linspace(1,100,500)
ax.plot(N_smooth, 0.498*numpy.power(N_smooth,-0.5), color="tab:orange", label=r"$0.498N^{-\frac{1}{2}}$",ls="-")
ax.plot(N_smooth, (mean_1[-1]-mean_1[0])*numpy.ones_like(N_smooth), color="tab:blue", ls="--")

#print(mean_1[-1]-mean_1[0])

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
ax.plot(N_smoother, -0.5*N_smoother + (numpy.log(0.498)*numpy.ones_like(N_smoother)), color="tab:orange", label=r"$-\frac{1}{2}log(N)-0.697$")

# Cleanup plot
ax.set_xlabel(r"$log(N)$")
ax.legend()

plt.savefig(fname=os.path.join(path_results,"logmean-k_and_logstd-k__v__logN.svg"), format="svg")







# Plot histogram for N=1 (outside to get bins for pdf)
# -----
fig, ax = plt.subplots(1,1)
perm_effe_2 = numpy.load(os.path.join(path_results, "perm_effe_1_N-1.npy"))
count, bins_1, ignored = ax.hist(x=perm_effe_2[:], bins=75, density=True, align='mid', label=r"$N=1$", alpha=0.4)

# ...and compare with log-normal distribution that edges are drawn from 
# # -----

import configure
mu = configure.Configure(num_nodes=1,l1=1.0,l2=1.0).mean
sigma = configure.Configure(num_nodes=1,l1=1.0,l2=1.0).sd
x = numpy.linspace(min(bins_1), max(bins_1), 1_000)
pdf = (numpy.exp(-(numpy.log(x) - mu)**2 / (2 * sigma**2))  / (x * sigma * numpy.sqrt(2 * numpy.pi))) 
ax.plot(x, pdf, linewidth=2, color='r', label=r"pdf")

ax.set_xlabel(r"$k^{00}$")
ax.set_ylabel(r"Probability density")

ax.legend()
plt.savefig(fname=os.path.join(path_results,"prob_density__v__perm_N=1.svg"), format="svg")