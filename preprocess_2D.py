import numpy
import scipy.sparse.linalg as linalg



def get_reference(max_ref_dist:int, num_dims:int):
    """
    Given the max distance between node connections, and 
    the number of dimensions in the problem, 
    return the reference matrix.

    Parameters 
    ----------
    - max_ref_dist: int
        Maximum number of cells between j and i.
    - num_dims: int
        Number of dimensions in problem.

    Returns
    -------
    - refs_2: numpy.ndarray
        refs_2[r,m] = reference-distance references[r] in direction directions[m]. 
        For example, references = {-1,0,+1} and directions = {0,1} (for 2D problem)

    """
    # Get refs_1
    # -----
    if max_ref_dist == 1:
        refs_1 = numpy.array([0.0,1.0,-1.0])
        # refs_1[r] = reference \in {-1,0,+1}, for example
    else: 
        raise Exception("max_ref_dist != 1. Need to write refs_1 for this new value.")
    
    # Get refs_2
    # -----
    refs_2 = numpy.repeat(a=refs_1[:,numpy.newaxis], repeats=num_dims, axis=1)
    
    return refs_2




def get_conductance_and_adhesivity(conc_max_disc_1: numpy.ndarray, 
                                   cond_init_4: numpy.ndarray, 
                                   adhe_init_4: numpy.ndarray, 
                                   alpha: float):
    """
    Given the maximum concentrations, the intial conductances and adhesivites, and 
    the threshold above which an edge blocks, return the conductance and adhesivity 
    that results from each concentration. 

    Parameters 
    ----------
    - conc_max_disc_1: numpy.ndarray
        List of max concentration, so that conc_max_disc_1[k] = max-concentrations[k].
    - cond_init_4: numpy.ndarray
        cond_init_4[i,j,r,m] = initial conductance from i to j, where j is at reference references[r] 
        in direction directions[m] relative to i.
    - adhe_init_4: numpy.ndarray  
        adhe_init_4[i,j,r,m] = initial adhesivity from i to j, where j is at reference references[r] 
        in direction directions[m] relative to i.
    - alpha: float
        alpha = threshold value, fraction aboce which the edge blocks.

    Returns
    -------
    - cond_tabl_5: numpy.ndarray
        cond_tabl_5[k,i,j,r,m] = conductance from i to j, where j is at reference references[r] 
        in direction directions[m] relative to i, at concentration max-concentrations[k].
    - adhe_tabl_5: numpy.ndarray    
        adhe_tabl_5[k,i,j,r,m] = adhesivity from i to j, where j is at reference references[r] 
        in direction directions[m] relative to i, at concentration max-concentrations[k].
    

    """
    # Define params
    # -----
    num_concs = len(conc_max_disc_1)
    num_nodes = len(cond_init_4[0,:,0,0])
    num_refs  = len(cond_init_4[0,0,:,0])
    num_dims  = len(cond_init_4[0,0,0,:])


    # Resize for multiplication
    # -----
    cond_tabl_5 = numpy.repeat(a=cond_init_4[numpy.newaxis,:,:,:,:], repeats=num_concs, axis=0) # create conductance table to be filled
    # cond_tabl_5[k,i,j,r,m] = G_ij^rm at c[k]
    
    adhe_tabl_5 = numpy.repeat(a=adhe_init_4[numpy.newaxis,:,:,:,:], repeats=num_concs, axis=0) # create adhesivity table to be filled
    # adhe_tabl_5[k,i,j,r,m] = A_ij^rm at c[k]


    # Set conductance and adhesivity in tables for each possible concentration value
    # -----
    for k in range(num_concs):
        conc_disc = conc_max_disc_1[k] # discrete concentration
        for i in range(num_nodes):
            for j in range(num_nodes):
                for r in range(num_refs):
                    for m in range(num_dims):            
                        cond = cond_tabl_5[k,i,j,r,m]
                        if cond != 0: # we don't need to worry about G_ij==0
                            if conc_disc < alpha*cond or numpy.allclose(a=conc_disc,b=alpha*cond,rtol=1e-5,atol=1e-8):
                                pass
                            elif conc_disc > alpha*cond:
                                #pass
                                cond_tabl_5[k,i,j,r,m] = 0
                                adhe_tabl_5[k,i,j,r,m] = 1
                            else: 
                                raise Exception
    return (cond_tabl_5, adhe_tabl_5)




