import numpy 
import scipy
import scipy.sparse as sparse

def get_conductance_and_adhesivity(conc_max_discs_1, cond_init_3, adhe_init_3, alpha):
    """
    Given initial conditions for the conductance and adhesivity at each edge, 
    and a list of max concentrations, return the conductance and adhesivity that 
    would result from each max concentration.

    Parameters 
    ----------
    - conc_max_discs_1: numpy.ndarray 
        Max concentration values to be tested.
    - cond_init_3: numpy.ndarray
        cond_init_3[i,j,l] = initial conductance at edge i,j, r[l].
    - adhe_init_3: numpy.ndarray
        adhe_init_3[i,j,l] = initial adhesivity at edge i,j, r[l].
    
    Returns
    -------
    - cond_tabl_4: numpy.ndarray
        cond_tabl_4[k,i,j,l] = conductance at edge i,j, r[l] that results from concentration max_conc_discs_1[k].
    - adhe_tabl_4: numpy.ndarray
        adhe_tabl_4[k,i,j,l] = adhesivity at edge i,j, r[l] that results from concentration max_conc_discs_1[k].
    """

    # Define params
    # -----
    num_concs = len(conc_max_discs_1)
    num_nodes = len(cond_init_3[0,:,0])
    num_refs = len(cond_init_3[0,0,:])


    # Resize for multiplication
    # -----
    cond_tabl_4 = numpy.repeat(a=cond_init_3[numpy.newaxis,:,:,:], repeats=num_concs, axis=0) # create conductance table to be filled
    # cond_tabl_4[k,i,j,r] = G_ij^r at c[k]
    
    adhe_tabl_4 = numpy.repeat(a=adhe_init_3[numpy.newaxis,:,:,:], repeats=num_concs, axis=0) # create adhesivity table to be filled
    # adhe_tabl_4[k,i,j,r] = A_ij^r at c[k]


    # Set conductance and adhesivity in tables for each possible concentration value
    # -----
    for k in range(num_concs):
        conc_disc = conc_max_discs_1[k] # discrete concentration
        for i in range(num_nodes):
            for j in range(num_nodes):
                for l in range(num_refs):            
                    cond = cond_tabl_4[k,i,j,l]
                    if cond != 0: # we don't need to worry about G_ij==0
                        if conc_disc < alpha*cond or numpy.allclose(a=conc_disc,b=alpha*cond,rtol=1e-5,atol=1e-8):
                            pass
                        elif conc_disc > alpha*cond:
                            #pass
                            cond_tabl_4[k,i,j,l] = 0
                            adhe_tabl_4[k,i,j,l] = 1
                        else: 
                            raise Exception
    return (cond_tabl_4, adhe_tabl_4)




def get_cell_problem(refs_1, cond_tabl_4, length):
    """
    Given conductances, return the left and right hand sides 
    of the cell problem (the linear problem to solve).

    Parameters 
    ---------
    - refs_1: numpy.ndarray
        A list of all cell references ([0,1,-1] for networks that are only joined to neighbouring cells).
    - cond_tabl_4: numpy.ndarray
        cond_tabl_4[k,i,j,l] = conductance at edge i,j, r[l] that results from concentration max_conc_discs_1[k].
    - length: float 
        Dimensionless length of filter.
    
    Returns 
    -------
    - lhs_3: numpy.ndarray
        lhs_3[k,i,j] = left hand side of cell problem at concentration max_conc_discs_1[k].
    - rhs_3: numpy.ndarray
        rhs_3[k,i,j] = right hand side of cell problem at concentration max_conc_discs_1[k].
    """
    # Define params
    #-----
    num_nodes = len(cond_tabl_4[0,:,0,0])
    num_concs = len(cond_tabl_4[:,0,0,0])
    num_refs  = len(cond_tabl_4[0,0,0,:])


    # Repeat refs for multiplication in cell problem
    # -----
    refs_2 = numpy.repeat(a=refs_1[numpy.newaxis,:], repeats=num_nodes, axis=0) # add j axis 
    refs_3 = numpy.repeat(a=refs_2[numpy.newaxis,:,:], repeats=num_nodes, axis=0) # add i axis
    refs_4 = numpy.repeat(a=refs_3[numpy.newaxis,:,:,:], repeats=num_concs, axis=0) # add k axis
    # refs_4[k,i,j,r] = r (repeated for multiplication)


    # Get rhs of cell problem
    # -----
    rhs_4 = length*numpy.multiply(refs_4,cond_tabl_4) # inside of sum on rhs of cell problem
    rhs_3 = -numpy.sum(a=rhs_4,axis=3) # sum over r


    # Get lhs of cell problem
    # -----
    # TODO: do this without k loop -- I should be able to build this lhs without looking through k
    lhs_4 = numpy.zeros_like(rhs_4)
    for k in range(num_concs):
        for l in range(num_refs):
            # Form left part of lhs
            cond_2 = cond_tabl_4[k,:,:,l]
            # Form right part of lhs
            cond_sum_1 = numpy.sum(a=cond_2,axis=1) # sum over j
            cond_sum_2 = numpy.diag(cond_sum_1)
            # Subtract second part from first part
            lhs_2 = cond_2 - cond_sum_2
            # Insert into storage
            lhs_4[k,:,:,l] = lhs_2
    lhs_3 = numpy.sum(a=lhs_4,axis=3) # sum over r

    return (lhs_3, rhs_3)




