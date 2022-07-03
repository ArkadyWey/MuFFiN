from matplotlib import pyplot as plt
import numpy
import os

# Parameters 
# -----
path_results = os.path.join(".","results_kj_asymp")

N = numpy.linspace(1,10,10)**2
N_smooth = numpy.linspace(N[0],N[-1],1000)

def get_k(N_smooth,D,l):
    """
    Plot the asymptotic behaviour of permeability 
    as a function of number of nodes in cell, for any 
    dimension and length of cell.
    """
    k = N_smooth**((D-2)/D)*l**(2-D)
    return k

def get_j(N_smooth,D,l):
    """
    Plot the asymptotic behaviour of adhesivity 
    as a function of number of nodes in cell, for any 
    dimension and length of cell.
    """
    j = N_smooth**((D-1)/D)*l
    return j



Ds = [1,2,3]
ls = numpy.linspace(1,5,5)


colors = ["tab:blue","tab:orange","tab:green"]
linestyles = ["-",(0,(5,1)),(0,(5,5)),(0,(5,10)),(0,(1,1))]



# Plot k figure 
# -------------
fig, ax = plt.subplots(1,1)

for iD,D in enumerate(Ds):
    for il,l in enumerate(ls):
        k = get_k(N_smooth=N_smooth,D=D,l=l)
        ax.plot(N_smooth,k,color=colors[iD],ls=linestyles[il],label=r"$D={}$".format(D))

ax.legend()
ax.set_ylabel(r"$k^{00}$")
ax.set_xlabel(r"$N$")
plt.savefig(fname=os.path.join(path_results,"k__vs__N_sweep_l.svg"), format="svg")


# Plot j figure 
# -------------
fig, ax = plt.subplots(1,1)

for iD,D in enumerate(Ds):
    for il,l in enumerate(ls):
        j = get_j(N_smooth=N_smooth,D=D,l=l)
        ax.plot(N_smooth,j,color=colors[iD],ls=linestyles[il],label=r"$D={}$".format(D))

ax.legend()
ax.set_ylabel(r"$j^{0}$")
ax.set_xlabel(r"$N$")
plt.savefig(fname=os.path.join(path_results,"j__vs__N_sweep_l.svg"), format="svg")
