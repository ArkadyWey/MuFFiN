import numpy
import scipy.sparse.linalg as linalg
import matplotlib.pyplot as plt

import scipy.optimize as optimize

"""
Module of functions that are used specifically for preprocessing in the
deposition case. 
These functions are used in the run_preprocess module with 
preprocess functions that are common between 
blocking and deposition, which are stored in the preprocess module.

These functions are used to return 
- conductance 
- adherence
- delta 
- csol 

at particular values of ctot, which are indexed by k.
"""

def get_cell_problem(cond_4: numpy.ndarray, refs_2: numpy.ndarray, leng_1:numpy.ndarray):
    """
    Parameters
    -----
    - cond_4[i,j,r0,r1]
    - refs_2[rm,m]
    - leng_1[m]
    
    Returns 
    -----
    - lhs_2[i,j]
    - rhs_3[i,j,m]
    """

    # Define params 
    # -----
    num_nodes = len(cond_4[:,0,0,0])
    num_refs  = len(cond_4[0,0,:,0])
    num_dims  = len(leng_1[:])


    # Define integrands to fill
    # -----
    rhs_inte_5 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_refs,num_dims))
    # rhs_inte_5[i,j,r0,r1,m].
    lhs_inte_4 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_refs))
    # lhs_inte_4[i,j,r0,r1].


    # Build lhs and rhs
    # ------
    for r0 in range(num_refs):
        for r1 in range(num_refs):
                
            # Get lhs integrand
            # -----
            lhs_inte_4[:,:,r0,r1] = cond_4[:,:,r0,r1] - numpy.diag(numpy.sum(a=cond_4[:,:,r0,r1], axis=1))
            
            # Get rhs integrand
            # -----                     
            for m in range(num_dims):
                if m==0: 
                    r=r0
                elif m==1:
                    r=r1
                else: 
                    raise Exception("m != 0,1. This is impossible, since the problem is 2D.")
            
                rhs_inte_5[:,:,r0,r1,m] = cond_4[:,:,r0,r1]*refs_2[r,m]*leng_1[m]
            
    
    # Sum over references
    # -----
    rhs_3 = -numpy.sum(a=numpy.sum(a=rhs_inte_5, axis=3), axis=2) # sum over r1 then r0
    # NB: rhs of cell problem has minus sign by definition.

    lhs_2 =  numpy.sum(a=numpy.sum(a=lhs_inte_4, axis=3), axis=2) # sum over r1 then r0

    # Force a unique solution 
    # -------
    #lhs_2[-1,:] = numpy.zeros(num_nodes)
    #lhs_2[-1,-1] = 1
    #rhs_3[-1,:,0] = numpy.zeros(num_nodes)
    #rhs_3[-1,:,1] = numpy.zeros(num_nodes)

    return (lhs_2, rhs_3)



def get_cell_solution(lhs_2: numpy.ndarray, rhs_3: numpy.ndarray):
    """
    Parameters
    -----
    - lhs_2[i,j]
    - rhs_3[i,j,m]

    Returns 
    # -----
    - csol_2[i,m]
    """

    # Define params 
    # -----
    num_nodes = len(rhs_3[:,0,0])
    num_dims  = len(rhs_3[0,0,:])

    
    # Define array to be filled
    # -----
    csol_2 = numpy.zeros(shape=(num_nodes,num_dims))
    

    # Get solution
    # -----
    a_2 = lhs_2[:,:]
    for m in range(num_dims):
        b_1 = numpy.sum(a=rhs_3[:,:,m], axis=1) # sum over j
        csol_2[:,m] = linalg.lsqr(A=a_2,b=b_1)[0]
        #sol = optimize.lsq_linear(A=a_2,b=b_1)
        #csol_3[k,:,m] = sol.x

    return csol_2


def get_delta(csol_2: numpy.ndarray, refs_2:numpy.ndarray, leng_1: numpy.ndarray):
    """
    Given the cell problem solution, the references, and the lengths, 
    return the parameter delta.

    Parameters
    ----------
    - csol_2: numpy.ndarray
        The solution of the cell problem, W in notes. csol_3[i,m] = element nodes[i] of the solution of 
        the cell problem in direction dimensions[m].
    - refs_2: numpy.ndarray
        refs_2[r,m] = reference-distance references[r] in direction directions[m]. 
        For example, references = {-1,0,+1} and directions = {0,1} (for 2D problem)    
    - leng_1: numpy.ndarray
        leng_1[m] = length of filter in direction directions[m].
    
    Returns 
    -------
    - delt_4: numpy.ndarray
        The parameter delta between nodes i and j with reference references[r] in direction directions[m]. 
        so that delt_5[i,j,r,m] = csol_3[i,m] - (csol_3[j,m] + refs_2[r,m]*leng_1[m]), by defn.
        Note that references[r,m] is numerical equivalent to r^m in the notation.
    """

    # Get params
    # -----
    num_nodes = len(csol_2[:,0])
    num_refs  = len(refs_2[:,0])
    num_dims  = len(csol_2[0,:])


    # Make array to be filled
    # -----
    delt_4 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_dims))
    
    
    # Fill using definition of delta
    # -----
    for i in range(num_nodes):
        for j in range(num_nodes):
            for r in range(num_refs):
                for m in range(num_dims):
                    delt_4[i,j,r,m] = csol_2[i,m] - (csol_2[j,m] + refs_2[r,m]*leng_1[m])
    
    return delt_4




