
import os
import numpy
from matplotlib import pyplot as plt


import sys
sys.path.append("/home/user/utils_python")
import plotting

path_results = os.path.join(".","results/results_network/thesis/sweep-beta/small-sweep")

c = 1.69

plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

beta_1=numpy.linspace(0.01,10,1000)

ax.plot(beta_1, c*beta_1**(-1), color="tab:blue")


plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$\beta$",
                             y_label=r"$\tilde{\tau}$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)
plotting.save_fig(fig=fig,fname=os.path.join(path_results,"thro_aprx_1__v__alph_1.svg"), format="svg")