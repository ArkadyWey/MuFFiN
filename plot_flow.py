from matplotlib import pyplot as plt
import os
import numpy

# Parameters 
# -----
path_results = os.path.join(".","results_flow")


# Load variables 
# -----
time_1 = numpy.load(os.path.join(path_results, "time_1.npy"))
posi_1 = numpy.load(os.path.join(path_results, "posi_1.npy"))

conc_2 = numpy.load(os.path.join(path_results, "conc_2.npy"))
velo_1 = numpy.load(os.path.join(path_results, "velo_1.npy"))
psi_2  = numpy.load(os.path.join(path_results, "psi_2.npy"))
perm_solver_2 = numpy.load(os.path.join(path_results, "perm_solver_2.npy"))
depo_solver_2 = numpy.load(os.path.join(path_results, "depo_solver_2.npy"))
dpdx_2 = numpy.load(os.path.join(path_results, "dpdx_2.npy"))


num_times = len(time_1)

start          = 0
first_quarter  = int(1*(num_times-1)/4)
second_quarter = int(2*(num_times-1)/4)
third_quarter  = int(3*(num_times-1)/4)
end            = -1


# Plot conccentration
# -----
fig, ax = plt.subplots(1,1)
ax.plot(posi_1,conc_2[:,start])
ax.plot(posi_1,conc_2[:,first_quarter])
ax.plot(posi_1,conc_2[:,second_quarter])
ax.plot(posi_1,conc_2[:,third_quarter])
ax.plot(posi_1,conc_2[:,end])

ax.set_xlabel("x")
ax.set_ylabel("c")

plt.savefig(fname=os.path.join(path_results,"conc_2__v__posi_1.svg"), format="svg")


# Plot velocity 
# -----
fig, ax = plt.subplots(1,1)

ax.plot(time_1,velo_1)

ax.set_xlabel(r"$t$")
ax.set_ylabel(r"$u$")

plt.savefig(fname=os.path.join(path_results,"velo_1__v__time_1.svg"), format="svg")


# Plot reaction parameter 
# -----
fig, ax = plt.subplots(1,1)

ax.plot(posi_1,psi_2[:,start])
ax.plot(posi_1,psi_2[:,start+50])
ax.plot(posi_1,psi_2[:,second_quarter])
ax.plot(posi_1,psi_2[:,third_quarter])
ax.plot(posi_1,psi_2[:,end])

ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$ψ$")

plt.savefig(fname=os.path.join(path_results,"psi_2__v__posi_1.svg"), format="svg")


# Plot permeability 
# -----
fig, ax = plt.subplots(1,1)

ax.plot(posi_1,perm_solver_2[:,start])
ax.plot(posi_1,perm_solver_2[:,start+50])
ax.plot(posi_1,perm_solver_2[:,second_quarter])
ax.plot(posi_1,perm_solver_2[:,third_quarter])
ax.plot(posi_1,perm_solver_2[:,end])

ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$k$")

plt.savefig(fname=os.path.join(path_results,"perm_solver_2__v__posi_1.svg"), format="svg")


# Plot deposition parameter 
# -----
fig, ax = plt.subplots(1,1)

ax.plot(posi_1, depo_solver_2[:,start])
ax.plot(posi_1, depo_solver_2[:,start+50])
ax.plot(posi_1, depo_solver_2[:,second_quarter])
ax.plot(posi_1, depo_solver_2[:,third_quarter])
ax.plot(posi_1, depo_solver_2[:,end])

ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$j$")

plt.savefig(fname=os.path.join(path_results,"depo_solver_2__v__posi_1.svg"), format="svg")


# Plot pressure gradient 
# -----
fig, ax = plt.subplots(1,1)

ax.plot(posi_1, dpdx_2[:,start])
ax.plot(posi_1, dpdx_2[:,start+50])
ax.plot(posi_1, dpdx_2[:,second_quarter])
ax.plot(posi_1, dpdx_2[:,third_quarter])
ax.plot(posi_1, dpdx_2[:,end])

ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$dp/dx$")

plt.savefig(fname=os.path.join(path_results,"dpdx_2__v__posi_1.svg"), format="svg")