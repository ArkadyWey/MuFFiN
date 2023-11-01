import numpy

import multiscale_models.network_2D as network_2D

"""
This module collects functions that map cell indexes to grid indexes
and back again, and convert tensors that are indexed by one way 
to the other way.

Cell indexing
-------------
node: (i,i_c,j_c) is node i in the cell at row=i_c and col=j_c where the 0,0 cell is in the bottom left corner.
edge: (i,j,r0,r1,i_c,j_c) is the edge from the node (i,i_c,j_c) to the node (j,i_c+r1,j_c+r0).

Grid indexing
-------------
node: ii is node ii which is an index from 0 to num_nodes*num_rows*num_cols-1.
edge: (ii,jj) is the edge from ii to jj.


Note: 
reshape_..._all_edges():... converts every edge, even those that leave the network, into a 2D matric description. 
For example, converting the initial conductance using _all_edge... and back again, would give exactly 
the same tensor... 
This isn't what we need, since we don't care about all edges in the network model, we only care about internal ones.
"""


def convert_indx_cell_to_grid_node(i,i_c,j_c,num_nodes,num_rows):
    """
    Convert the cell index of a node, which is a triple (i,i_c,j_c) 
    to a grid index, which is a single number ii.

    Parameters 
    -----
    - i: int
        Index of node within the cell.
    - i_c: int 
        Row that the cell is in. Rows are indexed from 0 upwards. Row 0 is the bottom 
        row in the grid.
    - j_c: int 
        Column that the cell is in. Colums are indexed from 0 upwards. Column 0 is on the left.
    - num_nodes: int 
        Number of nodes in each cell. 
    - num_rows: int 
        Number of rows of cells in the grid.

    Returns 
    -----
    - ii: int 
        A grid index description of the cell index (i,i_c,j_c), 
        which is a number between 0 and num_nodes*num_rows*(num_cols-1)
        (inclusive, since num_nodes*num_rows*num_cols
        is the number of nodes in the network).
    """
    ii = j_c*num_rows*num_nodes+i_c*num_nodes+i
    return ii



def convert_indx_grid_to_cell_node(ii,num_nodes,num_rows):
    """
    Given a grid index of a node, 
    return the cell index of the same node.

    Parameters 
    -----
    - ii: int 
        A grid index description of the cell index (i,i_c,j_c), 
        which is a number between 0 and num_nodes*num_rows*(num_cols-1)
        (inclusive, since num_nodes*num_rows*num_cols
        is the number of nodes in the network).
    - num_nodes: int 
        Number of  nodes in a cell. 
    - num_rows: 
        Number of rows of cells in the network.
    
    Returns
    -----
    - i: int 
        Node index, from 0 to num_nodes-1.
    - i_c: int
        The row that the cell containing i is in.
    - j_c: int 
        The column that the cell containing i is in.
    """
    i = int(ii%num_nodes)
    num_cells_passed = int(numpy.floor(ii/num_nodes))
    j_c  = int(numpy.floor(num_cells_passed/num_rows))
    i_c  = int((ii-i-num_nodes*num_rows*j_c)/num_nodes)
    return (i,i_c,j_c)



def convert_indx_cell_to_grid_edge(i,j,r0,r1,i_c,j_c,num_nodes,num_rows):
    """
    Convert the cell index of an edge, which is a six-tuple (i,j,r0,r1,i_c,j_c), 
    to the grid index of an edge, which is a pair (ii,jj).

    Parameters 
    -----
    - i: int
        Index of node within the cell.
    - r0: int
        Horizontal position of the cell that contains node j, relative to the cell that contains node i.
    - r1: int 
        Vertical position of the cell that contains the node j, relative to the cell that contains node i.
    - i_c: int 
        Row that the cell that contains node i is in. Rows are indexed from 0 upwards. Row 0 is the bottom 
        row in the grid.
    - j_c: int 
        Column that the cell that containas node i is in. Colums are indexed from 0 upwards. Column 0 is on the left.
    - num_nodes: int 
        Number of nodes in each cell. 
    - num_rows: int 
        Number of rows of cells in the grid.

    Returns 
    -----
    - ii: int 
        A grid index description of the cell index (i,i_c,j_c), 
        which is a number between 0 and num_nodes*num_rows*num_cols-1 (inclusive, since num_nodes*num_rows*num_cols
        is the number of nodes in the network).
    - jj: int 
        A grid index description of the cell index (j,i_c+r1,j_c+r0), which is the cell index of node j. 
    """
    ii = convert_indx_cell_to_grid_node(i=i,i_c=i_c,j_c=j_c,num_nodes=num_nodes,num_rows=num_rows)
    jj = convert_indx_cell_to_grid_node(i=j,i_c=i_c+r1,j_c=j_c+r0,num_nodes=num_nodes,num_rows=num_rows)
    return (ii,jj)



