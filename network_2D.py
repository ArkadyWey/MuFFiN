import numpy 
import scipy.sparse.linalg as linalg

import initial_conditions_2D

import matplotlib
from matplotlib import pyplot as plt



def get_boundary_nodes(initialisation, num_nodes):
    """
    Get a dictionary that contains lists of the nodes indices of 
    nodes that we want to satisfy the inlet 
    boundary conditions and ones we want so satisfy the outlet 
    boundary conditions. 
    The result will be fed into the algebraic equation that finds
    the pressure. 

    Parameters 
    ------
    - initialisation: str 
        String describing the structure of the cell. 
    - num_nodes: int 
        Number of nodes in the cell.

    Returns
    -----
    - boundary_nodes: dict
        boundary_nodes_2["inlet"][i]  = the ith inlet node index
        boundary_nodes_2["outlet"][i] = the ith outlet node index
    """
    if initialisation == "4_reg_prescribed" or initialisation=="4-reg":
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
    boundary_nodes_2 = {}
    boundary_nodes_2["inlet"]  = inlet_nodes_1
    boundary_nodes_2["outlet"] = outlet_nodes_1
    return boundary_nodes_2



def get_pressure_problem(cond_4, boundary_nodes_2):
    """
    Get the left and right hand side of 
    the linear problem that gives pressure at each time step.
    
    Parameters 
    -----
    - boundary_nodes_2: dict 
        boundary_nodes_2["inlet"][i] = ith inlet node
        boundary_nodes_2["outlet"][i] = ith outlet node
    - cond_4: numpy.ndarray
        cond_tabl_5[i,j,r,m] = conductance from i to j, where j is at reference references[r] 
        in direction directions[m] relative to i.
    
    Returns
    -----
    - lhs_2: numpy.ndarray
        Left matrix of linear pressure problem. 
    - rhs_1: numpy.ndarray
        Right vector of linear pressure problem.
    """
    # Parameters 
    # ---------
    num_nodes = len(cond_4[:,0,0,0])
    num_refs  = len(cond_4[0,0,0,:])

    # lhs
    # Expand pressure so that can multiply
    lhs_4 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_refs))
    for r0 in range(num_refs):
        for r1 in range(num_refs):
            lhs_4[:,:,r0,r1] = cond_4[:,:,r0,r1]-numpy.diag(numpy.sum(a=cond_4[:,:,r0,r1], axis=1))

    lhs_3 = numpy.sum(a=lhs_4,axis=3)
    lhs_2 = numpy.sum(a=lhs_3,axis=2)
    
    # rhs
    rhs_1 = numpy.zeros(num_nodes) 

    # boundary conditions
    # incoming pressures are 1, outgoing are zero
    inlet_nodes_1 = boundary_nodes_2["inlet"]
    outlet_nodes_1 =  boundary_nodes_2["outlet"]
    for inlet_node in inlet_nodes_1:
        lhs_2[inlet_node,:]  = numpy.zeros(num_nodes)
        lhs_2[inlet_node, inlet_node]   = 1
        rhs_1[inlet_node]  = 1

    for outlet_node in outlet_nodes_1:        
        lhs_2[outlet_node,:] = numpy.zeros(num_nodes)
        lhs_2[outlet_node,outlet_node] = 1
        rhs_1[outlet_node] = 0

    return (lhs_2,rhs_1)


def get_pressure_solution(lhs_2,rhs_1):
    """
    Get the solution of the pressure problem, whcih is a vector 
    where each element is the pressure at the correspondingly 
    indexed node.

    Parameters
    -----
    - lhs_2: numpy.ndarray
        Left matrix of linear pressure problem. 
    - rhs_1: numpy.ndarray
        Right vector of linear pressure problem.

    Returns
    -----
    - pres_1: numpy.ndarray
        pres_1[i] = pressure at node nodes[i].
    """ 
    pres_1 = linalg.lsqr(A=lhs_2,b=rhs_1)[0]

    return pres_1



