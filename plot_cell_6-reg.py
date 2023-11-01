import matplotlib 
from matplotlib import pyplot as plt
import os 
import numpy
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D  

import multiscale_models.configure as configure

# Parameters 
# -----
path_results = os.path.join(".","results/results_cell_6-reg")

sigma = 0.3
initialisation = "6-reg"

# Arrays for first plot:
pts_to_tri_2 = numpy.load(os.path.join(path_results,"pts_to_tri_2.npy"))
simplices    = numpy.load(os.path.join(path_results,"simplices.npy"))
key          = numpy.load(os.path.join(path_results,"key.npy"))


# Arrays for second plot:
cond_init_4 = numpy.load(os.path.join(path_results,"cond_init_4.npy"))
num_nodes   = len(cond_init_4[:,0,0,0])
num_refs    = len(cond_init_4[0,0,:,0])
num_dims    = 2
pts_4       = numpy.load(os.path.join(path_results,"pts_4.npy"))


# Get the run's configuration parameters (needed for lengths etc in plot)
#  -------------------------------------
conf = configure.Configure(num_nodes=num_nodes,initialisation=initialisation,sigma=sigma,type_alpha=type_alpha)
num_rows_or_cols = int(numpy.sqrt(num_nodes/2.0))



# Plot original triangulation with no removal
# ------------------------------------------
fig, ax = plt.subplots(1,1)
pts_x = pts_to_tri_2[:,0] # x coordinates of all points being triangulated
pts_y = pts_to_tri_2[:,1] # y coordinates of all points being triangulated

# Plot edges 
ax.triplot(pts_x, pts_y, simplices, color="tab:blue", linewidth=2.0)

# Plot nodes
ax.plot(pts_x, pts_y, 'go', markersize=5.0)

# Plot crosses at where construction nodes should be
ax.plot(0.0,0.0,                 "+", color="black", markersize=5.0)
ax.plot(conf.l1/2.0,conf.l2/2.0, "+", color="black", markersize=5.0)

# Plot node index
for p in range(len(pts_x)):
    array = key[p]
    i = array[0]
    r = array[1]
    s = array[2]

    ax.annotate(r"{}".format(i), (pts_to_tri_2[p,0], pts_to_tri_2[p,1]))

# Plot cell boundaries
for x in [-num_rows_or_cols*conf.l1,0,num_rows_or_cols*conf.l1]:
    for y in [-num_rows_or_cols*conf.l2,0,num_rows_or_cols*conf.l2]:
        if x==0 and y==0:
            ax.add_patch(Rectangle(xy=(x, y), width=num_rows_or_cols*conf.l1, height=num_rows_or_cols*conf.l2, alpha=0.2, color="tab:red", edgecolor="tab:red", fill=True, linestyle="--"))
        else:
            ax.add_patch(Rectangle(xy=(x, y), width=num_rows_or_cols*conf.l1, height=num_rows_or_cols*conf.l2, alpha=0.8, color="tab:red", edgecolor="tab:red", fill=False, linestyle="--"))

# Clean up plot
ax.set_xlim(left=-num_rows_or_cols*conf.l1-1,right=+2*num_rows_or_cols*conf.l1+1)
ax.set_ylim(bottom=-num_rows_or_cols*conf.l2-1,top=+2*num_rows_or_cols*conf.l2+1)

ax.set_aspect("equal")
plt.axis('off')

plt.savefig(fname=os.path.join(path_results,"9-cells_random-structure.svg"), format="svg")




# Plot initial conductance of unit cell
# ----------------------------
fig, ax = plt.subplots(1,1)


# Plot edges
for r in range(num_refs):
    for s in range(num_refs):
        for i in range(num_nodes):
            for j in range(num_nodes):
                # Check if there is an edge here to plot
                if cond_init_4[i,j,r,s] != 0.0:
                    
                    # Get points of nodes
                    x_i = pts_4[i,0,0,0]
                    y_i = pts_4[i,1,0,0]

                    x_j = pts_4[j,0,r,s]
                    y_j = pts_4[j,1,r,s]


                    # Plot edge from point to point
                    x_vals_of_points = [x_i, x_j]
                    y_vals_of_points = [y_i, y_j]


                    linewidth = cond_init_4[i,j,r,s]
                    #ax.add_line(Line2D(xdata=x_vals_of_points,ydata=y_vals_of_points, linewidth=2.0, color="tab:blue"))
                    ax.add_line(Line2D(xdata=x_vals_of_points,ydata=y_vals_of_points, linewidth=linewidth, color="tab:blue"))
                    
                    # Plot nodes that have edges
                    #ax.plot(x_i,y_i,'go', markersize=5.0)
                    #ax.plot(x_j,y_j,'go', markersize=5.0) 
                    
                    #ax.plot(x_i,y_i,'ko', markersize=12.0)
                    #ax.plot(x_j,y_j,'ko', markersize=12.0) 
                    #ax.add_line(Line2D(xdata=x_vals_of_points,ydata=y_vals_of_points, linewidth=3.0, color="black"))


# Plot all nodes
ax.plot(pts_x, pts_y, 'go', markersize=1.0)

# Plot crosses at where construction nodes should be
ax.plot(0.0,0.0,                 "+", color="black", markersize=5.0)
ax.plot(conf.l1/2.0,conf.l2/2.0, "+", color="black", markersize=5.0)

# Plot node names
for p in range(len(pts_to_tri_2[:,0])):
    array = key[p]
    i = array[0]
    r = array[1]
    s = array[2]

    ax.annotate(r"{}".format(i), (pts_to_tri_2[p,0], pts_to_tri_2[p,1]))

# Plot cell boundaries
for x in [-conf.l1,0,conf.l1]:
    for y in [-conf.l2,0,conf.l2]:
        if x==0 and y==0:
            ax.add_patch(Rectangle(xy=(x, y), width=conf.l1, height=conf.l2, alpha=0.2, color="tab:red", edgecolor="tab:red", fill=True, linestyle="--"))
        else:
            ax.add_patch(Rectangle(xy=(x, y), width=conf.l1, height=conf.l2, alpha=0.8, color="tab:red", edgecolor="tab:red", fill=False, linestyle="--"))

# Clean up plot
ax.set_xlim(left  =-conf.l1-1,right=+2*conf.l1+1)
ax.set_ylim(bottom=-conf.l2-1,  top=+2*conf.l2+1)

ax.set_aspect("equal")
plt.axis('off')

plt.savefig(fname=os.path.join(path_results,"unit-cell_random-structure.svg"), format="svg")