def convert_indx_grid_to_cell_edge(ii,jj,num_nodes,num_rows):
    """
    Given the grid indiceces ii,jj of two nodes between which there is an edge, 
    return the cell index of the same two indices.

    Parameters 
    -----
    - ii: int 
        A grid index description of the cell index (i,i_c,j_c), 
        which is a number between 0 and num_nodes*num_rows*num_cols-1 (inclusive, since num_nodes*num_rows*num_cols
        is the number of nodes in the network).
    - jj: int 
        A grid index description of the cell index (j,i_c+r1,j_c+r0), which is the cell index of node j. 
    - num_nodes: int 
        Number of nodes in each cell. 
    - num_rows: int 
        Number of rows of cells in the grid.
    
    Returns
    -----
    - i: int
        Index of node within the cell.
    - r0: int
        Horizontal position of the cell that contains node j, relative to the cell that contains node i.
    - r1: int 
        Vertical position of the cell that contains the node j, relative to the cell that contains node i.
    - i_c: int 
        Row that the cell that contains node i is in. Rows are indexed from 0 upwards. Row 0 is the bottom 
        row in the grid.
    - j_c: int 
        Column that the cell that containas node i is in. Colums are indexed from 0 upwards. Column 0 is on the left.
    """
    i,i_c,j_c = convert_indx_grid_to_cell_node(ii=ii,num_nodes=num_nodes,num_rows=num_rows)
    j,i_c_for_j,j_c_for_j = convert_indx_grid_to_cell_node(ii=jj,num_nodes=num_nodes,num_rows=num_rows)
    r0 = j_c_for_j-j_c
    r1 = i_c_for_j-i_c
    return (i,j,r0,r1,i_c,j_c) 












def reshape_6_to_2_all_edges(a_6):
    """
    Reshape an edge quantity with cell indexing into the same edge quantity with grid indexing. 
    For example, cond_6.
    This includes nodes that are outside the network (but still in the grid) because, for example, a_6 
    tells us about the connections from nodes in bottom left cell to the cell on the left (using r0=-1)...
    this cell is outside the network.

    Parameters 
    -----
    - a_6: numpy.ndarray
        A quantity defined on edges, indexed with cell indexing. 
        a_6[i,j,r0,r1,i_c,j_c] is the quantity a defined on the edge between 
        the node i in cell i_c,j_c, and the node j located in the cell at 
        r0,r1 relative to the cell containing i (i.e. node j in cell i_c+r1,j_c+r0).
    
    Returns
    -----
    - a_2: numpy.ndarray
        The same quantity defined on edges, indexed with grid indexing.
        That is, the quantity a on edge (ii,jj). 
        We understand where this edge is by converting this grid descroption back to a cell 
        description.
        This includes edges to external nodes.
    """

    # Parameters 
    num_nodes = len(a_6[:,0,0,0,0,0])
    num_refs  = len(a_6[0,0,:,0,0,0])
    num_rows  = len(a_6[0,0,0,0,:,0])
    num_cols  = len(a_6[0,0,0,0,0,:])

    refs_1 = [0,1,-1]
    rows_1 = list(numpy.arange(start=1,stop=num_rows+1,step=1,dtype=int))
    cols_1 = list(numpy.arange(start=1,stop=num_cols+1,step=1,dtype=int))

    num_nodes_grid = num_nodes*(num_rows+2)*(num_cols+2) # +2 because need to index the cells left right up and down from the grid to use r
    a_2 = numpy.zeros(shape=(num_nodes_grid,num_nodes_grid))
    for i in range(num_nodes):
        for j in range(num_nodes):
            for r0 in refs_1:
                for r1 in refs_1:
                    for i_c in rows_1: # don't consider below or above network: r will take these into account
                        for j_c in cols_1: # don't consider left of right of network. r will take these into account
                            (ii,jj) = convert_indx_cell_to_grid_edge(i=i,j=j,r0=r0,r1=r1,i_c=i_c,j_c=j_c,num_nodes=num_nodes,num_rows=num_rows+2)
                            # + 2 since then r0 and r1 mean that nodes in cells outside network get indexed
                            a_2[ii,jj] = a_6[i,j,r0,r1,i_c-1,j_c-1] 
                            # -1 since a_6 knows about the cells outside network via r not i_c,j_c

    return a_2






