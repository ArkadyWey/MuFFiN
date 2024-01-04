import os
import numpy
from matplotlib import pyplot as plt

import muffin.network.network_2D as network_2D
import muffin.utils.utils_sl as utils_sl

import sys
sys.path.append("/home/user/utils_python")
import plotting


#model_parameters = ["alph-zero","alph-quar","alph-half","alph-thre","alph-full",] # large-sweep
#model_parameters = ["alph-1","alph-2","alph-3","alph-4","alph-5",] #small-sweep
model_parameters = ["alph-0.1","alph-0.2","alph-0.3","alph-0.4","alph-0.5","alph-0.6","alph-0.7","alph-0.8","alph-0.9","alph-1.0",] #small-sweep
#model_parameters = ["alph-0.2","alph-0.4","alph-0.6","alph-0.8","alph-1.0",] #small-sweep

colors = ["tab:blue","tab:orange","tab:green","tab:red","tab:purple","tab:blue","tab:orange","tab:green","tab:red","tab:purple",]

#results_sub_path = "thesis/sweep-epsi/alph-0"
results_sub_path = "thesis/sweep-alph/tiny-sweep/"
#results_sub_path = "thesis/sweep-alph/large-sweep/"
path_results_sweep = os.path.join(".","results/results_network/",results_sub_path)


# Prepare plots for filling
plotting.thesisify_pre_ax_creation()
fig_conc, ax_conc = plt.subplots(1,1)
fig_pres, ax_pres = plt.subplots(1,1)
fig_cond, ax_cond = plt.subplots(1,1)
fig_flow, ax_flow = plt.subplots(1,1)

efficiencies = [0.0]
for i_p,p in enumerate(model_parameters):
    # Set linestyle of for this param
    c = colors[i_p]
    ax_conc.set_prop_cycle(None) # reset color cycle but change ls

    # Get path to results
    path_results = os.path.join(".","results/results_network/"+results_sub_path,p)


    # Load variables 
    # -----
    time_1 = numpy.load(os.path.join(path_results, "time_1.npy"))

    conc_2 = numpy.load(os.path.join(path_results, "conc_2.npy"))
    pres_2 = numpy.load(os.path.join(path_results, "pres_2.npy"))
    volu_2 = numpy.load(os.path.join(path_results, "volu_2.npy"))
    cond_3 = numpy.load(os.path.join(path_results, "cond_3.npy"))
    adhe_3 = numpy.load(os.path.join(path_results, "adhe_3.npy"))


    parameters = utils_sl.load_dict(filename=os.path.join(path_results, "parameters.pkl"))


    num_times = len(time_1)

    end            = -1

    time_indxs_to_plot = [end]
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




    # Plot concentration
    # -----
    ax_conc.set_prop_cycle(None) # reset color cycle but change ls
    ax_conc.scatter(posi_nodes_1,conc_av_2[0,:],c=c)   #label=r"$t=0$"  

    # Interpolate the network values
    # ------
    ax_conc.set_prop_cycle(None) # reset color cycle but change ls
    for ii_t in range(num_time_indxs_to_plot):
        new_y_values_1 = network_2D.get_new_interpolated_point(table_x=posi_nodes_1,table_y=conc_av_2[ii_t,:],new_x_value=posi_nodes_1,type_clog="deposit")
        ax_conc.plot(posi_nodes_1,new_y_values_1,c=c)


    # Plot pressure
    # -----
    ax_pres.set_prop_cycle(None) # reset color cycle but change ls
    ax_pres.scatter(posi_nodes_1,pres_av_2[0,:],c=c)   #label=r"$t=0$"  

    # Interpolate the network values
    # ------
    ax_pres.set_prop_cycle(None) # reset color cycle but change ls
    for ii_t in range(num_time_indxs_to_plot):
        new_y_values_1 = network_2D.get_new_interpolated_point(table_x=posi_nodes_1,table_y=pres_av_2[ii_t,:],new_x_value=posi_nodes_1,type_clog="deposit")
        ax_pres.plot(posi_nodes_1,new_y_values_1,c=c)

    # Plot conductance
    # -----
    ax_cond.set_prop_cycle(None) # reset color cycle but change ls
    ax_cond.scatter(posi_edges_1,cond_av_2[0,:],c=c)  #label=r"$t=0$"  

    # Interpolate the network values
    # ------
    ax_cond.set_prop_cycle(None) # reset color cycle but change ls
    for ii_t in range(num_time_indxs_to_plot):
        new_y_values_1 = network_2D.get_new_interpolated_point(table_x=posi_edges_1,table_y=cond_av_2[ii_t,:],new_x_value=posi_edges_1,type_clog="deposit")
        ax_cond.plot(posi_edges_1,new_y_values_1,c=c)


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

    # Plot flow
    # ------
    ax_flow.set_prop_cycle(None) # reset color cycle but change ls
    ax_flow.plot(time_1,flux_out_1,c=c)

    efficiencies.append(1-conc_av_2[0,-1])

# Plot efficiency
# -------
fig_effi, ax_effi = plt.subplots(1,1)
#alphas = [0.0,0.2,0.4,0.6,0.8,1.0]
alphas = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
ax_effi.scatter(alphas,efficiencies,c="tab:blue")
new_alphas = numpy.linspace(0.0,1.0,100,endpoint=True)
new_y_values_1 = network_2D.get_new_interpolated_point(table_x=alphas,table_y=efficiencies,new_x_value=new_alphas,type_clog="deposit")
ax_effi.plot(new_alphas,new_y_values_1,c="tab:blue")
alph_1 = numpy.linspace(0,1,100)
ax_effi.plot(alph_1, 1-(((1-epsi*delt*alph_1)**(1.0/(delt*epsi)-1))), color="black", ls="--")

plotting.thesisify_post_plot(ax=ax_effi,
                             x_label=r"$\alpha$",
                             y_label=r"$\eta$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)
plotting.save_fig(fig=fig_effi,fname=os.path.join(path_results_sweep,"effi_net_1__v__alphas_1.svg"), format="svg")



# Post-process and save figures
# -----
# Concentration 
# --------
plotting.thesisify_post_plot(ax=ax_conc,
                             x_label=r"$x$",
                             y_label=r"$\bar{C}$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)
plotting.save_fig(fig=fig_conc,fname=os.path.join(path_results_sweep,"conc_2__v__posi_nodes_1.svg"), format="svg")

# Pressure 
# --------
plotting.thesisify_post_plot(ax=ax_pres,
                             x_label=r"$x$",
                             y_label=r"$\bar{P}$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)
plotting.save_fig(fig=fig_pres,fname=os.path.join(path_results_sweep,"pres_2__v__posi_nodes_1.svg"), format="svg")

# Conductance 
# ------
plotting.thesisify_post_plot(ax=ax_cond,
                             x_label=r"$x$",
                             y_label=r"$\bar{G}$",
                             x_left=-0.05,
                             x_right=+1.05,
                             y_bottom=None,
                             y_top=None)
plotting.save_fig(fig=fig_cond,fname=os.path.join(path_results_sweep,"cond_2__v__posi_edges_1.svg"), format="svg")


# Darcy flow
# ---------
plotting.thesisify_post_plot(ax=ax_flow,
                             x_label=r"$T$",
                             y_label=r"$U$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)
plotting.save_fig(fig=fig_flow,fname=os.path.join(path_results_sweep,"flux_out_1__v__time_1.svg"), format="svg")