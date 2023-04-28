import numpy 
import scipy.sparse.linalg as linalg
from scipy import interpolate

import initial_conditions_2D
import utils_indexing

import matplotlib
from matplotlib import pyplot as plt

def get_new_interpolated_point(table_x,table_y,new_x_value,type_clog):
    """
    Given a list of x values, and corresponding y values, and
    a new x value, approximate the corresponding function, 
    and use this function to return the new y value 
    corresponding to the new x value.

    Parameters 
    ----------
    - table_x: numpy.ndarray
        1-dimensional list of x values.
    - table_y: numpy.ndarray
        1-dimensional list of y values.
    - new_x_value: float
        New x value for which the corresponding y value is to be approximated.
    
    Returns
    -------
    - new_y_value: float
        Interpolated y value corresponding to new_x_value
    """
    if type_clog == "deposit":
        interpolated_function = interpolate.splrep(x=table_x,y=table_y,k=3)
        new_y_value = interpolate.splev(x=new_x_value, tck=interpolated_function)
        #print(new_x_value)
    elif type_clog == "block":
        step_fun = interpolate.interp1d(table_x, table_y, kind='next') 
        #print("new_x_value:\n{}".format(new_x_value))
        new_y_value = step_fun(new_x_value)
    else: 
        raise Exception("type_clog must be either 'block' or 'deposit'.")
    return new_y_value



def get_boundary_nodes_in_cell(initialisation:str, num_nodes:int):
    """
    Get a dictionary that contains lists of the indices of 
    nodes that would satisfy the inlet or outlet 
    boundary condition if the cell were at the boundary. 
    The result will eventually be fed into the algebraic equation that finds
    the pressure. 
    Since outut is node index, it is netiehr grid indexing or cell indexing.

    Parameters 
    ------
    - initialisation: str 
        String describing the structure of the cell. 
    - num_nodes: int 
        Number of nodes in the cell.

    Returns
    -----
    - boundary_nodes_cell_2: dict
        boundary_nodes_cell_2["inlet"][i]  = the ith inlet node index in the cell.
        boundary_nodes_cell_2["outlet"][i] = the ith outlet node index in the cell.
    """
    if initialisation == "4-reg_prescribed" or initialisation=="4-reg":
        inlet_nodes_1 = []
        outlet_nodes_1 = []
        n = int(numpy.sqrt(num_nodes))
        for i in range(n):
            inlet_node = int(i*n)
            inlet_nodes_1.append(inlet_node)

            outlet_node = int(inlet_node+(n-1))
            outlet_nodes_1.append(outlet_node)

    else: 
        raise Exception("Have only implemented boundary node calculator for '4-reg' initialisation. Create boundary node calculator for desired initialisation.")
    boundary_nodes_cell_2 = {}
    boundary_nodes_cell_2["inlet"]  = inlet_nodes_1
    boundary_nodes_cell_2["outlet"] = outlet_nodes_1
    return boundary_nodes_cell_2


def get_boundary_nodes_in_network(boundary_nodes_cell_2:dict, num_nodes:int, num_rows:int, num_cols:int):
    """
    Given that we know which nodes in a cell would have the potential to be boundary nodes, 
    for each cell, check if the cell is on the boundary, and then if the cell is in the boundary 
    check which nodes in that cell are on the boundary.

    Parameters 
    -----
    - boundary_nodes_cell_2: dict
        boundary_nodes_cell_2["inlet"][i]  = the ith inlet node index in the cell.
        boundary_nodes_cell_2["outlet"][i] = the ith outlet node index in the cell.
    - num_nodes: int 
        Number of nodes in the cell.
    - num_rows: int 
        Number of rows of cells in the network.
    - num_columns: int 
        Number of columns of cells in the network.

    Returns 
    ------
    - boundary_nodes_network_2: dict
        Lists of the grid indices that refer to inlet and outlet nodes in the network. 
        boundary_nodes_network_2["inlet"][ii] = grid index of a node in the inlet of the network. 
        boundary_ndoes_network_2["outlet"][ii] = grid_index of a node in the outlet of the network.
    """
    inlet_nodes_cell_1  = boundary_nodes_cell_2["inlet"]
    outlet_nodes_cell_1 = boundary_nodes_cell_2["outlet"]
    
    inlet_nodes_network_1  = []
    outlet_nodes_network_1 = []
    for i in range(num_nodes):
        for i_c in range(num_rows):
            for j_c in range(num_cols):
                (is_inlet_cell,is_outlet_cell) = get_cell_is_boundary_cell(i_c=i_c,j_c=j_c,num_rows=num_rows,num_cols=num_cols)
                if is_inlet_cell == True:
                    for node in inlet_nodes_cell_1:
                        if i==node:
                            # node is an inlet node
                            ii = utils_indexing.convert_indx_cell_to_grid_node(i=i,i_c=i_c,j_c=j_c,num_nodes=num_nodes,num_rows=num_rows)
                            inlet_nodes_network_1.append(ii)
                        else: 
                            # node is not an inlet node 
                            pass    
                else: 
                    # cell is not an inlet cell 
                    pass
                if is_outlet_cell==True:
                    for node in outlet_nodes_cell_1:
                        if i==node:
                            # node is an outlet node
                            ii = utils_indexing.convert_indx_cell_to_grid_node(i=i,i_c=i_c,j_c=j_c,num_nodes=num_nodes,num_rows=num_rows)
                            outlet_nodes_network_1.append(ii)
                        else: 
                            # node is not an outlet node 
                            pass
                else: 
                    # cell is not an outlet cell 
                    pass
    boundary_nodes_network_2 = {}
    boundary_nodes_network_2["inlet"] = inlet_nodes_network_1
    boundary_nodes_network_2["outlet"] = outlet_nodes_network_1
    return boundary_nodes_network_2



