import numpy
import scipy.sparse.linalg as linalg

import scipy.optimize as optimize



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
        leng_1[m] = length of filter in direction directions[m].
    
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
            #csol_3[k,:,m] = linalg.lsqr(A=a_2,b=b_1)[0]
            sol = optimize.lsq_linear(A=a_2,b=b_1)
            csol_3[k,:,m] = sol.x

    return csol_3



def get_delta(csol_3: numpy.ndarray, refs_2:numpy.ndarray, leng_1: numpy.ndarray):
    """
    Given the cell problem solution, the references, and the lengths, 
    return the parameter delta.

    Parameters
    ----------
    - csol_3: numpy.ndarray
        The solution of the cell problem, W in notes. csol_3[k,i,m] = element nodes[i] of the solution of 
        the cell problem at concentration max-concentrations[k] in direction dimensions[m].
    - refs_2: numpy.ndarray
        refs_2[r,m] = reference-distance references[r] in direction directions[m]. 
        For example, references = {-1,0,+1} and directions = {0,1} (for 2D problem)    
    - leng_1: numpy.ndarray
        leng_1[m] = length of filter in direction directions[m].
    
    Returns 
    -------
    - delt_5: numpy.ndarray
        The parameter delta between nodes i and j with refernce references[r] in direction directions[m]
        at concentration max-concentrations[k], 
        so that delt_5[k,i,j,r,m] = csol_3[k,i,m] - (csol_3[k,j,m] + refs_2[r,m]*leng_1[m]), by defn.
    """

    # Get params
    # -----
    num_concs = len(csol_3[:,0,0])
    num_nodes = len(csol_3[0,:,0])
    num_refs  = len(refs_2[:,0])
    num_dims  = len(csol_3[0,0,:])


    # Make array to be filled
    # -----
    delt_5 = numpy.zeros(shape=(num_concs,num_nodes,num_nodes,num_refs,num_dims))
    
    
    # Fill using definition of delta
    # -----
    for k in range(num_concs):
        for i in range(num_nodes):
            for j in range(num_nodes):
                for r in range(num_refs):
                    for m in range(num_dims):
                        delt_5[k,i,j,r,m] = csol_3[k,i,m] - (csol_3[k,j,m] + refs_2[r,m]*leng_1[m])

    return delt_5



def get_heaviside(delt_5: numpy.ndarray):
    """
    Given delta parameter, indicate whether it is greater 
    or smaller than zero in the m direction.

    Parameters 
    ----------
    - delt_5: numpy.ndarray
        The parameter delta between nodes i and j with refernce references[r] in direction directions[m]
        at concentration max-concentrations[k], 
        so that delt_5[k,i,j,r,m] = csol_3[k,i,m] - (csol_3[k,j,m] + refs_2[r,m]*leng_1[m]), by defn.

    Returns 
    -------
    - heav_5: numpy.ndarray
        The parameter heaviside, which indicates whether there is flow from i to j, 
        so that heav_5 = indictaion of flow from i to j with 
        reference references[r] in direction directions[m] at concentration max-concentrations[k].

    """
    
    heav_5 = (-delt_5>0).astype(int)
    # Use delta to make heaviside
    # NB! H_ij^r = heav(delt_ij^r*dpdx) = heav(-delt_ijr) = heav(delt_ji(-r)), 
    # since dpdx<0 when flow from left to right.

    return heav_5



