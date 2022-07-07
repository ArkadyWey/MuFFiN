from matplotlib import pyplot as plt
import os 
import numpy


# Parameters 
# -----
path_results = os.path.join(".","results_experiment_permdist")
 

# Plot permeability histogram fo all N on same graph
# -----    
fig, ax = plt.subplots(1,1)

sds = []
Ns = [1,4,9,16,25,49]
for N in Ns:

    perm_effe_2 = numpy.load(os.path.join(path_results, "perm_effe_2_N-{}.npy".format(N)))

    count, bins, ignored = ax.hist(x=perm_effe_2[0,:], bins=50, density=True, align='mid', alpha=0.4, label=r"$N={}$".format(N))

    #print(numpy.mean(perm_effe_2[0,:])-2.77982)
    sd = numpy.std(perm_effe_2[0,:])
    sds.append(sd)


ax.set_xlabel(r"$k^{00}$")
ax.set_ylabel(r"Probability density")
#ax.set_xlim(left=0.0,right=3.5)
ax.legend()

plt.savefig(fname=os.path.join(path_results,"prob_density__v__perm.svg"), format="svg") 

fig, ax = plt.subplots(1,1)
ax.scatter(Ns,sds)
plt.savefig(fname=os.path.join(path_results,"std__v__N.svg"), format="svg") 
