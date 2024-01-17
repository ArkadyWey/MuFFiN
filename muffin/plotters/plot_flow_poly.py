from matplotlib import pyplot as plt
import os
import numpy
import scipy 
from scipy import integrate

import muffin.plotters.plotting as plotting

import muffin.variables.performance as performance

# Parameters 
# -----

variables = {}
stat_1 = ["mean", "abov", "belo"]
mono_1 = ["mono"]
stat_and_mono_1 = ["mean", "abov", "belo", "mono"]
vari_1 = ["time_1",
          "posi_1",
          "conc_2",
          "conc_max_or_tot_2",
          "perm_2",
          "depo_2",
          "velo_1",
          "dpdx_2",
          "psi_2"]

for stat in stat_and_mono_1:
    variables[stat] = {}
    if stat in stat_1:
        path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/poly/flow/N-4/{}".format(stat)) # paper
    elif stat in mono_1:
        path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/mono/sweep-beta/beta-0.01/flow") # paper
    else: 
        raise Exception()
    for vari in vari_1:
        # Load variables 
        # -----
        vari_X = numpy.load(os.path.join(path_results, vari+".npy"))
        variables[stat][vari] = vari_X


path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/poly/flow/N-4/") # paper

colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]

# Plot concentration
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

T = 400
x_right = 400

alph=1.0
for stat in ["mean"]:
    time_1 = variables[stat]["time_1"]
    posi_1 = variables[stat]["posi_1"]
    conc_2 = variables[stat]["conc_2"]
    for t in [2,50,100,150,200,250,300,350,400]:
        t = int(t)
        if t == 2:
            color="tab:orange"
        elif t == 200: 
            color = "tab:green"
        elif t==400:
            color = "tab:red"
        else: 
            color = "tab:blue"
        ax.plot(posi_1,conc_2[:,t],c=color,ls="-")
        if t in [2,200,400]:
            ax.fill_between(variables["mean"]["posi_1"], variables["belo"]["conc_2"][:,t], variables["abov"]["conc_2"][:,t], alpha=0.5, facecolor=color)

ax.plot(posi_1,numpy.exp(-alph*posi_1),c="tab:blue",ls="--")


plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$c$",
                             x_left=0,
                             x_right=1,
                             y_bottom=0,
                             y_top=1.01)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"conc_2__v__posi_1.svg"), format="svg")


# Plot concentration with spread
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]
for stat in ["mean"]:
    time_1 = variables[stat]["time_1"]
    posi_1 = variables[stat]["posi_1"]
    conc_2 = variables[stat]["conc_2"]
    for i_t,t in enumerate([2,200,400]):
        t = int(t)
        ax.plot(posi_1,conc_2[:,t],c=colors[i_t],ls="-")
        ax.fill_between(variables["mean"]["posi_1"], variables["belo"]["conc_2"][:,t], variables["abov"]["conc_2"][:,t], alpha=0.5, facecolor=colors[i_t])

ax.plot(posi_1,numpy.exp(-alph*posi_1),c="tab:blue",ls="--")


plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$c$",
                             x_left=0,
                             x_right=1,
                             y_bottom=0,
                             y_top=1.01)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"conc_2__v__posi_1_sd.svg"), format="svg")


# Plot outlet concentration mean, abov and below
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]
time_1 = variables["mean"]["time_1"]

ax.plot(time_1[0:T],variables["belo"]["conc_2"][-1,0:T]-variables["mean"]["conc_2"][-1,0:T],c="tab:blue",ls="-",label=r"$d_{+}$")
ax.plot(time_1[0:T],variables["mean"]["conc_2"][-1,0:T]-variables["abov"]["conc_2"][-1,0:T],c="tab:orange",ls="-",label=r"$d_{-}$")
ax.legend()
plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$t$",
                             y_label=None,
                             x_left=0,
                             x_right=400,
                             y_bottom=0,
                             y_top=0.06)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"devi_2__v__time_1.svg"), format="svg")



# Plot velocity 
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

T = 396
x_right = 500

for stat in ["mean"]:
    time_1 = variables[stat]["time_1"]
    velo_1 = variables[stat]["velo_1"]
    ax.plot(time_1[0:T],velo_1[0:T], c="tab:blue") # mono
ax.plot(variables["mono"]["time_1"][0:486], variables["mono"]["velo_1"][0:486],color="tab:blue",ls="--")
#ax.plot(time_1[0:T], 0.1*numpy.ones_like(time_1[0:T]), color="tab:red", ls=":")

ax.plot(variables["mono"]["time_1"][0:486], 0.1*numpy.ones_like(variables["mono"]["time_1"][0:486]), color="tab:orange", ls=":")