def get_conductance_rhs(cond_4,delt_4,adhe_4,beta,alph):
    """
    Returns the right hand side of the differential equation for conductance. 
    In paractice, we will take the arguments at the previous time step, 
    so that we can spit out the result at the current time step.

    Parameters 
    -----
    - cond_4[i,j,r0,r1]
    - delt_4[i,j,rm,m]
    - adhe_4[i,j,r0,r1]
    
    Returns
    -----
    - cond_rhs_4[i,j,r0,r1]
    """
    # Parameters 
    # ------
    num_nodes = len(delt_4[:,0,0,0])
    num_refs  = len(delt_4[0,0,:,0])
    num_dims  = len(delt_4[0,0,0,:])

    ## sum delta over m
    #delt_3 = numpy.sum(a=delt_4,axis=3)
#
    ## repeat delt so can multiply
    #delt_4 = numpy.repeat(a=delt_3[:,:,:,numpy.newaxis],repeats=num_refs,axis=3) # delt_4[i,j,r0,r1]

    #alph = 0.02564102564102564
    #epsi = 0.05
    #alph=0.5
    #delt_2 = delt_4[:,:,0,0]
    #delt_3= numpy.repeat(a=delt_2[:,:,numpy.newaxis],repeats=3,axis=2)
    #delt_4= numpy.repeat(a=delt_3[:,:,:,numpy.newaxis],repeats=3,axis=3)
    #cond_rhs_4  = -2.0*beta*(cond_4**(3.0/2.0))*alph*abs(delt_4) #*abs(delt_4) #*epsi    #*adhe_4*(1/(epsi**(1.0/2.0)))
    cond_rhs_4 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_refs))
    for r0 in range(num_refs):
        for r1 in range(num_refs):
            cond_rhs_4[:,:,r0,r1] = -beta*alph*abs(delt_4[:,:,r0,0])*cond_4[:,:,r0,r1]**(3.0/2.0) #*0.05
            #cond_rhs_4[:,:,r0,r1] = -1*abs(delt_4[:,:,r0,0])*cond_4[:,:,r0,r1]**(3.0/2.0)
            #print(abs(delt_4[:,:,r0,0]))
            #print(beta)
            #print(alph)
            #print(cond_4)
            #print(abs(delt_4[:,:,0,0])*cond_4[:,:,0,00])
            #raise Exception 

    #cond_rhs_4 = numpy.zeros_like(cond_rhs_4)
    print(beta)
    print(alph)
    return cond_rhs_4




def get_conductance(cond_4,cond_rhs_4,dt):
    """
    This function sppist out the result of one step of the differential 
    equation for the conductance. 
    In practice, we will take the argument sat the previous time step, 
    and we spit out the solution at the current time step.

    Parameters
    ------
    - cond_4[i,j,r0,r1]
    - cond_rhs_4[i,j,r,s]
    - dt

    Returns
    -----
    - cond_4[i,j,r0,r1]
    """
    # build delt_4

    # update cond
    cond_4 = cond_4+dt*cond_rhs_4 #beta*adhe_4*delt_4*
    return cond_4