def get_cell_is_boundary_cell(i_c:int, j_c:int, num_rows:int, num_cols:int):
    """
    Check if cell i_c,j_c is on any of the four boundaries of the network 
    given by num_nodes, num_rows,  num_cols.

    Parameters 
    -----
    - i_c: int 
        The row that the cell containing the node is in.
    - j_c: int 
        The column that the cell containing the node is in.
    - num_rows: int 
        The number of rows of cells in the network. 
    - n um_cols: int 
        The number of colyumns of cells in the network.

    Returns 
    ------
    - is_inlet_cell: bool
        True if cell i_c,j_c is a cell at the inlet of the network.
    - is_outlet_cell:bool
        True if cell i_c,j_c is a cell at the outlet of the network.
    """
    if j_c==0:
        is_inlet_cell=True
    else: 
        is_inlet_cell=False

    if j_c==num_cols-1:
        is_outlet_cell=True
    else:
        is_outlet_cell=False

    return (is_inlet_cell,is_outlet_cell)





def get_pressure_problem(cond_2:numpy.ndarray, boundary_nodes_network_2:dict):
    """
    Get the left and right hand side of 
    the linear problem on the entire  network that gives pressure at each time step.
    Note that we include the pressure boundary condition, that 
    inlet nodes have pressure one and the single out node 
    has pressure zero.
    
    Parameters 
    -----
    - boundary_nodes_network_2: dict 
        The grid indexes of all nodes that are on the boundary of the network.
        boundary_nodes_2["inlet"][ii] = iith inlet node in grid indexing.
        boundary_nodes_2["outlet"][ii] = iith outlet node in grid indexing.
    - cond_2: numpy.ndarray
        cond_2[ii,jj] = cond_6[i,j,r0,r1,i_c,j_c] = conductance from i to j, where 
        i is in cell in row i_c and column j_c, and j is in the cell at r0,r1 
        relative to the cell that i is in.
        Note that this must be an internal edge, we don't consider external edges.
    
    Returns
    -----
    - lhs_2: numpy.ndarray
        Left matrix of linear pressure problem on all the nodes in the network
        with the unit pressure drop condition. 
    - rhs_1: numpy.ndarray
        Right vector of linear pressure problem on all the nodes in the network
        with the unit pressure drop condition.
    """
    # Parameters 
    # ------
    num_nodes_network = len(cond_2[:,0])
    
    # Get lhs
    # -----
    # Expand pressure so that can multiply
    lhs_2 = cond_2[:,:]-numpy.diag(numpy.sum(a=cond_2[:,:], axis=1))
    
    # Get rhs
    # -----
    rhs_1 = numpy.zeros(num_nodes_network) 

    # boundary conditions
    # incoming pressures are 1, outgoing are zero
    inlet_nodes_network_1 = boundary_nodes_network_2["inlet"]
    outlet_nodes_network_1 = boundary_nodes_network_2["outlet"]
    for inlet_node in inlet_nodes_network_1:
        lhs_2[inlet_node,:]  = numpy.zeros(num_nodes_network)
        lhs_2[inlet_node, inlet_node]   = 1
        rhs_1[inlet_node]  = 1

    # if there is no out node
    #for outlet_node in outlet_nodes_network_1:        
    #    lhs_2[outlet_node,:] = numpy.zeros(num_nodes_network)
    #    lhs_2[outlet_node,outlet_node] = 1
    #    rhs_1[outlet_node] = 0

    # if there is a single out node connected to all outlet nodes
    lhs_2[-1,:] = numpy.zeros(num_nodes_network)
    lhs_2[-1,-1] = 1.0
    rhs_1[-1] = 0.0

    return (lhs_2,rhs_1)




def get_pressure_solution(lhs_2:numpy.ndarray, rhs_1:numpy.ndarray):
    """
    Get the solution of the pressure problem on the network, whcih is a vector 
    where each element is the pressure at the correspondingly 
    grid indexed node.

    Parameters
    -----
    - lhs_2: numpy.ndarray
        Left matrix of linear pressure problem in grid indexing. 
    - rhs_1: numpy.ndarray
        Right vector of linear pressure problem in grid indexing.

    Returns
    -----
    - pres_1: numpy.ndarray
        pres_1[ii] = pressure at node nodes[ii], where ii is the grid index.
    """ 
    pres_1 = linalg.lsqr(A=lhs_2,b=rhs_1)[0]

    return pres_1



