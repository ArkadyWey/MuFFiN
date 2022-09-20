from matplotlib import pyplot as plt
import numpy
import os

# Parameters 
# -----
path_results = os.path.join(".","results/results_exp_kj__vs__Nl")
 

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


l = 1.0

# Plot k figure 
# -------------
fig, ax = plt.subplots(1,1)

# D=1
k_1 = get_k(N_smooth=N_smooth,D=1,l=l)
ax.plot(N_smooth,k_1,color="tab:blue",ls="-",label=r"$N^{-1}$")
ax.scatter(N,1/N,color="tab:blue",label=r"$D=1$")

# D=2
k_2 = get_k(N_smooth=N_smooth,D=2,l=l)
ax.plot(N_smooth,k_2,color="tab:orange",ls="-")
ax.scatter(N,1*numpy.ones_like(N),color="tab:orange",label=r"$D=2$")

# D=3
k_3 = get_k(N_smooth=N_smooth,D=3,l=l)
ax.plot(N_smooth,k_3,color="tab:green",ls="-",label=r"$N^{\frac{1}{3}}$")


ax.legend()
ax.set_ylabel(r"$k^{00}$")
ax.set_xlabel(r"$N$")
plt.savefig(fname=os.path.join(path_results,"k__vs__N.svg"), format="svg")




# Plot j figure 
# -------------
fig, ax = plt.subplots(1,1)

# D=1
j_1 = get_j(N_smooth=N_smooth,D=1,l=l)
ax.plot(N_smooth,j_1,color="tab:blue",ls="-")
ax.scatter(N,1*numpy.ones_like(N),color="tab:blue",label=r"$D=1$")

# D=2
j_2 = get_j(N_smooth=N_smooth,D=2,l=l)
ax.plot(N_smooth,j_2,color="tab:orange",ls="-",label=r"$N^{\frac{1}{2}}$")
ax.scatter(N,numpy.sqrt(N),color="tab:orange",label=r"$D=2$")

# D=3
j_3 = get_j(N_smooth=N_smooth,D=3,l=l)
ax.plot(N_smooth,j_3,color="tab:green",ls="-",label=r"$N^{\frac{2}{3}}$")

ax.legend()
ax.set_ylabel(r"$j^{0}$")
ax.set_xlabel(r"$N$")
plt.savefig(fname=os.path.join(path_results,"j__vs__N.svg"), format="svg")