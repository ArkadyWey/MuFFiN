from matplotlib import pyplot as plt
import os 
import numpy 



# Parameters 
# -----
path_results = os.path.join(".","results_experiment_permdist")


# Load variables
# -----
perm_effe_2 = numpy.load(os.path.join(path_results, "perm_effe_2.npy"))


# Plot permeability histogram 
# -----

num_tests = len(perm_effe_2[:,0])
num_reps  = len(perm_effe_2[0,:])

num_nodes_list = [1,4]




# Plot histogram for N=1 (outside to get bins for pdf)
# -----
fig, ax = plt.subplots(1,1)

count, bins_1, ignored = ax.hist(x=perm_effe_2[0,:], bins=50, density=True, align='mid', label=r"$N=1$", alpha=0.4)
# ...and compare with log-normal distribution that edges are drawn from 
# -----
import configure
mu = configure.Configure(num_nodes=1).mean
sigma = configure.Configure(num_nodes=1).sd

x = numpy.linspace(min(bins_1), max(bins_1), 1_000)

pdf = (numpy.exp(-(numpy.log(x) - mu)**2 / (2 * sigma**2))  / (x * sigma * numpy.sqrt(2 * numpy.pi))) 

ax.plot(x, pdf, linewidth=2, color='r', label=r"pdf")

ax.legend()
plt.savefig(fname=os.path.join(path_results,"prob_density__v__perm_N=1.svg"), format="svg")




# Plot histogram for all N on same graph
# -----
fig, ax = plt.subplots(1,1)

for t in range(num_tests):
    count, bins, ignored = ax.hist(x=perm_effe_2[t,:], bins=50, density=True, align='mid', label=r"$N={}$".format(num_nodes_list[t]), alpha=0.4)

ax.set_xlabel(r"$k^{00}$")
ax.set_ylabel(r"Probability density")
ax.legend()

plt.savefig(fname=os.path.join(path_results,"prob_density__v__perm.svg"), format="svg")