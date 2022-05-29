from matplotlib import pyplot as plt
import os 
import numpy 

# Parameters 
# -----
path_results = os.path.join(".","results_preprocess_2D")


# Load variables
# -----
conc_max_disc_1 = numpy.load(os.path.join(path_results, "conc_max_disc_1.npy"))
perm_prep_3 = numpy.load(os.path.join(path_results, "perm_prep_3.npy"))
depo_prep_2 = numpy.load(os.path.join(path_results, "depo_prep_2.npy"))


# Plot permeability and deposition parameter values on one axis 
# -----
fig, ax = plt.subplots(1,1)

# Choose dimensions to plot
m = 0
n = 0


ax.plot(conc_max_disc_1, perm_prep_3[:,m,n], label=r"$k$", color="red")
ax.plot(conc_max_disc_1, depo_prep_2[:,m], label=r"$j$", color="blue")
ax.set_xlabel("c")
ax.legend()
plt.savefig(fname=os.path.join(path_results,"perm_prep_3__depo_prep_2__v__conc_max_disc_1.svg"), format="svg")