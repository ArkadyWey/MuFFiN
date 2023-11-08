
import numpy as numpy
from scipy import spatial
import os

# Parameters 
# -----
initialisation = "6-ireg"
type_alpha = "mean"
mu = 0.5
sigma=0.3

path_results = os.path.join(".","results/results_cell_{}".format(initialisation))

if not os.path.exists(os.path.join(".",path_results)):
    os.mkdir(path_results)

num_nodes = 2
num_refs  = 3
num_dims  = 2

# Get unit cell points
pts_x_0 = numpy.random.uniform(low=0.0, high=1.0, size=num_nodes) #numpy.array([0.5]) #numpy.array([0.05,0.15,0.25,0.35,0.45,0.55,0.65,0.75,0.85,0.95])
pts_y_0 = numpy.random.uniform(low=0.0, high=1.0, size=num_nodes) #numpy.array([0.5]) #numpy.array([0.05,0.15,0.25,0.35,0.45,0.55,0.65,0.75,0.85,0.95])

# Right and up components
pts_x_1 = 1.0*numpy.ones_like(pts_x_0) + pts_x_0 
pts_y_1 = 1.0*numpy.ones_like(pts_y_0) + pts_y_0

## Left and down components
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
pts_to_tri_2 = []
key = []
# pts_to_tri_2[p,m] = mth component of point p
# key[p] = [i,r,s] corresponding to point p
for r in range(num_refs):
    for s in range(num_refs):
        for i in range(num_nodes):
            i_x = pts_4[i,0,r,s] # x component of point corresponding to node i in cell r,s
            i_y = pts_4[i,1,r,s] # y component of point corresponding to node i in cell r,s

            pts_to_tri_2.append([i_x,i_y]) 
            key.append([i,r,s])
   
pts_to_tri_2 = numpy.array(pts_to_tri_2)

tri = spatial.Delaunay(points=pts_to_tri_2)
simplices = tri.simplices


# Save arrays for triangulation plot
# -------------------------------
# Send results to arrays for storage
key = numpy.array(key)

numpy.save(file=os.path.join(path_results,"pts_to_tri_2.npy"), arr=pts_to_tri_2, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_results,"simplices.npy"), arr=simplices, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_results,"key.npy"), arr=key, allow_pickle=True, fix_imports=True)


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




# Get conductance tensor by removing un-needed edges and adding conductance
# --------------------------------------------------------------------------
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
        cond_init_4[i_i,i_j,r_j,s_j]   = (1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_i,r_i,s_i,i_j,r_j,s_j])
        cond_init_4[i_j,i_i,-r_j,-s_j] = (1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_i,r_i,s_i,i_j,r_j,s_j]) 
    elif (r_j == 0 and s_j == 0):
        # j is in unit cell
        cond_init_4[i_j,i_i,r_i,s_i] =   (1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_j,r_j,s_j,i_i,r_i,s_i])
        cond_init_4[i_i,i_j,-r_i,-s_i] = (1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_j,r_j,s_j,i_i,r_i,s_i])
    else: 
        # neither i or j in unit cell so this edge is not in conductance
        pass



import cells
import muffin.configure.configure as configure
num_nodes = 4
sigma     = 0.3
initialisation = "6-ireg"
conf = configure.Configure(num_nodes=num_nodes,
                           initialisation=initialisation,
                           sigma=sigma, type_alpha=type_alpha) 
cell = cells.Cell_2D_six_ireg(num_nodes=conf.num_nodes,
                              num_refs=conf.num_refs, 
                              num_dims=2,
                              mean=conf.mean,
                              leng_1=conf.leng_1, 
                              mu=mu, 
                              sigma=sigma
                              )

cond_init_4 = cell.cond_init_4
pts_4       = cell.pts_4
pts_to_tri_2 = cell.pts_to_tri_2
simplices = cell.simplices
key = cell.key

# Save arrays for triangulation plot
# -------------------------------
# Send results to arrays for storage
key = numpy.array(key)

numpy.save(file=os.path.join(path_results,"pts_to_tri_2.npy"), arr=pts_to_tri_2, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_results,"simplices.npy"), arr=simplices, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_results,"key.npy"), arr=key, allow_pickle=True, fix_imports=True)

# Save arrays for initial conductance plot
# -------------------------------
numpy.save(file=os.path.join(path_results,"cond_init_4.npy"), arr=cond_init_4, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_results,"pts_4.npy"), arr=pts_4, allow_pickle=True, fix_imports=True)