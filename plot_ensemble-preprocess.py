from matplotlib import pyplot as plt
import os 
import numpy 
import copy 

import utils_preprocess_2D
import configure
import flow 


import sys
sys.path.append("/home/user/utils_python")
import plotting

# Parameters 
# -----
type_clog      = "deposit"
initialisation = "4-reg"
num_nodes      = 4

# path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/poly/prep/init-{}/N-{}/stats_init-{}_N-{}".format(initialisation,num_nodes,initialisation,num_nodes)) # paper
path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/poly/esbl_prep/init-{}/N-{}/stats_init-{}_N-{}".format(initialisation,num_nodes,initialisation,num_nodes)) # paper


# Load variables
# -----
conc_max_or_tot_1 = numpy.load(os.path.join(path_results, "conc_max_or_tot_1.npy"))

# Average
perm_prep_av_3 = numpy.load(os.path.join(path_results, "perm_prep_av_3.npy"))
depo_prep_av_2 = numpy.load(os.path.join(path_results, "depo_prep_av_2.npy"))
delt_av_5      = numpy.load(os.path.join(path_results, "delt_av_5.npy"))
cond_tabl_av_5 = numpy.load(os.path.join(path_results, "cond_tabl_av_5.npy"))

# Standard deviation
perm_prep_sd_3 = numpy.load(os.path.join(path_results, "perm_prep_sd_3.npy"))
depo_prep_sd_2 = numpy.load(os.path.join(path_results, "depo_prep_sd_2.npy"))
delt_sd_5      = numpy.load(os.path.join(path_results, "delt_sd_5.npy"))
cond_tabl_sd_5 = numpy.load(os.path.join(path_results, "cond_tabl_sd_5.npy"))


# Could add these later
#cond_tabl_5       = numpy.load(os.path.join(path_results, "cond_tabl_5.npy"))
#adhe_tabl_5       = numpy.load(os.path.join(path_results, "adhe_tabl_5.npy"))
#heav_5            = numpy.load(os.path.join(path_results, "heav_5.npy"))


# Plot permeability and deposition parameter values on one axis 
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

# Choose dimensions to plot
m = 0
n = 0


#ax.scatter(conc_max_or_tot_1, perm_prep_3[:,m,n], color="tab:blue",   marker="o"  ) # label=r"$k^{11}$"
#ax.scatter(conc_max_or_tot_1, depo_prep_2[:,m]  , color="tab:orange", marker="o") # label=r"$j^{1}$" 

f = numpy.linspace(0.0,conc_max_or_tot_1[-1],1000)

# Interpolate against f
perm_prep_av_itrp_1 = flow.get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=perm_prep_av_3[:,m,n],new_x_value=f,type_clog=type_clog)
depo_prep_av_itrp_1 = flow.get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=depo_prep_av_2[:,m],new_x_value=f,type_clog=type_clog)

perm_prep_sd_itrp_1 = flow.get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=perm_prep_sd_3[:,m,n],new_x_value=f,type_clog=type_clog)
depo_prep_sd_itrp_1 = flow.get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=depo_prep_sd_2[:,m],new_x_value=f,type_clog=type_clog)


# Average
ax.plot(f, perm_prep_av_itrp_1, color="tab:blue") # , label=r"$\hat{k}^{11}$"
ax.plot(f, depo_prep_av_itrp_1, color="tab:orange") # label=r"$\hat{j}^{1}$ "

ax.plot(f, perm_prep_av_itrp_1-depo_prep_av_itrp_1, color="tab:red") # , label=r"$\hat{k}^{11}$"

# Standard deviation
print(perm_prep_sd_3[0,m,n])
print(depo_prep_sd_2[0,m])
ax.plot(f, perm_prep_sd_itrp_1, color="tab:blue",ls="--") # , label=r"$\hat{k}^{11}$"
ax.plot(f, depo_prep_sd_itrp_1, color="tab:orange", ls="--") # label=r"$\hat{j}^{1}$ "

# Outline the standard deviation
#ax.plot(f, perm_prep_av_itrp_1-perm_prep_sd_itrp_1, c="k")
#ax.plot(f, perm_prep_av_itrp_1+perm_prep_sd_itrp_1, c="k")
#ax.plot(f, depo_prep_av_itrp_1-depo_prep_sd_itrp_1, c="k")
#ax.plot(f, depo_prep_av_itrp_1+depo_prep_sd_itrp_1, c="k")

