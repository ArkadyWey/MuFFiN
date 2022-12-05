import numpy
from matplotlib import pyplot as plt

import network_2D



def main(cond_init_6,adhe_init_6,conc_init_3,volu_init_3,time_1,dt,boundary_nodes_2):
    """
    - cond_init_6: numpy.ndarray
        cond_init_6[i,j,r0,r1,i_c,j_c]
    - conc_init_3: numpy.ndarray
        conc_init_3[i,i_c,j_c]
    - volu_init_3: numpy.ndarray
        volu_init_3[i,i_c,j_c]
    """
    # Parameters 
    num_nodes = len(cond_init_6[:,0,0,0,0,0])
    num_refs = len(cond_init_6[0,0,:,0,0,0])
    num_rows = len(cond_init_6[0,0,0,0,:,0])
    num_cols = len(cond_init_6[0,0,0,0,0,:])
    num_times = len(time_1)

    cond_7 = numpy.zeros(shape=(num_times,num_nodes,num_nodes,num_refs,num_refs,num_rows,num_cols))
    adhe_7 = numpy.zeros(shape=(num_times,num_nodes,num_nodes,num_refs,num_refs,num_rows,num_cols))
    conc_4 = numpy.zeros(shape=(num_times,num_nodes,num_rows,num_cols))
    volu_4 = numpy.zeros(shape=(num_times,num_nodes,num_rows,num_cols))
    pres_4 = numpy.zeros(shape=(num_times,num_nodes,num_rows,num_cols))
    for i_t in range(num_times):
        for i_c in range(num_rows):
            for j_c in range(num_cols):
                volu_4[i_t,:,i_c,j_c]       = volu_init_3[:,i_c,j_c]
                adhe_7[i_t,:,:,:,:,i_c,j_c] = adhe_init_6[:,:,:,:,i_c,j_c]
                
                if i_t==0:
                    # Get concentration 
                    # -----
                    conc_4[i_t,:,i_c,j_c]       = conc_init_3[:,i_c,j_c]
                    
                    # Get conductance 
                    # -----
                    cond_7[i_t,:,:,:,:,i_c,j_c] = cond_init_6[:,:,:,:,i_c,j_c]

                    # Get pressure 
                    # ------
                    if j_c == 0:
                        # inlet is in cell so no outlet nodes 
                        boundary_nodes_2["outlet"] = []
                    elif j_c == num_cols-1: 
                        # outlet is in cell so no inlet nodes 
                        boundary_nodes_2["inlet"] = []
                    else: 
                        # cell is in middle and no inlet or outlet nodes in cell
                        boundary_nodes_2["inlet"] = []
                        boundary_nodes_2["outlet"] = []

                    (lhs_2,rhs_1) = network_2D.get_pressure_problem(cond_4=cond_7[i_t,:,:,:,:,i_c,j_c], 
                                                                    boundary_nodes_2=boundary_nodes_2)  
                    pres_1 = network_2D.get_pressure_solution(lhs_2=lhs_2,rhs_1=rhs_1)
                    pres_4[i_t,:,i_c,j_c] = pres_1
                
                elif i_t>0:
                    conc_3 = conc_4[i_t-1,:,:,:]
                    volu_3 = volu_4[i_t-1,:,:,:]
                    pres_3 = pres_4[i_t-1,:,:,:]
                    cond_6 = cond_7[i_t-1,:,:,:,:,:,:]
                    adhe_6 = adhe_7[i_t-1,:,:,:,:,:,:]
                    
                    # Get concentration 
                    # -----
                    conc_1 = network_2D.get_concentration(conc_3=conc_3,pres_3=pres_3,volu_3=volu_3,cond_6=cond_6,adhe_6=adhe_6,i_c=i_c,j_c=j_c,dt=dt)
                    conc_4[i_t,:,i_c,j_c] = conc_1

                    # Get conductance
                    # -----
                    cond_4 = network_2D.get_conductance(conc_3=conc_3,pres_3=pres_3,cond_6=cond_6,adhe_6=adhe_6,i_c=i_c,j_c=j_c,dt=dt)
                    cond_7[i_t,:,:,:,:,i_c,j_c] = cond_4

                    # Get pressure 
                    # -----
                    (lhs_2,rhs_1) = network_2D.get_pressure_problem(cond_4=cond_7[i_t,:,:,:,:,i_c,j_c], 
                                                                    boundary_nodes_2=boundary_nodes_2)  
                    pres_1 = network_2D.get_pressure_solution(lhs_2=lhs_2,rhs_1=rhs_1)
                    pres_4[i_t,:,i_c,j_c] = pres_1

    return (conc_4,pres_4,volu_4,cond_7,adhe_7)


if __name__ == "__main__":

    # Parameters 
    # --------
    initialisation = "4-reg"
    num_nodes = 4
    num_refs  = 3

    mu = 0.5 
    sigma = 0.3

    conc_in = 1.0

    num_rows = 3
    num_cols = 3

    num_times = 101#5001#10001 # 1001
    time_1 = numpy.linspace(0,1,num_times)
    dt = time_1[1] - time_1[0]

    boundary_nodes_2 = network_2D.get_boundary_nodes(initialisation=initialisation,num_nodes=num_nodes)
    is_periodic = True

    # Initial conditions 
    # -----
    (cond_init_6,conc_init_3,volu_init_3) = network_2D.make_initial_network(num_nodes=num_nodes, num_refs=num_refs,
                                                                            num_rows=num_rows,num_cols=num_cols,
                                                                            is_periodic=is_periodic,
                                                                            initialisation=initialisation,
                                                                            mu=mu,sigma=sigma,
                                                                            boundary_nodes_2=boundary_nodes_2,conc_in=1.0)
    
    adhe_init_6 = 1.0*numpy.ones(shape=(num_nodes,num_nodes,num_refs,num_refs,num_rows,num_cols))


    (conc_4,pres_4,volu_4,cond_7,adhe_7) = main(cond_init_6=cond_init_6,
                                                adhe_init_6=adhe_init_6,
                                                conc_init_3=conc_init_3,
                                                volu_init_3=volu_init_3,
                                                time_1=time_1,
                                                dt=dt,
                                                boundary_nodes_2=boundary_nodes_2)

    row = 0
    node = 0
    cols_1 = numpy.linspace(0,num_cols-1,num_cols)
    for i_t in [0,10,20,30]:
        plt.plot(cols_1,conc_4[i_t,node,row,:])
    plt.show()