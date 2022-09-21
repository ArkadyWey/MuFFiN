from matplotlib import pyplot as plt
import os
import numpy

import sys
sys.path.append("/home/user/utils_python")
import plotting

# Parameters 
# -----
path_results = os.path.join(".","results/results_flow")


# Load variables 
# -----
time_1 = numpy.load(os.path.join(path_results, "time_1.npy"))
posi_1 = numpy.load(os.path.join(path_results, "posi_1.npy"))

conc_2     = numpy.load(os.path.join(path_results, "conc_2.npy"))
conc_max_2 = numpy.load(os.path.join(path_results, "conc_max_2.npy"))
perm_2     = numpy.load(os.path.join(path_results, "perm_2.npy"))
depo_2     = numpy.load(os.path.join(path_results, "depo_2.npy"))
velo_1     = numpy.load(os.path.join(path_results, "velo_1.npy"))
dpdx_2     = numpy.load(os.path.join(path_results, "dpdx_2.npy"))
psi_2      = numpy.load(os.path.join(path_results, "psi_2.npy"))


num_times = len(time_1)

start          = 0
first_quarter  = int(1*(num_times-1)/4)
second_quarter = int(2*(num_times-1)/4)
third_quarter  = int(3*(num_times-1)/4)
end            = -1


# Plot concentration
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(posi_1,conc_2[:,start], label=r"$t=0$")
ax.plot(posi_1,conc_2[:,first_quarter], label=r"$t=0.25$")
ax.plot(posi_1,conc_2[:,second_quarter], label=r"$t=0.50$")
ax.plot(posi_1,conc_2[:,third_quarter], label=r"$t=0.75$")
ax.plot(posi_1,conc_2[:,end], label=r"$t=1.0$")

ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$c$")

#ax.legend()
plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$c$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"conc_2__v__posi_1.svg"), format="svg")


# Plot velocity 
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(time_1,velo_1)

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$t$",
                             y_label=r"$u$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"velo_1__v__time_1.svg"), format="svg")



# Plot reaction parameter 
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(posi_1,psi_2[:,start])
ax.plot(posi_1,psi_2[:,first_quarter])
ax.plot(posi_1,psi_2[:,second_quarter])
ax.plot(posi_1,psi_2[:,third_quarter])
ax.plot(posi_1,psi_2[:,end])

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$\psi$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"psi_2__v__posi_1.svg"), format="svg")



# Plot permeability 
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(posi_1,perm_2[:,start])
ax.plot(posi_1,perm_2[:,first_quarter])
ax.plot(posi_1,perm_2[:,second_quarter]) #301 is index where prob starts
ax.plot(posi_1,perm_2[:,third_quarter])
ax.plot(posi_1,perm_2[:,end])

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$k$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"perm_2__v__posi_1.svg"), format="svg")



# Plot deposition parameter 
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(posi_1, depo_2[:,start])
ax.plot(posi_1, depo_2[:,first_quarter])
ax.plot(posi_1, depo_2[:,second_quarter])
ax.plot(posi_1, depo_2[:,third_quarter])
ax.plot(posi_1, depo_2[:,end])

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$j$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"depo_2__v__posi_1.svg"), format="svg")



# Plot pressure gradient 
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(posi_1, dpdx_2[:,start])
ax.plot(posi_1, dpdx_2[:,first_quarter])
ax.plot(posi_1, dpdx_2[:,second_quarter])
ax.plot(posi_1, dpdx_2[:,third_quarter])
ax.plot(posi_1, dpdx_2[:,end])

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$dp/dx$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"dpdx_2__v__posi_1.svg"), format="svg")


# Plot permeability ad deposition on on graph
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(posi_1,perm_2[:,start], label=r"$k^{00}$", color="tab:red")
#ax.plot(posi_1,perm_2[:,first_quarter])
#ax.plot(posi_1,perm_2[:,second_quarter])
#ax.plot(posi_1,perm_2[:,third_quarter])
#ax.plot(posi_1,perm_2[:,end])

ax.plot(posi_1,depo_2[:,start], label=r"$j^{0}$", color="tab:blue")
#ax.plot(posi_1, depo_2[:,first_quarter])
#ax.plot(posi_1, depo_2[:,second_quarter])
#ax.plot(posi_1, depo_2[:,third_quarter])
#ax.plot(posi_1, depo_2[:,end])

ax.set_xlabel(r"$x$")
#ax.set_ylabel(r"$k$")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"initial parameters",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"perm_2_and_depo_1__v__posi_1.svg"), format="svg")


