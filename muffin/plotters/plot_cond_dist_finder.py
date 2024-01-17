import matplotlib
from matplotlib import pyplot as plt
import numpy
import os

import muffin.plotters.plotting as plotting

path_results = os.path.join(".","results/results_cond-dist")

num_nodes = 4

edge_lengs = numpy.load(os.path.join(path_results,"edge_lengs_N-{}.npy".format(num_nodes)))
edge_conds    = numpy.load(os.path.join(path_results,"edge_conds_N-{}.npy".format(num_nodes)))

fig, ax = plt.subplots()
ax.hist(numpy.array(edge_lengs), bins=1000)
plotting.save_fig(fig=fig,fname=os.path.join(path_results,"edge_lengs.svg"), format="svg")

fig, ax = plt.subplots()
ax.hist(numpy.array(edge_conds), bins=1000)
plotting.save_fig(fig=fig,fname=os.path.join(path_results,"edge_conds.svg"), format="svg")