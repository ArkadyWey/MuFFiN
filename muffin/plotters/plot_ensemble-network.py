from matplotlib import pyplot as plt
import os
import numpy
from scipy import interpolate

import muffin.utils.utils_sl as utils_sl
import muffin.network_2D as network_2D

import sys
sys.path.append("/home/user/utils_python")
import plotting





if __name__ == "__main__":


    # Parameters 
    # -----
    #path_results = os.path.join(".","results/results_network") # thesis
    path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/results_ensemble-network/stats") # paper
    path_results_r = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/results_ensemble-network/r-0") # paper


    # Load variables 
    # -----
    time_1 = numpy.load(os.path.join(path_results_r, "time_1.npy"))
    parameters = utils_sl.load_dict(filename=os.path.join(path_results_r, "parameters.pkl"))

    # Average
    conc_av_2 = numpy.load(os.path.join(path_results, "conc_av_2.npy"))
    pres_av_2 = numpy.load(os.path.join(path_results, "pres_av_2.npy"))
    volu_av_2 = numpy.load(os.path.join(path_results, "volu_av_2.npy"))
    cond_av_3 = numpy.load(os.path.join(path_results, "cond_av_3.npy"))
    adhe_av_3 = numpy.load(os.path.join(path_results, "adhe_av_3.npy"))

    # Standard deviation
    conc_sd_2 = numpy.load(os.path.join(path_results, "conc_sd_2.npy"))
    pres_sd_2 = numpy.load(os.path.join(path_results, "pres_sd_2.npy"))
    volu_sd_2 = numpy.load(os.path.join(path_results, "volu_sd_2.npy"))
    cond_sd_3 = numpy.load(os.path.join(path_results, "cond_sd_3.npy"))
    adhe_sd_3 = numpy.load(os.path.join(path_results, "adhe_sd_3.npy"))

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
    flux_out_av_1 = numpy.zeros(shape=(num_times))
    flux_out_sd_up_1 = numpy.zeros(shape=(num_times))
    flux_out_sd_do_1 = numpy.zeros(shape=(num_times))
    for i_t in range(num_times):
        # Average 
        flux_out_av = network_2D.get_flux_through_network(cond_2=cond_av_3[i_t,:,:],
                                                          pres_1=pres_av_2[i_t,:],
                                                          boundary_nodes_network_2=boundary_nodes_network_2,
                                                          delt=delt,
                                                          epsi=epsi)
        flux_out_av_1[i_t] = flux_out_av
        
        # reset the first flux to be the second one, since vlocity is artificially zero initially
        flux_out_av_1[0] = flux_out_av_1[1]


        # Standard deviation up
        flux_out_sd_up = network_2D.get_flux_through_network(cond_2=cond_av_3[i_t,:,:]+cond_sd_3[i_t,:,:],
                                                             pres_1=pres_av_2[i_t,:]+pres_sd_2[i_t,:],
                                                             boundary_nodes_network_2=boundary_nodes_network_2,
                                                             delt=delt,
                                                             epsi=epsi)
        flux_out_sd_up_1[i_t] = flux_out_sd_up
        # reset the first flux to be the second one, since vlocity is artificially zero initially
        flux_out_sd_up_1[0] = flux_out_sd_up_1[1]


        # Standard deviation down
        flux_out_sd_do = network_2D.get_flux_through_network(cond_2=cond_av_3[i_t,:,:]-cond_sd_3[i_t,:,:],
                                                             pres_1=pres_av_2[i_t,:]-pres_sd_2[i_t,:],
                                                             boundary_nodes_network_2=boundary_nodes_network_2,
                                                             delt=delt,
                                                             epsi=epsi)
        flux_out_sd_do_1[i_t] = flux_out_sd_do
        # reset the first flux to be the second one, since vlocity is artificially zero initially
        flux_out_sd_do_1[0] = flux_out_sd_do_1[1]


    plotting.thesisify_pre_ax_creation()
    fig, ax = plt.subplots(1,1)

    ax.plot(time_1,flux_out_av_1, color="tab:blue")
    ax.fill_between(time_1, flux_out_sd_do_1, flux_out_sd_up_1, alpha=0.5, facecolor="tab:blue")

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
    # Average
    (conc_av_4,pres_av_4,volu_av_4,cond_av_7,adhe_av_7) = network_2D.reshape_solution_grid_to_cell(conc_2=conc_av_2[:,0:-1],
                                                                                                   pres_2=pres_av_2[:,0:-1],
                                                                                                   volu_2=volu_av_2[:,0:-1],
                                                                                                   cond_3=cond_av_3[:,0:-1,0:-1],
                                                                                                   adhe_3=adhe_av_3[:,0:-1,0:-1],
                                                                                                   num_nodes=num_nodes,
                                                                                                   num_rows=num_rows,
                                                                                                   num_cols=num_cols,
                                                                                                   num_refs=num_refs,
                                                                                                   internal_edges=internal_edges,
                                                                                                   reshape_times_1=reshape_times_1)
    # Standard deviation 
    (conc_sd_4,pres_sd_4,volu_sd_4,cond_sd_7,adhe_sd_7) = network_2D.reshape_solution_grid_to_cell(conc_2=conc_sd_2[:,0:-1],
                                                                                                   pres_2=pres_sd_2[:,0:-1],
                                                                                                   volu_2=volu_sd_2[:,0:-1],
                                                                                                   cond_3=cond_sd_3[:,0:-1,0:-1],
                                                                                                   adhe_3=adhe_sd_3[:,0:-1,0:-1],
                                                                                                   num_nodes=num_nodes,
                                                                                                   num_rows=num_rows,
                                                                                                   num_cols=num_cols,
                                                                                                   num_refs=num_refs,
                                                                                                   internal_edges=internal_edges,
                                                                                                   reshape_times_1=reshape_times_1)

    num_posis = num_nodes_hori
    posi_nodes_1 = numpy.linspace(0,1,num_posis)
    dx = posi_nodes_1[1]-posi_nodes_1[0]
    posi_edges_1 = numpy.linspace(0+dx,1-dx,num_posis-1)

    top           = 0
    upper_quarter = int(1*(num_posis-1)/4)
    middle        = int(2*(num_posis-1)/4)
    lower_quarter = int(3*(num_posis-1)/4)
    bottom        = -1

    # Average
    (conc_av_av_2, volu_av_av_2, cond_av_av_2, adhe_av_av_2, pres_av_av_2) = network_2D.get_average_solutions_down_columns(reshape_times_1=reshape_times_1, 
                                                                                                                           num_nodes_hori=num_nodes_hori, 
                                                                                                                           num_rows=num_rows,
                                                                                                                           num_cols=num_cols,
                                                                                                                           cond_7=cond_av_7, 
                                                                                                                           adhe_7=adhe_av_7, 
                                                                                                                           conc_4=conc_av_4, 
                                                                                                                           volu_4=volu_av_4, 
                                                                                                                           pres_4=pres_av_4)
    # Standard deviation 
    (conc_sd_av_2, volu_sd_av_2, cond_sd_av_2, adhe_sd_av_2, pres_sd_av_2) = network_2D.get_average_solutions_down_columns(reshape_times_1=reshape_times_1, 
                                                                                                                           num_nodes_hori=num_nodes_hori, 
                                                                                                                           num_rows=num_rows,
                                                                                                                           num_cols=num_cols,
                                                                                                                           cond_7=cond_sd_7, 
                                                                                                                           adhe_7=adhe_sd_7, 
                                                                                                                           conc_4=conc_sd_4, 
                                                                                                                           volu_4=volu_sd_4, 
                                                                                                                           pres_4=pres_sd_4)


    plotting.thesisify_pre_ax_creation()
    fig_conc, ax_conc = plt.subplots(1,1)

    plotting.thesisify_pre_ax_creation()
    fig_cond, ax_cond = plt.subplots(1,1)

    plotting.thesisify_pre_ax_creation()
    fig_pres, ax_pres = plt.subplots(1,1)

    new_x_values_1 = numpy.linspace(0,1,1000,endpoint=True)
    colors = ["tab:blue","tab:orange","tab:green","tab:red","tab:purple"]

    for ii_t in range(num_time_indxs_to_plot):
        print(ii_t)

        if ii_t == 1:
            # Plot concentration
            # -----

            # Average
            #ax_conc.scatter(posi_nodes_1,conc_av_av_2[ii_t,:])   #label=r"$t=0$"  


            # Interpolate the network values
            # ------
            new_y_values_1 = network_2D.get_new_interpolated_point(table_x=posi_nodes_1,table_y=conc_av_av_2[ii_t,:],new_x_value=posi_nodes_1,type_clog="deposit")
            ax_conc.plot(posi_nodes_1,new_y_values_1, color=colors[ii_t]) 
            ax_conc.plot(posi_nodes_1,conc_av_av_2[ii_t,:], color=colors[ii_t]) 

            if ii_t == 0:
                ax_conc.plot(numpy.linspace(0,1,num_nodes_hori), ((1-epsi*delt*alph)**numpy.linspace(0,1.0/(delt*epsi)-1, int(numpy.sqrt(num_nodes)*num_cols))), color="black", ls="--")
                ax_conc.plot(numpy.linspace(0,1,num_nodes_hori), ((1-epsi*delt*alph)**(1.0/(delt*epsi)-1))*numpy.ones(num_nodes_hori), color="black", ls=":")
            # Standard deviation 
            #ax_conc.scatter(posi_nodes_1,conc_av_av_2[ii_t,:]+conc_sd_av_2[ii_t,:])  
            #ax_conc.scatter(posi_nodes_1,conc_av_av_2[ii_t,:]-conc_sd_av_2[ii_t,:])  

            ax_conc.fill_between(posi_nodes_1, conc_av_av_2[ii_t,:]-conc_sd_av_2[ii_t,:], conc_av_av_2[ii_t,:]+conc_sd_av_2[ii_t,:], alpha=0.5, facecolor=colors[ii_t])
    



        # Plot average conductance
        # -----

        # Average
        #ax_cond.scatter(posi_edges_1,cond_av_av_2[ii_t,:])  

        # Interpolate the network values
        # ------
        new_y_values_1 = network_2D.get_new_interpolated_point(table_x=posi_edges_1,table_y=cond_av_av_2[ii_t,:],new_x_value=posi_edges_1,type_clog="deposit")
        ax_cond.plot(posi_edges_1,new_y_values_1, c=colors[ii_t])

        # Standard deviation 
        #ax_cond.scatter(posi_edges_1,cond_av_av_2[ii_t,:]+cond_sd_av_2[ii_t,:])  
        #ax_cond.scatter(posi_edges_1,cond_av_av_2[ii_t,:]-cond_sd_av_2[ii_t,:])  

        ax_cond.fill_between(posi_edges_1,cond_av_av_2[ii_t,:]-cond_sd_av_2[ii_t,:], cond_av_av_2[ii_t,:]+cond_sd_av_2[ii_t,:], alpha=0.5, facecolor=colors[ii_t])  





        # Plot average pressure
        # -----

        # Average
        #ax_pres.scatter(posi_nodes_1,pres_av_av_2[ii_t,:])   #label=r"$t=0$"  

        # Interpolate the network values
        # ------
        new_y_values_1 = network_2D.get_new_interpolated_point(table_x=posi_nodes_1,table_y=pres_av_av_2[ii_t,:],new_x_value=posi_nodes_1,type_clog="deposit")
        ax_pres.plot(posi_nodes_1,new_y_values_1, c=colors[ii_t])

        # Standard deviation 
        #ax_pres.scatter(posi_nodes_1,pres_av_av_2[ii_t,:]+pres_sd_av_2[ii_t,:])   #label=r"$t=0$"  
        #ax_pres.scatter(posi_nodes_1,pres_av_av_2[ii_t,:]-pres_sd_av_2[ii_t,:])   #label=r"$t=0$"  
        
        ax_pres.fill_between(posi_nodes_1, pres_av_av_2[ii_t,:]-pres_sd_av_2[ii_t,:], pres_av_av_2[ii_t,:]+pres_sd_av_2[ii_t,:], alpha=0.5, facecolor=colors[ii_t])   #label=r"$t=0$"  





    plotting.thesisify_post_plot(ax=ax_conc,
                                 x_label=r"$x$",
                                 y_label=r"$\bar{C}$",
                                 x_left=None,
                                 x_right=None,
                                 y_bottom=None,
                                 y_top=None)

    plotting.save_fig(fig=fig_conc,fname=os.path.join(path_results,"conc_2__v__posi_nodes_1.svg"), format="svg")


    plotting.thesisify_post_plot(ax=ax_cond,
                                 x_label=r"$x$",
                                 y_label=r"$\bar{G}$",
                                 x_left=-0.05,
                                 x_right=+1.05,
                                 y_bottom=None,
                                 y_top=None)

    plotting.save_fig(fig=fig_cond,fname=os.path.join(path_results,"cond_2__v__posi_edges_1.svg"), format="svg")

    plotting.thesisify_post_plot(ax=ax_pres,
                                 x_label=r"$x$",
                                 y_label=r"$\bar{P}$",
                                 x_left=None,
                                 x_right=None,
                                 y_bottom=None,
                                 y_top=None)

    plotting.save_fig(fig=fig_pres,fname=os.path.join(path_results,"pres_2__v__posi_nodes_1.svg"), format="svg")
