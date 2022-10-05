import numpy

import cells 

def four_reg_prescribed(num_nodes: int, num_refs: int):
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
        cond_init_4[0,0,1,0]  = 0.1#1.0 #1.72461
        cond_init_4[0,0,-1,0] = 0.1#1.0 #1.72461

        cond_init_4[0,0,0,1]  = 0.1#1.0 #1.72461
        cond_init_4[0,0,0,-1] = 0.1#1.0 #1.72461


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
        cond_init_4[0,1,0,0] = 0.99#0.1#1.2#1.72461##0.8 #1.0
        cond_init_4[1,0,0,0] = 0.99#0.1#1.2#1.72461##0.8 #1.0

        cond_init_4[1,3,0,0] = 1.0#0.2#1.2#1.72461#1.0#0.2 #1.0
        cond_init_4[3,1,0,0] = 1.0#0.2#1.2#1.72461#1.0#0.2 #1.0

        cond_init_4[2,3,0,0] = 1.0#0.3#1.2#1.72461#1.0#0.4 #1.0
        cond_init_4[3,2,0,0] = 1.0#0.3#1.2#1.72461#1.0#0.4 #1.0

        cond_init_4[0,2,0,0] = 1.0#0.4#1.2#1.72461#1.0#0.6 #1.0
        cond_init_4[2,0,0,0] = 1.0#0.4#1.2#1.72461#1.0#0.6 #1.0

        ## External edges
        cond_init_4[1,0,1,0]  = 1.0#0.5#1.2#1.72461#1.0#1.0 #1.0
        cond_init_4[0,1,-1,0] = 1.0#0.5#1.2#1.72461#1.0#1.0 #1.0

        cond_init_4[3,2,1,0]  = 1.0#0.6#1.2#1.72461#1.0#1.0 #1.0
        cond_init_4[2,3,-1,0] = 1.0#0.6#1.2#1.72461#1.0#1.0 #1.0
        
        cond_init_4[0,2,0,1]  = 1.0#0.7#1.2#1.72461#1.0
        cond_init_4[2,0,0,-1] = 1.0#0.7#1.2#1.72461#1.0
        
        cond_init_4[1,3,0,1]  = 1.0#0.8#1.2#1.72461#1.0
        cond_init_4[3,1,0,-1] = 1.0#0.8#1.2#1.72461#1.0


    elif num_nodes == 9:
        # Internal edges
        cond_init_4[0,1,0,0] = 1.0#0.8 #1.0
        cond_init_4[1,0,0,0] = 1.0#0.8 #1.0

        cond_init_4[1,2,0,0] = 1.0#0.8 #1.0
        cond_init_4[2,1,0,0] = 1.0#0.8 #1.0

        cond_init_4[3,4,0,0] = 1.0#0.8 #1.0
        cond_init_4[4,3,0,0] = 1.0#0.8 #1.0

        cond_init_4[4,5,0,0] = 1.0#0.8 #1.0
        cond_init_4[5,4,0,0] = 1.0#0.8 #1.0
        
        cond_init_4[6,7,0,0] = 1.0#0.8 #1.0
        cond_init_4[7,6,0,0] = 1.0#0.8 #1.0

        cond_init_4[7,8,0,0] = 1.0#0.8 #1.0
        cond_init_4[8,7,0,0] = 1.0#0.8 #1.0

        cond_init_4[0,3,0,0] = 1.0#0.8 #1.0
        cond_init_4[3,0,0,0] = 1.0#0.8 #1.0
        
        cond_init_4[1,4,0,0] = 1.0#0.8 #1.0
        cond_init_4[4,1,0,0] = 1.0#0.8 #1.0
        
        cond_init_4[2,5,0,0] = 1.0#0.8 #1.0
        cond_init_4[5,2,0,0] = 1.0#0.8 #1.0

        cond_init_4[3,6,0,0] = 1.0#0.8 #1.0
        cond_init_4[6,3,0,0] = 1.0#0.8 #1.0

        cond_init_4[4,7,0,0] = 1.0#0.8 #1.0
        cond_init_4[7,4,0,0] = 1.0#0.8 #1.0

        cond_init_4[5,8,0,0] = 1.0#0.8 #1.0
        cond_init_4[8,5,0,0] = 1.0#0.8 #1.0

        ## External edges
        cond_init_4[2,0,1,0]  = 1.0#1.0 #1.0
        cond_init_4[0,2,-1,0] = 1.0#1.0 #1.0

        cond_init_4[5,3,1,0]  = 1.0#1.0 #1.0
        cond_init_4[3,5,-1,0] = 1.0#1.0 #1.0

        cond_init_4[8,6,1,0]  = 1.0#1.0 #1.0
        cond_init_4[6,8,-1,0] = 1.0#1.0 #1.0

        cond_init_4[0,6,0,1]  = 1.0#1.0 #1.0
        cond_init_4[6,0,0,-1] = 1.0#1.0 #1.0

        cond_init_4[1,7,0,1]  = 1.0#1.0 #1.0
        cond_init_4[7,1,0,-1] = 1.0#1.0 #1.0

        cond_init_4[2,8,0,1]  = 1.0#1.0 #1.0
        cond_init_4[8,2,0,-1] = 1.0#1.0 #1.0

    return cond_init_4



