import numpy


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
        Number of nodes in the cell.
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
    
    
    if num_nodes == 1:

        edge_hori = numpy.random.lognormal(mean=mean, sigma=sd, size=None)
        edge_vert = numpy.random.lognormal(mean=mean, sigma=sd, size=None)
        # Grid of one node
        # ----------------
        cond_init_4[0,0,+1,0] = edge_hori
        cond_init_4[0,0,-1,0] = edge_hori

        cond_init_4[0,0,0,+1] = edge_vert
        cond_init_4[0,0,0,-1] = edge_vert
    
    elif num_nodes == 4: 
        pass
    
    return cond_init_4