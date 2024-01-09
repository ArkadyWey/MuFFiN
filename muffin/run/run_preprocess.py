import os
import datetime

import muffin.configure.configure as configure
import muffin.preprocess.preprocess as preprocess
import muffin.preprocess.preprocess_blocking as preprocess_blocking
import muffin.preprocess.preprocess_deposition as preprocess_deposition
import muffin.utils.load_and_save as load_and_save

def main(num_nodes: int, 
         initialisation: str, 
         sigma: float, 
         type_alpha: str, 
         type_clog: str, 
         path_cond_init_4: str, 
         alph: int, 
         beta: int):
    """_summary_

    Args:
        num_nodes (int): _description_
        initialisation (str): _description_
        sigma (float): _description_
        type_alpha (str): _description_
        type_clog (str): _description_
        path_cond_init_4 (str): _description_
        alph (int): _description_
        beta (int): _description_

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """

    # Get paameters needed to find perm and depo
    # -----
    conf = configure.Configure(num_nodes=num_nodes, 
                               initialisation=initialisation, 
                               sigma=sigma,
                               type_alpha=type_alpha, 
                               path_cond_init_4=path_cond_init_4)
    
    conc_max_or_tot_1 = conf.conc_max_or_tot_1 
    cond_init_4       = conf.cond_init_4 
    adhe_init_4       = alph*conf.adhe_init_4 
    alpha             = conf.alpha 
    refs_2            = conf.refs_2 
    leng_1            = conf.leng_1


    if type_clog == "block":
        cond_tabl_5, adhe_tabl_5 = preprocess_blocking.get_conductance_and_adhesivity(conc_max_or_tot_1=conc_max_or_tot_1, 
                                                                                         cond_init_4=cond_init_4, 
                                                                                         adhe_init_4=adhe_init_4, 
                                                                                         alpha=alpha)


        lhs_3, rhs_4 = preprocess_blocking.get_cell_problem(cond_tabl_5=cond_tabl_5, 
                                                               refs_2=refs_2, 
                                                               leng_1=leng_1)


        csol_3 = preprocess_blocking.get_cell_solution(lhs_3=lhs_3, 
                                                          rhs_4=rhs_4)



        delt_5 = preprocess_blocking.get_delta(csol_3=csol_3, 
                                         refs_2=refs_2, 
                                         leng_1=leng_1)

    elif type_clog == "deposit":
        cond_tabl_5,adhe_tabl_5,csol_3,delt_5 = preprocess_deposition.get_conductance_adherence_csol_delta(conc_tot_disc_1=conc_max_or_tot_1,
                                                                                                              cond_init_4=cond_init_4,
                                                                                                              adhe_init_4=adhe_init_4,
                                                                                                              refs_2=refs_2,
                                                                                                              leng_1=leng_1,
                                                                                                              beta=beta,
                                                                                                              alph=alph)
    else: 
        raise Exception("type_clog must be either 'block' or 'deposit'.")

    heav_5 = preprocess.get_heaviside(delt_5=delt_5)

    perm_3, depo_2 = preprocess.get_permeability_and_deposition(refs_2=refs_2,
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
    return (perm_3, depo_2, conc_max_or_tot_1, cond_tabl_5, adhe_tabl_5, delt_5, heav_5)

def get_path_to_initial_conductance():
    """
    In the case where the initial conductance is 'specified' by the network model, 
    get the path to where the initial cell is stored. 
    """
    path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/results_preprocess") # paper
    path_head, path_tail = os.path.split(path_results)
    path_cond_init_4 = os.path.join(path_head,"results_network") + "/cond_init_4.npy"
    print(path_cond_init_4)
    return path_cond_init_4

if __name__ == "__main__":

    #path_results = os.path.join(".","results/results_preprocess") # thesis
    #path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/results_preprocess") # paper
    #path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/mono/prep") # paper

    # Parameters
    # -----

    # List required parameters
    parameters_required = [
        "path_results",
        "num_nodes",
        "initialisation",
        "alph",
        "beta", 
        "sigma",
        "type_alpha",
        "type_clog",
        "path_cond_init_4",
    ]

    # Load required parameters 
    parameters_used = load_and_save.load_required_parameters(parameters_required=parameters_required)

    # Make simulation output directory
    if not os.path.exists(parameters_used["path_results"]):
        os.makedirs(parameters_used["path_results"])

    # Save parameters used at simulation output
    load_and_save.save_dict_as_json(d=parameters_used, path_json=parameters_used["path_results"]+"/parameters.json")

    begin_time = datetime.datetime.now()
    
    # Get solution variables as functions of mass flux
    # -----
    perm_prep_3, depo_prep_2, conc_max_or_tot_1, cond_tabl_5, adhe_tabl_5, delt_5, heav_5 = main(num_nodes        = parameters_used["num_nodes"], 
                                                                                                 initialisation   = parameters_used["initialisation"],
                                                                                                 sigma            = parameters_used["sigma"],
                                                                                                 type_alpha       = parameters_used["type_alpha"],
                                                                                                 type_clog        = parameters_used["type_clog"], 
                                                                                                 path_cond_init_4 = parameters_used["path_cond_init_4"], 
                                                                                                 alph             = parameters_used["alph"], 
                                                                                                 beta             = parameters_used["beta"]
                                                                                                 )

    end_time = datetime.datetime.now()
    print("sim_time:\n {}".format(end_time-begin_time))

    # Save results 
    # ----- 
    load_and_save.save_nparray_as_npy(path_results=parameters_used["path_results"], a=perm_prep_3,       name="perm_prep_3")
    load_and_save.save_nparray_as_npy(path_results=parameters_used["path_results"], a=depo_prep_2,       name="depo_prep_2")
    load_and_save.save_nparray_as_npy(path_results=parameters_used["path_results"], a=conc_max_or_tot_1, name="conc_max_or_tot_1")
    load_and_save.save_nparray_as_npy(path_results=parameters_used["path_results"], a=cond_tabl_5,       name="cond_tabl_5")
    load_and_save.save_nparray_as_npy(path_results=parameters_used["path_results"], a=adhe_tabl_5,       name="adhe_tabl_5")
    load_and_save.save_nparray_as_npy(path_results=parameters_used["path_results"], a=heav_5,            name="heav_5")
    load_and_save.save_nparray_as_npy(path_results=parameters_used["path_results"], a=delt_5,            name="delt_5")
