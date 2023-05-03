from matplotlib import pyplot as plt
import os
import numpy
from scipy import interpolate

import utils_sl
import network_2D

import sys
sys.path.append("/home/user/utils_python")
import plotting





if __name__ == "__main__":


    # Parameters 
    # -----
    #path_results = os.path.join(".","results/results_network") # thesis
    path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/results_network") # paper

    #path_results = os.path.join(".","results/results_network/thesis/sweep-alph/tiny-sweep/alph-0.1_T-1")
    #path_results = "/home/user/Dropbox/Gore-OxfordCDT-2019/repos/multiscale-models/multiscale_models/results/results_network/thesis/sweep-alph/large-sweep/alph-zero"




    # Load variables 
    # -----
    time_1 = numpy.load(os.path.join(path_results, "time_1.npy"))

    conc_2 = numpy.load(os.path.join(path_results, "conc_2.npy"))
    pres_2 = numpy.load(os.path.join(path_results, "pres_2.npy"))
    volu_2 = numpy.load(os.path.join(path_results, "volu_2.npy"))
    cond_3 = numpy.load(os.path.join(path_results, "cond_3.npy"))
    adhe_3 = numpy.load(os.path.join(path_results, "adhe_3.npy"))
    print(conc_2.shape)


    parameters = utils_sl.load_dict(filename=os.path.join(path_results, "parameters.pkl"))


    num_times = len(time_1)

    start          = 0
    first_quarter  = int(1*(num_times-1)/4)
    second_quarter = int(2*(num_times-1)/4)
    third_quarter  = int(3*(num_times-1)/4)
    end            = -1

    time_indxs_to_plot = [start,first_quarter,second_quarter,third_quarter,end]
    reshape_times_1 = time_indxs_to_plot
    num_time_indxs_to_plot = len(time_indxs_to_plot)


    num_nodes = parameters["num_nodes"]
    num_refs = parameters["num_refs"]
    num_rows = parameters["num_rows"]
    num_cols = parameters["num_cols"]
    internal_edges = parameters["internal_edges"]
    num_nodes_hori = parameters["num_nodes_hori"]
    alph = parameters["alph"]
    beta = parameters["beta"]
    delt = parameters["delt"]
    epsi = parameters["epsi"]
    initialisation = parameters["initialisation"]

    print("alph: {}".format(alph))
    print("beta: {}".format(beta))
    print("delt: {}".format(delt))
    print("epsi: {}".format(epsi))

    # Plot flux out as function of time
    # -----
    boundary_nodes_cell_2 = network_2D.get_boundary_nodes_in_cell(initialisation=initialisation,num_nodes=num_nodes)
    boundary_nodes_network_2 = network_2D.get_boundary_nodes_in_network(boundary_nodes_cell_2=boundary_nodes_cell_2,
                                                                        num_nodes=num_nodes,
                                                                        num_rows=num_rows,
                                                                        num_cols=num_cols)
    flux_out_1 = numpy.zeros(shape=(num_times))
    for i_t in range(num_times):
        flux_out = network_2D.get_flux_through_network(cond_2=cond_3[i_t,:,:],
                                                       pres_1=pres_2[i_t,:],
                                                       boundary_nodes_network_2=boundary_nodes_network_2,
                                                       delt=delt,
                                                       epsi=epsi)
        flux_out_1[i_t] = flux_out
        # reset the first flux to be the second one, since vlocity is artificially zero initially
        flux_out_1[0] = flux_out_1[1]


    plotting.thesisify_pre_ax_creation()
    fig, ax = plt.subplots(1,1)

    ax.plot(time_1,flux_out_1)

    plotting.thesisify_post_plot(ax=ax,
                                 x_label=r"$T$",
                                 y_label=r"$U$",
                                 x_left=None,
                                 x_right=None,
                                 y_bottom=None,
                                 y_top=None)

    plotting.save_fig(fig=fig,fname=os.path.join(path_results,"flux_out_1__v__time_1.svg"), format="svg")





    # Get solution in cell_indexed form at desired times 
    # -----
    print("Cell-indexing the solution...")
    (conc_4,pres_4,volu_4,cond_7,adhe_7) = network_2D.reshape_solution_grid_to_cell(conc_2=conc_2[:,0:-1],
                                                                                    pres_2=pres_2[:,0:-1],
                                                                                    volu_2=volu_2[:,0:-1],
                                                                                    cond_3=cond_3[:,0:-1,0:-1],
                                                                                    adhe_3=adhe_3[:,0:-1,0:-1],
                                                                                    num_nodes=num_nodes,
                                                                                    num_rows=num_rows,
                                                                                    num_cols=num_cols,
                                                                                    num_refs=num_refs,
                                                                                    internal_edges=internal_edges,
                                                                                    reshape_times_1=reshape_times_1)


    num_posis = num_nodes_hori
    print(num_nodes_hori)
    posi_nodes_1 = numpy.linspace(0,1,num_posis)
    dx = posi_nodes_1[1]-posi_nodes_1[0]
    posi_edges_1 = numpy.linspace(0+dx,1-dx,num_posis-1)

    top           = 0
    upper_quarter = int(1*(num_posis-1)/4)
    middle        = int(2*(num_posis-1)/4)
    lower_quarter = int(3*(num_posis-1)/4)
    bottom        = -1

    (conc_av_2, volu_av_2, cond_av_2, adhe_av_2, pres_av_2) = network_2D.get_average_solutions_down_columns(reshape_times_1=reshape_times_1, 
                                                                                                            num_nodes_hori=num_nodes_hori, 
                                                                                                            num_rows=num_rows,
                                                                                                            num_cols=num_cols,
                                                                                                            cond_7=cond_7, 
                                                                                                            adhe_7=adhe_7, 
                                                                                                            conc_4=conc_4, 
                                                                                                            volu_4=volu_4, 
                                                                                                            pres_4=pres_4)





    # Plot average concentration
    # -----
    plotting.thesisify_pre_ax_creation()
    fig, ax = plt.subplots(1,1)

    ax.scatter(posi_nodes_1,conc_av_2[0,:])   #label=r"$t=0$"  
    ax.scatter(posi_nodes_1,conc_av_2[1,:])   #label=r"$t=1/4$"
    ax.scatter(posi_nodes_1,conc_av_2[2,:])   #label=r"$t=1/2$"
    ax.scatter(posi_nodes_1,conc_av_2[3,:])   #label=r"$t=3/4$"
    ax.scatter(posi_nodes_1,conc_av_2[4,:])   #label=r"$t=1$"  

    # Interpolate the network values
    # ------
    for ii_t in range(num_time_indxs_to_plot):
        new_y_values_1 = network_2D.get_new_interpolated_point(table_x=posi_nodes_1,table_y=conc_av_2[ii_t,:],new_x_value=posi_nodes_1,type_clog="deposit")
        ax.plot(posi_nodes_1,new_y_values_1)

    ax.plot(numpy.linspace(0,1,num_nodes_hori), ((1-epsi*delt*alph)**numpy.linspace(0,1.0/(delt*epsi)-1, int(numpy.sqrt(num_nodes)*num_cols))), color="black", ls="--")
    ax.plot(numpy.linspace(0,1,num_nodes_hori), ((1-epsi*delt*alph)**(1.0/(delt*epsi)-1))*numpy.ones(num_nodes_hori), color="black", ls=":")

    plotting.thesisify_post_plot(ax=ax,
                                 x_label=r"$x$",
                                 y_label=r"$\bar{C}$",
                                 x_left=None,
                                 x_right=None,
                                 y_bottom=None,
                                 y_top=None)

    plotting.save_fig(fig=fig,fname=os.path.join(path_results,"conc_2__v__posi_nodes_1.svg"), format="svg")






    # Plot average conductance
    # -----
    plotting.thesisify_pre_ax_creation()
    fig, ax = plt.subplots(1,1)

    ax.scatter(posi_edges_1,cond_av_2[0,:])  #label=r"$t=0$"  
    ax.scatter(posi_edges_1,cond_av_2[1,:])  #label=r"$t=1/4$"
    ax.scatter(posi_edges_1,cond_av_2[2,:])  #label=r"$t=1/2$"
    ax.scatter(posi_edges_1,cond_av_2[3,:])  #label=r"$t=3/4$"
    ax.scatter(posi_edges_1,cond_av_2[4,:])  #label=r"$t=1$"  

    # Interpolate the network values
    # ------
    for ii_t in range(num_time_indxs_to_plot):
        new_y_values_1 = network_2D.get_new_interpolated_point(table_x=posi_edges_1,table_y=cond_av_2[ii_t,:],new_x_value=posi_edges_1,type_clog="deposit")
        ax.plot(posi_edges_1,new_y_values_1)

    plotting.thesisify_post_plot(ax=ax,
                                 x_label=r"$x$",
                                 y_label=r"$\bar{G}$",
                                 x_left=-0.05,
                                 x_right=+1.05,
                                 y_bottom=None,
                                 y_top=None)

    plotting.save_fig(fig=fig,fname=os.path.join(path_results,"cond_2__v__posi_edges_1.svg"), format="svg")





    # Plot average pressure
    # -----
    plotting.thesisify_pre_ax_creation()
    fig, ax = plt.subplots(1,1)

    ax.scatter(posi_nodes_1,pres_av_2[0,:])   #label=r"$t=0$"  
    ax.scatter(posi_nodes_1,pres_av_2[1,:])   #label=r"$t=1/4$"
    ax.scatter(posi_nodes_1,pres_av_2[2,:])   #label=r"$t=1/2$"
    ax.scatter(posi_nodes_1,pres_av_2[3,:])   #label=r"$t=3/4$"
    ax.scatter(posi_nodes_1,pres_av_2[4,:])   #label=r"$t=1$"  

    # Interpolate the network values
    # ------
    for ii_t in range(num_time_indxs_to_plot):
        new_y_values_1 = network_2D.get_new_interpolated_point(table_x=posi_nodes_1,table_y=pres_av_2[ii_t,:],new_x_value=posi_nodes_1,type_clog="deposit")
        ax.plot(posi_nodes_1,new_y_values_1)

    plotting.thesisify_post_plot(ax=ax,
                                 x_label=r"$x$",
                                 y_label=r"$\bar{P}$",
                                 x_left=None,
                                 x_right=None,
                                 y_bottom=None,
                                 y_top=None)

    plotting.save_fig(fig=fig,fname=os.path.join(path_results,"pres_2__v__posi_nodes_1.svg"), format="svg")


    # Plot conductance at boundary 
    # ----------
    plotting.thesisify_pre_ax_creation()
    fig, ax = plt.subplots(1,1)

    #ax.plot(time_1,cond_3[:,0,1])  
    ax.plot(time_1,cond_3[:,0,0])  
    #ax.plot(time_1,cond_7[:,0,1,0,0,0,0])  
    ax.plot(time_1,1.0/(1.0-1.0*0.5*time_1)**2.0)  


    plotting.thesisify_post_plot(ax=ax,
                                 x_label=r"$t$",
                                 y_label=r"$\bar{G}(0)$",
                                 x_left=None,
                                 x_right=None,
                                 y_bottom=None,
                                 y_top=None)

    plotting.save_fig(fig=fig,fname=os.path.join(path_results,"cond_3__v__time_1.svg"), format="svg")
