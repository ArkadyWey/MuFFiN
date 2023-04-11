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
#path_results = os.path.join(".","results_experiment_permdist_temp")
path_results = os.path.join(".","results_experiment_permdist_reps-50k")
#path_results = os.path.join(".","results_experiment_depodist_random-conductance")

#num_nodes_list = [16,25,36,49,64,81,100]
num_nodes_list = [1,4,9,16,25,36,49,64,81,100]
#num_nodes_list = [16,36,64,100]
num_tests = len(num_nodes_list)


# Plot permeability histogram fo all N on same graph
# -----    
#num_bins = numpy.linspace(42,12,num_tests,dtype=int)
num_bins = 20

fig, ax = plt.subplots(1,1)
counts_1 = []
bins_1 = []
for t in range(num_tests):
    N = num_nodes_list[t]

    perm_effe_2 = -numpy.load(os.path.join(path_results, "depo_effe_2_N-{}.npy".format(N)))/numpy.sqrt(N)

    count, bins, ignored = ax.hist(x=perm_effe_2[0,:], bins=num_bins, density=True, align='mid', label=r"$N={}$".format(num_nodes_list[t]), alpha=0.4)
    counts_1.append(count)
    bins_1.append(bins)

# Reset the color cycle
plt.gca().set_prop_cycle(None)
for t in range(num_tests):
    N = num_nodes_list[t]

    perm_effe_2 = -numpy.load(os.path.join(path_results, "depo_effe_2_N-{}.npy".format(N)))
    count = counts_1[t]
    bins  = bins_1[t]

    num_pts_to_interp =500
    # TODO: make interp with lower binned histogram to get cleaner lines
    #hist = numpy.histogram(a=perm_effe_2[0,:], bins=num_bins[t], range=None, normed=True, weights=None, density=True)
    dist_interp_1 = get_new_interpolated_point(table_x=numpy.linspace(min(bins), max(bins), num_bins), 
                                               table_y=count, 
                                               new_x_value=numpy.linspace(min(bins), max(bins), num_pts_to_interp))
    
    ax.plot(numpy.linspace(min(bins), max(bins), num_pts_to_interp), dist_interp_1)

#ax.set_xlabel(r"$k^{11}$")
ax.set_xlabel(r"$j^{1}$")
ax.set_ylabel(r"Probability density")
#ax.set_xlim(left=0.0,right=3.5)
ax.legend()

plt.savefig(fname=os.path.join(path_results,"prob_density__v__perm.svg"), format="svg")





# Plot mean and standard deviation of each histogram 
# ------
fig, ax = plt.subplots(1,1)

mean_1 = numpy.zeros(shape=num_tests)
sd_1 = numpy.zeros(shape=num_tests)
for t in range(num_tests):
    N = num_nodes_list[t]

    perm_effe_2 = -numpy.load(os.path.join(path_results, "depo_effe_2_N-{}.npy".format(N)))
    mean_1[t] = numpy.mean(a=perm_effe_2/numpy.sqrt(N), axis=1)
    sd_1[t]   = numpy.std(a=perm_effe_2/numpy.sqrt(N), axis=1)

print(mean_1)


#ax.scatter(num_nodes_list,mean_1-mean_1[0], label=r"mean-$k^{11}_{N=1}$")
ax.scatter(num_nodes_list,mean_1, label=r"mean $j^{1}$")
ax.plot(numpy.linspace(1,100,500), 0.406*numpy.power(numpy.linspace(1,100,500),-0.5), color="tab:orange")
ax.scatter(num_nodes_list,sd_1, label=r"std. dev. $j^{1}$")
#ax.plot(numpy.linspace(1,100,500), (mean_1[-1]-mean_1[0])*numpy.ones_like(numpy.linspace(1,100,500)), color="tab:blue", ls="--")
#ax.plot(numpy.linspace(0,100,1000), 0.1*numpy.power(numpy.linspace(0,100,1000),-0.5)-0.1, color="tab:blue")
#ax.plot(numpy.linspace(0,100,500), 0.498*numpy.power(numpy.linspace(0,100,500),-0.5), color="tab:blue")

# Log Log
# -------
#ax.scatter(numpy.log(num_nodes_list),numpy.log(mean_1), label=r"mean $j^{1}$")
#ax.scatter(numpy.log(num_nodes_list),numpy.log(sd_1), label=r"std. dev. $j^{1}$")
#ax.plot( numpy.linspace(1,5,500), -0.5*numpy.linspace(1,5,500) + (-0.9*numpy.ones_like(numpy.linspace(1,5,500))), color="tab:orange")

ax.set_xlabel(r"$N$")

ax.legend()

plt.savefig(fname=os.path.join(path_results,"mean_and_std__v__N.svg"), format="svg")







# Plot histogram for N=1 (outside to get bins for pdf)
# -----
fig, ax = plt.subplots(1,1)
perm_effe_2 = -numpy.load(os.path.join(path_results, "depo_effe_2_N-1.npy"))
count, bins_1, ignored = ax.hist(x=perm_effe_2[0,:], bins=75, density=True, align='mid', label=r"$N=1$", alpha=0.4)

# ...and compare with log-normal distribution that edges are drawn from 
# # -----

import configure
mu = configure.Configure(num_nodes=1,initialisation="4-reg").mean
sigma = configure.Configure(num_nodes=1,initialisation="4-reg").sd
x = numpy.linspace(min(bins_1), max(bins_1), 1_000)
pdf = (numpy.exp(-(numpy.log(x) - mu)**2 / (2 * sigma**2))  / (x * sigma * numpy.sqrt(2 * numpy.pi))) 
ax.plot(x, pdf, linewidth=2, color='r', label=r"pdf")

ax.set_xlabel(r"$k^{11}$")
ax.set_ylabel(r"Probability density")

ax.legend()
plt.savefig(fname=os.path.join(path_results,"prob_density__v__perm_N=1.svg"), format="svg")