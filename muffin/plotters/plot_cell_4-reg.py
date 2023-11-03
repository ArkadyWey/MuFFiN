from turtle import color
import matplotlib 
from matplotlib import pyplot as plt
import os 
import numpy
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D  

import networkx as nx
from matplotlib import pyplot as plt

import multiscale_models.configure as configure

# Parameters 
# -----
path_results = os.path.join(".","results/results_cell_4-reg")
if not os.path.exists(path_results):
    os.mkdir(path_results)

sigma = 0.3
initialisation = "4-reg"
type_alpha = "mean"

N =  100
n = int(numpy.sqrt(N))+2 # =2 since need extras on either side for deletion
fig, ax = plt.subplots(1,1,figsize=(8,8))


# Make node graph
G = nx.grid_2d_graph(n,n)
pos = {(x,y):(y,-x) for x,y in G.nodes()}
print(pos)

# Get position of cell boundary 
coord = pos[(n-1,1)]
x = coord[0]-0.5
y = coord[1]+0.5
print(coord)

# Delete external nodes as not in cell
for node in G.nodes():
    if node[0] == 0 or node[0] == n-1 or node[1] == 0 or node[1] == n-1:
        G.remove_node(node)

nodes = nx.draw_networkx_nodes(G, 
                               pos=pos, 
                               node_color='white',
                               style='solid', 
                               with_labels=False,
                               node_size=300,
                               node_shape="o",
                               alpha=1.0,
                               linewidths=2.0
                               )
nodes.set_edgecolor('black')


H = nx.grid_2d_graph(n,n)
pos = {(x,y):(y,-x) for x,y in H.nodes()}

# Delete corner nodes so edges don't show
for edge in H.edges():
    node_1 = edge[0]
    node_2 = edge[1]
    if node_1[1] == 0 and node_2[1] == 0 or node_1[0] == 0 and node_2[0] == 0 or node_1[1] == n-1 and node_2[1] == n-1 or node_1[0] == n-1 and node_2[0] == n-1:
        H.remove_edge(node_1,node_2)

nodes = nx.draw_networkx_edges(H, 
                               pos=pos, 
                               edge_color='black',
                               style='solid', 
                               with_labels=False,
                               node_shape="o",
                               alpha=1.0,
                               linewidths=2.0,
                               width=2.0
                               )


# Plot cell boundaries
print(plt.xlim())
print(plt.ylim()) 
ax.add_patch(Rectangle(xy=(x, y), width=n-2, height=n-2, alpha=1.0, color="black", edgecolor="black", fill=False, linestyle="-",linewidth=2.0))

ax.set_aspect("equal")
plt.axis('off')

plt.savefig(fname=os.path.join(path_results,"unit-cell_N-{}.svg".format(N)), format="svg")

