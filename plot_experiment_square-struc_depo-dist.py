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
path_results = os.path.join(".","results_experiment_permdist_reps-50k")

#num_nodes_list = [16,25,36,49,64,81,100]
num_nodes_list = [1,4,9,16,25,36,49,64,81,100]
#num_nodes_list = [16,36,64,100]
num_tests = len(num_nodes_list)


# Plot deposition parameter histogram fo all N on same graph
# -----    
fig, ax = plt.subplots(1,1)

# Plot histogram for each N
num_bins = 20
#num_bins = numpy.linspace(42,12,num_tests,dtype=int)
counts_1 = []
bins_1 = []
for t in range(num_tests):
    N = num_nodes_list[t]

    depo_effe_2 = -numpy.load(os.path.join(path_results, "depo_effe_2_N-{}.npy".format(N)))/numpy.sqrt(N)

    count, bins, ignored = ax.hist(x=depo_effe_2[0,:], bins=num_bins, density=True, align='mid', label=r"$N={}$".format(num_nodes_list[t]), alpha=0.4)
    counts_1.append(count)
    bins_1.append(bins)

# Reset the color cycle and plot interpolation for each N
plt.gca().set_prop_cycle(None)
for t in range(num_tests):
    N = num_nodes_list[t]

    depo_effe_2 = -numpy.load(os.path.join(path_results, "depo_effe_2_N-{}.npy".format(N)))
    count = counts_1[t]
    bins  = bins_1[t]

    num_pts_to_interp =500
    # TODO: make interp with lower binned histogram to get cleaner lines
    dist_interp_1 = get_new_interpolated_point(table_x=numpy.linspace(min(bins), max(bins), num_bins), 
                                               table_y=count, 
                                               new_x_value=numpy.linspace(min(bins), max(bins), num_pts_to_interp))
    
    ax.plot(numpy.linspace(min(bins), max(bins), num_pts_to_interp), dist_interp_1)

ax.set_xlabel(r"$j^{0}$")
ax.set_ylabel(r"Probability density")
ax.set_xlim(left=0.0,right=0.5)

ax.legend()

plt.savefig(fname=os.path.join(path_results,"prob_density__v__depo.svg"), format="svg")






# Plot mean and standard deviation of each histogram 
# ------

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

ax.scatter(num_nodes_list,mean_1-mean_1[0], label=r"mean $j^{0}-j^{0}_{N=1}$")
ax.scatter(num_nodes_list,sd_1, label=r"std. dev. $j^{0}$")

# Plot guide lines
N_smooth =  numpy.linspace(1,100,500)
ax.plot(N_smooth, (mean_1[-1]-mean_1[0])*numpy.ones_like(N_smooth), color="tab:blue",ls="--")
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