ax.fill_between(variables["mean"]["time_1"][0:T], variables["belo"]["velo_1"][0:T], variables["abov"]["velo_1"][0:T], alpha=0.5, facecolor="tab:blue")
#ax.fill_between(variables["mean"]["time_1"][0:T], variables["belo"]["velo_1"][T]*numpy.ones_like(time_1[0:T]), variables["abov"]["velo_1"][394]*numpy.ones_like(time_1[0:T]), alpha=0.5, facecolor="tab:orange")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$t$",
                             y_label=r"$u$",
                             x_left=0,
                             x_right=x_right,
                             y_bottom=0,
                             y_top=1.1)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"velo_1__v__time_1.svg"), format="svg")



# Plot reaction parameter vs position
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

T = 396
y_top = 1.2

for t in time_1[0:T:50]:
    t = int(t)
    print(t)
    if t == 0: 
        color = "tab:orange"
    elif t == 200:
        color = "tab:green"
    elif t == 350:
        color = "tab:red"
    else: 
        color = "tab:blue"
    ax.plot(variables["mean"]["posi_1"][:], variables["mean"]["psi_2"][:,t], c=color, ls="-")
    #ax.plot(variables["mono"]["posi_1"][:], variables["mono"]["psi_2"][:,t], c=color, ls="--")
    if t in [0,200,350]:
        ax.fill_between(variables["mean"]["posi_1"][:], variables["belo"]["psi_2"][:,t], variables["abov"]["psi_2"][:,t], alpha=0.5, facecolor=color)


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

T = 396
x_right = 400

ax.plot(variables["mean"]["time_1"][0:T],variables["mean"]["psi_2"][0,0:T] ,color="tab:orange"  , ls="-") # mono
ax.plot(variables["mean"]["time_1"][0:T],variables["mean"]["psi_2"][-1,0:T],color="tab:green", ls="-") # mono
ax.plot(variables["mono"]["time_1"][0:T],variables["mono"]["psi_2"][-1,0:T],color="tab:blue", ls="--") # mono

ax.fill_between(variables["mean"]["time_1"][0:T], variables["belo"]["psi_2"][0,0:T], variables["abov"]["psi_2"][0,0:T], alpha=0.5, facecolor="tab:orange")
ax.fill_between(variables["mean"]["time_1"][0:T], variables["belo"]["psi_2"][-1,0:T], variables["abov"]["psi_2"][-1,0:T], alpha=0.5, facecolor="tab:green")

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

T = 396
y_top = 1.2

for t in time_1[0:T:50]:
    t = int(t)
    print(t)
    if t == 0: 
        color = "tab:orange"
    elif t == 200:
        color = "tab:green"
    elif t == 350:
        color = "tab:red"
    else: 
        color = "tab:blue"
    ax.plot(variables["mean"]["posi_1"][:], variables["mean"]["perm_2"][:,t], c=color, ls="-")
    #ax.plot(variables["mono"]["posi_1"][:], variables["mono"]["perm_2"][:,t], c=color, ls="--")
    if t in [0,200,350]:
        ax.fill_between(variables["mean"]["posi_1"][:], variables["belo"]["perm_2"][:,t], variables["abov"]["perm_2"][:,t], alpha=0.5, facecolor=color)

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

T = 396
y_top = 1.2

for t in time_1[0:T:50]:
    t = int(t)
    print(t)
    if t == 0: 
        color = "tab:orange"
    elif t == 200:
        color = "tab:green"
    elif t == 350:
        color = "tab:red"
    else: 
        color = "tab:blue"
    ax.plot(variables["mean"]["posi_1"][:], variables["mean"]["depo_2"][:,t], c=color, ls="-")
    #ax.plot(variables["mono"]["posi_1"][:], variables["mono"]["depo_2"][:,t], c=color, ls="--")
    if t in [0,200,350]:
        ax.fill_between(variables["mean"]["posi_1"][:], variables["belo"]["depo_2"][:,t], variables["abov"]["depo_2"][:,t], alpha=0.5, facecolor=color)

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

T = 396
y_top = 1.2

