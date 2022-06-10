import numpy
import networkx
from scipy import spatial

def grid_prescribed(num_nodes: int, num_refs: int):
    """
    - num_nodes: int
        Number of nodes in the cell.
    num_refs: int
        Number of lengths in the reference set. 
        For example, if reference set is {-1,0,+1} then num_refs==3.
    """
    
    # Define parameters 
    # -----
    cond_init_4 = numpy.zeros(shape=(num_nodes, num_nodes, num_refs, num_refs))
    
    if num_nodes == 1:

        # Grid of one node
        # ----------------
        cond_init_4[0,0,1,0] = 1.0 #1.72461
        cond_init_4[0,0,-1,0] = 1.0 #1.72461

        cond_init_4[0,0,0,1] = 1.0 #1.72461
        cond_init_4[0,0,0,-1] = 1.0 #1.72461


    elif num_nodes == 4:
        
        # Grid of four nodes
        #--------------------
        #           2         3 
        #           |         |
        #         (1.0)     (1.0)
        #           |         |
        # 1--(1.0)--0--(0.8)--1--(1.0)--0
        #           |         |
        #         (0.6)     (0.2)
        #           |         |
        # 3--(1.0)--2--(0.4)--3--(1.0)--2
        #           |         |
        #         (1.0)     (1.0)
        #           |         |
        #           0         1

        # Internal edges
        cond_init_4[0,1,0,0] = 0.8 #1.0
        cond_init_4[1,0,0,0] = 0.8 #1.0

        cond_init_4[1,3,0,0] = 0.2 #1.0
        cond_init_4[3,1,0,0] = 0.2 #1.0

        cond_init_4[2,3,0,0] = 0.4 #1.0
        cond_init_4[3,2,0,0] = 0.4 #1.0

        cond_init_4[0,2,0,0] = 0.6 #1.0
        cond_init_4[2,0,0,0] = 0.6 #1.0

        ## External edges
        cond_init_4[1,0,1,0] = 1.0 #1.0
        cond_init_4[0,1,-1,0] = 1.0 #1.0

        cond_init_4[3,2,1,0] = 1.0 #1.0
        cond_init_4[2,3,-1,0] = 1.0 #1.0
        #
        #cond_init_4[0,2,0,1]  = 1.0
        #cond_init_4[2,0,0,-1] = 1.0
        #
        #cond_init_4[1,3,0,1] = 1.0
        #cond_init_4[3,1,0,-1] = 1.0


    return cond_init_4



def grid_log_normal(num_nodes: int, num_refs: int, mean: float, sd: float):
    """
    - num_nodes: int
        Number of nodes in the cell. Must be square number.
    num_refs: int
        Number of lengths in the reference set. 
        For example, if reference set is {-1,0,+1} then num_refs==3.
    - mean: float 
        Mean of underlying normal distribution.
        Must be non-negative. 
    - sd: float: 
        Standard deviation of underlying distribution.
    """
    
    # Define parameters 
    # -----
    cond_init_4 = numpy.zeros(shape=(num_nodes, num_nodes, num_refs, num_refs))
    num_unique_edges = int(2*num_nodes)
    samples = numpy.random.lognormal(mean=mean, sigma=sd, size=num_unique_edges)
    num_nodes_row = int(numpy.sqrt(num_nodes))

    # Internal edges
    # ------
    # Make grid graph for internal edges
    G = networkx.grid_graph(dim=[num_nodes_row,num_nodes_row],periodic=False)


    # Add random sample to graph edges as weight
    # -----
    num_internal_edges = 2*num_nodes_row*(num_nodes_row-1)
    samples_internal = samples[0:num_internal_edges]
    k = 0
    for i,j in G.edges():
        G[i][j]['weight'] = samples_internal[k]
        k=k+1


    # Get the adjacency matrix of internal graph
    # ------
    A = networkx.adjacency_matrix(G)


    # Send adjacency matrix of internal graph to conductance tensor
    # -----
    cond_init_4[:,:,0,0] = A.toarray()


    # External edges
    # --------------
    # Define node indexes
    # -----
    nodes = numpy.linspace(0,num_nodes_row**2-1,num_nodes_row**2)

    # Get nodes on outside of internal graph
    # ------
    left_nodes = nodes[0::num_nodes_row]
    right_nodes = nodes[num_nodes_row-1::num_nodes_row]
    top_nodes = nodes[0:num_nodes_row]
    bottom_nodes = nodes[num_nodes-num_nodes_row::]

    # Get external horizontal and vertical edge samples from main set of samples
    # ------
    samples_external_hori = samples[2*num_nodes_row*(num_nodes_row-1):2*num_nodes_row*(num_nodes_row-1)+num_nodes_row]
    samples_external_vert = samples[2*num_nodes_row*(num_nodes_row-1)+num_nodes_row::]

    # Fill external edges with samples
    # -----
    for i in range(num_nodes_row):
        # Get index of node
        left_node =   int(left_nodes[i])
        right_node =  int(right_nodes[i])
        top_node =    int(top_nodes[i])
        bottom_node = int(bottom_nodes[i])

        # Fill horizotal and vertical edges    
        cond_init_4[left_node,right_node,-1,0] = samples_external_hori[i]
        cond_init_4[right_node,left_node,+1,0] = samples_external_hori[i]
        cond_init_4[bottom_node,top_node,0,-1] = samples_external_vert[i]
        cond_init_4[top_node,bottom_node,0,+1] = samples_external_vert[i]


        # Divide all conductances by sqrt(N) to make fair test
        cond_init_4 = cond_init_4/numpy.sqrt(num_nodes)

    return cond_init_4



