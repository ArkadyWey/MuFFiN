import numpy
import os
import datetime
import matplotlib.pyplot as plt

import configure
import preprocess_2D
import preprocess_blocking_2D
import preprocess_deposition_2D


def main(num_nodes: int, initialisation: str, sigma: float, type_alpha: str, type_clog: str, path_cond_init_4: str, alph: int, beta: int):
    """
    """

    # Get paameters needed to find perm and depo
    # -----
    conf = configure.Configure(num_nodes=num_nodes, 
                               initialisation=initialisation, 
                               sigma=sigma,
                               type_alpha=type_alpha, 
                               path_cond_init_4=path_cond_init_4)
    
    conc_max_or_tot_1 = conf.conc_max_or_tot_1 
    #a = numpy.linspace(0.0,0.85,11)
    #b = numpy.linspace(0.85,0.95,101-10-10)
    #c = numpy.linspace(0.95,1.0,11)
    #a = numpy.arange(0.0,0.88,0.01)
    #b = numpy.arange(0.88,0.92,0.0001)
    #c = numpy.arange(0.92,1.01,0.01)
    #conc_max_or_tot_1 = numpy.concatenate((a,b,c))
    #print(len(conc_max_or_tot_1))
    #print(conc_max_or_tot_1)
    cond_init_4     = conf.cond_init_4 
    adhe_init_4     = alph*conf.adhe_init_4 
    alpha           = conf.alpha 
    refs_2          = conf.refs_2 
    leng_1          = conf.leng_1


    if type_clog == "block":
        cond_tabl_5, adhe_tabl_5 = preprocess_blocking_2D.get_conductance_and_adhesivity(conc_max_or_tot_1=conc_max_or_tot_1, 
                                                                                         cond_init_4=cond_init_4, 
                                                                                         adhe_init_4=adhe_init_4, 
                                                                                         alpha=alpha)
        #r = 0
        #m = 0
        #print("avrg cond:",numpy.mean(cond_tabl_5))
        #print("cond_tabl_5[0,:,:,0,0]: \n{}".format(cond_tabl_5[0,:,:,r,0]))
        #print("adhe_tabl_5[0,:,:,0,0]: \n{}".format(adhe_tabl_5[0,:,:,0,0]))



        lhs_3, rhs_4 = preprocess_blocking_2D.get_cell_problem(cond_tabl_5=cond_tabl_5, 
                                                               refs_2=refs_2, 
                                                               leng_1=leng_1)

        #print("rhs_4[0,:,:,0]: \n{}".format(rhs_4[0,:,:,0]))
        #print("lhs_3[0,:,:]: \n{}".format(lhs_3[0,:,:]))



        csol_3 = preprocess_blocking_2D.get_cell_solution(lhs_3=lhs_3, 
                                                          rhs_4=rhs_4)
        #print("csol_3[0,:,0]: \n{}".format(csol_3[0,:,:]))



        delt_5 = preprocess_blocking_2D.get_delta(csol_3=csol_3, 
                                         refs_2=refs_2, 
                                         leng_1=leng_1)
        #print("delt_5[0,:,:,0,0]: \n{}".format(delt_5[-1,:,:,-1,0]))

    elif type_clog == "deposit":
        cond_tabl_5,adhe_tabl_5,csol_3,delt_5 = preprocess_deposition_2D.get_conductance_adherence_csol_delta(conc_tot_disc_1=conc_max_or_tot_1,
                                                                                                              cond_init_4=cond_init_4,
                                                                                                              adhe_init_4=adhe_init_4,
                                                                                                              refs_2=refs_2,
                                                                                                              leng_1=leng_1,
                                                                                                              beta=beta,
                                                                                                              alph=alph)
    else: 
        raise Exception("type_clog must be either 'block' or 'deposit'.")
        #print(csol_3[0:2,:,:])
        #plt.plot(conc_max_or_tot_1,cond_tabl_5[:,0,1,0,0])
        #plt.plot(conc_max_or_tot_1,1/((1/1)+(conc_max_or_tot_1/2))**2,ls="--")
        #plt.show()

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
    #print("csol_3[0,:,0]: \n{}".format(csol_3[0,:,0]))
    #print("perm_3[:,0,0]: \n{}".format(perm_3[:,0,0]))
    #print("perm_3[:,1,0]: \n{}".format(perm_3[:,1,0]))
    #print("depo_2[:,0]: \n{}".format(depo_2[:,0]))
    #print("depo_2[:,1]: \n{}".format(depo_2[-1,1]))
    #print("delt_5[:,i,j,r,m]: \n{}".format(delt_5[0,:,:,-1,0]))
    #print("heav_5[:,i,j,r,m]: \n{}".format(heav_5[0,:,:,-1,0]))

    #if depo_2[-1,0] > 4.0:
    #    exit()
    return (perm_3, depo_2, conc_max_or_tot_1, cond_tabl_5, adhe_tabl_5, delt_5, heav_5)