def reshape_2_to_6_all_edges(a_2,num_nodes,num_refs,num_rows,num_cols):
    """
    Reshape an edge quantity with grid indexing into the same edge quantity with cell indexing. 
    For example, cond_2 back to cond_6 after the problem has been solved.

    Parameters 
    -----
    - a_2: numpy.ndarray
        The same quantity defined on edges, indexed with grid indexing.
        That is, the quantity a on edge (ii,jj). 
        We understand where this edge is by converting this grid descroption back to a cell 
        description.
    - num_nodes: int
        The number of nodes in a cell. 
    - num_rows: int
        The number of rows of cells in the network (not including external cells).
    - num_cols: int 
        The number of columns of cells in the network (not including external cells).
        
  
    Returns
    -----
    - a_6: numpy.ndarray
        A quantity defined on edges, indexed with cell indexing. 
        a_6[i,j,r0,r1,i_c,j_c] is the quantity a defined on the edge between 
        the node i in cell i_c,j_c, and the node j located in the cell at 
        r0,r1 relative to the cell containing i (i.e. node j in cell i_c+r1,j_c+r0).
        This includes edges to external nodes.
    """
    refs_1 = [0,1,-1]
    rows_1 = list(numpy.arange(start=1,stop=num_rows+1,step=1,dtype=int))
    cols_1 = list(numpy.arange(start=1,stop=num_cols+1,step=1,dtype=int))

    a_6 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_refs,num_rows,num_cols))
    num_nodes_grid = num_nodes*(num_rows+2)*(num_cols+2)
    for ii in range(num_nodes_grid):
        for jj in range(num_nodes_grid):
            (i,j,r0,r1,i_c,j_c) = convert_indx_grid_to_cell_edge(ii=ii,jj=jj,num_nodes=num_nodes,num_rows=num_rows+2)
            if r0 in refs_1 and r1 in refs_1 and i_c in rows_1 and j_c in cols_1:
                # only add edges between cells that are adjacent
                a_6[i,j,r0,r1,i_c-1,j_c-1] = a_2[ii,jj] #-1 since a_6 doesn't know about external cells
            else: 
                # edge is not in network and we never considered it in a_6
                pass 
    return a_6












def reshape_6_to_2_internal_edges(a_6):
    """
    Reshape an edge quantity with cell indexing into the same edge quantity with grid indexing. 
    For example, cond_6.

    Parameters 
    -----
    - a_6: numpy.ndarray
        A quantity defined on edges, indexed with cell indexing. 
        a_6[i,j,r0,r1,i_c,j_c] is the quantity a defined on the edge between 
        the node i in cell i_c,j_c, and the node j located in the cell at 
        r0,r1 relative to the cell containing i (i.e. node j in cell i_c+r1,j_c+r0).
    
    Returns
    -----
    - a_2: numpy.ndarray
        The same quantity defined on edges, indexed with grid indexing.
        That is, the quantity a on edge (ii,jj). 
        We understand where this edge is by converting this grid descroption back to a cell 
        description.
        This does not include edges to external nodes.
    - internal_edges: list 
        internal_edges[i] = ([ii,jj],[i,j,r0,r1,i_c,j_c]). internal_edges[i][0] is the grid index of an internal 
        edge, internal_edge[i][1] is the corresponding cell index of the same internal edge.
    """

    # Parameters 
    num_nodes = len(a_6[:,0,0,0,0,0])
    num_refs  = len(a_6[0,0,:,0,0,0])
    num_rows  = len(a_6[0,0,0,0,:,0])
    num_cols  = len(a_6[0,0,0,0,0,:])

    refs_1 = [0,1,-1]
    rows_1 = list(numpy.arange(start=0,stop=num_rows,step=1,dtype=int))
    cols_1 = list(numpy.arange(start=0,stop=num_cols,step=1,dtype=int))

    num_nodes_net = num_nodes*num_rows*num_cols # take only internal nodes
    a_2 = numpy.zeros(shape=(num_nodes_net,num_nodes_net))
    internal_edges = [] # internal_edges[i] = ([ii,jj],[i,j,r0,r1,i_c,j_c]) that is not an external edge
    # i..e internal_edges stores indices of internal edges
    for i in range(num_nodes):
        for j in range(num_nodes):
            for r0 in refs_1:
                for r1 in refs_1:
                    for i_c in rows_1: # don't consider below or above network: r will take these into account
                        for j_c in cols_1: # don't consider left of right of network. r will take these into account                                                        
                            edge_is_external = get_edge_is_external(r0=r0,r1=r1,i_c=i_c,j_c=j_c,num_rows=num_rows,num_cols=num_cols)
                            if edge_is_external == False:
                                (ii,jj) = convert_indx_cell_to_grid_edge(i=i,j=j,r0=r0,r1=r1,i_c=i_c,j_c=j_c,num_nodes=num_nodes,num_rows=num_rows)
                                a_2[ii,jj] = a_6[i,j,r0,r1,i_c,j_c]
                                internal_edges.append(([ii,jj],[i,j,r0,r1,i_c,j_c]))
                            else: 
                                # edge is not part of network 
                                pass
    return (a_2, internal_edges)



