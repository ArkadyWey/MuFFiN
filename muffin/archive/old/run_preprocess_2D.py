import numpy
import os

import muffin.preprocess.preprocess as preprocess

def main(conc_max_disc_1,
         cond_init_4,
         adhe_init_4,
         alpha,
         refs_2,
         leng_1,
         v):
    """
    """
    cond_tabl_5, adhe_tabl_5 = preprocess.get_conductance_and_adhesivity(conc_max_disc_1=conc_max_disc_1, 
                                                                            cond_init_4=cond_init_4, 
                                                                            adhe_init_4=adhe_init_4, 
                                                                            alpha=alpha)
    #print("cond_tabl_5[0,:,:,0,0]: \n{}".format(cond_tabl_5[0,:,:,0,1]))
    #print("adhe_tabl_5[0,:,:,0,0]: \n{}".format(adhe_tabl_5[0,:,:,0,0]))
    
    

    lhs_3, rhs_4 = preprocess.get_cell_problem(cond_tabl_5=cond_tabl_5, 
                                                  refs_2=refs_2, 
                                                  leng_1=leng_1)
    
    #print("rhs_4[0,:,:,0]: \n{}".format(rhs_4[0,:,:,0]))
    #print("lhs_3[0,:,:]: \n{}".format(lhs_3[0,:,:]))
    
    
    
    csol_3 = preprocess.get_cell_solution(lhs_3=lhs_3, 
                                             rhs_4=rhs_4)
    print("csol_3[0,:,0]: \n{}".format(csol_3[0,:,0]))



    delt_5 = preprocess.get_delta(csol_3=csol_3, 
                                     refs_2=refs_2, 
                                     leng_1=leng_1)
    print("delt_5[0,:,:,0,0]: \n{}".format(delt_5[0,:,:,-1,1]))



    heav_5 = preprocess.get_heaviside(delt_5=delt_5)
    #print("heav_5[0,:,:,0,0]: \n{}".format(heav_5[0,:,:,0,0]))


    perm_3, depo_2 = preprocess.get_permeability_and_deposition(refs_2=refs_2,
                                                                   cond_tabl_5=cond_tabl_5,
                                                                   adhe_tabl_5=adhe_tabl_5,
                                                                   delt_5=delt_5,
                                                                   heav_5=heav_5,
                                                                   leng_1=leng_1,
                                                                   v=v, 
                                                                   cond_init_4=cond_init_4)
    #print("perm_3[:,0,0]: \n{}".format(perm_3[:,0,0]))
    #print("depo_2[:,0]: \n{}".format(depo_2[:,0]))

    #return (perm_3, depo_2)
    
if __name__ == "__main__":

    # Parameters 
    # -----
    max_ref_dist = 1
    num_dims     = 2
    num_concs    = 1001
    num_nodes    = 1#4

    alpha        = 1.0
    v            = 1.0#2.0 # Sum of volumes of nodes in cell
    #phi          = 0.5 # TODO: Define this properly
    l1           = 1.0
    l2           = 1.0
    
    leng_1     = numpy.array([l1,l2])
    conc_max_disc_1 = numpy.linspace(0,1,num_concs)


    # Cell references
    # -----
    refs_2 = preprocess.get_reference(max_ref_dist=max_ref_dist,
                                         num_dims=num_dims)


    # Conductance and adhesivity 
    # -----
    num_refs = len(refs_2[:,0])
    cond_init_4 = numpy.zeros(shape=(num_nodes, num_nodes, num_refs, num_dims)) 
    adhe_init_4 = numpy.zeros(shape=(num_nodes, num_nodes, num_refs, num_dims)) 

    # Grid of one node
    # ----------------
    cond_init_4[0,0,1,0] = 1.0 #1.72461
    cond_init_4[0,0,-1,0] = 1.0 #1.72461

    cond_init_4[0,0,1,1] = 1.0 #1.72461
    cond_init_4[0,0,-1,1] = 1.0 #1.72461
    
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
    #cond_init_4[0,1,0,0] = 0.8 #1.0
    #cond_init_4[1,0,0,0] = 0.8 #1.0
    #
    #cond_init_4[1,3,0,1] = 0.2 #1.0
    #cond_init_4[3,1,0,1] = 0.2 #1.0
    #
    #cond_init_4[2,3,0,0] = 0.4 #1.0
    #cond_init_4[3,2,0,0] = 0.4 #1.0
    #
    #cond_init_4[0,2,0,1] = 0.6 #1.0
    #cond_init_4[2,0,0,1] = 0.6 #1.0
    #
    ## External edges
    #cond_init_4[1,0,1,0] = 1.0 #1.0
    #cond_init_4[0,1,-1,0] = 1.0 #1.0
    #
    #cond_init_4[3,2,1,0] = 1.0 #1.0
    #cond_init_4[2,3,-1,0] = 1.0 #1.0

    #cond_init_4[0,2,1,1]  = 1.0
    #cond_init_4[2,0,-1,1] = 1.0

    #cond_init_4[1,3,1,1] = 1.0
    #cond_init_4[3,1,-1,1] = 1.0

    #perm_prep_3, depo_prep_2 = 
    main(conc_max_disc_1=conc_max_disc_1,
                                    cond_init_4=cond_init_4,
                                    adhe_init_4=adhe_init_4,
                                    alpha=alpha,
                                    refs_2=refs_2,
                                    leng_1=leng_1,
                                    v=v)



    # Save results 
    # -----
    path_results = os.path.join(".","results_preprocess")
    if not os.path.exists(path_results):
        os.mkdir(path_results)

    #numpy.save(file=os.path.join(path_results,"perm_prep_3.npy"),     arr=perm_prep_3,     allow_pickle=True, fix_imports=True)
    #numpy.save(file=os.path.join(path_results,"depo_prep_2.npy"),     arr=depo_prep_2,     allow_pickle=True, fix_imports=True)
    #numpy.save(file=os.path.join(path_results,"conc_max_disc_1.npy"), arr=conc_max_disc_1, allow_pickle=True, fix_imports=True)