# Plus minus standard deviation
ax.fill_between(f, perm_prep_av_itrp_1-perm_prep_sd_itrp_1, perm_prep_av_itrp_1+perm_prep_sd_itrp_1, alpha=0.5, facecolor="tab:blue")
ax.fill_between(f, depo_prep_av_itrp_1-depo_prep_sd_itrp_1, depo_prep_av_itrp_1+depo_prep_sd_itrp_1, alpha=0.5, facecolor="tab:orange")


# Error bars
ax.errorbar(x=conc_max_or_tot_1[0::10],y=perm_prep_av_3[0::10,m,n], yerr=perm_prep_sd_3[0::10,m,n], xerr=None, color="k", lolims=False,uplims=False, fmt='.', capsize=2.5, elinewidth=1.0)
ax.errorbar(x=conc_max_or_tot_1[0::10],y=depo_prep_av_2[0::10,m], yerr=depo_prep_sd_2[0::10,m], xerr=None, color="k", lolims=False,uplims=False, fmt='.', capsize=2.5, elinewidth=1.0)


# Construction lines
#ax.plot(f,0.05*numpy.ones_like(f),c="k",ls=":")
#ax.grid()

# Plot the mono-dispersed case
alph = 1
beta = 0.01
ax.plot(conc_max_or_tot_1, 4/((alph*beta*conc_max_or_tot_1+2)**2), color="black", ls=":")


plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$f$",
                             y_label=r"$k^{11},j^{1}$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"perm_prep_3__depo_prep_2__v__s_1.svg"), format="svg")





# Plot permeability
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

# Choose dimensions to plot
m = 0
n = 0

f = numpy.linspace(0.0,conc_max_or_tot_1[-1],1000)

# Interpolate against f
perm_prep_av_itrp_1 = flow.get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=perm_prep_av_3[:,m,n],new_x_value=f,type_clog=type_clog)
perm_prep_sd_itrp_1 = flow.get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=perm_prep_sd_3[:,m,n],new_x_value=f,type_clog=type_clog)

# Average
ax.plot(f, perm_prep_av_itrp_1, color="tab:blue") # , label=r"$\hat{k}^{11}$"

# Standard deviation
#ax.plot(f, perm_prep_sd_itrp_1, color="tab:blue",ls="--") # , label=r"$\hat{k}^{11}$"

# Plus minus standard deviation
ax.fill_between(f, perm_prep_av_itrp_1-perm_prep_sd_itrp_1, perm_prep_av_itrp_1+perm_prep_sd_itrp_1, alpha=0.5, facecolor="tab:blue")

# Error bars
#ax.errorbar(x=conc_max_or_tot_1[0::10],y=perm_prep_av_3[0::10,m,n], yerr=perm_prep_sd_3[0::10,m,n], xerr=None, color="k", lolims=False,uplims=False, fmt='.', capsize=2.5, elinewidth=1.0)

# Plot the mono-dispersed case
alph = 1
beta = 0.01
ax.plot(f, 4/((alph*beta*f+2)**2), color="tab:blue", ls="--")


plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$s$",
                             y_label=r"$k$",
                             x_left=0,
                             x_right=1000,
                             y_bottom=0,
                             y_top=1.2)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"perm_prep_3__v__s_1.svg"), format="svg")




# Plot adhesivity
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

# Choose dimensions to plot
m = 0
n = 0

f = numpy.linspace(0.0,conc_max_or_tot_1[-1],1000)

# Interpolate against f
depo_prep_av_itrp_1 = flow.get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=depo_prep_av_2[:,m],new_x_value=f,type_clog=type_clog)
depo_prep_sd_itrp_1 = flow.get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=depo_prep_sd_2[:,m],new_x_value=f,type_clog=type_clog)

# Average
ax.plot(f, depo_prep_av_itrp_1, color="tab:blue") # , label=r"$\hat{k}^{11}$"

# Standard deviation
#ax.plot(f, perm_prep_sd_itrp_1, color="tab:blue",ls="--") # , label=r"$\hat{k}^{11}$"

