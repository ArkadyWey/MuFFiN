from matplotlib import pyplot as plt
import os
import numpy
import scipy
from scipy import integrate

import sys
sys.path.append("/home/user/utils_python")
import plotting

import multiscale_models.performance as performance

# Parameters 
# -----
#path_results = os.path.join(".","results/results_flow") # thesis
#path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/results_flow") # paper
#path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/mono/flow_test") # paper
#path_results = os.path.join(".","results/results_comparison/epsi-0.025/results_flow")
path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/mono/sweep-beta/beta-0.01/flow") # paper

time_1 = numpy.load(os.path.join(path_results, "time_1.npy"))
posi_1 = numpy.load(os.path.join(path_results, "posi_1.npy"))
conc_2     = numpy.load(os.path.join(path_results, "conc_2.npy"))
conc_max_or_tot_2 = numpy.load(os.path.join(path_results, "conc_max_or_tot_2.npy"))
perm_2     = numpy.load(os.path.join(path_results, "perm_2.npy"))
depo_2     = numpy.load(os.path.join(path_results, "depo_2.npy"))
velo_1     = numpy.load(os.path.join(path_results, "velo_1.npy"))
dpdx_2     = numpy.load(os.path.join(path_results, "dpdx_2.npy"))
psi_2      = numpy.load(os.path.join(path_results, "psi_2.npy"))


cond = "mono" # change limits of plots depending on whether initial conductances are mono-dispersed or poly-dispersed 



# Plot concentration
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

alph=1.0
ax.plot(posi_1,numpy.exp(-alph*posi_1),c="tab:blue",ls="--")
ax.plot(posi_1,numpy.exp(-alph)*numpy.ones_like(posi_1), c="black", ls="--")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$c$",
                             x_left=0,
                             x_right=1,
                             y_bottom=0,
                             y_top=1.01)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"conc_2__v__posi_1.svg"), format="svg")

# Plot velocity 
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

T = 490
x_right = 500

ax.plot(time_1[0:T],velo_1[0:T]) # mono
ax.plot(time_1[0:T], 0.1*numpy.ones_like(time_1[0:T]), color="tab:orange", ls=":")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$t$",
                             y_label=r"$u$",
                             x_left=0,
                             x_right=x_right,
                             y_bottom=0,
                             y_top=1.01)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"velo_1__v__time_1.svg"), format="svg")



# Plot reaction parameter vs position
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

T = 500
y_top = 1.01

for t in time_1[0:T:50]:
    t = int(t)
    ax.plot(posi_1,psi_2[:,t],c="tab:blue")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$\psi$",
                             x_left=0,
                             x_right=1,
                             y_bottom=0,
                             y_top=y_top)


plotting.save_fig(fig=fig,fname=os.path.join(path_results,"psi_2__v__posi_1.svg"), format="svg")


# Plot reaction parameter vs time
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

T = 490
x_right = 500
y_top = 1

ax.plot(time_1[0:T],psi_2[1,0:T])

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$t$",
                             y_label=r"$\psi$",
                             x_left=0,
                             x_right=x_right,
                             y_bottom=0,
                             y_top=y_top)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"psi_2__v__time_1.svg"), format="svg")



# Plot permeability 
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

T = 500
y_top = 1.01

for t in time_1[0:T:50]:
    t = int(t)
    ax.plot(posi_1,perm_2[:,t],c="tab:blue")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$k$",
                             x_left=0,
                             x_right=1,
                             y_bottom=0,
                             y_top=y_top)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"perm_2__v__posi_1.svg"), format="svg")



# Plot deposition parameter vs position
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

T = 500
y_top = 1.01

for t in time_1[0:T:50]:
    t = int(t)
    ax.plot(posi_1,depo_2[:,t],c="tab:blue")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$j$",
                             x_left=0,
                             x_right=1,
                             y_bottom=0,
                             y_top=y_top)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"depo_2__v__posi_1.svg"), format="svg")


# Plot pressure gradient 
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

T = 500
y_bottom = -8 

for t in time_1[0:T:50]:
    t = int(t)
    ax.plot(posi_1,dpdx_2[:,t],c="tab:blue")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$\partial p/\partial x$",
                             x_left=0,
                             x_right=1,
                             y_bottom=y_bottom,
                             y_top=0)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"dpdx_2__v__posi_1.svg"), format="svg")


# Plot pressure 
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

tau = 450
T   = 500

pres_2 = numpy.ones_like(dpdx_2)
for i_t in numpy.linspace(0,tau,tau+1,endpoint=True,dtype=int):
    dpdx_1 = dpdx_2[:,i_t]
    for i_x in numpy.linspace(1,100,100,endpoint=True,dtype=int):
        pres = integrate.trapezoid(y=dpdx_1[0:i_x],x=posi_1[0:i_x],dx=posi_1[1]-posi_1[0])
        pres_2[i_x,i_t] = pres