def get_cell_solution(lhs_3,rhs_3):
    """
    Given the left and right hand sides of the cell problem, 
    return the cell solution. 

    Parameters 
    ---------
    - lhs_3: numpy.ndarray
        lhs_3[k,i,j] = left hand side of cell problem at concentration max_conc_discs_1[k].
    - rhs_3: numpy.ndarray
        rhs_3[k,i,j] = right hand side of cell problem at concentration max_conc_discs_1[k].

    Returns
    ---------
    - csol_2: numpy.ndarray
        csol[k,i] = i^{th} element of the cell solution at concentration max_conc_discs_1[k]. 
        That is, W_i at c[k].
    """
    # Define params
    #-----
    num_concs = len(lhs_3[:,0,0])
    num_nodes = len(lhs_3[0,:,0])


    # Define storage for solution
    # ----- 
    csol_2 = numpy.zeros(shape=(num_concs,num_nodes)) # cell solution W[k,i], is W_i at the k^th concentration


    # Solve the cell problem for each possible conc value
    # ------
    for k in range(num_concs):
        a_2 = lhs_3[k,:,:] # a_2[i,j] = lhs of cell problem at max_conc_discs_1[k]
        b_1 = numpy.sum(a=rhs_3[k,:,:],axis=1) # b_1[i] = rhs of cell problem at max_conc_discs_1[k] (summing over j here)
        
        #if k==5:
        #    print("a_2: \n{}".format(a_2))
        #    print("b_1: \n{}".format(b_1))
        # ---- solve ----
        #print("k: \n{}".format(k))
        #print("a_2: \n{}".format(a_2))
        #print("b_1: \n{}".format(b_1))
        #csol_1 = numpy.linalg.solve(a=a_2,b=b_1)
        #csol_1 = optimize.lsq_linear(A=a_2,b=b_1)
        csol_1 = sparse.linalg.lsqr(A=a_2,b=b_1)

        #csol_2[k,:] = csol_1
        #csol_2[k,:] = csol_1.x
        csol_2[k,:] = csol_1[0]

    return csol_2



def get_delta(csol_2, refs_1, length):
    """
    Given the cell solution, return the parameter Delta, 
    which is the homogenised flux, and represents microscale
    pressure difference per unit pressure gradient.

    Parameters 
    ---------
    - csol_2: numpy.ndarray
        csol[k,i] = i^{th} element of the cell solution at concentration max_conc_discs_1[k]. 
        That is, W_i at c[k].
    - refs_1: numpy.ndarray
        A list of all cell references ([0,1,-1] for networks that are only joined to neighbouring cells).
    - length: float 
        Dimensionless length of filter.

    Returns
    --------
    - delt_4: numpy.ndarray
        delt_4[k,i,j,l] = delta_ij^r[l] at concentration max_conc_discs_1[k].
    """

    # Define params 
    # ------
    num_concs = len(csol_2[:,0])
    num_nodes = len(csol_2[0,:])
    num_refs  = len(refs_1)

    # Define storage for solution
    # ------
    delt_4 = numpy.zeros(shape=(num_concs,num_nodes,num_nodes,num_refs)) 
    # delt_4[k,i,j,l] is delta_ij^r[l] at concentration c[k]
    # Note that we'll need delta_ji^{-r}, which is the negative of this object

    for k in range(num_concs):
        csol_1 = csol_2[k,:]
        csol_iway_2 = numpy.repeat(a=csol_1[:,numpy.newaxis],repeats=num_nodes,axis=1)
        csol_jway_2 = numpy.repeat(a=csol_1[numpy.newaxis,:],repeats=num_nodes,axis=0)
        csol_diff_2 = csol_iway_2 - csol_jway_2
        for l in range(num_refs):
            ref = refs_1[l]
            ref_2 = ref*numpy.ones(shape=(num_nodes,num_nodes))
            delt_2 = csol_diff_2 - length*ref_2
            delt_4[k,:,:,l] = delt_2
    
    return delt_4



def get_heaviside(delt_4):
    """
    Given the parameter delta, 
    return the parameter heaviside, which indicates whether the 
    flow is from i to j.

    Parameters 
    ----------
    - delt_4: numpy.ndarray
        delt_4[k,i,j,l] = delta_ij^r[l] at concentration max_conc_discs_1[k].
    
    Returns
    ----------
    - heav_4: numpy.ndarray
        heav_4[k,i,j,l] = indicates (with 1,0) whether or not delta is larger than zero at 
        concentration max_conc_discs_1[k]. That is, whether the pressure at i 
        is larger than the pressure at j for edge (i,j,r[l]) at concentration 
        max_conc_discs_1[k].
    """
    # Use delta to make heaviside
    # NB! H_ij^r = heav(delt_ij^r*dpdx) = heav(-delt_ijr) = heav(delt_ji(-r)), since dpdx<0 when flow from left to right.         
    heav_4 = (-delt_4>0).astype(int)

    return heav_4