def get_initial_conds_with_out_node(cond_init_2:numpy.ndarray, adhe_init_2:numpy.ndarray, conc_init_1:numpy.ndarray, volu_init_1:numpy.ndarray, boundary_nodes_network_2:dict):
    """
    Add an out node to the network. 
    The out node will simply collect all particles that have left the main network. 
    The out node connects to all outlet nodes.
    There will be no deposition on edges between outlet nodes and the out node.
    
    Parameters 
    -----
    - cond_init_2: numpy.ndarray
        Has shape (num_nodes_network,num_nodes_network).
        cond_init_2[ii,jj] = the initial conductance between ii and jj. 
    - adhe_init_2: numpy.ndarray
        Has shape (num_nodes_network,num_nodes_network).
        cond_init_2[ii,jj] = the initial adherence between ii and jj.
    - conc_init_1: numpy.ndarray
        Has shape (num_nodes_network).
        conc_init_1[ii] = the initial concentration at ii.
    - volu_init_1: numpy.ndarray
        Has shape (num_nodes_network).
        volu_init_1[ii] = the initial volume at ii.

    Returns
    -------
    - cond_init_2: numpy.ndarray
        Has shape (num_nodes_network+1,num_nodes_network+1).
        cond_init_2[ii,jj] = the initial conductance between ii and jj. 
    - adhe_init_2: numpy.ndarray
        Has shape (num_nodes_network+1,num_nodes_network+1).
        cond_init_2[ii,jj] = the initial adherence between ii and jj.
    - conc_init_1: numpy.ndarray
        Has shape (num_nodes_network+1).
        conc_init_1[ii] = the initial concentration at ii.
    - volu_init_1: numpy.ndarray
        Has shape (num_nodes_network+1).
        volu_init_1[ii] = the initial volume at ii.
    """
    # Parameters
    # -----
    num_nodes_network  = len(cond_init_2[:,0])
    num_nodes_with_out = num_nodes_network+1
    

    cond_init_network_2 = numpy.zeros(shape=(num_nodes_with_out,num_nodes_with_out))
    adhe_init_network_2 = numpy.zeros(shape=(num_nodes_with_out,num_nodes_with_out))
    conc_init_network_1 = numpy.zeros(shape=(num_nodes_with_out))
    volu_init_network_1 = numpy.zeros(shape=(num_nodes_with_out))

    cond_init_network_2[0:-1,0:-1] = cond_init_2 
    adhe_init_network_2[0:-1,0:-1] = adhe_init_2 
    conc_init_network_1[0:-1] = conc_init_1 
    volu_init_network_1[0:-1] = volu_init_1 

    for ii in boundary_nodes_network_2["outlet"]:
        cond_init_network_2[-1,ii] = 1.0
        cond_init_network_2[ii,-1] = 1.0
        adhe_init_network_2[-1,ii] = 1.0
        adhe_init_network_2[ii,-1] = 1.0
    
    conc_init_network_1[-1] = 0.0
    volu_init_network_1[-1] = 1.0

    cond_init_2 = cond_init_network_2
    adhe_init_2 = adhe_init_network_2
    conc_init_1 = conc_init_network_1
    volu_init_1 = volu_init_network_1

    return (cond_init_2, adhe_init_2, conc_init_1, volu_init_1)

def get_sol_without_out_node(cond_2,adhe_2,conc_1,volu_1):
    """
    """