for t in time_1[0:T:50]:
    t = int(t)
    ax.plot(posi_1,pres_2[:,t],c="tab:blue")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$p$",
                             x_left=0.01,
                             x_right=1,
                             y_bottom=-1,
                             y_top=0)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"pres_2__v__posi_1.svg"), format="svg")


# Plot permeability ad deposition on on graph
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(posi_1,perm_2[:,0], label=r"$k^{11}$", color="tab:red")
#ax.plot(posi_1,perm_2[:,first_quarter])
#ax.plot(posi_1,perm_2[:,second_quarter])
#ax.plot(posi_1,perm_2[:,third_quarter])
#ax.plot(posi_1,perm_2[:,end])

ax.plot(posi_1,depo_2[:,0], label=r"$j^{1}$", color="tab:blue")
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



# Plot mass flux vs position
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

for t in time_1[0:500:50]:
    t = int(t)
    ax.plot(posi_1,conc_max_or_tot_2[:,t],c="tab:blue")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$s$",
                             x_left=0,
                             x_right=1,
                             y_bottom=0,
                             y_top=1300)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"cmax_2__v__posi_1.svg"), format="svg")







# Get terminal time and lifetime
# -----------------
mu_1 = numpy.linspace(0.1,0.5,101)
term_1 = numpy.zeros_like(mu_1)
life_1 = numpy.zeros_like(mu_1)

for i_mu,mu in enumerate(mu_1):
    term_1[i_mu] = performance.get_termination(velo_1=velo_1,time_1=time_1,mu=mu)

    life = performance.get_lifetime(velo_1=velo_1,time_1=time_1,tau=int(term_1[i_mu]))
    life_1[i_mu] = life



# Plot terminal time v velocity threshold
# ---------------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(mu_1, term_1)

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$\mu$",
                             y_label=r"$\tau$",
                             x_left=0.1,
                             x_right=0.5,
                             y_bottom=100,
                             y_top=500)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"term_1__v__thre_1.svg"), format="svg")


# Plot life time v termination
# ---------------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(term_1, life_1)

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$\tau$",
                             y_label=r"$\lambda$",
                             x_left=100,
                             x_right=500,
                             y_bottom=80,
                             y_top=180)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"life_1__v__term_1.svg"), format="svg")


# Plot life time v velocity threshold
# ---------------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(mu_1, life_1)
m = -220
c = 198
ax.plot(mu_1,m*mu_1+c, color="tab:orange", ls=":")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$\mu$",
                             y_label=r"$\lambda$",
                             x_left=0.1,
                             x_right=0.5,
                             y_bottom=80,
                             y_top=180)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"life_1__v__thre_1.svg"), format="svg")




# Terminal time (for mu = 0.1)
T = int(term_1[0])


# Get efficiency and throughput
# --------------
thro_1 = numpy.zeros_like(time_1) # thro_1[t]
effi_1 = numpy.zeros_like(time_1) # effi_1[t]
for t in time_1: 
    t = int(t)
    
    thro_1[t] = performance.get_throughput(velo_1,time_1=time_1,t=t)

effi_1[:] = performance.get_efficiency(conc_2=conc_2)


# Plot efficiency v time
# ---------------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(time_1[0:T+1],effi_1[0:T+1])
ax.vlines(x=term_1[0], ymin=0, ymax=effi_1[-1], colors='tab:orange', linestyles=':')

plotting.thesisify_post_plot(ax=ax,
                            x_label=r"$t$",
                            y_label=r"$\eta$",
                            x_left=0,
                            x_right=500,
                             y_bottom=0.62,
                             y_top=0.64)


plotting.save_fig(fig=fig,fname=os.path.join(path_results,"effi_1__v__time_1.svg"), format="svg")


# Plot throughput v time
# ---------------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(time_1[0:T+1],thro_1[0:T+1])
ax.plot(time_1[0:T+1], thro_1[-1]*numpy.ones_like(time_1[0:T+1]),ls=":", c="tab:orange")
#ax.plot(time_1[0:T+1], life_1[0]*numpy.ones_like(time_1[0:T+1]),ls=":", c="tab:green")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$t$",
                             y_label=r"$\theta$",
                             x_left=0,
                             x_right=501,
                             y_bottom=0,
                             y_top=200)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"thro_1__v__time_1.svg"), format="svg")


# Plot throughput v efficiency
# ---------------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(thro_1[0:T+1], effi_1[0:T+1])
ax.vlines(x=thro_1[-1], ymin=0, ymax=effi_1[-1], colors='tab:orange', linestyles=':')

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$\theta$",
                             y_label=r"$\eta$",
                             x_left=0,
                             x_right=200,
                             y_bottom=0.62,
                             y_top=0.64)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"effi_1__v__thro_1.svg"), format="svg")