for t in time_1[0:T:50]:
    t = int(t)
    print(t)
    if t == 0: 
        color = "tab:orange"
    elif t == 200:
        color = "tab:green"
    elif t == 350:
        color = "tab:red"
    else: 
        color = "tab:blue"
    ax.plot(variables["mean"]["posi_1"][:], variables["mean"]["dpdx_2"][:,t], c=color, ls="-")
    #ax.plot(variables["mono"]["posi_1"][:], variables["mono"]["dpdx_2"][:,t], c=color, ls="--")
    if t in [0,200,350]:
        ax.fill_between(variables["mean"]["posi_1"][:], variables["belo"]["dpdx_2"][:,t], variables["abov"]["dpdx_2"][:,t], alpha=0.5, facecolor=color)

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$\partial p/\partial x$",
                             x_left=0,
                             x_right=1,
                             y_bottom=-8,
                             y_top=0)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"dpdx_2__v__posi_1.svg"), format="svg")



# Get pressure 
# -----
tau = 396
for stat in stat_and_mono_1:
    variables[stat]["pres_2"] = performance.get_pressure(dpdx_2=variables[stat]["dpdx_2"],posi_1=variables[stat]["posi_1"],tau=tau)


# Plot pressure 
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

T = 396
y_top = 1.2

for t in time_1[0:T:50]:
    t = int(t)
    print(t)
    if t == 0: 
        color = "tab:orange"
    elif t == 200:
        color = "tab:green"
    elif t == 350:
        color = "tab:red"
    else: 
        color = "tab:blue"
    ax.plot(variables["mean"]["posi_1"][:], variables["mean"]["pres_2"][:,t], c=color, ls="-")
    #ax.plot(variables["mono"]["posi_1"][:], variables["mono"]["pres_2"][:,t], c=color, ls="--")
    if t in [0,200,350]:
        ax.fill_between(variables["mean"]["posi_1"][:], variables["belo"]["pres_2"][:,t], variables["abov"]["pres_2"][:,t], alpha=0.5, facecolor=color)

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$p$",
                             x_left=0.01,
                             x_right=1,
                             y_bottom=-1,
                             y_top=0)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"pres_2__v__posi_1.svg"), format="svg")



# Plot conc_max_or_tot vs position
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

T = 396
y_top = 1.2

for t in time_1[0:T:50]:
    t = int(t)
    print(t)
    if t == 0: 
        color = "tab:orange"
    elif t == 200:
        color = "tab:green"
    elif t == 350:
        color = "tab:red"
    else: 
        color = "tab:blue"
    ax.plot(variables["mean"]["posi_1"][:], variables["mean"]["conc_max_or_tot_2"][:,t], c=color, ls="-")
    #ax.plot(variables["mono"]["posi_1"][:], variables["mono"]["conc_max_or_tot_2"][:,t], c=color, ls="--")
    if t in [0,200,350]:
        ax.fill_between(variables["mean"]["posi_1"][:], variables["belo"]["conc_max_or_tot_2"][:,t], variables["abov"]["conc_max_or_tot_2"][:,t], alpha=0.5, facecolor=color)

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
mu_1   = numpy.linspace(0.1,0.5,101)

for stat in stat_and_mono_1:
    variables[stat]["term_1"] = numpy.zeros_like(mu_1)
    variables[stat]["life_1"] = numpy.zeros_like(mu_1)

    for i_mu,mu in enumerate(mu_1):
        variables[stat]["term_1"][i_mu] = performance.get_termination(velo_1=variables[stat]["velo_1"],time_1=variables[stat]["time_1"],mu=mu)
        
        life = performance.get_lifetime(velo_1=variables[stat]["velo_1"],time_1=variables[stat]["time_1"],tau=int(variables[stat]["term_1"][i_mu]))
        variables[stat]["life_1"][i_mu] = life




# Plot terminal time v velocity threshold
# ---------------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1) 

ax.plot(mu_1, variables["mean"]["term_1"], ls="-" , color="tab:blue")
ax.plot(mu_1, variables["mono"]["term_1"], ls="--", color="tab:blue")

ax.fill_between(mu_1, variables["belo"]["term_1"], variables["abov"]["term_1"], alpha=0.5, facecolor="tab:blue")


plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$\mu$",
                             y_label=r"$\tau$",
                             x_left=0.1,
                             x_right=0.5,
                             y_bottom=50,
                             y_top=500)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"term_1__v__thre_1.svg"), format="svg")



# Plot life time v termination
# ---------------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(variables["mean"]["term_1"], variables["mean"]["life_1"], ls="-" , color="tab:blue")
ax.plot(variables["mono"]["term_1"], variables["mono"]["life_1"], ls="--", color="tab:blue")

ax.fill_between(variables["mean"]["term_1"], variables["belo"]["life_1"], variables["abov"]["life_1"], alpha=0.5, facecolor="tab:blue")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$\tau$",
                             y_label=r"$\lambda$",
                             x_left=75,
                             x_right=500,
                             y_bottom=25,
                             y_top=180)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"life_1__v__term_1.svg"), format="svg")




