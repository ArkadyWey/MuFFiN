from matplotlib import pyplot as plt
import numpy
import os

# Parameters 
# -----
path_results = os.path.join(".","results/results_kj_asymp")

l = numpy.linspace(1,10,10)
l_smooth = numpy.linspace(l[0],l[-1],1000)

def get_k(N,D,l_smooth):
    """
    Plot the asymptotic behaviour of permeability 
    as a function of number of nodes in cell, for any 
    dimension and length of cell.
    """
    k = N**((D-2)/D)*l_smooth**(2-D)
    return k

def get_j(N,D,l_smooth):
    """
    Plot the asymptotic behaviour of adhesivity 
    as a function of number of nodes in cell, for any 
    dimension and length of cell.
    """
    j = N**((D-1)/D)*l_smooth
    return j

# n = N**(1/D)
N = 1

# Plot k figure 
# -------------
fig, ax = plt.subplots(1,1)

# D=1
k_1 = get_k(N=N,D=1,l_smooth=l_smooth)
ax.plot(l_smooth,k_1,color="tab:blue",ls="-",label=r"$l$")
ax.scatter(l,l,color="tab:blue",label=r"$D=1$")

# D=2
k_2 = get_k(N=N,D=2,l_smooth=l_smooth)
ax.plot(l_smooth,k_2,color="tab:orange",ls="-")
ax.scatter(l,1*numpy.ones_like(l),color="tab:orange",label=r"$D=2$")

# D=3
k_3 = get_k(N=N,D=3,l_smooth=l_smooth)
ax.plot(l_smooth,k_3,color="tab:green",ls="-", label=r"$l^{-1}$")
#ax.scatter(l,l**(-1),color="tab:green",label=r"$D=3$")


ax.legend()
ax.set_ylabel(r"$k^{00}$")
ax.set_xlabel(r"$l$")
plt.savefig(fname=os.path.join(path_results,"k__vs__l.svg"), format="svg")




# Plot j figure 
# -------------
fig, ax = plt.subplots(1,1)

# D=1
j_1 = get_j(N=N,D=1,l_smooth=l_smooth)
ax.plot(l_smooth,j_1,color="tab:blue",ls="-",label=r"$l$")
ax.scatter(l,l,color="tab:blue",label=r"$D=1$")

# D=2
j_2 = get_j(N=N,D=2,l_smooth=l_smooth)
ax.plot(l_smooth,j_2,color="tab:orange",ls="-",label=r"$l$")
ax.scatter(l,l,color="tab:orange",label=r"$D=2$")

# D=3
j_3 = get_j(N=N,D=3,l_smooth=l_smooth)
ax.plot(l_smooth,j_3,color="tab:green",ls="-", label=r"$l$")
#ax.scatter(l,l**(-1),color="tab:green",label=r"$D=3$")


ax.legend()
ax.set_ylabel(r"$j^{0}$")
ax.set_xlabel(r"$l$")
plt.savefig(fname=os.path.join(path_results,"j__vs__l.svg"), format="svg")