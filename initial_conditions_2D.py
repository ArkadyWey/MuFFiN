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

    if num_nodes == 1:     
               
        # External edges
        # ------
        cond_init_4[0,0,+1,0] = samples[0]
        cond_init_4[0,0,-1,0] = samples[0]

        cond_init_4[0,0,0,+1] = samples[1]
        cond_init_4[0,0,0,-1] = samples[1]

        
    

    elif num_nodes == 4: 
        
        # External edges
        # ------
        
        # Horizontal 
        cond_init_4[0,1,-1,0] = samples[0]
        cond_init_4[1,0,+1,0] = samples[0]
        
        cond_init_4[2,3,-1,0] = samples[1]
        cond_init_4[3,2,+1,0] = samples[1]

        # Vertical
        cond_init_4[0,2,0,+1] = samples[2]
        cond_init_4[2,0,0,-1] = samples[2]
        
        cond_init_4[1,3,0,+1] = samples[3]
        cond_init_4[3,1,0,-1] = samples[3]


        # Internal edges
        # ------

        # Horizontal
        cond_init_4[0,1,0,0] = samples[4]
        cond_init_4[1,0,0,0] = samples[4]

        cond_init_4[2,3,0,0] = samples[5]
        cond_init_4[3,2,0,0] = samples[5]

        # Vertical 
        cond_init_4[0,2,0,0] = samples[6]
        cond_init_4[2,0,0,0] = samples[6]

        cond_init_4[1,3,0,0] = samples[7]
        cond_init_4[3,1,0,0] = samples[7]
        
        print(cond_init_4[:,:,0,0])

    return cond_init_4