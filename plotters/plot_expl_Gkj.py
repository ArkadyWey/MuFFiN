from matplotlib import pyplot as plt
import os 
import numpy 


import sys
sys.path.append("/home/user/utils_python")
import plotting

# Parameters 
# -----
path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/mono/expl/prep")
if not os.path.exists(path_results):
    os.makedirs(path_results)

#alph = 1
#beta = 0.01
s = numpy.linspace(0,1000,10001)
alphabeta_1 = numpy.linspace(0.000,0.01,11)
print("alphabeta_1",alphabeta_1)


# Plot conductance as a function of s 
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

for alphabeta in alphabeta_1:
    ax.plot(s, 4/((alphabeta*s+2)**2), color="tab:blue", ls="-")
#ax.plot(s, 4/((alph*beta*s+2)**2), color="tab:blue", ls="-")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$s$",
                             y_label=r"$G_{ij}^{\bm{r}}$",
                             x_left=0,
                             x_right=1000,
                             y_bottom=0,
                             y_top=1.01)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"cond_5__v__s_1.svg"), format="svg")


# Plot permeability as a function of s 
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

for alphabeta in alphabeta_1:
    ax.plot(s, 4/((alphabeta*s+2)**2), color="tab:blue", ls="-")
#ax.plot(s, 4/((alph*beta*s+2)**2), color="tab:blue", ls="-")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$s$",
                             y_label=r"$k$",
                             x_left=0,
                             x_right=1000,
                             y_bottom=0,
                             y_top=1.01)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"perm_3__v__s_1.svg"), format="svg")



# Plot adhesivity as a function of s sweep alph
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

alph_1 = numpy.linspace(1,0,11,endpoint=True)
print("alph_1:",alph_1)

beta = 0.01
for a,alph in enumerate(alph_1):
    ax.plot(s, alph*4/((alph*beta*s+2)**2), color="tab:blue", ls="-")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$s$",
                             y_label=r"$j$",
                             x_left=0,
                             x_right=1000,
                             y_bottom=0,
                             y_top=1)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"depo_2__v__s_1__sweep-alph.svg"), format="svg")



# Plot adhesivity as a function of s sweep beta
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

beta_1 = numpy.linspace(0.00,0.1,11,endpoint=True)
print("beta_1:",beta_1)

alph = 1
for b,beta in enumerate(beta_1):
    ax.plot(s, alph*4/((alph*beta*s+2)**2), color="tab:blue", ls="-")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$s$",
                             y_label=r"$j$",
                             x_left=0,
                             x_right=1000,
                             y_bottom=0,
                             y_top=1.01)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"depo_2__v__s_1__sweep-beta.svg"), format="svg")