# Plot life time v velocity threshold
# ---------------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(mu_1, variables["mean"]["life_1"], ls="-" , color="tab:blue")
ax.plot(mu_1, variables["mono"]["life_1"], ls="--", color="tab:blue")

ax.fill_between(mu_1, variables["belo"]["life_1"], variables["abov"]["life_1"], alpha=0.5, facecolor="tab:blue")


m = -220
c = 198
ax.plot(mu_1,m*mu_1+c, color="tab:orange", ls=":")

m = -185
c = 145
ax.plot(mu_1,m*mu_1+c, color="tab:red", ls=":")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$\mu$",
                             y_label=r"$\lambda$",
                             x_left=0.1,
                             x_right=0.5,
                             y_bottom=25,
                             y_top=180)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"life_1__v__thre_1.svg"), format="svg")



# Terminal time (for mu = 0.1)
T = int(variables["mean"]["term_1"][0])


# Get efficiency and throughput
# --------------
for stat in stat_and_mono_1:
    variables[stat]["thro_1"] = numpy.zeros_like(variables[stat]["time_1"]) # thro_1[t]
    variables[stat]["effi_1"] = numpy.zeros_like(variables[stat]["time_1"]) # effi_1[t]
    for t in variables[stat]["time_1"]: 
        t = int(t)

        variables[stat]["thro_1"][t] = performance.get_throughput(velo_1=variables[stat]["velo_1"],time_1=variables[stat]["time_1"],t=t)

    variables[stat]["effi_1"][:] = performance.get_efficiency(conc_2=variables[stat]["conc_2"])



# Plot efficiency v time
# ---------------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(variables["mean"]["time_1"][2:T+1], variables["mean"]["effi_1"][2:T+1], ls="-" , color="tab:blue")
ax.plot(variables["mono"]["time_1"][2:486], variables["mono"]["effi_1"][2:486], ls="--", color="tab:blue")

ax.fill_between(variables["mean"]["time_1"][2:T+1], variables["belo"]["effi_1"][2:T+1], variables["abov"]["effi_1"][2:T+1], alpha=0.5, facecolor="tab:blue")

ax.vlines(x=variables["mono"]["term_1"][0], ymin=0, ymax=variables["mono"]["effi_1"][T+1], colors='tab:orange', linestyles=':')
ax.vlines(x=variables["mean"]["term_1"][0], ymin=0, ymax=variables["abov"]["effi_1"][T+1], colors='tab:red', linestyles=':')

plotting.thesisify_post_plot(ax=ax,
                            x_label=r"$t$",
                            y_label=r"$\eta$",
                            x_left=0,
                            x_right=500,
                             y_bottom=0.6,
                             y_top=0.85)


plotting.save_fig(fig=fig,fname=os.path.join(path_results,"effi_1__v__time_1.svg"), format="svg")




# Plot throughput v time
# ---------------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(variables["mean"]["time_1"][0:T+1], variables["mean"]["thro_1"][0:T+1], ls="-" , color="tab:blue")
ax.plot(variables["mono"]["time_1"][0:486], variables["mono"]["thro_1"][0:486], ls="--", color="tab:blue")

ax.fill_between(variables["mean"]["time_1"][0:T+1], variables["belo"]["thro_1"][0:T+1], variables["abov"]["thro_1"][0:T+1], alpha=0.5, facecolor="tab:blue")

ax.plot(variables["mono"]["time_1"][0:486], variables["mono"]["thro_1"][485]*numpy.ones_like(variables["mono"]["time_1"][0:486]),ls=":", c="tab:orange")
ax.plot(variables["mono"]["time_1"][0:T+1], variables["mean"]["thro_1"][T+1]*numpy.ones_like(variables["mono"]["time_1"][0:T+1]),ls=":", c="tab:red")

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


ax.plot(variables["mean"]["thro_1"][2:T+1], variables["mean"]["effi_1"][2:T+1], ls="-" , color="tab:blue")
ax.plot(variables["mono"]["thro_1"][2:486], variables["mono"]["effi_1"][2:486], ls="--", color="tab:blue")

ax.fill_between(variables["mean"]["thro_1"][2:T+1], variables["belo"]["effi_1"][2:T+1], variables["abov"]["effi_1"][2:T+1], alpha=0.5, facecolor="tab:blue")

ax.vlines(x=variables["mono"]["thro_1"][485], ymin=0, ymax=variables["mono"]["effi_1"][485], colors='tab:orange', linestyles=':')
ax.vlines(x=variables["mean"]["thro_1"][T+1], ymin=0, ymax=variables["abov"]["effi_1"][T+1], colors='tab:red',    linestyles=':')


