
from random import randrange
import numpy
from scipy.spatial import Delaunay
import numpy as np
from matplotlib.lines import Line2D  
from matplotlib import pyplot as plt
import networkx as nx
from matplotlib.patches import Rectangle

"""
This is an alternative method to calculating Delaunay that involves 
getting the adjacency matric 
in the p indexing way first, 
then extracting the condcutance tensor from that. 
Should revisit this if current method doesn't work.
Migiht also be useful to store this in cells module as a class, 
since has same structure as other cells.
"""



def get_points_tensor(pts_x_0, pts_y_0, pts_x_1, pts_y_1, pts_x_m1, pts_y_m1):
    """
    """
    num_nodes = len(pts_x_0)
    num_dims = 2
    num_refs = 3

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

    return pts_4







# Triangulation
# -------------
def get_points_in_tri_format(pts_4):
    """
    """
    num_refs = len(pts_4[0,0,:,0])
    num_nodes = len(pts_4[:,0,0,0])

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

    return points, key



def get_triangulation_edges(points):
    """
    """

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

        # Add the corresponding edges reversed since we'll need a symmetric adj matrix
        edge_1_reversed = [loop[1],loop[0]]
        edge_2_reversed = [loop[3], loop[2]]

        edges.append(edge_1_reversed)
        edges.append(edge_2_reversed)
    
    return edges, simplices



def get_adjacency_matrix(num_nodes, edges):
    """
    """
    
    # 3. Get adj from list of edges 
    num_pts = num_nodes*9
    A = np.zeros(shape=(num_pts,num_pts))   
    for edge in edges:
        pi = edge[0]
        pj = edge[1]

        A[pi,pj] = 1
    
    return A


def weight_adjacency_matrix(A, points):
    """
    """
    num_pts = len(A[:,0])

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

            if i!=j:
                dist_2[i,j] = np.linalg.norm(pi-pj)
                print(dist_2[i,j])
                weig_2[i,j] = 1.0 #(1.72461)*(1/np.sqrt(num_nodes))*(1/dist_2[i,j])



    # Get weighted adjacency matrix
    A = A*weig_2

    return A


def get_conductance_from_adjacency_matrix(num_nodes, num_refs, A, key):
    """
    """
    num_pts = len(A[:,0])


    cond_init_4 = np.zeros(shape=(num_nodes, num_nodes, num_refs, num_refs))
    # Get the cond from this adjacency matrix
    # --------------------------------
    for i in range(num_nodes):
        for j in range(num_nodes):
            for r in range(num_refs):
                for s in range(num_refs):
                    #if r!=0 and s!=0:
                    #    pass
                    #else:
                    # Get p corresponding to j,r,s
                    for p in range(num_pts):
                        if np.array_equal(a1=key[p], a2=np.array([j,r,s])):
                            # Fill edge (i,j,r,s) where i is in reference cell
                            cond_init_4[i,j,r,s] = A[i,p]
                            cond_init_4[j,i,-r,-s] = cond_init_4[i,j,r,s]
                
    return cond_init_4




def main(num_nodes, num_refs, pts_x_0, pts_y_0, pts_x_1, pts_y_1, pts_x_m1, pts_y_m1):
    """
    """
    pts_4 = get_points_tensor(pts_x_0, pts_y_0, pts_x_1, pts_y_1, pts_x_m1, pts_y_m1)

    (points, key) = get_points_in_tri_format(pts_4=pts_4)

    print(pts_4.shape)
    print(points.shape)
    edges, simplices = get_triangulation_edges(points=points)
    print(simplices)

    A = get_adjacency_matrix(num_nodes=num_nodes, edges=edges)

    A = weight_adjacency_matrix(A=A, points=points)

    cond_init_4 = get_conductance_from_adjacency_matrix(num_nodes=num_nodes, 
                                                        num_refs=num_refs, 
                                                        A=A, 
                                                        key=key)

    return cond_init_4, points, A, key, simplices, pts_4



if __name__ == "__main__":


    num_nodes = 1
    num_refs = 3


    # Get positions of all points 
    # ----------------------------

    # Central components
    #pts_x_0 = np.array([0.85983879])
    #pts_y_0 = np.array([0.65102802])
    #pts_x_0 = np.array([0.2,0.8,0.2,0.8])
    #pts_y_0 = np.array([0.2,0.2,0.8,0.8])    
    pts_x_0 = np.random.uniform(low=0.0, high=1.0, size=num_nodes)
    pts_y_0 = np.random.uniform(low=0.0, high=1.0, size=num_nodes)

    print("pts_x_0:\n{}".format(pts_x_0))
    print("pts_y_0:\n{}".format(pts_y_0))

    # Right or up components
    pts_x_1 = 1.0*np.ones_like(pts_x_0) + pts_x_0 
    pts_y_1 = 1.0*np.ones_like(pts_y_0) + pts_y_0

    # Left or down components
    #pts_x_m1 = -1.0*np.array([el for el in reversed(list(pts_x_0))])
    pts_x_m1 = -1.0*np.ones_like(pts_x_0) + pts_x_0
    pts_y_m1 = -1.0*np.ones_like(pts_y_0) + pts_y_0


    cond_init_4, points, A, key, simplices, pts_4= main(num_nodes=num_nodes, 
                       num_refs=num_refs, 
                       pts_x_0=pts_x_0, 
                       pts_y_0=pts_y_0, 
                       pts_x_1=pts_x_1, 
                       pts_y_1=pts_y_1, 
                       pts_x_m1=pts_x_m1, 
                       pts_y_m1=pts_y_m1)

    num_pts = len(A[:,0])


