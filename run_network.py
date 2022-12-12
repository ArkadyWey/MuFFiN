import numpy
from matplotlib import pyplot as plt
import os
import datetime

import utils_indexing
import network_2D

begin_time = datetime.datetime.now()
print(datetime.datetime.now())


def main(cond_init_6,adhe_init_6,conc_init_3,volu_init_3,time_1,boundary_nodes_network_2,conc_in,beta,gamm,epsi):
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
        print("Calculating solution at time step {} of {}".format(i_t,num_times-1))
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
                                                         adhe_2=adhe_3[i_t-1,:,:],
                                                         boundary_nodes_network_2=boundary_nodes_network_2, 
                                                         conc_in=conc_in, 
                                                         epsi=epsi,
                                                         gamm=gamm,
                                                         dt=dt)

            # Get conductance 
            # -----
            cond_3[i_t,:,:] = network_2D.get_conductance(conc_1=conc_2[i_t-1,:],
                                                         pres_1=pres_2[i_t-1,:],
                                                         volu_1=volu_2[i_t-1,:],
                                                         cond_2=cond_3[i_t-1,:,:],
                                                         adhe_2=adhe_3[i_t-1,:,:], 
                                                         boundary_nodes_network_2=boundary_nodes_network_2, 
                                                         beta=beta,
                                                         gamm=gamm,
                                                         dt=dt)

            # Get pressure 
            # ------
            (lhs_2,rhs_1) = network_2D.get_pressure_problem(cond_2=cond_3[i_t,:,:], boundary_nodes_network_2=boundary_nodes_network_2)  
            pres_1        = network_2D.get_pressure_solution(lhs_2=lhs_2,rhs_1=rhs_1)
            pres_2[i_t,:] = pres_1

    # Remove out node
    conc_2

    return (conc_2,pres_2,volu_2,cond_3,adhe_3,internal_edges)

if __name__ == "__main__":

    # Parameters 
    # --------
    initialisation = "4-reg"
    num_nodes = 4
    num_refs  = 3

    mu = 0.5 
    sigma = 0.3

    conc_in = 1.0
    beta    = 0.1
    adhe    = 1.0#0.1

    num_rows = 2
    num_cols = 5

    epsi = 1.0/num_cols

    num_edge_hori = int(numpy.sqrt(num_nodes)*num_cols)-1
    num_edge_vert = int(numpy.sqrt(num_nodes)*num_rows)-1
    num_edge_network  = num_edge_hori*num_edge_vert
    gamm = 1.0/(num_edge_hori)

    print(num_edge_hori)
    print(num_cols)

    num_times = 1001#5001#10001 # 1001
    #2*int(num_edge_hori)
    # int(numpy.sqrt(num_nodes))*num_edge_hori
    time_1 = numpy.linspace(0,2*num_nodes*num_cols,num_times)

    boundary_nodes_cell_2    = network_2D.get_boundary_nodes_in_cell(initialisation=initialisation,num_nodes=num_nodes)
    boundary_nodes_network_2 = network_2D.get_boundary_nodes_in_network(boundary_nodes_cell_2=boundary_nodes_cell_2,
                                                                        num_nodes=num_nodes,
                                                                        num_rows=num_rows,
                                                                        num_cols=num_cols)
    is_periodic = True

    # Initial conditions 
    # -----
    (cond_init_6,conc_init_3,volu_init_3) = network_2D.make_initial_network(num_nodes=num_nodes, 
                                                                            num_refs=num_refs,
                                                                            num_rows=num_rows,
                                                                            num_cols=num_cols,
                                                                            is_periodic=is_periodic,
                                                                            initialisation=initialisation,
                                                                            mu=mu,
                                                                            sigma=sigma,
                                                                            boundary_nodes_cell_2=boundary_nodes_cell_2,
                                                                            conc_in=conc_in)

    
    adhe_init_6 = adhe*numpy.ones(shape=(num_nodes,num_nodes,num_refs,num_refs,num_rows,num_cols))

    # Solver 
    # ------
    (conc_2,pres_2,volu_2,cond_3,adhe_3,internal_edges) = main(cond_init_6=cond_init_6,
                                                               adhe_init_6=adhe_init_6,
                                                               conc_init_3=conc_init_3,
                                                               volu_init_3=volu_init_3,
                                                               time_1=time_1,
                                                               boundary_nodes_network_2=boundary_nodes_network_2, 
                                                               conc_in=conc_in,
                                                               beta=beta,
                                                               gamm=gamm,
                                                               epsi=epsi)


    # Save results 
    # ----- 
    path_results = os.path.join(".","results/results_network")
    if not os.path.exists(path_results):
        os.mkdir(path_results)

    numpy.save(file=os.path.join(path_results,"time_1.npy"), arr=time_1, allow_pickle=True, fix_imports=True) 

    numpy.save(file=os.path.join(path_results,"conc_2.npy"), arr=conc_2, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"pres_2.npy"), arr=pres_2, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"volu_2.npy"), arr=volu_2, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"cond_3.npy"), arr=cond_3, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"adhe_3.npy"), arr=adhe_3, allow_pickle=True, fix_imports=True)

    print(datetime.datetime.now() - begin_time)

    row = 0
    cols_1 = numpy.linspace(0,num_cols-1,num_cols)
    for i_t in [0,250,500,750,1000]:
        conc_3 = utils_indexing.reshape_1_to_3_internal_nodes(a_1=conc_2[i_t,0:-1], num_nodes=num_nodes,num_rows=num_rows,num_cols=num_cols)
        concs = []
        for col in range(num_cols):
            for i in [0,1]:
                concs.append(conc_3[i,row,col])
        plt.plot(numpy.linspace(0,1,int(num_cols*numpy.sqrt(num_nodes))),concs)   
    plt.plot(numpy.linspace(0,1,int(num_cols*numpy.sqrt(num_nodes))),   ((1-gamm)**numpy.linspace(0,int(numpy.sqrt(num_nodes)*num_cols)-1, int(numpy.sqrt(num_nodes)*num_cols))))
    print((1-epsi)**numpy.linspace(0,num_cols-1,num_cols))
    print((1-epsi)**(num_cols-1))
    print((1-epsi)**(num_cols-2))
    plt.ylim(0,1.01)
    plt.show()

    print(datetime.datetime.now() - begin_time)

    # Reshape results into cell indexing
    # -------
    print("Reshaping the solution...")
    (conc_4,pres_4,volu_4,cond_7,adhe_7) = network_2D.reshape_solution_grid_to_cell(conc_2=conc_2,
                                                                                    pres_2=pres_2,
                                                                                    volu_2=volu_2,
                                                                                    cond_3=cond_3,
                                                                                    adhe_3=adhe_3,
                                                                                    num_nodes=num_nodes,
                                                                                    num_rows=num_rows,
                                                                                    num_cols=num_cols,
                                                                                    num_refs=num_refs,
                                                                                    internal_edges=internal_edges)

    numpy.save(file=os.path.join(path_results,"conc_4.npy"), arr=conc_4, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"pres_4.npy"), arr=pres_4, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"volu_4.npy"), arr=volu_4, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"cond_7.npy"), arr=cond_7, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"adhe_7.npy"), arr=adhe_7, allow_pickle=True, fix_imports=True)


