from matplotlib import pyplot as plt
import os 
import numpy 

# Parameters 
# -----
path_results = os.path.join(".","results/results_preprocess_1D")


# Load variables
# -----
conc_max_disc_1 = numpy.load(os.path.join(path_results, "conc_max_disc_1.npy"))
perm_prep_1 = numpy.load(os.path.join(path_results, "perm_prep_1.npy"))
depo_prep_1 = numpy.load(os.path.join(path_results, "depo_prep_1.npy"))


# Plot permeability and deposition parameter values on one axis 
# -----
fig, ax = plt.subplots(1,1)

ax.plot(conc_max_disc_1, perm_prep_1, label=r"$k^{11}$", color="tab:red")
ax.plot(conc_max_disc_1,-depo_prep_1, label=r"$j^{1}$", color="tab:blue")
ax.set_xlabel(r"$C_{\mathrm{max}}$")
ax.legend()
plt.savefig(fname=os.path.join(path_results,"perm_prep_1__depo_prep_1__v__conc_max_disc_1.svg"), format="svg")