def make_initial_network(num_nodes:int, num_refs:int, num_rows:int, num_cols:int, is_periodic:bool, initialisation:str, mu:float, sigma:float, boundary_nodes_cell_2:dict, conc_in:float):
    """
    """
    # Get boundary nodes
    # -----
    inlet_nodes_1 = boundary_nodes_cell_2["inlet"]
    outlet_nodes_1 = boundary_nodes_cell_2["outlet"]
    
    # Define initial conc and volu
    # -----
    # Note: inlet and outlet nodes will have to be corrected for boundary condition
    volu_init_3 = numpy.ones(shape=(num_nodes,num_rows,num_cols))
    conc_init_3 = numpy.zeros(shape=(num_nodes,num_rows,num_cols))

    # Define initial cond
    # -----
    cond_init_6 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_refs,num_rows,num_cols))
    # Get initial cell 
    if initialisation == "4-reg":
        cond_init_4 = initial_conditions_2D.four_reg(num_nodes=num_nodes,num_refs=num_refs,mu=mu,sigma=sigma)
    elif initialisation == "4-reg_prescribed":
        cond_init_4 = initial_conditions_2D.four_reg_prescribed(num_nodes=num_nodes,num_refs=num_refs)
    else: 
        raise Exception("Can only make initial network if initialisation=='4-reg'. Write make_initial_network() for new initialisation.")

    for i_cell in range(num_rows):
        for j_cell in range(num_cols):
            cond_init_6[:,:,:,:,i_cell,j_cell] = cond_init_4
            
            # Correct boundary conditions
            # -----
            if j_cell==0:
                # this cell is on the left
                for i_node in range(num_nodes):
                    if i_node in inlet_nodes_1:
                        # this node is inlet node and concentration needs correcting
                        conc_init_3[i_node,i_cell,j_cell] = conc_in
                    else: 
                        pass
            elif j_cell==num_cols-1:
                # this cell is on the right 
                    if i_node in outlet_nodes_1:
                        # this node is outlet node and concentration needs correcting
                        conc_init_3[i_node,i_cell,j_cell] = 0
                    else: 
                        pass
            

            # Make these seperate cells into a network
            # ----
            if i_cell == 0:
                # cell is at the bottom
                if j_cell == 0:
                    # cell is at bottom and left
                    pass
                elif j_cell > 0: 
                    # cell is at bottom but not left
                    cond_init_6[:,:,-1,0,i_cell,j_cell] = numpy.transpose(cond_init_6[:,:,1,0,i_cell,j_cell-1])
                else: 
                    pass

            elif i_cell > 0:
                # cell is not at bottom
                if j_cell == 0:
                    # cell is not at bottom but is on left
                    cond_init_6[:,:,0,-1,i_cell,j_cell] = numpy.transpose(cond_init_6[:,:,0,1,i_cell-1,j_cell])
                    cond_init_6[:,:,1,-1,i_cell,j_cell] = numpy.transpose(cond_init_6[:,:,-1,1,i_cell-1,j_cell+1])
                elif ((j_cell > 0) and (j_cell < num_cols-1)):
                    # cell is not on bottom or on left or on right
                    cond_init_6[:,:,0,-1,i_cell,j_cell]  = numpy.transpose(cond_init_6[:,:,0,1,i_cell-1,j_cell])
                    cond_init_6[:,:,1,-1,i_cell,j_cell]  = numpy.transpose(cond_init_6[:,:,-1,1,i_cell-1,j_cell+1])
                    cond_init_6[:,:,-1,-1,i_cell,j_cell] = numpy.transpose(cond_init_6[:,:,1,1,i_cell-1,j_cell-1])
                    cond_init_6[:,:,-1,0,i_cell,j_cell]  = numpy.transpose(cond_init_6[:,:,1,0,i_cell,j_cell-1])  
                elif j_cell == num_cols-1:
                    # cell is not on bottom and is on right
                    cond_init_6[:,:,0,-1,i_cell,j_cell]  = numpy.transpose(cond_init_6[:,:,0,1,i_cell-1,j_cell])
                    cond_init_6[:,:,-1,-1,i_cell,j_cell] = numpy.transpose(cond_init_6[:,:,1,1,i_cell-1,j_cell-1])
                    cond_init_6[:,:,-1,0,i_cell,j_cell]  = numpy.transpose(cond_init_6[:,:,1,0,i_cell,j_cell-1])
                else: 
                    raise Exception("Should have considered all columns. Revise code.") 
            
            else: 
                raise Exception("Should have considered all rows. Revise code.")


            if is_periodic == True:
                if i_cell == num_rows-1:
                    # cell is at top and it should be periodic with bottom cells
                    if j_cell == 0:
                        # cell is at top and on left 
                        cond_init_6[:,:,0,1,i_cell,j_cell] = numpy.transpose(cond_init_6[:,:,0,-1,0,j_cell])
                        cond_init_6[:,:,1,1,i_cell,j_cell] = numpy.transpose(cond_init_6[:,:,-1,-1,0,j_cell+1])    
                    elif (j_cell>0) and (j_cell<num_cols-1):      
                        # cell is at top and not on left or right
                        cond_init_6[:,:,0,1,i_cell,j_cell]  = numpy.transpose(cond_init_6[:,:,0,-1,0,j_cell])
                        cond_init_6[:,:,1,1,i_cell,j_cell]  = numpy.transpose(cond_init_6[:,:,-1,-1,0,j_cell+1])   
                        cond_init_6[:,:,-1,1,i_cell,j_cell] = numpy.transpose(cond_init_6[:,:,1,-1,0,j_cell-1])   
                    elif j_cell == num_cols-1:
                        cond_init_6[:,:,0,1,i_cell,j_cell]  = numpy.transpose(cond_init_6[:,:,0,-1,0,j_cell])
                        cond_init_6[:,:,-1,1,i_cell,j_cell] = numpy.transpose(cond_init_6[:,:,1,-1,0,j_cell-1])   
                    else: 
                        raise Exception("Should have considered all rows. Revise code")
                else:
                    pass
            elif is_periodic==False: 
                pass
            else: 
                raise Exception("is_periodic should be a boolean.")
    
    return (cond_init_6,conc_init_3,volu_init_3,  cond_init_4) # cond_init_4 only needed for saving









