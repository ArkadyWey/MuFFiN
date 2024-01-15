
import os
import numpy
from matplotlib import pyplot as plt


import muffin.plotters.plotting as plotting

path_results = os.path.join(".","results/results_network/thesis/sweep-alph/tiny-sweep")


delt=0.5
epsi=0.1

plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

alph_1=numpy.linspace(0,10,100)

ax.plot(alph_1, 1-(((1-epsi*delt*alph_1)**(1.0/(delt*epsi)-1))), color="tab:blue")


plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$\alpha$",
                             y_label=r"$\tilde{\eta}$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)
plotting.save_fig(fig=fig,fname=os.path.join(path_results,"eff_aprx_1__v__alph_1.svg"), format="svg")