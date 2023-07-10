from matplotlib import pyplot as plt
import os 
import numpy 


import sys
sys.path.append("/home/user/utils_python")
import plotting

# Parameters 
# -----
path_results = os.path.join("/home/user/home_temp/projects/papers/2023_homogenisation/figures/mono/prep/expl/")



# Plot conductance as a function of f 
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)


alph = 1
beta = 0.01
s = numpy.linspace(0,1000,10001)

alphabeta_1 = numpy.linspace(0.001,0.01,10)
print(alphabeta_1)
for alphabeta in alphabeta_1:
    ax.plot(s, 4/((alphabeta*s+2)**2), color="tab:blue", ls="-")
#ax.plot(s, 4/((alph*beta*s+2)**2), color="tab:blue", ls="-")


plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$s$",
                             y_label=r"$G_{ij}^{\bm{r}}$",
                             x_left=0,
                             x_right=1000,
                             y_bottom=0,
                             y_top=1)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"cond_5_v__s_1.svg"), format="svg")