# Plus minus standard deviation
ax.fill_between(f, depo_prep_av_itrp_1-depo_prep_sd_itrp_1, depo_prep_av_itrp_1+depo_prep_sd_itrp_1, alpha=0.5, facecolor="tab:blue")

# Error bars
#ax.errorbar(x=conc_max_or_tot_1[0::10],y=perm_prep_av_3[0::10,m,n], yerr=perm_prep_sd_3[0::10,m,n], xerr=None, color="k", lolims=False,uplims=False, fmt='.', capsize=2.5, elinewidth=1.0)

# Plot the mono-dispersed case
alph = 1
beta = 0.01
ax.plot(f, 4/((alph*beta*f+2)**2), color="tab:blue", ls="--")


plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$s$",
                             y_label=r"$j$",
                             x_left=0,
                             x_right=1000,
                             y_bottom=0,
                             y_top=1.2)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"depo_prep_3__v__s_1.svg"), format="svg")



# Plot delta
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

f = numpy.linspace(0.0,conc_max_or_tot_1[-1],1000)

# Choose dimensions to plot
i = 2 
j = 3
r = 0
m = 0

colors = ["tab:blue", "tab:orange"]
for i in [0]:
    for jj,j in enumerate([1,2]):

        # Interpolate against f
        delt_av_itrp_1 = flow.get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=delt_av_5[:,i,j,r,m],new_x_value=f,type_clog=type_clog)
        delt_sd_itrp_1 = flow.get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=delt_sd_5[:,i,j,r,m],new_x_value=f,type_clog=type_clog)


        # Average
        ax.plot(f, abs(delt_av_itrp_1), color=colors[jj], ls="-") # , label=r"$\hat{k}^{11}$"

        # Standard deviation
        #ax.plot(f, abs(delt_sd_itrp_1), color="tab:blue",ls="--") # , label=r"$\hat{k}^{11}$"

        # Outline the standard deviation
        #ax.plot(f, delt_av_itrp_1-perm_prep_sd_itrp_1, c="k")
        #ax.plot(f, delt_av_itrp_1+perm_prep_sd_itrp_1, c="k")

        # Plus minus standard deviation
        ax.fill_between(f, abs(delt_av_itrp_1)-abs(delt_sd_itrp_1), abs(delt_av_itrp_1)+abs(delt_sd_itrp_1), alpha=0.5, facecolor=colors[jj])


        # Error bars
        #ax.errorbar(x=conc_max_or_tot_1[0::10],y=delt_av_5[0::10,i,j,r,m], yerr=delt_sd_5[0::10,i,j,r,m], xerr=None, color="k", lolims=False,uplims=False, fmt='.', capsize=2.5, elinewidth=1.0)


# Construction lines
#ax.plot(f,0.05*numpy.ones_like(f),c="k",ls=":")
#ax.grid()

# Plot the mono-dispersed case
#ax.plot(f, numpy.ones_like(f), color="tab:blue", ls="--")
#ax.plot(f, 0*numpy.ones_like(f), color="tab:orange", ls="--")


plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$s$",
                             y_label=r"$\Delta_{ij}^{r}$",
                             x_left=0,
                             x_right=1000,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"delt_5__v__s_1.svg"), format="svg")





# Plot conductance
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

f = numpy.linspace(0.0,conc_max_or_tot_1[-1],1000)

# Choose dimensions to plot
r = 0
m = 0

colors = ["tab:blue", "tab:orange", "tab:green"]
for i in [0]:
    for jj,j in enumerate([1,2,3]):

        # Interpolate against f
        cond_tabl_av_itrp_1 = flow.get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=cond_tabl_av_5[:,i,j,r,m],new_x_value=f,type_clog=type_clog)
        cond_tabl_sd_itrp_1 = flow.get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=cond_tabl_sd_5[:,i,j,r,m],new_x_value=f,type_clog=type_clog)


        # Average
        ax.plot(f, cond_tabl_av_itrp_1, color=colors[jj], ls="-") # , label=r"$\hat{k}^{11}$"

        # Standard deviation
        #ax.plot(f, cond_tabl_sd_itrp_1, color=colors[jj], ls="--") # , label=r"$\hat{k}^{11}$"

        # Outline the standard deviation
        #ax.plot(f, delt_av_itrp_1-perm_prep_sd_itrp_1, c="k")
        #ax.plot(f, delt_av_itrp_1+perm_prep_sd_itrp_1, c="k")

        # Plus minus standard deviation
        ax.fill_between(f, cond_tabl_av_itrp_1-cond_tabl_sd_itrp_1, cond_tabl_av_itrp_1+cond_tabl_sd_itrp_1, alpha=0.5, facecolor=colors[jj])


        # Error bars
        #ax.errorbar(x=conc_max_or_tot_1[0::4],y=cond_tabl_av_5[0::4,i,j,r,m], yerr=cond_tabl_sd_5[0::4,i,j,r,m], xerr=None, color="k", lolims=False,uplims=False, fmt='.', capsize=2.5, elinewidth=1.0)


