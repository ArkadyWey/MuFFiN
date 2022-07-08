import numpy
import os
import datetime

import configure
import preprocess_2D



def main(num_nodes):
    """
    """

    # Get parameters needed to find perm and depo
    # -----
    conf = configure.Configure(num_nodes=num_nodes)
    
    conc_max_disc_1 = conf.conc_max_disc_1 
    cond_init_4     = conf.cond_init_4 
    adhe_init_4     = conf.adhe_init_4 
    alpha           = conf.alpha 
    refs_2          = conf.refs_2 
    leng_1          = conf.leng_1 
    v               = conf.v


    cond_tabl_5, adhe_tabl_5 = preprocess_2D.get_conductance_and_adhesivity(conc_max_disc_1=conc_max_disc_1, 
                                                                            cond_init_4=cond_init_4, 
                                                                            adhe_init_4=adhe_init_4, 
                                                                            alpha=alpha)
    #print("cond_tabl_5[0,:,:,0,0]: \n{}".format(cond_tabl_5[0,:,:,0,1]))
    #print("adhe_tabl_5[0,:,:,0,0]: \n{}".format(adhe_tabl_5[0,:,:,0,0]))
    
    

    lhs_3, rhs_4 = preprocess_2D.get_cell_problem(cond_tabl_5=cond_tabl_5, 
                                                  refs_2=refs_2, 
                                                  leng_1=leng_1)
    
    #print("rhs_4[0,:,:,0]: \n{}".format(rhs_4[0,:,:,0]))
    #print("lhs_3[0,:,:]: \n{}".format(lhs_3[0,:,:]))
    
    
    
    csol_3 = preprocess_2D.get_cell_solution(lhs_3=lhs_3, 
                                             rhs_4=rhs_4)
    #print("csol_3[0,:,0]: \n{}".format(csol_3[0,:,0]))



    delt_5 = preprocess_2D.get_delta(csol_3=csol_3, 
                                     refs_2=refs_2, 
                                     leng_1=leng_1)
    #print("delt_5[0,:,:,0,0]: \n{}".format(delt_5[0,:,:,-1,1]))



    heav_5 = preprocess_2D.get_heaviside(delt_5=delt_5)
    #print("heav_5[0,:,:,0,0]: \n{}".format(heav_5[0,:,:,0,0]))


    perm_3, depo_2 = preprocess_2D.get_permeability_and_deposition(refs_2=refs_2,
                                                                   cond_tabl_5=cond_tabl_5,
                                                                   adhe_tabl_5=adhe_tabl_5,
                                                                   delt_5=delt_5,
                                                                   heav_5=heav_5,
                                                                   leng_1=leng_1,
                                                                   v=v, 
                                                                   cond_init_4=cond_init_4)
    #print("perm_3[:,0,0]: \n{}".format(perm_3[:,0,0]))
    #print("depo_2[:,0]: \n{}".format(depo_2[:,0]))

    return (perm_3, depo_2, conc_max_disc_1)
    
if __name__ == "__main__":


    begin_time = datetime.datetime.now()

    # Define parameters that aren't in default dictionary
    # -----   
    num_nodes = 2
    
    # Get permeability and deposition parameter
    # -----
    perm_prep_3, depo_prep_2, conc_max_disc_1 = main(num_nodes=num_nodes)

    end_time = datetime.datetime.now()
    print("sim_time:\n {}".format(end_time-begin_time))

    # Save results 
    # -----
    path_results = os.path.join(".","results_preprocess_2D")
    if not os.path.exists(path_results):
        os.mkdir(path_results)

    numpy.save(file=os.path.join(path_results,"perm_prep_3.npy"),     arr=perm_prep_3,     allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"depo_prep_2.npy"),     arr=depo_prep_2,     allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"conc_max_disc_1.npy"), arr=conc_max_disc_1, allow_pickle=True, fix_imports=True)