def get_pressure_difference(pres_1:numpy.ndarray):
    """
    Get the pressure difference matrix from the pressure vector.

    Parameters 
    -----
    - pres_1: numpy.ndarray
        pres_1[ii] = pressure at node nodes[ii], where ii is the grid index.
    
    Returns 
    -----
    - pdif_2: numpy.ndarray
        pdif_2[ii,jj] = pres_1[ii]-pres_1[jj].
    """
    # Parameters 
    # -----
    num_nodes_network = len(pres_1)

    pres_i_2 = numpy.repeat(a=pres_1[:,numpy.newaxis],repeats=num_nodes_network,axis=1)
    pres_j_2 = numpy.repeat(a=pres_1[numpy.newaxis,:],repeats=num_nodes_network,axis=0)
    pdif_2   = pres_i_2-pres_j_2
    return pdif_2



def get_heaviside(pdif_2:numpy.ndarray):
    """
    Get the heaviside function of pressure difference.

    Parameters
    ------
    - pdif_2: numpy.ndarray
        Pressure difference between node i and node j. pdif_2[ii,jj] = pres_1[ii]-pres_1[jj]
        in grid indexing.

    Returns 
    ------
    - heav_2: numpy.ndarray
        The heaviside function. H[ii,jj] = 1 if pdif>tol
                                           0 if pdif<tol
    """
    tol = 1E-5
    heav_2 = numpy.array(pdif_2>tol,dtype=float)
    return heav_2



def get_edge_concentration(conc_1:numpy.ndarray, pdif_2:numpy.ndarray):
    """
    """
    # Parameters 
    # -----
    num_nodes_network = len(conc_1)

    conc_i_2 = numpy.repeat(a=conc_1[:,numpy.newaxis],repeats=num_nodes_network, axis=1)
    conc_j_2 = numpy.repeat(a=conc_1[numpy.newaxis,:],repeats=num_nodes_network, axis=0)

    heav_ij_2 = get_heaviside(pdif_2=pdif_2)
    heav_ji_2 = get_heaviside(pdif_2=-pdif_2)

    conc_2 = conc_i_2*heav_ij_2 + conc_j_2*heav_ji_2

    return conc_2



def get_concentration(conc_1:numpy.ndarray, pres_1:numpy.ndarray, volu_1:numpy.ndarray, cond_2:numpy.ndarray, boundary_nodes_network_2:dict, conc_in:float, alph:float, delt:float, epsi:float, dt:float):
    """
    """
    # Parameters 
    # ------
    num_nodes_network = len(conc_1)
    n = num_nodes_network

    # i to j
    # -----
    cond_ij_2 = cond_2
    pdif_ij_2 = get_pressure_difference(pres_1=pres_1)
    conc_j_2  = numpy.repeat(conc_1[numpy.newaxis,:], repeats=n, axis=0)
    heav_ij_2 = get_heaviside(pdif_2=pdif_ij_2)
    
    # into i
    # -----
    cond_ji_2 = numpy.transpose(a=cond_ij_2)
    pdif_ji_2 = numpy.transpose(a=pdif_ij_2)
    conc_i_2  = numpy.repeat(a=conc_1[:,numpy.newaxis], repeats=n, axis=1)
    heav_ji_2 = numpy.transpose(a=heav_ij_2)

    ones_2 = numpy.ones(shape=(n,n))
    
    #ones_2-gamm*epsi
    #*(1.0/gamm)
    # NETWORK MODEL
    inte_2 = (ones_2-epsi*delt*alph)*cond_ji_2*(1.0/epsi)*pdif_ji_2*conc_j_2*heav_ji_2-cond_ij_2*(1.0/epsi)*pdif_ij_2*conc_i_2*heav_ij_2
    rhs_1 = (1.0/(epsi*delt**2))*(numpy.ones(n)/volu_1)*numpy.sum(a=inte_2, axis=1)

    # MULTISCALE MODEL
    #inte_2 = (ones_2-delt*epsi*alph)*cond_ji_2*(1.0/epsi)*pdif_ji_2*conc_j_2*heav_ji_2-cond_ij_2*(1.0/epsi)*pdif_ij_2*conc_i_2*heav_ij_2
    #rhs_1 =  (numpy.ones(n)/volu_1)*numpy.sum(a=inte_2, axis=1)


    # NOTE: If no deposition then:
    # -----
    #rhs_1 = numpy.zeros_like(rhs_1)

    # Boundary condition
    # -----
    for ii in boundary_nodes_network_2["inlet"]:
        rhs_1[ii] = 0.0


    conc_1 = conc_1 + dt*rhs_1

    
    return conc_1



