
import numpy as numpy
from scipy import spatial
from  matplotlib import pyplot as plt
from matplotlib.lines import Line2D  
    
num_nodes = 3
num_refs  = 3
num_dims  = 2

# Get unit cell points
pts_x_0 = numpy.random.uniform(low=0.0, high=1.0, size=num_nodes) #numpy.array([0.5])#
pts_y_0 = numpy.random.uniform(low=0.0, high=1.0, size=num_nodes) #numpy.array([0.5])#

# Right or up components
pts_x_1 = 1.0*numpy.ones_like(pts_x_0) + pts_x_0 
pts_y_1 = 1.0*numpy.ones_like(pts_y_0) + pts_y_0

## Left or down components
pts_x_m1 = -1.0*numpy.ones_like(pts_x_0) + pts_x_0
pts_y_m1 = -1.0*numpy.ones_like(pts_y_0) + pts_y_0



# Get points tensor 
# ------------------
pts_4 = numpy.zeros(shape=(num_nodes,num_dims,num_refs,num_refs))
# pts_4[i,m,r,s] is the x^m component of node i in cell at reference r,s

for r in range(num_refs):
    for s in range(num_refs):
        for i in range(num_nodes):
            
            if r == 0:
                pts_x = pts_x_0
            elif r == 1:
                pts_x = pts_x_1
            elif r == 2: 
                pts_x = pts_x_m1

            if s == 0:
                pts_y = pts_y_0
            elif s == 1:
                pts_y = pts_y_1
            elif s == 2: 
                pts_y = pts_y_m1

            pts_4[i,0,r,s] = pts_x[i]
            pts_4[i,1,r,s] = pts_y[i]




# Triangulate unit cell with upper quartile
# -----------------------------------------
# The rest will be made via reflection
pts_to_tri_2 = []
key = []
# pts_to_tri_2[p,m] = mth component of point p
# key[p] = [i,r,s] corresponding to point p
for r in range(2):
    for s in range(2):
        for i in range(num_nodes):
            i_x = pts_4[i,0,r,s] # x component of point corresponding to node i in cell r,s
            i_y = pts_4[i,1,r,s] # y component of point corresponding to node i in cell r,s

            pts_to_tri_2.append([i_x,i_y]) 
            key.append([i,r,s])
            
pts_to_tri_2 = numpy.array(pts_to_tri_2)

tri = spatial.Delaunay(points=pts_to_tri_2)
simplices = tri.simplices



# Get edges given by triangulation
# --------------------------------
loops = []
for simplex in simplices: 
    path = list(simplex)
    path.append(path[0])
    loops.append(path)


edges = []
for loop in loops:
    # Add the three edges contained in the triangular loop
    # NB there are always three becuase it's a triangle
    edge_1 = [loop[0], loop[1]]
    edge_2 = [loop[1], loop[2]]
    edge_3 = [loop[2], loop[3]]

    edges.append(edge_1)
    edges.append(edge_2)
    edges.append(edge_3)


# Get distances between points
# ----------------------------
dist_6 = numpy.zeros(shape=(num_nodes,num_refs,num_refs,num_nodes,num_refs,num_refs))
# dist_6[i,r_i,s_i, j,r_j,s_j] = distance between node (i,r_i,s_i) and (j,r_j,s_j)
for r_i in range(num_refs):
    for s_i in range(num_refs):
        for r_j in range(num_refs):
            for s_j in range(num_refs):
                for i in range(num_nodes):
                    for j in range(num_nodes):
                        # Get points corresponding to nodes
                        p_i = pts_4[i,:,r_i,s_i]
                        p_j = pts_4[j,:,r_j,s_j]
                        # Get distance between points
                        dist_6[i,r_i,s_i,j,r_j,s_j] = numpy.linalg.norm(p_i-p_j)



# Get conductanc tensor 
# ---------------------
cond_init_4 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_refs))
useful_edges = []
for edge in edges:
    # Get points that edge involves
    p_i = edge[0]
    p_j = edge[1]

    # Get nodes that edge involves
    n_i = key[p_i]
    n_j = key[p_j]

    # Get i,r,s triples that edge involves
    [i_i, r_i, s_i] = n_i
    [i_j, r_j, s_j] = n_j

    # Keep edge if involves unit cell
    # Either first or second node is in unit cell or they both are
    if (r_i == 0 and s_i == 0):
        # i is in unit cell
        cond_init_4[i_i,i_j,r_j,s_j] = (1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_i,r_i,s_i,i_j,r_j,s_j])    #1.0
        cond_init_4[i_j,i_i,-r_j,-s_j] = (1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_i,r_i,s_i,i_j,r_j,s_j]) #1.0
    elif (r_j == 0 and s_j == 0):
        # j is in unit cell
        cond_init_4[i_j,i_i,r_i,s_i] = (1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_j,r_j,s_j,i_i,r_i,s_i])
        cond_init_4[i_i,i_j,-r_i,-s_i] = (1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_j,r_j,s_j,i_i,r_i,s_i])
    else: 
        # neither i or j in unit cell so this edge is not in conductance
        pass