def four_reg(num_nodes: int, num_refs: int, mu: float, sigma: float):
    """
    - num_nodes: int
        Number of nodes in the cell. Must be square number.
    num_refs: int
        Number of lengths in the reference set. 
        For example, if reference set is {-1,0,+1} then num_refs==3.
    - mu: float 
        Mean of underlying normal distribution.
        Must be non-negative. 
    - sigma: float: 
        Standard deviation of underlying distribution.
    """
    
    # Define parameters 
    # -----
    cond_init_4 = numpy.zeros(shape=(num_nodes, num_nodes, num_refs, num_refs))
    num_unique_edges = int(2*num_nodes)
    samples = numpy.random.lognormal(mean=mu, sigma=sigma, size=num_unique_edges) #/numpy.sqrt(num_nodes)
    num_nodes_row = int(numpy.sqrt(num_nodes))
    # numpy.random.choice(a=numpy.array([4,8]), size=num_unique_edges)#

    # Internal edges
    # ------
    ## Make grid graph for internal edges
    #G = networkx.grid_graph(dim=[num_nodes_row,num_nodes_row],periodic=False)
    #networkx.convert_node_labels_to_integers(G)
#
    ## Add random sample to graph edges as weight
    ## -----
    num_internal_edges = 2*num_nodes_row*(num_nodes_row-1)
    samples_internal = samples[0:num_internal_edges]
    #k = 0
    #print(G.edges())
    #for i,j in G.edges():
    #    G[i][j]['weight'] = samples_internal[k]
    #    k=k+1
#
#
    ## Get the adjacency matrix of internal graph
    ## ------
    #A = networkx.adjacency_matrix(G)

    # Get cell class 
    cell = cells.Cell_2D_four_reg(num_rows_cell=num_nodes_row, 
                                  num_cols_cell=num_nodes_row)

    # Get adjacency matrix with ones 
    adj_2 = cell.adj_intra_2
    

    # Fill adjacency matrix with samples 
    k = 0 #  index of element we'll take from sample
    for i in range(num_nodes):
        for j in range(num_nodes):
            if j>=i: # fill upper triangle then reflect
                if adj_2[i,j] == 1.0:
                    adj_2[i,j] = samples_internal[k]
                    adj_2[j,i] = adj_2[i,j]
                    k = k+1 # increase k so don't take same twice
                    #print(k)

    # Send adjacency matrix of internal graph to conductance tensor
    # -----
    #cond_init_4[:,:,0,0] = A.toarray()
    cond_init_4[:,:,0,0] = adj_2[:,:]

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
    #samples_external_hori = numpy.ones_like(samples_external_hori)
    #samples_external_vert = numpy.ones_like(samples_external_vert)

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
    #cond_init_4 = cond_init_4 #/numpy.sqrt(num_nodes)

    return cond_init_4



def six_ireg(num_nodes: int, num_refs: int, mean: float, leng_1: numpy.ndarray, mu: float, sigma: float):
    """
    - Get specified number of (x,y) points within a unit cell. 
    - Calculate simplices of delauney triangulation. 
    - Use simplices to get a graph. 
    - Use simplices to calculate distances between connected points.
    - Use distances between points to get their conductance. 
    - Add conductances to graph as weights.
    """
    num_dims  = 2

    cell = cells.Cell_2D_six_ireg(num_nodes=num_nodes,
                                  num_refs=num_refs,
                                  num_dims=num_dims,
                                  mean=mean, 
                                  leng_1=leng_1, 
                                  mu=mu,
                                  sigma=sigma)

    #cond_init_4 = cell.cond_init_4/numpy.sqrt(num_nodes)
    cond_init_4 = cell.cond_init_4
    
    return cond_init_4


def six_reg(num_nodes: int, num_refs: int, mu: float, sigma: float):
    """
    - Get specified number of (x,y) points within a unit cell. 
    - Calculate simplices of delauney triangulation. 
    - Use simplices to get a graph. 
    - Use simplices to calculate distances between connected points.
    - Use distances between points to get their conductance. 
    - Add conductances to graph as weights.
    """
    num_dims  = 2

    cell = cells.Cell_2D_six_reg(num_nodes=num_nodes,
                                 num_refs=num_refs,
                                 num_dims=num_dims, 
                                 mu=mu, 
                                 sigma=sigma)

    cond_init_4 = cell.cond_init_4

    return cond_init_4