# Construction lines
#ax.plot(f,0.05*numpy.ones_like(f),c="k",ls=":")
#ax.grid()

# Plot the mono-dispersed case
alph = 1
beta = 0.01
ax.plot(f, 4/((alph*beta*f+2)**2), color="tab:blue", ls="--")
ax.plot(f, numpy.ones_like(f), color="tab:orange", ls="--")


plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$s$",
                             y_label=r"$G_{ij}^{\bm{r}}$",
                             x_left=0,
                             x_right=1001,
                             y_bottom=-0.0,
                             y_top=1.40)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"cond_5__v__s_1.svg"), format="svg")












# Plot conductance as a function of f 
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

# non-random
## Choose components to plot
#i = 0 
#j = 1
#r1 = 0
#r2 = 0
#
##ax.plot(conc_max_or_tot_1, cond_tabl_5[:,i,j,r1,r2], color="tab:green", ls="-")


##ax.scatter(conc_max_or_tot_1, cond_tabl_5[:,i,j,r1,r2], color="tab:blue", marker="o")
## random
#for i in [0,1,2,3]:
#    for j in [0,1,2,3]:
#        for r1 in [-1,0,1]:
#            for r2 in [-1,0,1]:
#                if r1==0 and r2==0:
#                    c = "tab:blue"
#                elif r2!=0:
#                    c="tab:orange"
#                elif r1!=0:
#                    c="tab:green"
#                else: 
#                    raise Exception("There is another scenario, we need another colour!")
#                ax.plot(conc_max_or_tot_1, cond_tabl_5[:,i,j,r1,r2], color=c, ls="-")
##ax.plot(conc_max_or_tot_1, cond_tabl_5[:,i,j,r1,r2], color="tab:blue", marker="o")
# r = 0
# -----
# hori
ax.plot(conc_max_or_tot_1, (cond_tabl_5[:,0,1,0,0]), color="tab:blue", ls="-")
ax.plot(conc_max_or_tot_1, (cond_tabl_5[:,2,3,0,0]), color="tab:blue", ls="--")
# vert
ax.plot(conc_max_or_tot_1, (cond_tabl_5[:,0,2,0,0]), color="tab:orange", ls="-")
ax.plot(conc_max_or_tot_1, (cond_tabl_5[:,1,3,0,0]), color="tab:orange", ls="--")
# r = 1
# -----
# hori
ax.plot(conc_max_or_tot_1, (cond_tabl_5[:,1,0,1,0]), color="tab:green", ls="-")
ax.plot(conc_max_or_tot_1, (cond_tabl_5[:,3,2,1,0]), color="tab:green", ls="--")
# vert
ax.plot(conc_max_or_tot_1, (cond_tabl_5[:,0,2,0,1]), color="tab:red", ls="-")
ax.plot(conc_max_or_tot_1, (cond_tabl_5[:,1,3,0,1]), color="tab:red", ls="--")


alph = 1
beta = 1

ax.plot(conc_max_or_tot_1, 4/((alph*beta*conc_max_or_tot_1+2)**2), color="black", ls="--")
ax.plot(conc_max_or_tot_1, numpy.ones_like(conc_max_or_tot_1), color="black", ls=":")

f = numpy.linspace(0.0,conc_max_or_tot_1[-1],1000)

#ax.plot(f, flow.get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=cond_tabl_5[:,i,j,r1,r2],new_x_value=f,type_clog=type_clog), color="tab:blue")
#ax.plot(conc_max_1, flow.get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=depo_prep_2[:,m]  ,new_x_value=conc_max_1,type_clog=type_clog), label=r"$\hat{j}^{1}$", color="blue")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$f$",
                             y_label=r"$G_{ij}^{\bm{r}}$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"cond_5_v__conc_max_or_tot_1.svg"), format="svg")