def get_edge_is_external(r0,r1,i_c,j_c,num_rows,num_cols):
    """
    Check if the edge going to j in the cell defined by the arguments 
    leaves the network into the external cells that form the outer grid.

    Parameters 
    -------
    - r0: int
        Horizontal position of the cell that contains node j, relative to the cell that contains node i.
    - r1: int 
        Vertical position of the cell that contains the node j, relative to the cell that contains node i.
    - i_c: int 
        Row that the cell that contains node i is in. Rows are indexed from 0 upwards. Row 0 is the bottom 
        row in the grid.
    - j_c: int 
        Column that the cell that containas node i is in. Colums are indexed from 0 upwards. Column 0 is on the left.
    - num_rows: int 
        Number of rows of cells in the network (not including the external cells).
    - num_cols: int 
        Number of cols of cells in the network (not including the external cells).

    Returns 
    -----
    - edge_is_external: bool
        True if the edge to cell defined by arguments from i,i_c,j_c is external, False if it is internal.
    """
    if i_c!=0 and i_c!=num_rows-1:
        # cell is not on boundary so edge is internal
        edge_is_external=False
    else:
        # cell is on a boundary so edge might be external
        if i_c==0:
            # cell is on bottom 
            if r1==-1:
                # j is outside network so edge is external
                edge_is_external=True
            else:
                # j is inside network so edge is internal
                edge_is_external=False
        elif i_c==num_rows-1:
            # cell is on top 
            if r1==1:
                # j is outside network so edge is external
                edge_is_external=True
            else:
                # j is inside network so edge is internal
                edge_is_external=False
    
    if edge_is_external == False:
        # If edge was not external in the row direction
        if j_c!=0 and j_c!=num_cols-1:
            # cell is not on boundary so edge is internal
            edge_is_external=False
        else:
            # cell is on a boundary so edge might be external
            if j_c==0:
                # cell is on left 
                if r0==-1:
                    # j is outside network so edge is external
                    edge_is_external=True
                else:
                    # j is inside network so edge is internal
                    edge_is_external=False
            elif j_c==num_cols-1:
                # cell is on right 
                if r0==1:
                    # j is outside network so edge is external
                    edge_is_external=True
                else:
                    # j is inside network so edge is internal
                    edge_is_external=False
    else: 
        # We have already established its external via row so don't need to check with j
        edge_is_external = True
    return edge_is_external