# Plot original triangulation in top quartile
# ------------------------------------------
fig, ax = plt.subplots(1,1)
ax.triplot(pts_to_tri_2[:,0], pts_to_tri_2[:,1], simplices)

ax.plot(pts_to_tri_2[:,0], pts_to_tri_2[:,1], 'o')

for p in range(len(pts_to_tri_2[:,0])):
    array = key[p]
    i = array[0]
    r = array[1]
    s = array[2]

    ax.annotate(r"{}".format(i), (pts_to_tri_2[p,0], pts_to_tri_2[p,1]))

from matplotlib.patches import Rectangle
for x in [-1,0,1]:
    for y in [-1,0,1]:
        if x==0 and y==0:
            ax.add_patch(Rectangle(xy=(x, y), width=1, height=1, alpha=0.2, color="tab:red"))
        else:
            ax.add_patch(Rectangle(xy=(x, y), width=1, height=1, alpha=0.8, color="tab:red", edgecolor="tab:red", fill=False, linestyle="--"))

ax.set_xlim(left=-1,right=+2)
ax.set_ylim(bottom=-1,top=+2)
plt.savefig(fname="edges_all", format="svg")




# Plot initial conductance
# ----------------------------
fig, ax = plt.subplots(1,1)

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

                    ax.plot(x_i,y_i,'ro')
                    ax.plot(x_j,y_j,'ro') 
                    ax.add_line(Line2D(xdata=x_vals_of_points,ydata=y_vals_of_points))

#for p in range(len(pts_to_tri_2[:,0])):
#    array = key[p]
#    i = array[0]
#    r = array[1]
#    s = array[2]
#
#    ax.annotate(r"{}".format(i), (pts_to_tri_2[p,0], pts_to_tri_2[p,1]))

for x in [-1,0,1]:
    for y in [-1,0,1]:
        if x==0 and y==0:
            ax.add_patch(Rectangle(xy=(x, y), width=1, height=1, alpha=0.2, color="tab:red"))
        else:
            ax.add_patch(Rectangle(xy=(x, y), width=1, height=1, alpha=0.8, color="tab:red", edgecolor="tab:red", fill=False, linestyle="--"))

ax.set_xlim(left=-1,right=+2)
ax.set_ylim(bottom=-1,top=+2)
plt.savefig(fname="edges_removed", format="svg")
                        


# One is a special case and i think i should give it 
# triangulation manually
#### Triangulate 
###triangulation_started = False # indicates whether triangulation has started
###pts_batch_to_tri = []
#### pts_batch_to_tri[p][m] = mth component of pth point to triangulate
###for r in range(2):
###    for s in range(2): 
###        for i in range(num_nodes):
###        # Notice we do not traingulate negative cells since 
###        # these will be mirrors of triangulation in positive cells.
###        # Hence over 2 directions only.
###            i_x = pts_4[i,0,r,s] # x component of point corresponding to node i in cell r,s
###            i_y = pts_4[i,1,r,s] # y component of point corresponding to node i in cell r,s
###            pts_batch_to_tri.append([i_x,i_y])
###
###        # Check if can triangulate current batch
###        num_pts_in_batch = len(pts_batch_to_tri)
###
###        if triangulation_started == False:
###            if num_pts_in_batch >= 4: 
###                # Start triangulation
###                tri = spatial.Delaunay(points=numpy.array(pts_batch_to_tri),incremental=True,qhull_options="Qz")
###                # Announce triangulation start
###                triangulation_started = True
###                # Reset points batch 
###                pts_batch_to_tri = []
###            else:
###                # Triangulation cannot be started becasue not enough points in batch 
###                pass
###        elif triangulation_started == True:
###            # Continue triangulation
###            tri = spatial.Delaunay.add_points(points=numpy.array(pts_batch_to_tri), restart=False)
###            # Reset points batch 
###            pts_batch_to_tri = []
###        else: 
###            raise Exception