def make_initial_network(num_nodes:int, num_refs:int, num_rows:int, num_cols:int, is_periodic:bool, initialisation:str, mu:float, sigma:float, boundary_nodes_2:dict, conc_in:float):
    """
    """
    # Get boundary nodes
    # -----
    inlet_nodes_1 = boundary_nodes_2["inlet"]
    outlet_nodes_1 = boundary_nodes_2["outlet"]
    
    # Define initial conc and volu
    # -----
    # Note: inlet and outlet nodes will have to be corrected for boundary condition
    volu_init_3 = numpy.ones(shape=(num_nodes,num_rows,num_cols))
    conc_init_3 = numpy.zeros(shape=(num_nodes,num_rows,num_cols))

    # Define initial cond
    # -----
    cond_init_6 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_refs,num_rows,num_cols))
    for i_cell in range(num_rows):
        for j_cell in range(num_cols):
            if initialisation == "4-reg":
                cond_init_6[:,:,:,:,i_cell,j_cell] = initial_conditions_2D.four_reg(num_nodes=num_nodes,num_refs=num_refs,mu=sigma,sigma=sigma)
            else: 
                raise Exception("Can only make initial network if initialisation=='4-reg'. Write make_initial_network() for new initialisation.")
            
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
    
    return (cond_init_6,conc_init_3,volu_init_3)



def get_flux_and_heav_and_conc_or(cond_6,pres_3,conc_3):
    """
    - cond_6: numpy.ndarray
        cond_4[i,j,r0,r1,i_c,j_c]
    - pres_3: numpy.ndarray
        pres_1[i,i_c,j_c]
    """
    # Parameters 
    # -----
    num_nodes = len(cond_6[:,0,0,0,0,0])
    num_refs = len(cond_6[0,0,:,0,0,0])
    num_rows = len(cond_6[0,0,0,0,:,0])
    num_cols = len(cond_6[0,0,0,0,0,:])
    tol=1E-6


    pres_i_4 = numpy.repeat(a=pres_3[:,numpy.newaxis,:,:], repeats=num_nodes, axis=1) # matrix where each row is pres_1
    pres_j_4 = numpy.repeat(a=pres_3[numpy.newaxis,:,:,:], repeats=num_nodes, axis=0) # matrix where each col is pres_1

    conc_i_4 = numpy.repeat(a=conc_3[:,numpy.newaxis,:,:], repeats=num_nodes, axis=1) # matrix where each row is conc_1
    conc_j_4 = numpy.repeat(a=conc_3[numpy.newaxis,:,:,:], repeats=num_nodes, axis=0) # matrix where each col is conc_1

    flux_6 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_refs,num_rows,num_cols))
    heav_ij_6 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_refs,num_rows,num_cols))
    heav_ji_6 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_refs,num_rows,num_cols))
    conc_or_6 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_refs,num_rows,num_cols))
    for r0 in range(num_refs):
        for r1 in range(num_refs):
            for i_c in range(num_rows):
                for j_c in range(num_cols):
                    pdif_2 = pres_i_4[:,:,i_c,j_c]-pres_j_4[:,:,i_c,j_c]
                    flux_2 = cond_6[:,:,r0,r1,i_c,j_c]*pdif_2

                    heav_ij_2 = (flux_2>+tol)*numpy.ones_like(flux_2)
                    heav_ji_2 = (flux_2<-tol)*numpy.ones_like(flux_2)

                    flux_6[:,:,r0,r1,i_c,j_c] = flux_2[:,:]
                    heav_ij_6[:,:,r0,r1,i_c,j_c] = heav_ij_2[:,:]
                    heav_ji_6[:,:,r0,r1,i_c,j_c] = heav_ji_2[:,:]

                    conc_or_6[:,:,r0,r1,i_c,j_c] = conc_i_4[:,:,i_c,j_c]*heav_ij_2+conc_j_4[:,:,i_c,j_c]*heav_ji_2

    return (flux_6,heav_ij_6,heav_ji_6,conc_or_6)