def get_permeability_and_deposition(cond_tabl_4, adhe_tabl_4, refs_1, delt_4, heav_4, cond_init_3, length):
    """
    Given a set of conductances, adhesivities, cell references, 
    deltas, heavisides, and initial conductances, 
    return the associated permeability and deposition parameter for each 
    element of the set.
    To get the permeability and deposition parameter:
    - create the 'sum integrand' of the two sums,
    - sum these integrands over i and j,
    - multiply by the coefficient and sum over the cell reference.

    Parameters 
    ----------
    - cond_tabl_4: numpy.ndarray
        cond_tabl_4[k,i,j,l] = conductance at edge i,j, r[l] that results from concentration max_conc_discs_1[k].
    - adhe_tabl_4: numpy.ndarray
        adhe_tabl_4[k,i,j,l] = adhesivity at edge i,j, r[l] that results from concentration max_conc_discs_1[k].
    - refs_1: numpy.ndarray
        A list of all cell references ([0,1,-1] for networks that are only joined to neighbouring cells).
    - delt_4: numpy.ndarray
        delt_4[k,i,j,l] = delta_ij^r[l] at concentration max_conc_discs_1[k].
    - cond_init_3: numpy.ndarray
        cond_init_3[i,j,l] = initial conductance at edge i,j, r[l].
    - v: float
        Sum of volumes of nodes in cell.
    
    Returns
    -------
    - perm_prep_1: numpy.ndarray
        Set of permeabilities, so that perm_prep_1[k] = permeability with concentration of max_conc_discs_1[k].
    - depo_prep_1: numpy.ndarray
        Set of deposition parameters, so that depo_prep_1[k] = depositions parameter with concentration of max_conc_discs_1[k].

    """
    # Define params 
    # -----
    num_concs = len(cond_tabl_4[:,0,0,0])
    num_refs  = len(cond_tabl_4[0,0,0,:])
    num_nodes = len(cond_tabl_4[0,:,0,0])

    refs_2 = numpy.repeat(a=refs_1[numpy.newaxis,:], repeats=num_nodes, axis=0) # add j axis 
    refs_3 = numpy.repeat(a=refs_2[numpy.newaxis,:,:], repeats=num_nodes, axis=0) # add i axis
    refs_4 = numpy.repeat(a=refs_3[numpy.newaxis,:,:,:], repeats=num_concs, axis=0) # add k axis

    # Define inside of permeability and deposition parameters sums in their definitions
    # -----
    perm_inte_4 = refs_4*cond_tabl_4*(-delt_4) # the inside of the sum for k, which is G_ij^r[l]*(-delta_ij^r[l]) at c[k]

    cond_init_4 = numpy.repeat(a=cond_init_3[numpy.newaxis,:,:,:], repeats=num_concs, axis=0)
    heav_reversed_4 = numpy.ones_like(heav_4)-heav_4
    depo_inte_4 = cond_init_4*(-delt_4)*adhe_tabl_4*heav_reversed_4 # the inside of the sum for j, which is G_ij^r[l]*(-delta_ij^r[l])*A_ij^r[l]*(1-H_ij^r[l]) at c[k]
    # TODO: THIS SHOULD NOT BE COND_init because it shoudln't rely on initial condition 
    #print("cond_tabl_4[k,:,:,l]: \n{}".format(cond_tabl_4[0,:,:,0]))
    #print("perm_inte_4[k,:,:,l]: \n{}".format(perm_inte_4[0,:,:,0]))


    # Define storage 
    # -----
    perm_2 = numpy.zeros(shape=(num_concs,num_refs)) # perm_2[k,l] is the r[l] element of the permeability at concentration c[k]
    depo_2 = numpy.zeros(shape=(num_concs,num_refs)) # perm_2[k,l] is the r[l] element of the permeability at concentration c[k]
    
    # Get permeabilty and deposition parameter at each concentration for all r
    for k in range(num_concs):
        for l in range(num_refs):
            ref = refs_1[l]
            #print(ref)
            perm_inte_2 = perm_inte_4[k,:,:,l]
            depo_inte_2 = depo_inte_4[k,:,:,l]
            #print("perm_inte_2:\n",perm_inte_2)
            perm_2[k,l] = numpy.sum(a=numpy.sum(a=perm_inte_2,axis=0),axis=0) # sum over i then j
            depo_2[k,l] = numpy.sum(a=numpy.sum(a=depo_inte_2,axis=0),axis=0) # sum over i then j
    
    perm_prep_1 = 0.5*numpy.sum(a=perm_2,axis=1) # sum over r,   perm_prep_1[k] is the permeability at concentration c[k]
    depo_prep_1 = -(1/length)*numpy.sum(a=depo_2,axis=1) # sum over r, depo_prep_1[k] is the deposition paramaeter at concentration c[k]

    return perm_prep_1, depo_prep_1