
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
pts_x_m1 = -1.0*pts_x_0
pts_y_m1 = -1.0*pts_y_0

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

#print(tri.simplices)

plt.triplot(points[:,0], points[:,1], tri.simplices)
#
plt.plot(points[:,0], points[:,1], 'o')

for p in range(len(points[:,0])):
    plt.annotate("num", (points[p,0], points[p,1]))

plt.show()


# Get graph 
# --------
simplices = tri.simplices
# Simplices are unclosed paths that make up triangles. 
# I.e. They are sets of three points.

# Make path graph that for some reason has wrong adj
# but right edges
S = nx.Graph()
for path in simplices:
    # Close path to make triangle in networkx sense, 
    # by adding first point of path as last point.
    path = list(path)
    path.append(path[0])
    
    # Add this closed path (aka triangle) to graph
    nx.add_path(S, path)


# Get correct edges from S
nodes = range(num_nodes)
edges = S.edges

# Make graph G.
# G is triangulated grpah over nodes indexed by points over 
# 9 cells.
G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# Get adjacency matrix of G 
# This is indexed by points
A = nx.adjacency_matrix(G).toarray()

print(A)


# Now put actual weights into this adjacency matrix 
# -----------------------------------


# Now get the cond from this adjacency matrix
# --------------------------------
for i in range(num_nodes):
    for j in range(num_nodes):
        for r in range(num_refs): 
            for s in range(num_refs):
                
                # Get point indices corresponding to (i,r,s) and (j,r,s)
                for p in range(len(key)):

                    if np.array_equal(a1=key[p], a2=np.array([i,r,s])):
                        pi = p
                    else: 
                        pass

                    if np.array_equal(a1=key[p], a2=np.array([j,r,s])):
                        pj = p
                    else: 
                        pass

                # Fill corresponding element of conductance        
                cond_init_4[i,j,r,s] = A[pi,pj]



#
#nx.draw(G, with_labels=True, node_size=500, node_color='lightgreen')
#
#plt.show()


# Plot the graph arising from Delauney triangulation.
plt.triplot(points[:,0], points[:,1], tri.simplices)
#
plt.plot(points[:,0], points[:,1], 'o')

for p in range(len(points[:,0])):
    array = key[p]
    i = array[0]
    r = array[1]
    s = array[2]

    plt.annotate(r"{}".format(i), (points[p,0], points[p,1]))

plt.show()

# Check that this graph agrees with cond tensor