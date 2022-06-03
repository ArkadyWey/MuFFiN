import numpy
import networkx

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


    return cond_init_4