def get_path_to_initial_conductance():
    """
    In the case where the initial conductance is specified by the network model, 
    get the path to where the initial cell is stored. 
    """
    path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/results_preprocess") # paper
    path_head, path_tail = os.path.split(path_results)
    path_cond_init_4 = os.path.join(path_head,"results_network") + "/cond_init_4.npy"
    return path_cond_init_4

if __name__ == "__main__":


    begin_time = datetime.datetime.now()

    # Define parameters that aren't in default dictionary
    # -----   
    num_nodes = 4
    initialisation = "4-reg" # specified #"4-reg_prescribed" # 4-reg
    sigma = 0.3
    type_alpha = "mean"
    type_clog  = "deposit"
    path_cond_init_4 = get_path_to_initial_conductance()


    alph=1.0#1.0#0.3#0.35#0.5#0.3333333333333333#0.5#0.5#1.0#0.1#0.5 (epsi*delt**2)
    beta=1.0#1.0#10#20.0

    
    # Get permeability and deposition parameter
    # -----
    perm_prep_3, depo_prep_2, conc_max_or_tot_1, cond_tabl_5, adhe_tabl_5, delt_5, heav_5 = main(num_nodes=num_nodes, 
                                                                                                 initialisation=initialisation,
                                                                                                 sigma=sigma,
                                                                                                 type_alpha=type_alpha,
                                                                                                 type_clog=type_clog, 
                                                                                                 path_cond_init_4=path_cond_init_4, 
                                                                                                 alph=alph, 
                                                                                                 beta=beta)

    end_time = datetime.datetime.now()
    print("sim_time:\n {}".format(end_time-begin_time))



    # Save results 
    # ----- 
    ensemble = True
    if ensemble == False:
        #path_results = os.path.join(".","results/results_preprocess_2D") # thesis
        path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/results_preprocess") # paper
        if not os.path.exists(path_results):
            os.mkdir(path_results)


    elif ensemble == True:
        import argparse
        parser = argparse.ArgumentParser()

        parser.add_argument("-pr", "--path_results", help="Path to results")

        args = parser.parse_args()

        path_results = args.path_results
    
        if not os.path.exists(path_results):
            os.makedirs(path_results)

    else: 
        raise Exception("ensemble should be a boolean.")




    numpy.save(file=os.path.join(path_results,"perm_prep_3.npy"),       arr=perm_prep_3,     allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"depo_prep_2.npy"),       arr=depo_prep_2,     allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"conc_max_or_tot_1.npy"), arr=conc_max_or_tot_1, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"cond_tabl_5.npy"),       arr=cond_tabl_5,     allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"adhe_tabl_5.npy"),       arr=adhe_tabl_5,     allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"heav_5.npy"),            arr=heav_5,          allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"delt_5.npy"),            arr=delt_5,          allow_pickle=True, fix_imports=True)