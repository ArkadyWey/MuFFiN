from matplotlib import pyplot as plt
import os 
import numpy 


import sys
sys.path.append("/home/user/utils_python")
import plotting

# Parameters 
# -----
path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/mono/sweep-alph/")


# Plot efficiency
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

alph_1 = numpy.linspace(0,11,101)
ax.plot(alph_1,numpy.ones_like(alph_1)-numpy.exp(-alph_1),c="tab:blue",ls="-")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$\alpha$",
                             y_label=r"$\eta$",
                             x_left=0,
                             x_right=10,
                             y_bottom=0,
                             y_top=1.01)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"eta_1__v__alph_1.svg"), format="svg")