def reshape_2_to_6_internal_edges(a_2,internal_edges,num_nodes,num_refs,num_rows,num_cols):
    """
    Reshape an edge quantity with grid indexing into the same edge quantity with cell indexing. 
    For example, cond_2 back to cond_6 after the problem has been solved.

    Parameters 
    -----
    - a_2: numpy.ndarray
        The same quantity defined on edges, indexed with grid indexing.
        That is, the quantity a on edge (ii,jj). 
        We understand where this edge is by converting this grid descroption back to a cell 
        description.
        This does not include edges to nodes that are in cells outside the network.
    - internal_edges: list 
        internal_edges[i] = ([ii,jj],[i,j,r0,r1,i_c,j_c]). internal_edges[i][0] is the grid index of an internal 
        edge, internal_edge[i][1] is the corresponding cell index of the same internal edge.
    - num_nodes: int
        Number of nodes in each cell. 
    - num_refs: int 
        Number of references.
    - num_rows: int 
        Number of rows of cells in the network (does not include external cells).
    - num_cols: int 
        Number of cols of cells in the network (does not include external cells).

    Returns
    -----
    - a_6: numpy.ndarray
        A quantity defined on edges, indexed with cell indexing. 
        a_6[i,j,r0,r1,i_c,j_c] is the quantity a defined on the edge between 
        the node i in cell i_c,j_c, and the node j located in the cell at 
        r0,r1 relative to the cell containing i (i.e. node j in cell i_c+r1,j_c+r0).
    """
    refs_1 = [0,1,-1]
    rows_1 = list(numpy.arange(start=0,stop=num_rows,step=1,dtype=int))
    cols_1 = list(numpy.arange(start=0,stop=num_cols,step=1,dtype=int))

    a_6 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_refs,num_rows,num_cols))
    num_nodes_net = num_nodes*num_rows*num_cols
    for ii in range(num_nodes_net):
        for jj in range(num_nodes_net):
            this_edge = [ii,jj]
            for edge in internal_edges:
                if edge[0]==this_edge:
                    # this_edge is an internal_edge
                    i = edge[1][0]
                    j = edge[1][1]
                    r0 = edge[1][2]
                    r1 = edge[1][3]
                    i_c = edge[1][4]
                    j_c = edge[1][5]
    
                    a_6[i,j,r0,r1,i_c,j_c] = a_2[ii,jj] #-1 since a_6 doesn't know about external cells
    return a_6













def reshape_3_to_1_internal_nodes(a_3:numpy.ndarray):
    """
    """
    # Parameters 
    # -----
    num_nodes = len(a_3[:,0,0])
    num_rows  = len(a_3[0,:,0])
    num_cols  = len(a_3[0,0,:])

    refs_1 = [0,1,-1]
    rows_1 = list(numpy.arange(start=0,stop=num_rows,step=1,dtype=int)) # notice we index network differently from edges, ... here we don't have r to account for external cells
    cols_1 = list(numpy.arange(start=0,stop=num_cols,step=1,dtype=int)) # notice we index network differently from edges, ... here we don't have r to account for external cells

    num_nodes_grid = num_nodes*(num_rows)*(num_cols) # usual size since don't consider external cells
    a_1 = numpy.zeros(shape=num_nodes_grid)
    for i in range(num_nodes):
        for i_c in rows_1:
            for j_c in cols_1:
                ii = convert_indx_cell_to_grid_node(i=i,i_c=i_c,j_c=j_c,num_nodes=num_nodes,num_rows=num_rows) # no +2 since not indexing external rows too
                a_1[ii] = a_3[i,i_c,j_c]
    return a_1


def reshape_1_to_3_internal_nodes(a_1:numpy.ndarray, num_nodes:int, num_rows:int, num_cols:int):
    """
    """
    # Parameters 
    # -----
    num_nodes_network = num_nodes*(num_rows)*(num_cols) # +2 because need to index the cells left right up and down from the grid to use r

    a_3 = numpy.zeros(shape=(num_nodes,num_rows,num_cols))
    for ii in range(num_nodes_network):
        i,i_c,j_c = convert_indx_grid_to_cell_node(ii=ii,num_nodes=num_nodes,num_rows=num_rows)
        a_3[i,i_c,j_c] = a_1[ii]
    return a_3