def get_conductance(conc_1:numpy.ndarray, pres_1:numpy.ndarray, cond_2:numpy.ndarray, boundary_nodes_network_2:dict, alph:float, beta:float, delt:float, epsi:float, dt:float):
    """
    """
    # Parameters 
    # ------
    pdif_2 = get_pressure_difference(pres_1=pres_1)
    conc_2 = get_edge_concentration(conc_1=conc_1,pdif_2=pdif_2)


    # NETWORK MODEL
    rhs_2  = -((delt*alph*beta)/(epsi*delt**2))*conc_2*abs(pdif_2)*cond_2**(3.0/2.0)#*(1.0/gamm)#*(gamm)#*epsi      #*adhe_2*(1/(epsi**(1.0/2.0)))
    
    # MULTISCALE MODEL
    #rhs_2  = -alph*delt*beta*conc_2*abs(pdif_2)*cond_2**(3.0/2.0)#*(1.0/gamm)#*(gamm)#*epsi      #*adhe_2*(1/(epsi**(1.0/2.0)))
    #print(beta)
    #print(gamm)
    #print(conc_2)
    #print(pdif_2[0,1]/(0.1*gamm))
    #print(conc_2[0,1]*abs(pdif_2[0,1])*cond_2[0,1]/(0.1*gamm))
    #rhs_2  = numpy.zeros_like(rhs_2)
    # Condition on edges between outlet nodes and out node
    # -----
    # There is no deposition on out edges
    for ii in boundary_nodes_network_2["outlet"]:
        rhs_2[-1,ii] = 0.0
        rhs_2[ii,-1] = 0.0

    # NOTE: If no deposition then:
    # -----
    #rhs_2 = numpy.zeros_like(rhs_2)
    
    
    cond_2 = cond_2 + dt*rhs_2

    
    return cond_2



def reshape_solution_grid_to_cell(conc_2:numpy.ndarray, pres_2:numpy.ndarray, volu_2:numpy.ndarray, cond_3:numpy.ndarray, adhe_3:numpy.ndarray,
                                  num_nodes:int, num_rows:int, num_cols:int, num_refs:int, internal_edges:list, 
                                  reshape_times_1:list):
    """
    - reshape_times_1:list 
        Times at which to reshape the time-dependent solution.
    """

    # Parameters 
    # -----
    num_times = len(reshape_times_1)

    adhe_7 = numpy.zeros(shape=(num_times,num_nodes,num_nodes,num_refs,num_refs,num_rows,num_cols))
    cond_7 = numpy.zeros(shape=(num_times,num_nodes,num_nodes,num_refs,num_refs,num_rows,num_cols))
    conc_4 = numpy.zeros(shape=(num_times,num_nodes,num_rows,num_cols))
    pres_4 = numpy.zeros(shape=(num_times,num_nodes,num_rows,num_cols))
    volu_4 = numpy.zeros(shape=(num_times,num_nodes,num_rows,num_cols))

    # Reshape solution 
    # -----
    for ii_t,i_t in enumerate(reshape_times_1):
        print("Reshaping solution at i_t={}.".format(i_t))
        adhe_7[ii_t,:,:,:,:,:,:] = utils_indexing.reshape_2_to_6_internal_edges(a_2=adhe_3[i_t,:,:], 
                                                                               internal_edges=internal_edges,
                                                                               num_nodes=num_nodes,
                                                                               num_refs=num_refs,
                                                                               num_rows=num_rows,
                                                                               num_cols=num_cols)
        cond_7[ii_t,:,:,:,:,:,:] = utils_indexing.reshape_2_to_6_internal_edges(a_2=cond_3[i_t,:,:], 
                                                                               internal_edges=internal_edges,
                                                                               num_nodes=num_nodes,
                                                                               num_refs=num_refs,
                                                                               num_rows=num_rows,
                                                                               num_cols=num_cols)
        volu_4[ii_t,:,:,:]       = utils_indexing.reshape_1_to_3_internal_nodes(a_1=volu_2[i_t,:], 
                                                                               num_nodes=num_nodes,
                                                                               num_rows=num_rows,
                                                                               num_cols=num_cols)
        conc_4[ii_t,:,:,:]       = utils_indexing.reshape_1_to_3_internal_nodes(a_1=conc_2[i_t,:], 
                                                                               num_nodes=num_nodes,
                                                                               num_rows=num_rows,
                                                                               num_cols=num_cols)
        pres_4[ii_t,:,:,:]       = utils_indexing.reshape_1_to_3_internal_nodes(a_1=pres_2[i_t,:], 
                                                                               num_nodes=num_nodes,
                                                                               num_rows=num_rows,
                                                                               num_cols=num_cols)                                                                    
    return (conc_4,pres_4,volu_4,cond_7,adhe_7)