# Plot delta as a function of f 
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

# Choose components to plot
f = numpy.linspace(0.0,conc_max_or_tot_1[-1],1000)

# non-random
# ----------------
#ax.scatter(conc_max_or_tot_1, abs(delt_5[:,0,1,0,0]), color="tab:blue", marker="o")
#ax.plot(   conc_max_or_tot_1, abs(delt_5[:,0,1,0,0]), color="tab:blue", ls="-")

#ax.scatter(conc_max_or_tot_1, abs(delt_5[:,0,1,0,1]), color="tab:orange", marker="o")
#ax.plot(   conc_max_or_tot_1, abs(delt_5[:,0,1,0,1]), color="tab:orange", ls="-")

#ax.plot(conc_max_or_tot_1, cond_tabl_5[:,i,j,r1,r2], color="tab:blue", marker="o")

# random
# -----------------
#for i in [0,1,2,3]:
#    for j in [0,1,2,3]:
#        for r in [-1,0,1]:
#            for m in [0]:
#                if r==-1:
#                    c="tab:blue"
#                    ls="-"
#                elif r==0:
#                    c="tab:orange"
#                    ls="--"
#                elif r==1:
#                    c="tab:green"
#                    ls=":"
#                ax.plot(   conc_max_or_tot_1, abs(delt_5[:,i,j,r,m]), color=c, ls=ls)
# r = 0
# -----
# hori
ax.plot(conc_max_or_tot_1, (delt_5[:,1,0,0,0]), color="tab:blue", ls="-")
ax.plot(conc_max_or_tot_1, (delt_5[:,3,2,0,0]), color="tab:blue", ls="--")
# vert
ax.plot(conc_max_or_tot_1, (delt_5[:,2,0,0,0]), color="tab:orange", ls="-")
ax.plot(conc_max_or_tot_1, (delt_5[:,3,1,0,0]), color="tab:orange", ls="--")
# r = 1
# -----
# hori
ax.plot(conc_max_or_tot_1, (delt_5[:,0,1,-1,0]), color="tab:green", ls="-")
ax.plot(conc_max_or_tot_1, (delt_5[:,2,3,-1,0]), color="tab:green", ls="--")
# vert
ax.plot(conc_max_or_tot_1, (delt_5[:,0,2,0,0]), color="tab:red", ls="-")
ax.plot(conc_max_or_tot_1, (delt_5[:,1,3,0,0]), color="tab:red", ls="--")


## r = 0
## -----
## hori
#ax.plot(conc_max_or_tot_1, (heav_5[:,1,0,0,0]), color="tab:blue", ls="-")
#ax.plot(conc_max_or_tot_1, (heav_5[:,3,2,0,0]), color="tab:blue", ls="--")
## vert
#ax.plot(conc_max_or_tot_1, (heav_5[:,0,2,0,0]), color="tab:orange", ls="-")
#ax.plot(conc_max_or_tot_1, (heav_5[:,1,3,0,0]), color="tab:orange", ls="--")
## r = 1
## -----
## hori
#ax.plot(conc_max_or_tot_1, (heav_5[:,0,1,-1,0]), color="tab:green", ls="-")
#ax.plot(conc_max_or_tot_1, (heav_5[:,2,3,-1,0]), color="tab:green", ls="--")
## vert
#ax.plot(conc_max_or_tot_1, (heav_5[:,2,0,0,0]), color="tab:red", ls="-")
#ax.plot(conc_max_or_tot_1, (heav_5[:,3,1,0,0]), color="tab:red", ls="--")
## r = -1
## -----
## hori
#ax.plot(conc_max_or_tot_1, abs(delt_5[:,0,1,-1,0]), color="tab:red", ls="-")
#ax.plot(conc_max_or_tot_1, abs(delt_5[:,2,3,-1,0]), color="tab:red", ls="--")


#f = numpy.linspace(0.0,20.0,1000)

