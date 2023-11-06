from turtle import shape
import numpy
import scipy 
from scipy import optimize
from scipy import sparse
import datetime
import matplotlib
from matplotlib import pyplot as plt
from scipy import interpolate
from scipy import integrate
import os


import preprocess_1D

def main(conc_max_or_tot_1,cond_init_3,adhe_init_3,alpha,refs_1,length):
    """
    """

    # preprocess_1D
    # ------------
    # Get conductance and adhesivity 
    # -----
    cond_tabl_4, adhe_tabl_4 = preprocess_1D.get_conductance_and_adhesivity(conc_max_or_tot_1=conc_max_or_tot_1, 
                                                                            cond_init_3=cond_init_3, 
                                                                            adhe_init_3=adhe_init_3, 
                                                                            alpha=alpha)
    #print("cond_tabl_4[k,:,:,l]: \n",cond_tabl_4[3,:,:,-1])
    #print("adhe_tabl_4[k,:,:,l]: \n",adhe_tabl_4[3,:,:,-1])


    # Get lhs and rhs of cell problem 
    # ------
    lhs_3, rhs_3 = preprocess_1D.get_cell_problem(refs_1=refs_1, 
                                                  cond_tabl_4=cond_tabl_4,
                                                  length=length)
    #print("lhs_3[k,:,:]: \n", lhs_3[0,:,:])
    #print("rhs_3[k,:,:]: \n", rhs_3[0,:,:])


    # Get solution of cell problem
    # ------
    csol_2 = preprocess_1D.get_cell_solution(lhs_3=lhs_3,
                                             rhs_3=rhs_3)
    #print("csol_2[k,:]: \n", csol_2[0,:])


    # Get delta
    # ------
    # Form delt_4 where delta_4[k,i,j,r] = W_i-W_j-rl at the kth concentration 
    delt_4 = preprocess_1D.get_delta(csol_2=csol_2, 
                                     refs_1=refs_1, 
                                     length=length)
    #print("delt_4[k,:,:,l]: \n", delt_4[3,:,:,1])



    # Get heaviside 
    # -----
    # Use delt_4 to form heavisude which is H(delta)
    heav_4 = preprocess_1D.get_heaviside(delt_4=delt_4)
    #print("heav_4[k,:,:,l]: \n", heav_4[0,:,:,0])



    # Get local permeability and deposition parameter
    # ------ 
    perm_prep_1, depo_prep_1 = preprocess_1D.get_permeability_and_deposition(cond_tabl_4=cond_tabl_4, 
                                                                             adhe_tabl_4=adhe_tabl_4, 
                                                                             refs_1=refs_1, 
                                                                             delt_4=delt_4, 
                                                                             heav_4=heav_4, 
                                                                             cond_init_3=cond_init_3, 
                                                                             length=length)
    #print("perm_prep_1[:]: \n{}".format(perm_prep_1[0]))
    #print("depo_prep_1[:]: \n{}".format(depo_prep_1[-1]))
    return (perm_prep_1,depo_prep_1)


if __name__ == "__main__":

    begin_time = datetime.datetime.now()
    print(datetime.datetime.now())
    
    # Parameters
    # ------------
    refs_1  = numpy.array([0,1,-1]) # TODO: needs to include all possible r
    #print("refs_1: \n {}".format(refs_1))
    
    num_refs  = len(refs_1)
    num_concs = 1_001
    num_nodes = 4
    alpha     = 0.1
    v         = 0.5 #2.0 # Sum of volumes of nodes in cell
    length    = 1.0
    phi       = v/length # TODO: Define this properly
    
    # Concentrations to tabulate 
    conc_max_or_tot_1 = numpy.linspace(0,1.0,num_concs) # discrete list of possible concentrations
    #print("conc_max_or_tot_1: \n {}".format(conc_max_or_tot_1))
    
    # Conductance and adhesivity 
    cond_init_3 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs)) 
    adhe_init_3 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs)) 
    # TODO: initial condition should be random
    
    # Line of one node:
    # -----
    # External edges
    #cond_init_3[0,0,1]  = 1.0
    #cond_init_3[0,0,-1] = 1.0

    # Line of two nodes:
    # -----
    ## Internal edges
    #cond_init_3[0,1,0] = 1.0
    #cond_init_3[1,0,0] = 1.0
    ## External edges 
    #cond_init_3[1,0,1] = 1.0
    #cond_init_3[0,1,-1] = 1.0
    
    
    # Line of three nodes
    # -----
    # Internal
    #cond_init_3[0,1,0] = 1.0
    #cond_init_3[1,0,0] = 1.0
    #
    #cond_init_3[1,2,0] = 1.0
    #cond_init_3[2,1,0] = 1.0
    #
    ## External
    #cond_init_3[2,0,1] = 1.0
    #cond_init_3[0,2,-1] = 1.0
    
    # grid of four nodes (embedded in 1D)
    cond_init_3[0,1,0] = 0.8  #1.6  #1.0
    cond_init_3[1,0,0] = 0.8  #1.6  #1.0
    cond_init_3[1,3,0] = 0.2  #0.4  #1.0
    cond_init_3[3,1,0] = 0.2  #0.4  #1.0
    cond_init_3[2,3,0] = 0.4  #0.8  #1.0
    cond_init_3[3,2,0] = 0.4  #0.8  #1.0
    cond_init_3[0,2,0] = 0.6  #1.2  #1.0
    cond_init_3[2,0,0] = 0.6  #1.2  #1.0
    cond_init_3[1,0,1] = 1.0  #2.0 
    cond_init_3[0,1,2] = 1.0  #2.0 
    cond_init_3[3,2,1] = 1.0  #2.0 
    cond_init_3[2,3,2] = 1.0  #2.0 

    #cond_init_3[0,1,0] = 2.0 #1.0
    #cond_init_3[1,0,0] = 2.0 #1.0
    #cond_init_3[1,3,0] = 2.0 #1.0
    #cond_init_3[3,1,0] = 2.0 #1.0
    #cond_init_3[2,3,0] = 2.0 #1.0
    #cond_init_3[3,2,0] = 2.0 #1.0
    #cond_init_3[0,2,0] = 2.0 #1.0
    #cond_init_3[2,0,0] = 2.0 #1.0
    #cond_init_3[1,0,1] = 2.0 #1.0
    #cond_init_3[0,1,2] = 2.0 #1.0
    #cond_init_3[3,2,1] = 2.0 #1.0
    #cond_init_3[2,3,2] = 2.0 #1.0


    # Get permeability and deposition parameter tables
    # -----
    perm_prep_1, depo_prep_1 = main(conc_max_or_tot_1=conc_max_or_tot_1,
                                    cond_init_3=cond_init_3,
                                    adhe_init_3=adhe_init_3,
                                    alpha=alpha,
                                    refs_1=refs_1,
                                    length=length)
    

    # Save results 
    # -----
    path_results = os.path.join(".","results/results_preprocess_1D")
    if not os.path.exists(path_results):
        os.mkdir(path_results)

    numpy.save(file=os.path.join(path_results,"perm_prep_1.npy"), arr=perm_prep_1, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"depo_prep_1.npy"), arr=depo_prep_1, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"conc_max_or_tot_1.npy"), arr=conc_max_or_tot_1, allow_pickle=True, fix_imports=True)




        
