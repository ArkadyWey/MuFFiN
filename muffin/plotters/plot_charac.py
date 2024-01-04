from matplotlib import pyplot as plt
import os
import numpy
from scipy import interpolate

import muffin.utils.utils_sl as utils_sl
import muffin.network.network_2D as network_2D

import sys
sys.path.append("/home/user/utils_python")
import plotting


def get_charac(z_1,t0,z0):
    """
    """
    t_1 = z_1 + (t0-z0)
    return t_1

path_results = "/home/user/"


# Plot characeteristics
# ------------------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)


z_1 = numpy.linspace(0,1,11)
t0_1  = [0] #numpy.linspace(0,1,11)
z0_1  = numpy.linspace(-3,1,41)

for t0 in t0_1:
    for z0 in z0_1:
        t_1 = get_charac(z_1,t0,z0)
        if (t0-z0) < 0:
            color = "tab:blue"
        elif (t0-z0) >= 0:
            color = "tab:orange"
        if (t0-z0) == 0: 
            ls = "--"
        else: 
            ls = "-"
        
        ax.plot(z_1,t_1,color=color,ls=ls)

for y in numpy.linspace(0,3,31):
    # ax.arrow(x=0.5, y=y, dx=0.2, dy=0.2, 
    #          color = "tab:orange",
    #          arrowstyle="->",
    #          shape='full', lw=0, length_includes_head=False, head_width=0.05)
    if y < 0.5:
        color="tab:blue"
    elif y>= 0.5:
        color="tab:orange"

    ax.annotate("", 
                xytext=(0.45, y-0.05), 
                xy=(0.55, y+0.05),
                arrowprops=dict(arrowstyle="->", color=color), 
                size=15  
                )

ax.plot(z_1,numpy.ones_like(z_1),color="k",ls="--")

# Cleanup graph 
# -------------
plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$z$",
                             y_label=r"$t$",
                             x_left=0,
                             x_right=1.1,
                             y_bottom=0,
                             y_top=3)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"charac.svg"), format="svg")