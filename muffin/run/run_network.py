import numpy
from matplotlib import pyplot as plt
import os
import datetime

import muffin.utils.utils_indexing as utils_indexing
import muffin.network.network_2D as network_2D
import muffin.utils.utils_sl as utils_sl

begin_time = datetime.datetime.now()
print(datetime.datetime.now())


def main(cond_init_6,adhe_init_6,conc_init_3,volu_init_3,time_1,boundary_nodes_network_2,conc_in,alph,beta,delt,epsi,incr):
    """
    - cond_init_6: numpy.ndarray
        cond_init_6[i,j,r0,r1,i_c,j_c]
    - conc_init_3: numpy.ndarray
        conc_init_3[i,i_c,j_c]
    - volu_init_3: numpy.ndarray
        volu_init_3[i,i_c,j_c]
    """
    # Parameters 
    # --------
    num_nodes = len(cond_init_6[:,0,0,0,0,0])
    num_rows  = len(cond_init_6[0,0,0,0,:,0])
    num_cols  = len(cond_init_6[0,0,0,0,0,:])
    num_refs  = len(cond_init_6[0,0,:,0,0,0])
    num_nodes_network = num_nodes*num_rows*num_cols
    num_nodes_with_out = num_nodes_network+1
    num_times = len(time_1)
    dt        = time_1[1]-time_1[0]

    # Reshape initial conditions 
    # ------
    (cond_init_2, internal_edges) = utils_indexing.reshape_6_to_2_internal_edges(a_6=cond_init_6)
    (adhe_init_2, internal_edges) = utils_indexing.reshape_6_to_2_internal_edges(a_6=adhe_init_6)
    conc_init_1 = utils_indexing.reshape_3_to_1_internal_nodes(a_3=conc_init_3)
    volu_init_1 = utils_indexing.reshape_3_to_1_internal_nodes(a_3=volu_init_3)

    # Add out node
    # -----
    (cond_init_2,adhe_init_2,conc_init_1,volu_init_1) = network_2D.get_initial_conds_with_out_node(cond_init_2=cond_init_2,adhe_init_2=adhe_init_2,
                                                                                                   conc_init_1=conc_init_1,volu_init_1=volu_init_1,
                                                                                                   boundary_nodes_network_2=boundary_nodes_network_2)


    # Create storage for grid indexed solution 
    # -----
    cond_3 = numpy.zeros(shape=(num_times,num_nodes_with_out,num_nodes_with_out))
    adhe_3 = numpy.zeros(shape=(num_times,num_nodes_with_out,num_nodes_with_out))
    conc_2 = numpy.zeros(shape=(num_times,num_nodes_with_out))
    volu_2 = numpy.zeros(shape=(num_times,num_nodes_with_out))
    pres_2 = numpy.zeros(shape=(num_times,num_nodes_with_out))
     
    for i_t in range(num_times):               
        #print("Calculating solution at time step {} of {}".format(i_t,num_times-1))
        # Get adherence 
        # -----
        adhe_3[i_t,:,:] = adhe_init_2

        # Get volume 
        # -----
        volu_2[i_t,:] = volu_init_1 
  
        if i_t==0:

            # Get concentration 
            # -----
            conc_2[i_t,:] = conc_init_1
            
            # Get conductance 
            # -----
            cond_3[i_t,:,:] = cond_init_2
        
        elif i_t>0:

            # Get concentration 
            # -----
            conc_2[i_t,:] = network_2D.get_concentration(conc_1=conc_2[i_t-1,:],
                                                         pres_1=pres_2[i_t-1,:],
                                                         volu_1=volu_2[i_t-1,:],
                                                         cond_2=cond_3[i_t-1,:,:],
                                                         boundary_nodes_network_2=boundary_nodes_network_2, 
                                                         conc_in=conc_in, 
                                                         alph=alph,
                                                         delt=delt,
                                                         epsi=epsi,
                                                         dt=dt)

            # Get conductance 
            # -----
            cond_3[i_t,:,:] = network_2D.get_conductance(conc_1=conc_2[i_t-1,:],
                                                         pres_1=pres_2[i_t-1,:],
                                                         cond_2=cond_3[i_t-1,:,:],
                                                         boundary_nodes_network_2=boundary_nodes_network_2, 
                                                         alph=alph,
                                                         beta=beta,
                                                         delt=delt,
                                                         epsi=epsi,
                                                         dt=dt)

        # Get pressure 
        # ------
        (lhs_2,rhs_1) = network_2D.get_pressure_problem(cond_2=cond_3[i_t,:,:], boundary_nodes_network_2=boundary_nodes_network_2)  
        pres_1        = network_2D.get_pressure_solution(lhs_2=lhs_2,rhs_1=rhs_1)
        pres_2[i_t,:] = pres_1

    
    conc_2 = conc_2[0::incr,:] 
    pres_2 = pres_2[0::incr,:]
    volu_2 = volu_2[0::incr,:]
    cond_3 = cond_3[0::incr,:]
    adhe_3 = adhe_3[0::incr,:]

    return (conc_2,pres_2,volu_2,cond_3,adhe_3,internal_edges)