def get_permeability_and_deposition(refs_2: numpy.ndarray, 
                                    cond_tabl_5: numpy.ndarray,
                                    adhe_tabl_5: numpy.ndarray,
                                    delt_5: numpy.ndarray,
                                    heav_5: numpy.ndarray, 
                                    leng_1: numpy.ndarray, 
                                    v: float, 
                                    cond_init_4: numpy.ndarray):
    """
    Given the working parameters, return the permeability as a spatial matrix, and
    the deposition parameter as a spatial vector. That is, return information about these two 
    parameters in each direction.

    Parameters 
    ----------
    - refs_2: numpy.ndarray
        refs_2[r,m] = reference-distance references[r] in direction directions[m]. 
        For example, references = {-1,0,+1} and directions = {0,1} (for 2D problem.
    - cond_tabl_5: numpy.ndarray
        cond_tabl_5[k,i,j,r,m] = conductance from i to j, where j is at reference references[r] 
        in direction directions[m] relative to i, at concentration max-concentrations[k].
    - adhe_tabl_5: numpy.ndarray    
        adhe_tabl_5[k,i,j,r,m] = adhesivity from i to j, where j is at reference references[r] 
        in direction directions[m] relative to i, at concentration max-concentrations[k].
    - delt_5: numpy.ndarray
        The parameter delta between nodes i and j with refernce references[r] in direction directions[m]
        at concentration max-concentrations[k], 
        so that delt_5[k,i,j,r,m] = csol_3[k,i,m] - (csol_3[k,j,m] + refs_2[r,m]*leng_1[m]), by defn.
    - heav_5: numpy.ndarray
        The parameter heaviside, which indicates whether there is flow from i to j, 
        so that heav_5 = indictaion of flow from i to j with 
        reference references[r] in direction directions[m] at concentration max-concentrations[k].
    - leng_1: numpy.ndarray
        leng_1[m] = length of filter in direction directions[m].
    - v: float 
        Parameter.
    - cond_init_4: numpy.ndarray
        The initial conductance, so that cond_init_4[i,j,r,m] = initial conductance on edge ijrn.
        NB! TODO: This shouldn't be in function, really it is conductance at time, but have a problem 
        when edge blocks since that goes to zero, so no adhesivity is recorded. Fix this.

    Returns 
    -------- 
    - perm_3: numpy.ndarray
        The permeability. perm_3[k,m,n] = the directional directions[mn] element of the permeability 
        at concentration max-concentrations[k].
    - depo_2: numpy.ndarray
        The deposition parameter. depo_2[k,m] = the direction directions[m] element of the deposition 
        parameter at concentration max-concentrations[k].
    """ 

    # Define params
    # -----
    num_concs = len(cond_tabl_5[:,0,0,0,0])
    num_nodes = len(cond_tabl_5[0,:,0,0,0])
    num_refs  = len(cond_tabl_5[0,0,0,:,0])
    num_dims  = len(cond_tabl_5[0,0,0,0,:])


    # Make array to fill with permeability and deposition-parameter integrands
    # -----
    perm_inte_7 = numpy.zeros(shape=(num_concs,num_nodes,num_nodes,num_refs,num_dims,num_dims,num_dims))
    # perm_inte_7[k,i,j,r,m,a,n]
    depo_inte_6 = numpy.zeros(shape=(num_concs,num_nodes,num_nodes,num_refs,num_dims,num_dims))
    # depo_inte_6[k,i,j,r,m,a]


    # Get integrand of permeability and integrand of deposition parameter
    # ------
    for k in range(num_concs):
        for r in range(num_refs):
            for m in range(num_dims):
                for a in range(num_dims):
                    depo_inte_6[k,:,:,r,m,a] = cond_init_4[:,:,r,a]*(-delt_5[k,:,:,r,m])*adhe_tabl_5[k,:,:,r,a]*(numpy.ones_like(heav_5[k,:,:,r,a])-heav_5[k,:,:,r,a])
                    for n in range(num_dims):
                        perm_inte_7[k,:,:,r,m,a,n] = refs_2[r,m]*cond_tabl_5[k,:,:,r,a]*(-delt_5[k,:,:,r,n])

    


    # Get permeability and deposition without prefactors
    # -----
    perm_6 = numpy.sum(a=perm_inte_7, axis=5) # sum over a
    perm_5 = numpy.sum(a=perm_6, axis=3) # sum over r
    perm_4 = numpy.sum(a=perm_5, axis=2) # sum over j
    perm_3 = numpy.sum(a=perm_4, axis=1) # sum over i
    # perm_3[k,m,n]    

    depo_5 = numpy.sum(a=depo_inte_6, axis=5) # sum over a
    depo_4 = numpy.sum(a=depo_5, axis=3) # sum over r
    depo_3 = numpy.sum(a=depo_4, axis=2) # sum over j
    depo_2 = numpy.sum(a=depo_3, axis=1) # sum over i
    # depo_2[k,m]

    # Multiply permeability and deposition-parameter by prefactors
    # -----
    for m in range(num_dims):
        for n in range(num_dims):
            perm_3[:,m,n] = 0.5*(leng_1[m]/numpy.prod(leng_1))*perm_3[:,m,n]

    depo_2 = (1/v)*depo_2


    return (perm_3, depo_2)