def get_flux_through_network(cond_2:numpy.ndarray, pres_1:numpy.ndarray, boundary_nodes_network_2:dict, delt:float, epsi:float):
    """
    """ 
    outlet_nodes_network_1 = boundary_nodes_network_2["outlet"]
    num_nodes_outlet = len(outlet_nodes_network_1)
    pdif_2 = get_pressure_difference(pres_1=pres_1)
    flux_2 = (1.0/delt)*(1.0/epsi)*cond_2*pdif_2
    flux_out_1 = numpy.ndarray(shape=(num_nodes_outlet))
    for i,ii in enumerate(outlet_nodes_network_1):
        flux_out_1[i] = flux_2[ii,-1]
    flux_out = numpy.mean(a=flux_out_1,axis=0)
    return flux_out


def get_average_solutions_down_columns(reshape_times_1:list, num_nodes_hori:int, num_rows:int, num_cols:int, cond_7:numpy.ndarray, adhe_7:numpy.ndarray, conc_4:numpy.ndarray, volu_4:numpy.ndarray, pres_4:numpy.ndarray):
    """
    Get average values of solution down columns that can be plotted against position at times 
    that we have selected. 
    The solutions fed in have been reshaped into cell indexing.    
    """
    
    # Parameters 
    # ------
    num_nodes = len(conc_4[0,:,0,0])
    n = int(numpy.sqrt(num_nodes))

    num_time_indxs_to_plot = len(reshape_times_1)
    num_posis = num_nodes_hori

    # -------
    conc_2 = numpy.zeros(shape=(num_time_indxs_to_plot,num_posis))
    volu_2 = numpy.zeros(shape=(num_time_indxs_to_plot,num_posis))
    pres_2 = numpy.zeros(shape=(num_time_indxs_to_plot,num_posis))

    cond_2 = numpy.zeros(shape=(num_time_indxs_to_plot,num_posis-1)) # one less edge col than node col
    adhe_2 = numpy.zeros(shape=(num_time_indxs_to_plot,num_posis-1)) # one less edge col than node col
    for ii_t,i_t in enumerate(reshape_times_1):
        for j_c in range(num_cols):
            for sub_col in range(n):
                # we are now in a particular sub_col aka column of nodes
                # get the indexes of nodes that can appear in this sub col
                indxs_in_sub_col = numpy.linspace(start=0.0+sub_col,stop=num_nodes-n+sub_col,num=n,dtype=int)

                # Get mean conc and volu down each node column
                # -------
                concs_in_this_sub_col_1 = []
                volus_in_this_sub_col_1 = []
                press_in_this_sub_col_1 = []
                for i_c in range(num_rows):
                    for i in indxs_in_sub_col:
                        conc = conc_4[ii_t,i,i_c,j_c]
                        concs_in_this_sub_col_1.append(conc)

                        volu = volu_4[ii_t,i,i_c,j_c]
                        volus_in_this_sub_col_1.append(volu)

                        pres = pres_4[ii_t,i,i_c,j_c]
                        press_in_this_sub_col_1.append(pres)

                mean_conc_in_this_sub_col = numpy.mean(concs_in_this_sub_col_1)
                conc_2[ii_t,sub_col+j_c*n] = mean_conc_in_this_sub_col

                mean_volu_in_this_sub_col = numpy.mean(volus_in_this_sub_col_1)
                volu_2[ii_t,sub_col+j_c*n] = mean_volu_in_this_sub_col

                mean_pres_in_this_sub_col = numpy.mean(press_in_this_sub_col_1)
                pres_2[ii_t,sub_col+j_c*n] = mean_pres_in_this_sub_col
                # Get cond and adhe in each edge column
                # --------
                if (j_c==num_cols-1 and sub_col==n-1)==False:
                    # If we're not in the last node column
                    # Get mean cond and adhe down each edge column
                    # ------
                    if sub_col!=n-1:
                        # If not last ndoe col in cell, 
                        # then there is another to the right
                        sub_col_to_right = sub_col+1
                        indxs_in_sub_col_to_right = numpy.linspace(start=0.0+sub_col_to_right,stop=num_nodes-n+sub_col_to_right,num=n,dtype=int)   
                    elif sub_col==n-1:
                        # In last col of nodes in cell, 
                        # col to the right is 0th col of the next cell
                        sub_col_to_right = 0
                        indxs_in_sub_col_to_right = numpy.linspace(start=0.0+sub_col_to_right,stop=num_nodes-n+sub_col_to_right,num=n,dtype=int)   
                    else: 
                        raise Exception("Current node column does not exist.")

                    conds_in_this_sub_col_1 = []
                    adhes_in_this_sub_col_1 = []
                    for i_c in range(num_rows):
                        for ii in range(len(indxs_in_sub_col)):
                            i = indxs_in_sub_col[ii]
                            j = indxs_in_sub_col_to_right[ii]

                            if sub_col!=n-1:
                                # Not in last col so j is in same cell as i
                                r0 = 0
                                r1 = 0
                            elif sub_col==n-1:
                                # In last col so j in celll to right of i
                                r0=1
                                r1=0
                            else: 
                                raise Exception("Current node column does not exist.")
                            cond = cond_7[ii_t,i,j,r0,r1,i_c,j_c]
                            conds_in_this_sub_col_1.append(cond)

                            adhe = cond_7[ii_t,i,j,r0,r1,i_c,j_c]
                            adhes_in_this_sub_col_1.append(adhe)

                    mean_cond_in_this_sub_col = numpy.mean(conds_in_this_sub_col_1)
                    cond_2[ii_t,sub_col+j_c*n] = mean_cond_in_this_sub_col

                    mean_adhe_in_this_sub_col = numpy.mean(adhes_in_this_sub_col_1)
                    adhe_2[ii_t,sub_col+j_c*n] = mean_adhe_in_this_sub_col
                elif (j_c==num_cols-1 and sub_col==n-1)==True:
                    pass
                else:
                    raise Exception("Current node column does not exist.")

    return (conc_2, volu_2, cond_2, adhe_2, pres_2)



