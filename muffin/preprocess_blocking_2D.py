import numpy
import scipy.sparse.linalg as linalg

import scipy.optimize as optimize

"""
Module of functions that are used specifically for preprocessing in the
blocking case. 
These functions are used in the run_preprocess module with 
preprocess functions that are common between 
blocking and deposition, which are stored in the preprocess_2D module.

These functions are used to return 
- conductance 
- adherence
- delta 
- csol 

at particular values of cmax, which are indexed by k.
"""


def get_conductance_and_adhesivity(conc_max_disc_1: numpy.ndarray, 
                                   cond_init_4: numpy.ndarray, 
                                   adhe_init_4: numpy.ndarray, 
                                   alpha: float):
    """
    Given the maximum concentrations, the initial conductances and adhesivites, and 
    the threshold above which an edge blocks, return the conductance and adhesivity 
    that results from each concentration. 

    Parameters 
    ----------
    - conc_max_disc_1: numpy.ndarray
        List of max concentration, so that conc_max_disc_1[k] = max-concentrations[k].
    - cond_init_4: numpy.ndarray
        cond_init_4[i,j,r0,r1] = initial conductance from i to j, where j is at reference references[r0,r1] 
        in direction directions[m] relative to i.
    - adhe_init_4: numpy.ndarray  
        adhe_init_4[i,j,r0,r1] = initial adhesivity from i to j, where j is at reference references[r0,r1] 
        in direction directions[m] relative to i.
    - alpha: float
        alpha = threshold value, fraction above which the edge blocks.

    Returns
    -------
    - cond_tabl_5: numpy.ndarray
        cond_tabl_5[k,i,j,r0,r1] = conductance from i to j, where j is at reference references[r0,r1] 
        relative to i, at concentration max-concentrations[k].
    - adhe_tabl_5: numpy.ndarray    
        adhe_tabl_5[k,i,j,r0,r1] = adhesivity from i to j, where j is at reference references[r0,r1] 
        relative to i, at concentration max-concentrations[k].
    

    """
    # Define params
    # -----
    num_concs = len(conc_max_disc_1)
    num_nodes = len(cond_init_4[0,:,0,0])
    num_refs  = len(cond_init_4[0,0,:,0])


    # Resize for multiplication
    # -----
    cond_tabl_5 = numpy.repeat(a=cond_init_4[numpy.newaxis,:,:,:,:], repeats=num_concs, axis=0) # create conductance table to be filled
    # cond_tabl_5[k,i,j,r0,r1] = G_ij^r0r1 at c[k]
    
    adhe_tabl_5 = numpy.repeat(a=adhe_init_4[numpy.newaxis,:,:,:,:], repeats=num_concs, axis=0) # create adhesivity table to be filled
    # adhe_tabl_5[k,i,j,r0,r1] = A_ij^r0r1 at c[k]


    # Set conductance and adhesivity in tables for each possible concentration value
    # -----
    for k in range(num_concs):
        conc_disc = conc_max_disc_1[k] # discrete concentration
        for i in range(num_nodes):
            for j in range(num_nodes):
                for r0 in range(num_refs):
                    for r1 in range(num_refs):            
                        cond = cond_tabl_5[k,i,j,r0,r1]
                        if cond != 0.0: # we don't need to worry about G_ij==0
                            #if conc_disc < alpha*cond or numpy.allclose(a=conc_disc,b=alpha*cond,rtol=1e-5,atol=1e-8):
                            #    pass
                            if conc_disc > alpha*cond:
                                #pass
                                cond_tabl_5[k,i,j,r0,r1] = 0.0
                                adhe_tabl_5[k,i,j,r0,r1] = 1.0
                            else: 
                                pass
                            #else: 
                            #    raise Exception
    
    return (cond_tabl_5, adhe_tabl_5)




def get_cell_problem(cond_tabl_5: numpy.ndarray, refs_2: numpy.ndarray, leng_1:numpy.ndarray):
    """
    Given a table of conductances at each max concentration, a set of references, 
    and a set of lengths, return the left and right hand sides of the cell problem.

    Parameters
    ----------
    - cond_tabl_5: numpy.ndarray
        cond_tabl_5[k,i,j,r0,r1] = conductance from i to j, where j is at reference references[r0,r1] 
        relative to i, at concentration max-concentrations[k].
    - refs_2: numpy.ndarray
        refs_2[r,m] = reference-distance references[r] in direction directions[m]. 
        For example, references = {-1,0,+1} and directions = {0,1} (for 2D problem)
        In notatioal form, this is r^m, which has two degrees of freedom: r and m. 
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
    num_dims  = len(leng_1[:])


    # Define integrands to fill
    # -----
    rhs_inte_6 = numpy.zeros(shape=(num_concs,num_nodes,num_nodes,num_refs,num_refs,num_dims))
    # rhs_inte_6[k,i,j,r0,r1,m].
    lhs_inte_5 = numpy.zeros(shape=(num_concs,num_nodes,num_nodes,num_refs,num_refs))
    # lhs_inte_5[k,i,j,r0,r1].


    # Build lhs and rhs
    # ------
    for k in range(num_concs):
        for r0 in range(num_refs):
            for r1 in range(num_refs):
                    
                # Get lhs integrand
                # -----
                lhs_inte_5[k,:,:,r0,r1] = cond_tabl_5[k,:,:,r0,r1] - numpy.diag(numpy.sum(a=cond_tabl_5[k,:,:,r0,r1], axis=1))
                

                # Get rhs integrand
                # -----                     
                for m in range(num_dims):

                    if m==0: 
                        r=r0
                    elif m==1:
                        r=r1
                    else: 
                        raise Exception("m != 0,1. This is impossible, since the problem is 2D.")
                
                    rhs_inte_6[k,:,:,r0,r1,m] = cond_tabl_5[k,:,:,r0,r1]*refs_2[r,m]*leng_1[m]
            
    
    # Sum over references
    # -----
    rhs_4 = -numpy.sum(a=numpy.sum(a=rhs_inte_6, axis=4), axis=3) # sum over r1 then r0
    # NB: rhs of cell problem has minus sign by definition.

    lhs_3 =  numpy.sum(a=numpy.sum(a=lhs_inte_5, axis=4), axis=3) # sum over r1 then r0

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
            #sol = optimize.lsq_linear(A=a_2,b=b_1)
            #csol_3[k,:,m] = sol.x

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
        The parameter delta between nodes i and j with reference references[r] in direction directions[m]
        at concentration max-concentrations[k]. 
        so that delt_5[k,i,j,r,m] = csol_3[k,i,m] - (csol_3[k,j,m] + refs_2[r,m]*leng_1[m]), by defn.
        Note that references[r,m] is numerical equivalent to r^m in the notation.
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
    
    #delt_5 = numpy.rint(delt_5)
    return delt_5