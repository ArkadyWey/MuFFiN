from matplotlib import pyplot as plt
import os
import numpy

import muffin.plotters.plotting as plotting

# Parameters 
# -----
path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/mono/flow_sweep-alph") # paper


posi_1 = numpy.linspace(0,1,1001)

# Plot concentration
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

for alph in [0,0.5,1.0,1.5,2.0,2.5,3.0]:

    ax.plot(posi_1,numpy.exp(-alph*posi_1))#,c="black",ls="--")
    #ax.plot(posi_1,numpy.exp(-alph)*numpy.ones_like(posi_1), c="black", ls=":")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$c$",
                             x_left=0,
                             x_right=None,
                             y_bottom=0,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"conc_2__v__posi_1.svg"), format="svg")


# Plot efficiency
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

alph_1 = numpy.linspace(0,5,1001)

ax.plot(alph_1, 1-numpy.exp(-alph_1), c="tab:blue", ls="-")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$\alpha$",
                             y_label=r"$\eta$",
                             x_left=0,
                             x_right=None,
                             y_bottom=0,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"effi__v__alph_1.svg"), format="svg")