## Check that cond components are equal to adj components
## ------------------------------------------
#a = cond_init_4[:,:,2,2]
#b = A[0:4,32:36]
##print(a)
##print(b)
#for i in range(num_nodes):
#    for j in range(num_nodes):
#        for r in range(num_refs):
#            for s in range(num_refs):
#                if r ==0:
#                    mr = 0
#                elif r == 1:
#                    mr = 2
#                elif r == 2:
#                    mr = 1
#
#                if s == 0:
#                    ms = 0
#                elif s == 1:
#                    ms = 2
#                elif s == 2:
#                    ms = 1
#                                
#                if np.array_equal(cond_init_4[i,j,r,s],cond_init_4[j,i,mr,ms]):
#                    pass 
#                else: 
#                    print("i={},j={},r={},s={}".format(i,j,r,s))
                

#
#
##
##nx.draw(G, with_labels=True, node_size=500, node_color='lightgreen')
##
##plt.show()
#
#
# Plot the graph arising from Delauney triangulation.
fig, ax = plt.subplots(1,1)
ax.triplot(points[:,0], points[:,1], simplices)
#
ax.plot(points[:,0], points[:,1], 'o')

for p in range(len(points[:,0])):
    array = key[p]
    i = array[0]
    r = array[1]
    s = array[2]

    ax.annotate(r"{}".format(i), (points[p,0], points[p,1]))

from matplotlib.patches import Rectangle
for x in [-1,0,1]:
    for y in [-1,0,1]:
        if x==0 and y==0:
            ax.add_patch(Rectangle(xy=(x, y), width=1, height=1, alpha=0.2, color="tab:red"))
        else:
            ax.add_patch(Rectangle(xy=(x, y), width=1, height=1, alpha=0.8, color="tab:red", edgecolor="tab:red", fill=False, linestyle="--"))


plt.show()

fig, ax = plt.subplots(1,1)
for p in range(num_pts):
    array = key[p]
    i = array[0]
    r = array[1]
    s = array[2]
    ax.annotate(r"{}".format(i), (points[p,0], points[p,1]), color="black")
    ax.plot(points[p,0], points[p,1], 'o', color="tab:green")

for x in [-1,0,1]:
    for y in [-1,0,1]:
        if x==0 and y==0:
            ax.add_patch(Rectangle(xy=(x, y), width=1, height=1, alpha=0.2, color="tab:red"))
        else:
            ax.add_patch(Rectangle(xy=(x, y), width=1, height=1, alpha=0.8, color="tab:red", edgecolor="tab:red", fill=False, linestyle="--"))

for pi in range(4):
    for pj in range(num_pts):
        if A[pi,pj] !=0:
            x_vals_of_points = [points[pi,0],points[pj,0]]
            y_vals_of_points = [points[pi,1],points[pj,1]]
            ax.add_line(Line2D(xdata=x_vals_of_points,ydata=y_vals_of_points))


plt.show()


fig, ax = plt.subplots(1,1)
for i in range(num_nodes):
    for r in range(num_refs):
        for s in range(num_refs):
            ax.annotate(r"{}".format(i), (pts_4[i,0,r,s], pts_4[i,1,r,s]), color="black")
            ax.plot(pts_4[i,0,r,s], pts_4[i,1,r,s], 'o', color="tab:green")
for x in [-1,0,1]:
    for y in [-1,0,1]:
        if x==0 and y==0:
            ax.add_patch(Rectangle(xy=(x, y), width=1, height=1, alpha=0.2, color="tab:red"))
        else:
            ax.add_patch(Rectangle(xy=(x, y), width=1, height=1, alpha=0.8, color="tab:red", edgecolor="tab:red", fill=False, linestyle="--"))

for i in range(num_nodes):
    for j in range(num_nodes):
        for r in range(num_refs):
            for s in range(num_refs):
                if cond_init_4[i,j,r,s] !=0:
                    x_vals_of_points = [pts_4[i,0,0,0], pts_4[j,0,r,s]]
                    y_vals_of_points = [pts_4[i,1,0,0], pts_4[j,1,r,s]]
                    ax.add_line(Line2D(xdata=x_vals_of_points,ydata=y_vals_of_points))
plt.show()
####  ##
####  ### Check that this graph agrees with cond tensor
####  ### allocate the points lists to the points that are still there, and 
####  ### then use these as coordinates in G and plot G using networkx