if __name__ == "__main__":
    
    num_nodes = 4
    num_rows  = 2

    i   = 0
    i_c = 1
    j_c = 1

    j   = 3
    r0  = 0
    r1  = 0

    # Check node conversion
    # -------------
    ii = convert_indx_cell_to_grid_node(i=i,i_c=i_c,j_c=j_c,num_nodes=num_nodes,num_rows=num_rows)
    print("ii:{}".format(ii))
    
    i_new,i_c_new,j_c_new = convert_indx_grid_to_cell_node(ii=ii,num_nodes=num_nodes,num_rows=num_rows)
    print("i:{}".format(i_new))
    print("i_c:{}".format(i_c_new))
    print("j_c:{}".format(j_c_new))

    print("i_res:{}".format(i-i_new))
    print("i_c_res:{}".format(i_c-i_c_new))
    print("j_c_res:{}".format(j_c-j_c_new))


    # Check edge conversion
    # --------------
    (ii,jj) = convert_indx_cell_to_grid_edge(i=i,j=j,r0=r0,r1=r1,i_c=i_c,j_c=j_c,num_nodes=num_nodes,num_rows=num_rows)

    (i_new,j_new,r0_new,r1_new,i_c_new,j_c_new) = convert_indx_grid_to_cell_edge(ii=ii,jj=jj,num_nodes=num_nodes,num_rows=num_rows)

    print("ii={},jj={}".format(ii,jj))

    print("i_res:{}".format(i-i_new))
    print("j_res:{}".format(j-j_new))
    print("r0_res:{}".format(r0-r0_new))
    print("r1_res:{}".format(r1-r1_new))
    print("i_c_res:{}".format(i_c-i_c_new))
    print("j_c_res:{}".format(j_c-j_c_new))




    num_nodes = 4
    num_refs  = 3
    initialisation = "4-reg"
    mu = 0.5
    sigma = 0.3
    num_rows = 3
    num_cols = 4
    is_periodic = True


    boundary_nodes_2 = network_2D.get_boundary_nodes(initialisation=initialisation,num_nodes=num_nodes)


    (cond_init_6,conc_init_3,volu_init_3) = network_2D.make_initial_network(num_nodes=num_nodes, num_refs=num_refs,
                                                                            num_rows=num_rows,num_cols=num_cols,
                                                                            is_periodic=is_periodic,
                                                                            initialisation=initialisation,
                                                                            mu=mu,sigma=sigma,
                                                                            boundary_nodes_2=boundary_nodes_2,conc_in=1.0)
    #print(cond_init_6.shape)
    cond_init_2     = cond_init_2 = reshape_6_to_2_all_edges(a_6=cond_init_6)
    cond_init_6_new = reshape_2_to_6_all_edges(a_2=cond_init_2,num_nodes=num_nodes,num_refs=num_refs,num_rows=num_rows,num_cols=num_cols)


    res = numpy.sum(cond_init_6-cond_init_6_new)
    print(res)

    # Check that
    for i_c in range(num_rows):
        for j_c in range(num_cols):
            for r0 in [0,1,-1]:
                for r1 in [0,1,-1]:
                    #i_c=1
                    #j_c=1
                    #r0 =-1
                    #r1 =0
                    before =     cond_init_6[:,:,r0,r1,i_c,j_c]
                    after  = cond_init_6_new[:,:,r0,r1,i_c,j_c]
                    #print(before)
                    #print(after)
                    print(numpy.sum(before-after))

    
    node_prep = numpy.array(range(num_nodes*num_rows*num_cols))
    node_3 = numpy.reshape(a=node_prep,newshape=(num_nodes,num_rows,num_cols))
    #print(node_3)

    node_1 = reshape_3_to_1_internal_nodes(a_3=node_3)
    #print(node_1)
    node_3_new = reshape_1_to_3_internal_nodes(a_1=node_1,num_nodes=num_nodes,num_rows=num_rows,num_cols=num_cols)
    print(numpy.sum(node_3_new-node_3))






    cond_init_2, internal_edges     = reshape_6_to_2_internal_edges(a_6=cond_init_6)
    cond_init_6_new = reshape_2_to_6_internal_edges(a_2=cond_init_2,internal_edges=internal_edges,num_nodes=num_nodes,num_refs=num_refs,num_rows=num_rows,num_cols=num_cols)


    res = numpy.sum(cond_init_6-cond_init_6_new)
    #print(res)

    # Check that
    for i_c in range(num_rows):
        for j_c in range(num_cols):
            for r0 in [0,1,-1]:
                for r1 in [0,1,-1]:
                    #i_c=1
                    #j_c=1
                    #r0 =-1
                    #r1 =0
                    print("i_c={},j_c={},r0={},r1={}".format(i_c,j_c,r0,r1))
                    before =     cond_init_6[:,:,r0,r1,i_c,j_c]
                    after  = cond_init_6_new[:,:,r0,r1,i_c,j_c]
                    #print(before)
                    #print(after)
                    print(numpy.sum(before-after))