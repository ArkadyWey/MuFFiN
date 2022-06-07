
import numpy
from scipy.spatial import Delaunay
import numpy as np
from matplotlib import pyplot as plt
import networkx as nx


num_nodes = 4
num_dims = 2
num_refs = 3


cond_init_4 = np.zeros(shape=(num_nodes, num_nodes, num_refs, num_refs))



# Get positions of all points 
# ----------------------------

# Central components
pts_x_0 = np.array([0.2,0.8,0.2,0.8])
pts_y_0 = np.array([0.2,0.2,0.8,0.8])

# Right or up components
pts_x_1 = pts_x_0 + 1.0*np.ones_like(pts_x_0)
pts_y_1 = pts_y_0 + 1.0*np.ones_like(pts_y_0)

# Left or down components
pts_x_m1 = -1.0*np.array([el for el in reversed(list(pts_x_0))])
pts_y_m1 = -1.0*np.array([el for el in reversed(list(pts_y_0))])

# Fill the positions tensor
pts_4 = np.zeros(shape = (num_nodes, num_dims, num_refs, num_refs) )
#pts_4[i,m,r,s] = num_dims[m] component of position of node nodes[i] in cell with reference (r,s)

for r in range(num_refs):
    for s in range(num_refs):
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

        pts_2 = np.transpose(np.concatenate(([pts_x],[pts_y]), axis=0))
        
        pts_4[:,:,r,s] = pts_2[:,:]








# Triangulation
# --------------

# Transform points into correct format for triangulation
# ----------------------------------------------------
points  = []
key = []
# key[p] = [i,r,s]. So the pth entry of the adjacency matrix 
# orresponds to the (i,r,s) node. 
# This provides a mapping between teh graph and the indexing for cond.

for r in range(num_refs):
    for s in range(num_refs):
        for i in range(num_nodes):
            points.append([pts_4[i,0,r,s],pts_4[i,1,r,s]])
            key.append(np.array([i,r,s]))

# Triangulation requires array
points = np.array(points)
# points[p,m] = mth component of pth point


# Carry out Delauney triangulation 
# ------------------------------
tri = Delaunay(points=points)






# Get adjacency matrix of all nine cells
# --------------------------------------
simplices = tri.simplices
# NB: Simplices are sets of three points 
# thta make triangles.


# 1. Get closed cycle from simplex
# NB This is set of four points 
# to close the triangle. 
# Makes getting edges easily.
loops = []

for simplex in simplices: 
    path = list(simplex)
    path.append(path[0])
    loops.append(path)




# 2. Get list of all edge tuples
edges = []

for loop in loops:
    # Add the two edges contained in the triangular loop
    # NB there are always  two becuase it's a triangle
    edge_1 = [loop[0],loop[1]]
    edge_2 = [loop[2], loop[3]]

    edges.append(edge_1)
    edges.append(edge_2)

    # Add the corresponding edges since we'll need a symmetric adj matrix
    edge_1_reversed = [loop[1],loop[0]]
    edge_2_reversed = [loop[3], loop[2]]

    edges.append(edge_1_reversed)
    edges.append(edge_2_reversed)



# 3. Get adj from list of edges 
num_pts = num_nodes*9
A = np.zeros(shape=(num_pts,num_pts))   

for edge in edges:
    pi = edge[0]
    pj = edge[1]

    A[pi,pj] = 1


# Put actual weights into this adjacency matrix 
# -----------------------------------

# Get weights between points
dist_2 = np.zeros_like(A)
weig_2 = np.zeros_like(A)
# weigh_2[pi,pj] = weight between point pi and pj
for i in range(num_pts):
    pi = np.array(points[i,:]) 
    for j in range(num_pts):
        pj = np.array(points[j,:])

        dist_2[i,j] = np.linalg.norm(pi-pj)
        weig_2[i,j] = (1/1.72461)*(1/np.sqrt(num_nodes))*dist_2[i,j]



# Get weighted adjacency matrix
A = A*weig_2
        


# Get the cond from this adjacency matrix
# --------------------------------
for i in range(num_nodes):
    for j in range(num_nodes):
        for r in range(num_refs):
            for s in range(num_refs):
                
                # Get p corresponding to j,r,s
                for p in range(num_pts):
                    if np.array_equal(a1=key[p], a2=np.array([j,r,s])):

                        # Fill edge (i,j,r,s) where i is in reference cell
                        cond_init_4[i,j,r,s] = A[i,p]


# Check that cond components are equal to adj components
# ------------------------------------------
a = cond_init_4[:,:,2,2]
b = A[0:4,32:36]

#print(a-b)
#
#
##
##nx.draw(G, with_labels=True, node_size=500, node_color='lightgreen')
##
##plt.show()
#
#
# Plot the graph arising from Delauney triangulation.
#plt.triplot(points[:,0], points[:,1], tri.simplices)
##
#plt.plot(points[:,0], points[:,1], 'o')
#
#for p in range(len(points[:,0])):
#    array = key[p]
#    i = array[0]
#    r = array[1]
#    s = array[2]
#
#    plt.annotate(r"{}".format(i), (points[p,0], points[p,1]))
#
#plt.show()
##
### Check that this graph agrees with cond tensor
### allocate the points lists to the points that are still there, and 
### then use these as coordinates in G and plot G using networkx