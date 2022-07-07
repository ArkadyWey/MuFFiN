from matplotlib import pyplot as plt
import os 
import numpy
from numpy import dtype 
from scipy import interpolate

def get_new_interpolated_point(table_x,table_y,new_x_value):
    """
    Given a list of x values, and corresponding y values, and
    a new x value, approximate the corresponding function, 
    and use this function to return the new y value 
    corresponding to the new x value.

    Parameters 
    ----------
    - table_x: numpy.ndarray
        1-dimensional list of x values.
    - table_y: numpy.ndarray
        1-dimensional list of y values.
    - new_x_value: float
        New x value for which the corresponding y value is to be approximated.
    
    Returns
    -------
    - new_y_value: float
        Interpolated y value corresponding to new_x_value
    """
    interpolated_function = interpolate.splrep(x=table_x,y=table_y,k=3)
    new_y_value = interpolate.splev(x=new_x_value, tck=interpolated_function)
    return new_y_value

# Parameters 
# -----
path_results = os.path.join(".","results_experiment_permdist_random-structure")
#path_results = os.path.join(".","results_experiment_permdist_reps-50k")

#num_nodes_list = [1,4,9,16,25,36,49,64,81,100]
num_nodes_list = [1,4,9,16,25,36,49]
num_tests = len(num_nodes_list)


# Plot permeability histogram fo all N on same graph
# -----    

# Plot histogram for each N
num_bins = numpy.linspace(42,12,num_tests,dtype=int)

fig, ax = plt.subplots(1,1)
counts_1 = []
bins_1 = []
for t in range(num_tests):
    N = num_nodes_list[t]

    perm_effe_2 = numpy.load(os.path.join(path_results, "perm_effe_2_N-{}.npy".format(N)))

    count, bins, ignored = ax.hist(x=perm_effe_2[0,:], bins=num_bins[t], density=True, align='mid', label=r"$N={}$".format(num_nodes_list[t]), alpha=0.4)
    counts_1.append(count)
    bins_1.append(bins)

# Reset the color cycle and plot interpolation of histogram for each N
plt.gca().set_prop_cycle(None)
for t in range(num_tests):
    N = num_nodes_list[t]

    perm_effe_2 = numpy.load(os.path.join(path_results, "perm_effe_2_N-{}.npy".format(N)))
    count = counts_1[t]
    bins  = bins_1[t]

    num_pts_to_interp = 55
    # TODO: make interp with lower binned histogram to get cleaner lines
    #hist = numpy.histogram(a=perm_effe_2[0,:], bins=num_bins[t ], range=None, normed=True, weights=None, density=True)
    dist_interp_1 = get_new_interpolated_point(table_x=numpy.linspace(min(bins), max(bins), num_bins[t]), 
                                               table_y=count, 
                                               new_x_value=numpy.linspace(min(bins), max(bins), num_pts_to_interp))
    
    ax.plot(numpy.linspace(min(bins), max(bins), num_pts_to_interp), dist_interp_1)

ax.set_xlabel(r"$k^{00}$")
ax.set_ylabel(r"Probability density")
ax.set_xlim(left=0.0,right=7.0)
ax.legend()

plt.savefig(fname=os.path.join(path_results,"prob_density__v__perm.svg"), format="svg")





# Plot mean and standard deviation of each histogram 
# ------
fig, ax = plt.subplots(1,1)

# Get mean and standard deviation for each N
mean_1 = numpy.zeros(shape=num_tests)
sd_1 = numpy.zeros(shape=num_tests)
for t in range(num_tests):
    N = num_nodes_list[t]

    perm_effe_2 = numpy.load(os.path.join(path_results, "perm_effe_2_N-{}.npy".format(N)))
    mean_1[t] = numpy.mean(a=perm_effe_2, axis=1)
    sd_1[t]   = numpy.std(a=perm_effe_2, axis=1)


# Plot scatter for distribution means
ax.scatter(num_nodes_list,mean_1-mean_1[0], label=r"mean $k^{00}-k^{00}_{N=1}$")
ax.scatter(num_nodes_list,sd_1, label=r"std. dev. $k^{00}$")

# Plot guide lines
N_smooth = numpy.linspace(1,100,500)
# grid fit
ax.plot(N_smooth, 0.498*numpy.power(N_smooth,-0.5), color="tab:orange", label=r"grid fit",ls="--")
# new fit
ax.plot(N_smooth, 1.221*numpy.power(N_smooth,-0.5), color="tab:orange", label=r"$1.221N^{-\frac{1}{2}}$",ls="-")
ax.plot(N_smooth, (-0.07469260409119505)*numpy.ones_like(N_smooth), color="tab:blue", ls="--", label=r"grid mean")


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
ax.plot(N_smoother, -0.5*N_smoother + (numpy.log(0.498)*numpy.ones_like(N_smoother)), color="tab:orange", ls="--", label=r"grid fit")
ax.plot(N_smoother, -0.5*N_smoother + (0.2*numpy.ones_like(N_smoother)), color="tab:orange", label=r"new fit")
# Cleanup plot
ax.set_xlabel(r"$log(N)$")
ax.legend()

plt.savefig(fname=os.path.join(path_results,"logmean-k_and_logstd-k__v__logN.svg"), format="svg")







# Plot histogram for N=1 (outside to get bins for pdf)
# -----
fig, ax = plt.subplots(1,1)
perm_effe_2 = numpy.load(os.path.join(path_results, "perm_effe_2_N-1.npy"))
count, bins_1, ignored = ax.hist(x=perm_effe_2[0,:], bins=75, density=True, align='mid', label=r"$N=1$", alpha=0.4)

# ...and compare with log-normal distribution that edges are drawn from 
# # -----

import configure
mu = configure.Configure(num_nodes=1).mean
sigma = configure.Configure(num_nodes=1).sd
x = numpy.linspace(min(bins_1), max(bins_1), 1_000)
pdf = (numpy.exp(-(numpy.log(x) - mu)**2 / (2 * sigma**2))  / (x * sigma * numpy.sqrt(2 * numpy.pi))) 
ax.plot(x, pdf, linewidth=2, color='r', label=r"pdf")

ax.set_xlabel(r"$k^{00}$")
ax.set_ylabel(r"Probability density")

ax.legend()
plt.savefig(fname=os.path.join(path_results,"prob_density__v__perm_N=1.svg"), format="svg")