def random_structure_uniform(num_nodes: int, num_refs: int):
    """
    - Get specified number of (x,y) points within a unit cell. 
    - Calculate simplices of delauney triangulation. 
    - Use simplices to get a graph. 
    - Use simplices to calculate distances between connected points.
    - Use distances between points to get their conductance. 
    - Add conductances to graph as weights.
    """
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



    # Get conductance tensor 
    # ---------------------
    cond_init_4 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_refs))
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


    return cond_init_4

#    # Define parameters:
#    num_dims = 2
#
#    cond_init_4 = numpy.zeros(shape=(num_nodes, num_nodes, num_refs, num_refs))
#
#
#
#    # Get positions of all points 
#    # ----------------------------
#
#    # Central components
#    #pts_x_0 = numpy.array([0.85983879])
#    #pts_y_0 = numpy.array([0.65102802])
#    #pts_x_0 = numpy.array([0.5])#numpy.array([0.2,0.8,0.2,0.8])
#    #pts_y_0 = numpy.array([0.5])#numpy.array([0.2,0.2,0.8,0.8])    
#    pts_x_0 = numpy.random.uniform(low=0.0, high=1.0, size=num_nodes)
#    pts_y_0 = numpy.random.uniform(low=0.0, high=1.0, size=num_nodes)
#
#    # Right or up components
#    pts_x_1 = 1.0*numpy.ones_like(pts_x_0) + pts_x_0 
#    pts_y_1 = 1.0*numpy.ones_like(pts_y_0) + pts_y_0
#
#    # Left or down components
#    #pts_x_m1 = -1.0*numpy.array([el for el in reversed(list(pts_x_0))])
#    pts_x_m1 = -1.0*numpy.ones_like(pts_x_0) + pts_x_0
#    pts_y_m1 = -1.0*numpy.ones_like(pts_y_0) + pts_y_0
#
#    # Fill the positions tensor
#    pts_4 = numpy.zeros(shape = (num_nodes, num_dims, num_refs, num_refs) )
#    #pts_4[i,m,r,s] = num_dims[m] component of position of node nodes[i] in cell with reference (r,s)
#
#    for r in range(num_refs):
#        for s in range(num_refs):
#            if r == 0: 
#                pts_x = pts_x_0
#            elif r == 1: 
#                pts_x = pts_x_1
#            elif r == 2: 
#                pts_x = pts_x_m1
#
#            if s == 0: 
#                pts_y = pts_y_0
#            elif s == 1: 
#                pts_y = pts_y_1
#            elif s == 2: 
#                pts_y = pts_y_m1
#
#            pts_2 = numpy.transpose(numpy.concatenate(([pts_x],[pts_y]), axis=0))
#
#            pts_4[:,:,r,s] = pts_2[:,:]
#
#
#
#
#
#
#
#
#    # Triangulation
#    # --------------
#
#    # Transform points into correct format for triangulation
#    # ----------------------------------------------------
#    points  = []
#    key = []
#    # key[p] = [i,r,s]. So the pth entry of the adjacency matrix 
#    # orresponds to the (i,r,s) node. 
#    # This provides a mapping between teh graph and the indexing for cond.
#
#    for r in range(num_refs):
#        for s in range(num_refs):
#            for i in range(num_nodes):
#                points.append([pts_4[i,0,r,s],pts_4[i,1,r,s]])
#                key.append(numpy.array([i,r,s]))
#
#    # Triangulation requires array
#    points = numpy.array(points)
#    # points[p,m] = mth component of pth point
#
#
#    # Carry out Delauney triangulation 
#    # ------------------------------
#    tri = spatial.Delaunay(points=points)
#    #from pyhull.delaunay import DelaunayTri
#    #tri = DelaunayTri(points=points)
#    #print(tri.simplices)
#
#
#
#
#
#    # Get adjacency matrix of all nine cells
#    # --------------------------------------
#    simplices = tri.simplices
#    # NB: Simplices are sets of three points 
#    # thta make triangles.
#
#
#    # 1. Get closed cycle from simplex
#    # NB This is set of four points 
#    # to close the triangle. 
#    # Makes getting edges easily.
#    loops = []
#
#    for simplex in simplices: 
#        path = list(simplex)
#        path.append(path[0])
#        loops.append(path)
#
#
#
#
#    # 2. Get list of all edge tuples
#    edges = []
#
#    for loop in loops:
#        # Add the two edges contained in the triangular loop
#        # NB there are always  two becuase it's a triangle
#        edge_1 = [loop[0],loop[1]]
#        edge_2 = [loop[2], loop[3]]
#
#        edges.append(edge_1)
#        edges.append(edge_2)
#
#        # Add the corresponding edges since we'll need a symmetric adj matrix
#        edge_1_reversed = [loop[1],loop[0]]
#        edge_2_reversed = [loop[3], loop[2]]
#
#        edges.append(edge_1_reversed)
#        edges.append(edge_2_reversed)
#
#
#
#    # 3. Get adj from list of edges 
#    num_pts = num_nodes*9
#    A = numpy.zeros(shape=(num_pts,num_pts))   
#
#    for edge in edges:
#        pi = edge[0]
#        pj = edge[1]
#
#        A[pi,pj] = 1
#
#
#    # Put actual weights into this adjacency matrix 
#    # -----------------------------------
#
#    # Get weights between points
#    dist_2 = numpy.zeros_like(A)
#    weig_2 = numpy.zeros_like(A)
#    # weigh_2[pi,pj] = weight between point pi and pj
#    for i in range(num_pts):
#        pi = numpy.array(points[i,:]) 
#        for j in range(num_pts):
#            pj = numpy.array(points[j,:])
#
#            if i!=j:
#                dist_2[i,j] = numpy.linalg.norm(pi-pj)
#                weig_2[i,j] = (1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_2[i,j])
#
#
#
#    # Get weighted adjacency matrix
#    A = A*weig_2
#
#
#
#    # Get the cond from this adjacency matrix
#    # --------------------------------
#    for i in range(num_nodes):
#        for j in range(num_nodes):
#            for r in range(num_refs):
#                for s in range(num_refs):
#                    if r ==0:
#                        mr = 0
#                    elif r == 1:
#                        mr = 2
#                    elif r == 2:
#                        mr = 1
#
#                    if s == 0:
#                        ms = 0
#                    elif s == 1:
#                        ms = 2
#                    elif s == 2:
#                        ms = 1
#                    
#                    #if r!=0 and s!=0:
#                    #    pass
#                    #else:
#                    #    # Get p corresponding to j,r,s
#                    for p in range(num_pts):
#                        if numpy.array_equal(a1=key[p], a2=numpy.array([j,r,s])):
#                            # Fill edge (i,j,r,s) where i is in reference cell
#                            cond_init_4[i,j,r,s] = A[i,p]
#                            cond_init_4[j,i,mr,ms] = cond_init_4[i,j,r,s]
#
#
#
#    return cond_init_4