if __name__ == "__main__":
    num_nodes = 4
    num_refs  = 3
    initialisation = "4-reg"
    mu = 0.5
    sigma = 0.3
    num_rows = 2
    num_cols = 2
    is_periodic = True
    epsi = 0.1


    boundary_nodes_cell_2 = get_boundary_nodes_in_cell(initialisation=initialisation,num_nodes=num_nodes)
    #print(boundary_nodes_cell_2["inlet"])
    #print(boundary_nodes_cell_2["outlet"])
    boundary_nodes_network_2 = get_boundary_nodes_in_network(boundary_nodes_cell_2=boundary_nodes_cell_2,num_nodes=num_nodes,num_rows=num_rows,num_cols=num_cols)
    #print(boundary_nodes_network_2["inlet"])
    #print(boundary_nodes_network_2["outlet"])

    (cond_init_6,conc_init_3,volu_init_3) = make_initial_network(num_nodes=num_nodes, num_refs=num_refs,
                                                                 num_rows=num_rows,num_cols=num_cols,
                                                                 is_periodic=is_periodic,
                                                                 initialisation=initialisation,
                                                                 mu=mu,sigma=sigma,
                                                                 boundary_nodes_cell_2=boundary_nodes_cell_2,conc_in=1.0)

    (cond_init_2,internal_edges) = utils_indexing.reshape_6_to_2_internal_edges(a_6=cond_init_6)


    (lhs_2,rhs_1)    = get_pressure_problem(cond_2=cond_init_2, boundary_nodes_network_2=boundary_nodes_network_2)
    pres_1           = get_pressure_solution(lhs_2=lhs_2,rhs_1=rhs_1)
    pres_3           = utils_indexing.reshape_1_to_3_internal_nodes(a_1=pres_1,num_nodes=num_nodes,num_rows=num_rows,num_cols=num_cols)

    ##print(lhs_2)
    ##print(rhs_1)
    #i_c = 0
    #j_c = 1
    #print(pres_3[:,i_c,j_c])
    #for i_c in range(num_rows):
    #    i = 0
    #    for j_c in range(num_cols):
    #        plt.scatter(i,pres_3[2,i_c,j_c])
    #        i=i+1
    #        plt.scatter(i,pres_3[3,i_c,j_c])
    #        i=i+1
    #plt.plot(range(i),-(1/(numpy.sqrt(num_nodes)*num_cols-1))*numpy.array(range(i))+1)
    ##plt.plot(pres_1[0:int(numpy.sqrt(num_nodes))])
    #plt.show()
#
#
    #for j_c in range(num_cols):
    #    i = 0
    #    for i_c in range(num_rows):
    #        plt.scatter(i,pres_3[0,i_c,j_c])
    #        i=i+1
    #        plt.scatter(i,pres_3[2,i_c,j_c])
    #        i=i+1
    #plt.plot(range(i),(0/(numpy.sqrt(num_nodes)*num_cols-1))*numpy.ones_like(numpy.array(range(i))))
    #plt.plot(range(i),(1/(numpy.sqrt(num_nodes)*num_cols-1))*numpy.ones_like(numpy.array(range(i))))
    #plt.plot(range(i),(2/(numpy.sqrt(num_nodes)*num_cols-1))*numpy.ones_like(numpy.array(range(i))))
    #plt.plot(range(i),(3/(numpy.sqrt(num_nodes)*num_cols-1))*numpy.ones_like(numpy.array(range(i))))
    ##plt.plot(pres_1[0:int(numpy.sqrt(num_nodes))])
    #plt.show()
    
    pres_1 = numpy.array([1,2,3,4])
    pdif_2 = get_pressure_difference(pres_1=pres_1)
    #print(pdif_2)

    cond_2 = numpy.array([[5,6,7,8],[9,10,11,12],[13,14,15,16],[17,18,19,20]])

    heav_2 = get_heaviside(pdif_2= pdif_2)
    heav_2 = get_heaviside(pdif_2=-pdif_2)
    print(heav_2)

    conc_1 = numpy.array([1,2,3,4])
    conc_2 = get_edge_concentration(conc_1=conc_1, pdif_2=pdif_2)
    print(conc_2)