def get_concentration(conc_3,pres_3,volu_3,cond_6,adhe_6,i_c,j_c,dt):
    """
    Get concentration at node (i,i_c,j_c)
    - conc_3: numpy.ndarray
        conc_1[i,i_c,j_c]
    - pres_3: numpy.ndarray
        pres_1[i,i_c,j_c]
    - volu_1: numpy.ndarray
        volu_3[i,i_c,j_c]
    - cond_6: numpy.ndarray
        cond_4[i,j,r0,r1,i_c,j_c]
    - adhe_6: numpy.ndarray
        adhe_4[i,j,r0,r1,i_c,j_c]
    """
    # Parameters 
    # -----
    num_nodes = len(conc_3[:,0,0])
    num_refs = len(cond_6[0,0,:,0,0,0])

    # Get functions of rhs
    # -----
    (flux_6,heav_ij_6,heav_ji_6,_conc_or_6) = get_flux_and_heav_and_conc_or(cond_6=cond_6,pres_3=pres_3,conc_3=conc_3)

    # Reshape conc for multiplication 
    # -----    
    conc_4 = numpy.repeat(a=conc_3[:,numpy.newaxis,:,:],repeats=num_nodes,axis=1) # add j axis
    conc_5 = numpy.repeat(a=conc_4[:,:,numpy.newaxis,:,:],repeats=num_refs,axis=2) # add r0 axis
    conc_6 = numpy.repeat(a=conc_5[:,:,:,numpy.newaxis,:,:],repeats=num_refs,axis=3) # add r1 axis


    inte_6 = (numpy.ones_like(adhe_6)-adhe_6)*(-flux_6)*conc_6*heav_ji_6 - flux_6*conc_6*heav_ij_6
    inte_5 = numpy.sum(a=inte_6,axis=3)
    inte_4 = numpy.sum(a=inte_5,axis=2)
    inte_3 = numpy.sum(a=inte_4,axis=1)
    conc_1 = conc_3[:,i_c,j_c] + dt*(1/volu_3[:,i_c,j_c])*inte_3[:,i_c,j_c]
    return conc_1



def get_conductance(conc_3,pres_3,cond_6,adhe_6,i_c,j_c,dt):
    """
    """
    beta=1.0

    (flux_6,_heav_ij_6,_heav_ji_6,conc_or_6) = get_flux_and_heav_and_conc_or(cond_6=cond_6,pres_3=pres_3,conc_3=conc_3)

    cond_4 = cond_6[:,:,:,:,i_c,j_c] - dt*2*beta*abs(flux_6[:,:,:,:,i_c,j_c])*conc_or_6[:,:,:,:,i_c,j_c]*adhe_6[:,:,:,:,i_c,j_c]*(cond_6[:,:,:,:,i_c,j_c]**(1/2))
    return cond_4

if __name__ == "__main__":
    num_nodes = 9
    num_refs  = 3
    initialisation = "4-reg"
    mu = 0.5
    sigma = 0.3
    num_rows = 3
    num_cols = 3
    is_periodic = True

    cond_init_4 = initial_conditions_2D.four_reg(num_nodes=num_nodes, num_refs=num_refs, mu=mu, sigma=sigma)

    boundary_nodes_2 = get_boundary_nodes(initialisation=initialisation,num_nodes=num_nodes)
    #boundary_nodes_2["inlet"] = []
    #boundary_nodes_2["outlet"] = []
    (lhs_2,rhs_1)    = get_pressure_problem(cond_4=cond_init_4, boundary_nodes_2=boundary_nodes_2)
    pres_1           = get_pressure_solution(lhs_2=lhs_2,rhs_1=rhs_1)
    #print(lhs_2)
    #print(rhs_1)
    print(pres_1)
    #plt.plot(pres_1[0:int(numpy.sqrt(num_nodes))])
    #plt.show()

    (cond_init_6,conc_init_3,volu_init_3) = make_initial_network(num_nodes=num_nodes, num_refs=num_refs,
                                                                 num_rows=num_rows,num_cols=num_cols,
                                                                 is_periodic=is_periodic,
                                                                 initialisation=initialisation,
                                                                 mu=mu,sigma=sigma,
                                                                 boundary_nodes_2=boundary_nodes_2,conc_in=1.0)
    
    