def get_cell_problem(cond_tabl_5: numpy.ndarray, refs_2: numpy.ndarray, leng_1:numpy.ndarray):
    """
    Given a table of conductances at each max concentration, a set of references, 
    and a set of lengths, return the left and right hand sides of the cell problem.

    Parameters
    ----------
    - cond_tabl_5: numpy.ndarray
        cond_tabl_5[k,i,j,r,m] = conductance from i to j, where j is at reference references[r] 
        in direction directions[m] relative to i, at concentration max-concentrations[k].
    - refs_2: numpy.ndarray
        refs_2[r,m] = reference-distance references[r] in direction directions[m]. 
        For example, references = {-1,0,+1} and directions = {0,1} (for 2D problem)
    - leng_1: numpy.ndarray
    
    Returns
    -------
    - lhs_3: numpy.ndarray
        Left hand side of the cell problem, so that lhs_3[k,i,j] = left hand side of the cell problem for edge 
        i,j at concentration max-concentrations[k].
    - rhs_4: numpy.ndarray 
        Right hand side of the cell problem, so that rhs_4[k,i,j,m] = right hand side of the cell problem 
        for edge i,j at concentration max-concentrations[k] in direction m.
        Notice that rhs has one more dimension, since it depends on the direction.
    """

    # Define params 
    # -----
    num_concs = len(cond_tabl_5[:,0,0,0,0])
    num_nodes = len(cond_tabl_5[0,:,0,0,0])
    num_refs  = len(cond_tabl_5[0,0,0,:,0])
    num_dims  = len(cond_tabl_5[0,0,0,0,:])


    # Define integrands to fill
    # -----
    rhs_inte_6 = numpy.zeros(shape=(num_concs,num_nodes,num_nodes,num_refs,num_dims,num_dims))
    # rhs_inte_6[k,i,j,r,m,a], where a is dimension that'll be summed over.
    lhs_inte_5 = numpy.zeros(shape=(num_concs,num_nodes,num_nodes,num_refs,num_dims))
    # lhs_inte_5[k,i,j,r,m], and will sum over dimension m.


    # Build lhs and rhs
    # ------
    for k in range(num_concs):
        for r in range(num_refs):
            for m in range(num_dims):
                # Get lhs integrand
                # -----
                lhs_inte_5[k,:,:,r,m] = cond_tabl_5[k,:,:,r,m] - numpy.diag(numpy.sum(a=cond_tabl_5[k,:,:,r,m], axis=1))

                # Get rhs integrand
                # -----
                for a in range(num_dims):
                    rhs_inte_6[k,:,:,r,m,a] = cond_tabl_5[k,:,:,r,a]*refs_2[r,m]*leng_1[m]
    
    # Sum over references and dimensions
    # -----
    rhs_4 = -numpy.sum(a=numpy.sum(a=rhs_inte_6, axis=5), axis=3) # sum over a then r
    # NB: rhs of cell problem has minus sign by definition.

    lhs_3 =  numpy.sum(a=numpy.sum(a=lhs_inte_5, axis=4), axis=3) # sum over m then r

    return (lhs_3, rhs_4)



def get_cell_solution(lhs_3: numpy.ndarray, rhs_4: numpy.ndarray):
    """
    Given left and right hand sides of the cell problem, 
    find the cell solution at each max concentrationa and in each 
    direction.

    Parameters 
    ----------
    - lhs_3: numpy.ndarray
        Left hand side of the cell problem, so that lhs_3[k,i,j] = left hand side of the cell problem for edge 
        i,j at concentration max-concentrations[k].
    - rhs_4: numpy.ndarray 
        Right hand side of the cell problem, so that rhs_4[k,i,j,m] = right hand side of the cell problem 
        for edge i,j at concentration max-concentrations[k] in direction m.
        Notice that rhs has one more dimension, since it depends on the direction.
    
    Returns
    -------
    - csol_3: numpy.ndarray
        The solution of the cell problem, W in notes. csol_3[k,i,m] = element nodes[i] of the solution of 
        the cell problem at concentration max-concentrations[k] in direction dimensions[m].
    """

    # Define params 
    # -----
    num_concs = len(rhs_4[:,0,0,0])
    num_nodes = len(rhs_4[0,:,0,0])
    num_dims  = len(rhs_4[0,0,0,:])

    
    # Define array to be filled
    # -----
    csol_3 = numpy.zeros(shape=(num_concs,num_nodes,num_dims))
    

    # Get solution
    # -----
    for k in range(num_concs):
        a_2 = lhs_3[k,:,:]
        for m in range(num_dims):
            b_1 = numpy.sum(a=rhs_4[k,:,:,m], axis=1) # sum over j
            csol_3[k,:,m] = linalg.lsqr(A=a_2,b=b_1)[0]


    return csol_3