if __name__ == "__main__":

    # Parameters 
    # --------

    # Network
    # ----
    initialisation = "4-reg_prescribed" # 4-reg
    num_nodes = 4
    num_refs  = 3
    num_rows = 2
    num_cols = 20
    # Conductance 
    # ----
    sigma = 0.3
    #mu = 0.5 
    mu = -(sigma**2)/2.0 
    print(mu)

    conc_in = 1.0
    # NETWORK MODEL
    time_end = 1000
    # MULTISCALE MODEL
    #time_end = num_cols*int(numpy.sqrt(num_nodes))**2


    # Model 
    # ----
    
    #nu   = 1.0/numpy.sqrt(num_nodes)
    #epsi = 1.0/num_cols
    #delt = 1.0/(num_nodes*num_cols)
    #beta = 1.0/epsi#*numpy.sqrt(delt)/alph  #/2.0
    #alph = 1.0

    delt = 1.0/numpy.sqrt(num_nodes)
    epsi = 1.0/num_cols
    alph = 1.0#1.0#1.0#0.2#1.0#1.0*(1.0/(epsi*delt))
    beta = 0.01#1.0#0.5#1.0#1.0

    print("delt:{}".format(delt))
    print("epsi:{}".format(epsi))
    print("alph:{}".format(alph))
    print("beta:{}".format(beta))

    incr = 200 # time increment - save every incr-th time point

    num_nodes_hori = int(num_cols*numpy.sqrt(num_nodes))
    num_edge_hori = int(numpy.sqrt(num_nodes)*num_cols)-1
    num_edge_vert = int(numpy.sqrt(num_nodes)*num_rows)-1
    num_edge_network  = num_edge_hori*num_edge_vert

    # Discretisation 
    # -----
    num_times = 20001#40001#101#2001#5001#10001 # 1001
    #2*int(num_edge_hori)
    # int(numpy.sqrt(num_nodes))*num_edge_hori
    #num_nodes*num_cols
    #numpy.sqrt(num_nodes)*num_cols
    # numpy.sqrt(num_nodes)*num_cols
    time_1 = numpy.linspace(0.0,time_end,num_times)


    # Initial conditions 
    # -----
    boundary_nodes_cell_2    = network_2D.get_boundary_nodes_in_cell(initialisation=initialisation,num_nodes=num_nodes)
    boundary_nodes_network_2 = network_2D.get_boundary_nodes_in_network(boundary_nodes_cell_2=boundary_nodes_cell_2,
                                                                        num_nodes=num_nodes,
                                                                        num_rows=num_rows,
                                                                        num_cols=num_cols)
    is_periodic = True

    (cond_init_6,conc_init_3,volu_init_3, _cond_init_4) = network_2D.make_initial_network(num_nodes=num_nodes, 
                                                                                          num_refs=num_refs,
                                                                                          num_rows=num_rows,
                                                                                          num_cols=num_cols,
                                                                                          is_periodic=is_periodic,
                                                                                          initialisation=initialisation,
                                                                                          mu=mu,
                                                                                          sigma=sigma,
                                                                                          boundary_nodes_cell_2=boundary_nodes_cell_2,
                                                                                          conc_in=conc_in)



    
    adhe_init_6 = delt*alph*numpy.ones(shape=(num_nodes,num_nodes,num_refs,num_refs,num_rows,num_cols))

    # Solver 
    # ------
    (conc_2,pres_2,volu_2,cond_3,adhe_3,internal_edges) = main(cond_init_6=cond_init_6,
                                                               adhe_init_6=adhe_init_6,
                                                               conc_init_3=conc_init_3,
                                                               volu_init_3=volu_init_3,
                                                               time_1=time_1,
                                                               boundary_nodes_network_2=boundary_nodes_network_2, 
                                                               conc_in=conc_in,
                                                               alph=alph,
                                                               beta=beta,
                                                               delt=delt,
                                                               epsi=epsi,
                                                               incr=incr)


    # Save results 
    # ----- 
    ensemble = False
    if ensemble == False:
        #path_results = os.path.join(".","results/results_network") # thesis
        path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/results_network") # paper
        
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
    
    # Save the time
    time_1 = time_1[0::incr]
    numpy.save(file=os.path.join(path_results,"time_1.npy"), arr=time_1, allow_pickle=True, fix_imports=True) 

    # Save the results
    numpy.save(file=os.path.join(path_results,"conc_2.npy"), arr=conc_2, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"pres_2.npy"), arr=pres_2, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"volu_2.npy"), arr=volu_2, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"cond_3.npy"), arr=cond_3, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"adhe_3.npy"), arr=adhe_3, allow_pickle=True, fix_imports=True)

    # Save the parameters used
    parameters = {}
    parameters["num_nodes"] = num_nodes
    parameters["num_refs"] = num_refs
    parameters["num_rows"] = num_rows
    parameters["num_cols"] = num_cols
    parameters["internal_edges"] = internal_edges
    parameters["num_nodes_hori"] = num_nodes_hori
    parameters["alph"] = alph
    parameters["beta"] = beta
    parameters["delt"] = delt
    parameters["epsi"] = epsi
    parameters["incr"] = incr

    parameters["initialisation"] = initialisation

    utils_sl.save_dict(dictname=parameters,filename=os.path.join(path_results,"parameters.pkl"))

    # Save the cell used
    numpy.save(file=os.path.join(path_results,"cond_init_4.npy"), arr=_cond_init_4, allow_pickle=True, fix_imports=True)

    print(datetime.datetime.now() - begin_time)

    #row = 1
    #cols_1 = numpy.linspace(0,num_cols-1,num_cols)
    #for i_t in [0,250,500,750,1000]:
    #    conc_3 = utils_indexing.reshape_1_to_3_internal_nodes(a_1=conc_2[i_t,0:-1], num_nodes=num_nodes,num_rows=num_rows,num_cols=num_cols)
    #    concs = []
    #    for col in range(num_cols):
    #        for i in [0,1]:
    #            concs.append(conc_3[i,row,col])
    #    plt.plot(numpy.linspace(0,1,num_nodes_hori),concs)   
    #plt.plot(numpy.linspace(0,1,num_nodes_hori),   ((1-epsi*delt*alph)**numpy.linspace(0,1.0/(delt*epsi)-1, int(numpy.sqrt(num_nodes)*num_cols))), color="black", ls="--")
    #print((1-epsi)**numpy.linspace(0,num_cols-1,num_cols))
    #print((1-epsi)**(num_cols-1))
    #print((1-epsi)**(num_cols-2))
    ##plt.ylim(0,1.01)
    #plt.show()

    print(datetime.datetime.now() - begin_time)