#ax.plot(f, flow.get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=cond_tabl_5[:,i,j,r1,r2],new_x_value=f,type_clog=type_clog), color="tab:blue")
#ax.plot(conc_max_1, flow.get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=depo_prep_2[:,m]  ,new_x_value=conc_max_1,type_clog=type_clog), label=r"$\hat{j}^{1}$", color="blue")

ax.plot(conc_max_or_tot_1, numpy.zeros_like(conc_max_or_tot_1), color="black", ls=":")
ax.plot(conc_max_or_tot_1, numpy.ones_like(conc_max_or_tot_1), color="black", ls="--")


plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$f$",
                             y_label=r"$\Delta_{ij}^{r^1}$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)
#                             y_bottom=-0.1,
#                             y_top=1.1)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"delt_5_v__conc_max_or_tot_1.svg"), format="svg")


# Plot adhe distribution
# -----
fig, ax = plt.subplots(1,1)

# Count number of non zero in adhe
# -----
# get correct k array 
alpha = 1.0/1.72
# TODO Define alpha properly
 
count_cond = 0
count_adhe = 0
count_above_thresh = 0
num_refs = len( cond_tabl_5[0,0,0,:,0])
num_nodes = len(cond_tabl_5[0,:,0,0,0])

for r in range(num_refs):
    for s in range(num_refs):
        # Take upper triangle so that edges are unique
        cond_wo_reps_2 = numpy.triu(cond_tabl_5[0,:,:,r,s])
        adhe_wo_reps_2 = numpy.triu(adhe_tabl_5[-1,:,:,r,s])

        # Count number of unique non-zero edges
        count_cond = count_cond + numpy.count_nonzero(a=cond_wo_reps_2, axis=None, keepdims=False)

        # Count number of unique edges where adhesivity is 1
        count_adhe = count_adhe + numpy.count_nonzero(a=adhe_wo_reps_2, axis=None, keepdims=False)

        # Check above by counting number of edges that satisfy blocking condition
        for i in range(num_nodes):
            for j in range(num_nodes):
                if cond_wo_reps_2[i,j]<(1.0/alpha) and cond_wo_reps_2[i,j]>0.0:
                    count_above_thresh = count_above_thresh + 1

#print(count_cond)
#print(count_adhe)
#print(count_above_thresh)

# Count number of edges above threshold


def count_num_edges_blocked(adhe_tabl_5, heav_5, delt_5, cond_tanl_5):
    """
    Count the number of edges that are blocked 
    in particular run.
    """
    # Parameters 
    num_refs    = len(adhe_tabl_5[0,0,0,:,0])

    count_adhe = 0
    for r in range(num_refs):
        for s in range(num_refs):

            ## Take upper triangle so that edges are unique
            #a = adhe_wo_reps_2 = numpy.triu(adhe_tabl_4[:,:,r,s])
            a = adhe_tabl_5[-1,:,:,r,s]*heav_5[0,:,:,r,m]*cond_tabl_5[0,:,:,r,s]*(-delt_5[0,:,:,r,m])
            #print("a={}".format(a))
            # Count number of unique edges where adhesivity is 1
            #print("r={},s={},a=\n{}".format(r,s,a))
            #print("r={},s={},a=\n{}".format(r,s,a))
            count_adhe = count_adhe + numpy.count_nonzero(a=a, axis=None, keepdims=False)
    
    return count_adhe

count_adhe = count_num_edges_blocked(adhe_tabl_5, heav_5, delt_5, cond_tabl_5)
print(count_adhe)


count, count_hori, count_not_hori = utils_preprocess_2D.count_num_edges_blocked(initialisation="6-ireg",
                                                                                cond_tabl_5=cond_tabl_5, 
                                                                                adhe_tabl_5=adhe_tabl_5, 
                                                                                delt_5=delt_5, 
                                                                                heav_5=heav_5)
print(count, count_hori, count_not_hori)

r = -1
s = 0
m = 0
#print("heav_5[0,:,:,r,m]:\n{}".format(heav_5[0,:,:,r,m]))
#print("-delt_5[0,:,:,r,m]:\n{}".format(-delt_5[0,:,:,r,m]))
#print("cond_tabl_5[-1,:,:,r,s]:\n{}".format(cond_tabl_5[0,:,:,r,s]))
#print("adhe_tabl_5[-1,:,:,r,s]:\n{}".format(adhe_tabl_5[-1,:,:,r,s]))
