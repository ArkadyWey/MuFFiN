import numpy
import os
import datetime

import configure
import preprocess_2D



def main(num_nodes: int, initialisation: str, sigma: float, type_alpha: str):
    """
    """
    # Get parameters needed to find perm and depo
    # -----
    conf = configure.Configure(num_nodes=num_nodes, 
                               initialisation=initialisation, 
                               sigma=sigma,
                               type_alpha=type_alpha)
    
    conc_max_disc_1 = conf.conc_max_disc_1 
    #a = numpy.linspace(0.0,0.85,11)
    #b = numpy.linspace(0.85,0.95,101-10-10)
    #c = numpy.linspace(0.95,1.0,11)
    #a = numpy.arange(0.0,0.88,0.01)
    #b = numpy.arange(0.88,0.92,0.0001)
    #c = numpy.arange(0.92,1.01,0.01)
    #conc_max_disc_1 = numpy.concatenate((a,b,c))
    #print(len(conc_max_disc_1))
    print(conc_max_disc_1)
    cond_init_4     = conf.cond_init_4 
    adhe_init_4     = conf.adhe_init_4 
    alpha           = conf.alpha 
    refs_2          = conf.refs_2 
    leng_1          = conf.leng_1



    cond_tabl_5, adhe_tabl_5 = preprocess_2D.get_conductance_and_adhesivity(conc_max_disc_1=conc_max_disc_1, 
                                                                            cond_init_4=cond_init_4, 
                                                                            adhe_init_4=adhe_init_4, 
                                                                            alpha=alpha)
    #r = 0
    #m = 0
    #print("avrg cond:",numpy.mean(cond_tabl_5))
    #print("cond_tabl_5[0,:,:,0,0]: \n{}".format(cond_tabl_5[0,:,:,r,0]))
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
    #print("delt_5[0,:,:,0,0]: \n{}".format(delt_5[-1,:,:,-1,0]))



    heav_5 = preprocess_2D.get_heaviside(delt_5=delt_5)
    #print("heav_5[0,:,:,0,0]: \n{}".format(heav_5[0,:,:,0,0]))
    
    #print(-numpy.mean( a=(-delt_5[-1,:,:,0,0]), axis=None))



    #print(-numpy.mean( a=-delt_5[-1,:,:,r,m]*(heav_5[-1,:,:,r,m]), axis=None))
    #print(-delt_5[-1,:,:,r,m]*(heav_5[-1,:,:,r,m]))

    perm_3, depo_2 = preprocess_2D.get_permeability_and_deposition(refs_2=refs_2,
                                                                   cond_tabl_5=cond_tabl_5,
                                                                   adhe_tabl_5=adhe_tabl_5,
                                                                   delt_5=delt_5,
                                                                   heav_5=heav_5,
                                                                   leng_1=leng_1,
                                                                   cond_init_4=cond_init_4)
    print("perm_3[:,0,0]: \n{}".format(perm_3[:,0,0]))
    #print("perm_3[:,1,0]: \n{}".format(perm_3[:,1,0]))
    print("depo_2[:,0]: \n{}".format(depo_2[:,0]))
    #print("depo_2[:,1]: \n{}".format(depo_2[-1,1]))

    #if depo_2[-1,0] > 4.0:
    #    exit()
    return (perm_3, depo_2, conc_max_disc_1, cond_tabl_5, adhe_tabl_5, delt_5, heav_5)
    
if __name__ == "__main__":


    begin_time = datetime.datetime.now()

    # Define parameters that aren't in default dictionary
    # -----   
    num_nodes = 4
    initialisation = "4-reg_prescribed"
    sigma = 0.3
    type_alpha = "mean"
    
    # Get permeability and deposition parameter
    # -----
    perm_prep_3, depo_prep_2, conc_max_disc_1, cond_tabl_5, adhe_tabl_5, delt_5, heav_5 = main(num_nodes=num_nodes, 
                                                                                               initialisation=initialisation,
                                                                                               sigma=sigma,
                                                                                               type_alpha=type_alpha)

    end_time = datetime.datetime.now()
    print("sim_time:\n {}".format(end_time-begin_time))

    # Save results 
    # -----
    path_results = os.path.join(".","results/results_preprocess_2D")
    if not os.path.exists(path_results):
        os.mkdir(path_results)

    numpy.save(file=os.path.join(path_results,"perm_prep_3.npy"),     arr=perm_prep_3,     allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"depo_prep_2.npy"),     arr=depo_prep_2,     allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"conc_max_disc_1.npy"), arr=conc_max_disc_1, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"cond_tabl_5.npy"),     arr=cond_tabl_5,     allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"adhe_tabl_5.npy"),     arr=adhe_tabl_5,     allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"heav_5.npy"),          arr=heav_5,          allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"delt_5.npy"),          arr=delt_5,          allow_pickle=True, fix_imports=True)