def get_conductance_adherence_csol_delta(conc_tot_disc_1,cond_init_4,adhe_init_4,refs_2,leng_1,beta,alph):
    """
    """
    print("alph: {}".format(alph))
    print("beta: {}".format(beta))
    # Parameters 
    # ------
    num_concs = len(conc_tot_disc_1)
    # k is a time-like index that indexes concentrations
    num_nodes = len(cond_init_4[:,0,0,0])
    num_refs  = len(refs_2[:,0])
    num_dims  = len(refs_2[0,:])

    dt = conc_tot_disc_1[1]-conc_tot_disc_1[0]


    cond_5 = numpy.zeros(shape=(num_concs,num_nodes,num_nodes,num_refs,num_refs))
    csol_3 = numpy.zeros(shape=(num_concs,num_nodes,num_dims))
    adhe_5 = numpy.zeros(shape=(num_concs,num_nodes,num_nodes,num_refs,num_refs))
    delt_5 = numpy.zeros(shape=(num_concs,num_nodes,num_nodes,num_refs,num_dims))

    for k in range(num_concs):
        if k==0:
            # don't solve differential equation - we already have solution

            # use cond solution at t=0 to get csol solution at t=0
            (lhs_2, rhs_3) = get_cell_problem(cond_4=cond_init_4,refs_2=refs_2,leng_1=leng_1)
            csol_2 = get_cell_solution(lhs_2=lhs_2,rhs_3=rhs_3)

            # update solution
            cond_5[k,:,:,:,:] = cond_init_4
            csol_3[k,:,:]     = csol_2

            delt_5[k,:,:,:,:] = get_delta(csol_2=csol_2,refs_2=refs_2,leng_1=leng_1)
            adhe_5[k,:,:,:,:] = adhe_init_4

        else:
            # use solution cond and csol at t-1 to get rhs of cond eqn at t
            cond_4 = cond_5[k-1,:,:,:,:]
            csol_2 = csol_3[k-1,:,:]
            delt_4 = delt_5[k-1,:,:,:,:]    
            adhe_4 = adhe_5[k-1,:,:,:,:]

            # get new conductance
            cond_rhs_4 = get_conductance_rhs(cond_4=cond_4,delt_4=delt_4,adhe_4=adhe_4,beta=beta,alph=alph)
            cond_4     = get_conductance(cond_4=cond_4,cond_rhs_4=cond_rhs_4,dt=dt)

            # use solution at t to get lhs and rhs of alg equation
            (lhs_2, rhs_3) = get_cell_problem(cond_4=cond_4,refs_2=refs_2,leng_1=leng_1)
            csol_2         = get_cell_solution(lhs_2=lhs_2,rhs_3=rhs_3)

            # update solution
            cond_5[k,:,:,:,:] = cond_4
            csol_3[k,:,:]     = csol_2
            delt_5[k,:,:,:,:] = get_delta(csol_2=csol_2,refs_2=refs_2,leng_1=leng_1)
            adhe_5[k,:,:,:,:] = adhe_init_4
            

    return (cond_5,adhe_5,csol_3,delt_5)



if __name__ == "__main__":

    # Parameters 
    times = numpy.linspace(0,1,101)

    num_nodes = 4
    num_refs  = 3
    num_dims  = 2

    n = int(numpy.sqrt(num_nodes))
    l1 = n*1.0
    l2 = n*1.0

    refs_2 = numpy.array([[0.0,1.0,-1.0],[0.0,1.0,-1.0]])
    refs_2 = numpy.transpose(refs_2)
    leng_1 = numpy.array([l1,l2])

    # Initial condition
    cond_init_4 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_refs))
    # Internal edges
    cond_init_4[0,1,0,0] = 1.0#0.99#0.1#1.2#1.72461##0.8 #1.0
    cond_init_4[1,0,0,0] = 1.0#0.99#0.1#1.2#1.72461##0.8 #1.0
    cond_init_4[1,3,0,0] = 1.0#0.2#1.2#1.72461#1.0#0.2 #1.0
    cond_init_4[3,1,0,0] = 1.0#0.2#1.2#1.72461#1.0#0.2 #1.0
    cond_init_4[2,3,0,0] = 1.0#0.3#1.2#1.72461#1.0#0.4 #1.0
    cond_init_4[3,2,0,0] = 1.0#0.3#1.2#1.72461#1.0#0.4 #1.0
    cond_init_4[0,2,0,0] = 1.0#0.4#1.2#1.72461#1.0#0.6 #1.0
    cond_init_4[2,0,0,0] = 1.0#0.4#1.2#1.72461#1.0#0.6 #1.0
    ## External edges
    cond_init_4[1,0,1,0]  = 1.0#0.5#1.2#1.72461#1.0#1.0 #1.0
    cond_init_4[0,1,-1,0] = 1.0#0.5#1.2#1.72461#1.0#1.0 #1.0
    cond_init_4[3,2,1,0]  = 1.0#0.6#1.2#1.72461#1.0#1.0 #1.0
    cond_init_4[2,3,-1,0] = 1.0#0.6#1.2#1.72461#1.0#1.0 #1.0
    
    cond_init_4[0,2,0,1]  = 1.0#0.7#1.2#1.72461#1.0
    cond_init_4[2,0,0,-1] = 1.0#0.7#1.2#1.72461#1.0
    
    cond_init_4[1,3,0,1]  = 1.0#0.8#1.2#1.72461#1.0
    cond_init_4[3,1,0,-1] = 1.0#0.8#1.2#1.72461#1.0

    adhe_init_4 = numpy.ones_like(cond_init_4)

    cond_5,adhe_5,csol_3,delt_5 = get_conductance_adherence_csol_delta(conc_tot_disc_1=times,
                                                                       cond_init_4=cond_init_4,
                                                                       adhe_init_4=adhe_init_4,
                                                                       refs_2=refs_2,
                                                                       leng_1=leng_1)
    #print(csol_3[0:2,:,:])
    plt.plot(times,cond_5[:,0,1,0,0])
    plt.plot(times,1/((1/1)+(times/2))**2,ls="--")
    # plt.show()


    
    