#ax.plot(thro_1[0:T+1], effi_1[0:T+1])
#ax.vlines(x=thro_1[-1], ymin=0, ymax=effi_1[-1], colors='tab:orange', linestyles=':')

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$\theta$",
                             y_label=r"$\eta$",
                             x_left=0,
                             x_right=200,
                             y_bottom=0.60,
                             y_top=0.85)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"effi_1__v__thro_1.svg"), format="svg")





# Get efficiency and throughput
# --------------
T=396
thro_3 = numpy.zeros(shape=(3,T)) # thro_3["mean"/"abov","belo",t]
effi_3 = numpy.zeros(shape=(3,T)) # effi_3["mean"/"abov","belo",t]
for t in variables["mean"]["time_1"][0:T]: 
    t = int(t)
    
    thro_3[0,t] = performance.get_throughput(velo_1=variables["mean"]["velo_1"],time_1=variables["mean"]["time_1"],t=t)
    thro_3[1,t] = performance.get_throughput(velo_1=variables["belo"]["velo_1"],time_1=variables["mean"]["time_1"],t=t)
    thro_3[2,t] = performance.get_throughput(velo_1=variables["abov"]["velo_1"],time_1=variables["mean"]["time_1"],t=t)

effi_3[0,:] = performance.get_efficiency(conc_2=["mean"]["conc_2"])
effi_3[1,:] = performance.get_efficiency(conc_2=["belo"]["conc_2"])
effi_3[2,:] = performance.get_efficiency(conc_2=["abov"]["conc_2"])

# Plot efficiency v time
# ---------------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(variables["mean"]["time_1"][0:T],effi_3[0,:])
ax.fill_between(variables["mean"]["time_1"][0:T],effi_3[1,:],effi_3[2,:], alpha=0.5, facecolor="tab:blue")

plotting.thesisify_post_plot(ax=ax,
                            x_label=r"$t$",
                            y_label=r"$\eta$",
                            x_left=0,
                            x_right=T,
                            y_bottom=0.65,
                            y_top=0.85)


#plotting.save_fig(fig=fig,fname=os.path.join(path_results,"effi_1__v__time_1.svg"), format="svg")


# Plot throughput v time
# ---------------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(variables["mean"]["time_1"][0:T],thro_3[0,0:T])
ax.fill_between(variables["mean"]["time_1"][0:T],thro_3[1,:],thro_3[2,:], alpha=0.5, facecolor="tab:blue")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$t$",
                             y_label=r"$\theta$",
                             x_left=0,
                             x_right=400,
                             y_bottom=0,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"thro_1__v__time_1.svg"), format="svg")


# Plot throughput v efficiency
# ---------------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(thro_3[0,0:T], effi_3[0,0:T])
ax.fill_between(thro_3[0,0:T], effi_3[1,:], effi_3[2,:], alpha=0.5, facecolor="tab:blue")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$\theta$",
                             y_label=r"$\eta$",
                             x_left=0,
                             x_right=125,
                             y_bottom=0.65,
                             y_top=0.85)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"effi_1__v__thro_1.svg"), format="svg")



# Get terminal time
# -----------------
mu_1 = numpy.linspace(0.1,0.5,21)#51)
term_1 = numpy.zeros_like(mu_1)
life_1 = numpy.zeros_like(mu_1)
velo_1 = variables["mean"]["velo_1"]
time_1 = variables["mean"]["time_1"]

for i_mu,mu in enumerate(mu_1):
    indx_crit_1 = [i for i in range(len(velo_1)) if velo_1[i]<mu]
    indx_crit = indx_crit_1[0]
    
    term_1[i_mu] = time_1[indx_crit]

    life = performance.get_lifetime(velo_1,time_1,indx_crit)
    life_1[i_mu] = life

print(mu_1)
print(term_1)
print(life_1)

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
                             y_bottom=50,
                             y_top=400)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"term_1__v__thre_1.svg"), format="svg")


# Plot life time v velocity threshold
# ---------------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(mu_1, life_1)
c=145
m=-186
ax.plot(mu_1, m*mu_1+c, ls="--")

# plotting.thesisify_post_plot(ax=ax,
#                              x_label=r"$\mu$",
#                              y_label=r"$\lambda$",
#                              x_left=0.1,
#                              x_right=0.5,
#                              y_bottom=50,
#                              y_top=125)
plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$\mu$",
                             y_label=r"$\lambda$",
                             x_left=0.1,
                             x_right=0.5,
                             y_bottom=50,
                             y_top=130)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"life_1__v__thre_1.svg"), format="svg")





