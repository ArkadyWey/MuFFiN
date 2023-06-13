from matplotlib import pyplot as plt
import os
import numpy

import sys
sys.path.append("/home/user/utils_python")
import plotting

# Parameters 
# -----
#path_results = os.path.join(".","results/results_flow") # thesis
#path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/results_flow") # paper
path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/mono/flow_test") # paper
#path_results = os.path.join(".","results/results_comparison/epsi-0.025/results_flow")


# Load variables 
# -----
time_1 = numpy.load(os.path.join(path_results, "time_1.npy"))
posi_1 = numpy.load(os.path.join(path_results, "posi_1.npy"))

conc_2     = numpy.load(os.path.join(path_results, "conc_2.npy"))
conc_max_or_tot_2 = numpy.load(os.path.join(path_results, "conc_max_or_tot_2.npy"))
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

num_posis = len(posi_1)

top           = 0
upper_quarter = int(1*(num_posis-1)/4)
middle        = int(2*(num_posis-1)/4)
lower_quarter = int(3*(num_posis-1)/4)
bottom        = -1

# Plot concentration
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

alph=1.0
ax.plot(posi_1,conc_2[:,start],         )#label=r"$t=0$")
ax.plot(posi_1,conc_2[:,first_quarter], )#label=r"$t=1/4$")
ax.plot(posi_1,conc_2[:,second_quarter],)#label=r"$t=1/2$")
ax.plot(posi_1,conc_2[:,third_quarter], )#label=r"$t=3/4$")
ax.plot(posi_1,conc_2[:,end],           )#label=r"$t=1$")


ax.plot(posi_1,numpy.exp(-alph*posi_1),c="black",ls="--")
ax.plot(posi_1,numpy.exp(-alph)*numpy.ones_like(posi_1), c="black", ls=":")

#ax.legend()
plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$c$",
                             x_left=0,
                             x_right=None,
                             y_bottom=0,
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
                             x_left=0,
                             x_right=None,
                             y_bottom=0,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"velo_1__v__time_1.svg"), format="svg")



# Plot reaction parameter vs position
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(posi_1,psi_2[:,start])
ax.plot(posi_1,psi_2[:,first_quarter])
ax.plot(posi_1,psi_2[:,second_quarter])
ax.plot(posi_1,psi_2[:,third_quarter])
ax.plot(posi_1,psi_2[:,end])

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x^1$",
                             y_label=r"$\psi$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"psi_2__v__posi_1.svg"), format="svg")


# Plot reaction parameter vs time
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(time_1,psi_2[top,:],label=r"$x=0$")
ax.plot(time_1,psi_2[upper_quarter,:],label=r"$x=1/4$")
ax.plot(time_1,psi_2[middle,:],label=r"$x=1/2$")
ax.plot(time_1,psi_2[lower_quarter,:],label=r"$x=3/4$")
ax.plot(time_1,psi_2[bottom,:],label=r"$x=1$")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$t$",
                             y_label=r"$\psi$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"psi_2__v__time_1.svg"), format="svg")



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
                             x_left=0,
                             x_right=None,
                             y_bottom=0,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"perm_2__v__posi_1.svg"), format="svg")



# Plot deposition parameter vs position
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

print(first_quarter)
print(numpy.nonzero(depo_2[:,:]))
ax.plot(posi_1, depo_2[:,start])
ax.plot(posi_1, depo_2[:,first_quarter])
ax.plot(posi_1, depo_2[:,second_quarter])
ax.plot(posi_1, depo_2[:,third_quarter])
ax.plot(posi_1, depo_2[:,end])
#for i_t in numpy.arange(start=0,stop=num_times,step=30,dtype=int):
#    ax.plot(posi_1, depo_2[:,i_t])

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$j$",
                             x_left=0,
                             x_right=None,
                             y_bottom=0,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"depo_2__v__posi_1.svg"), format="svg")



# Plot deposition parameter vs time
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(time_1,depo_2[top,:],label=r"$x=0$")
ax.plot(time_1,depo_2[upper_quarter,:],label=r"$x=1/4$")
ax.plot(time_1,depo_2[middle,:],label=r"$x=1/2$")
ax.plot(time_1,depo_2[lower_quarter,:],label=r"$x=3/4$")
ax.plot(time_1,depo_2[bottom,:],label=r"$x=1$")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$t$",
                             y_label=r"$j^1$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"depo_2__v__time_1.svg"), format="svg")



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
                             x_label=r"$x^1$",
                             y_label=r"$\partial p/\partial x^1$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"dpdx_2__v__posi_1.svg"), format="svg")


# Plot permeability ad deposition on on graph
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(posi_1,perm_2[:,start], label=r"$k^{11}$", color="tab:red")
#ax.plot(posi_1,perm_2[:,first_quarter])
#ax.plot(posi_1,perm_2[:,second_quarter])
#ax.plot(posi_1,perm_2[:,third_quarter])
#ax.plot(posi_1,perm_2[:,end])

ax.plot(posi_1,depo_2[:,start], label=r"$j^{1}$", color="tab:blue")
#ax.plot(posi_1, depo_2[:,first_quarter])
#ax.plot(posi_1, depo_2[:,second_quarter])
#ax.plot(posi_1, depo_2[:,third_quarter])
#ax.plot(posi_1, depo_2[:,end])

ax.set_xlabel(r"$x^1$")
#ax.set_ylabel(r"$k$")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x^1$",
                             y_label=r"initial parameters",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"perm_2_and_depo_1__v__posi_1.svg"), format="svg")



# Plot conc_max_or_tot vs position
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(posi_1,conc_max_or_tot_2[:,start])
ax.plot(posi_1,conc_max_or_tot_2[:,first_quarter])
ax.plot(posi_1,conc_max_or_tot_2[:,second_quarter])
ax.plot(posi_1,conc_max_or_tot_2[:,third_quarter])
ax.plot(posi_1,conc_max_or_tot_2[:,end])

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$s$",
                             x_left=0,
                             x_right=1,
                             y_bottom=0,
                             y_top=300)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"cmax_2__v__posi_1.svg"), format="svg")

