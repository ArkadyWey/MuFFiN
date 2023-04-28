from matplotlib import pyplot as plt
import os
import numpy


import utils_sl
import network_2D

import sys
sys.path.append("/home/user/utils_python")
import plotting

#path_output = os.path.join(".","results/results_comparison/random/epsi-0.1") # thesis
path_output = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/results_comparison") # paper
if not os.path.exists(path_output):
    os.mkdir(path_output)


# Preprocess figures 
# -----

# Velocity 
plotting.thesisify_pre_ax_creation()
fig_velo, ax_velo = plt.subplots(1,1)

# Concentration 
plotting.thesisify_pre_ax_creation()
fig_conc, ax_conc = plt.subplots(1,1)

# Conductance 
plotting.thesisify_pre_ax_creation()
fig_cond, ax_cond = plt.subplots(1,1)

# MAE 
plotting.thesisify_pre_ax_creation()
fig_mae, ax_mae = plt.subplots(1,1)


# Flow 
# ------------------------------------------

# Get flow parameters 
# -----
#path_results_flow = os.path.join(path_output,"results_flow") # thesis
path_results_flow = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/results_flow") # paper

# Load flow variables 
# -----
time_flow_1 = numpy.load(os.path.join(path_results_flow, "time_1.npy"))
posi_flow_1 = numpy.load(os.path.join(path_results_flow, "posi_1.npy"))

conc_flow_2     = numpy.load(os.path.join(path_results_flow, "conc_2.npy"))
conc_max_or_tot_flow_2 = numpy.load(os.path.join(path_results_flow, "conc_max_or_tot_2.npy"))
perm_flow_2     = numpy.load(os.path.join(path_results_flow, "perm_2.npy"))
depo_flow_2     = numpy.load(os.path.join(path_results_flow, "depo_2.npy"))
velo_flow_1     = numpy.load(os.path.join(path_results_flow, "velo_1.npy"))
dpdx_flow_2     = numpy.load(os.path.join(path_results_flow, "dpdx_2.npy"))
psi_flow_2      = numpy.load(os.path.join(path_results_flow, "psi_2.npy"))

num_times_flow = len(time_flow_1)

start_flow          = 0
first_quarter_flow  = int(1*(num_times_flow-1)/4)
second_quarter_flow = int(2*(num_times_flow-1)/4)
third_quarter_flow  = int(3*(num_times_flow-1)/4)
end_flow            = -1



# Plot flow figures 
# -----
# Velocity
ax_velo.plot(time_flow_1,velo_flow_1, ls="-", c="tab:blue")

# Reset the color cycle and plot normal over histogram for each N
ax_velo.set_prop_cycle(None)


# Concentration 
ax_conc.plot(posi_flow_1,conc_flow_2[:,start_flow],         ) # label=r"$t=0$"
ax_conc.plot(posi_flow_1,conc_flow_2[:,first_quarter_flow], ) # label=r"$t=1/4$"
ax_conc.plot(posi_flow_1,conc_flow_2[:,second_quarter_flow],) # label=r"$t=1/2$"
ax_conc.plot(posi_flow_1,conc_flow_2[:,third_quarter_flow], ) # label=r"$t=3/4$"
ax_conc.plot(posi_flow_1,conc_flow_2[:,end_flow],           ) # label=r"$t=1$"
#ax_conc.plot(posi_flow_1,numpy.exp(-1.0)*numpy.ones_like(posi_flow_1))

# Reset the color cycle and plot normal over histogram for each N
ax_conc.set_prop_cycle(None)


# Conductance
ax_cond.plot(posi_flow_1,perm_flow_2[:,start_flow])
ax_cond.plot(posi_flow_1,perm_flow_2[:,first_quarter_flow])
ax_cond.plot(posi_flow_1,perm_flow_2[:,second_quarter_flow]) #301 is index where prob starts
ax_cond.plot(posi_flow_1,perm_flow_2[:,third_quarter_flow])
ax_cond.plot(posi_flow_1,perm_flow_2[:,end_flow])

# Reset the color cycle and plot normal over histogram for each N
ax_cond.set_prop_cycle(None)




# Network
# -------------------------------------
para_1 = [0.1,0.05,0.025]

param_names = []
for p in para_1:
    param_names.append("epsi-"+str(p))
#param_names = ["epsi-0.1", "epsi-0.05"]#, "epsi-0.025"]

linestyles = [":","--","-."]
mae_1 = []
#path_results_network = os.path.join(path_output,"results_network") # thesis
#path_results_network = os.path.join(".","results/results_network/thesis/sweep-alph/tiny-sweep/alph-0.1_T-1")
#path_results_network = "/home/user/Dropbox/Gore-OxfordCDT-2019/repos/multiscale-models/multiscale_models/results/results_network/thesis/sweep-alph/large-sweep/alph-zero"


for p,param in enumerate(param_names):
    path_results_network = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/results_network/",param) # paper
    ls =linestyles[p]

    # Load network variables 
    # -----
    parameters = utils_sl.load_dict(filename=os.path.join(path_results_network, "parameters.pkl"))

    time_1 = numpy.load(os.path.join(path_results_network, "time_1.npy"))
    conc_2 = numpy.load(os.path.join(path_results_network, "conc_2.npy"))
    pres_2 = numpy.load(os.path.join(path_results_network, "pres_2.npy"))
    volu_2 = numpy.load(os.path.join(path_results_network, "volu_2.npy"))
    cond_3 = numpy.load(os.path.join(path_results_network, "cond_3.npy"))
    adhe_3 = numpy.load(os.path.join(path_results_network, "adhe_3.npy"))
    

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


    # Velocity
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


    ax_velo.plot(time_1,flux_out_1, ls=ls, c="tab:orange")

    # Reset the color cycle and plot normal over histogram for each N
    ax_velo.set_prop_cycle(None)

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


    # Concentration
    # -----
    #ax_conc.scatter(posi_nodes_1,conc_av_2[0,:])   #label=r"$t=0$"  
    #ax_conc.scatter(posi_nodes_1,conc_av_2[1,:])   #label=r"$t=1/4$"
    #ax_conc.scatter(posi_nodes_1,conc_av_2[2,:])   #label=r"$t=1/2$"
    #ax_conc.scatter(posi_nodes_1,conc_av_2[3,:])   #label=r"$t=3/4$"
    #ax_conc.scatter(posi_nodes_1,conc_av_2[4,:])   #label=r"$t=1$"  

    # Reset the color cycle and plot normal over histogram for each N
    ax_conc.set_prop_cycle(None)

    # Interpolate the network values
    # ------
    for ii_t in range(num_time_indxs_to_plot):
        new_y_values_1 = network_2D.get_new_interpolated_point(table_x=posi_nodes_1,table_y=conc_av_2[ii_t,:],new_x_value=posi_nodes_1,type_clog="deposit")
        ax_conc.plot(posi_nodes_1,new_y_values_1,ls=ls)

    maes_network = numpy.zeros(num_time_indxs_to_plot)
    for ii_t in range(num_time_indxs_to_plot):
        new_y_values_1 = network_2D.get_new_interpolated_point(table_x=posi_nodes_1,table_y=conc_av_2[ii_t,:],new_x_value=posi_flow_1,type_clog="deposit")
        #ax_conc.plot(posi_nodes_1,new_y_values_1,ls=ls)

        if ii_t == 0:
            y_flow = conc_flow_2[:,start_flow]
        elif ii_t == 1:
            y_flow = conc_flow_2[:,first_quarter_flow]
        elif ii_t == 2:
            y_flow = conc_flow_2[:,second_quarter_flow]
        elif ii_t == 3:
            y_flow = conc_flow_2[:,third_quarter_flow]
        elif ii_t == 4:
            y_flow = conc_flow_2[:,end_flow]

        y_network = new_y_values_1
        maes_network[ii_t] = numpy.absolute(numpy.subtract(y_flow, y_network)).mean()
    mae = maes_network.mean()
    print(mae)
    mae_1.append(mae)
    #ax.plot(numpy.linspace(0,1,num_nodes_hori), ((1-epsi*delt*alph)**numpy.linspace(0,1.0/(delt*epsi)-1, int(numpy.sqrt(num_nodes)*num_cols))), color="black", ls=ls)
    #ax.plot(numpy.linspace(0,1,num_nodes_hori), ((1-epsi*delt*alph)**(1.0/(delt*epsi)-1))*numpy.ones(num_nodes_hori), color="black", ls=":")


    # Conductance
    # -----
    #ax_cond.scatter(posi_edges_1,cond_av_2[0,:])  #label=r"$t=0$"  
    #ax_cond.scatter(posi_edges_1,cond_av_2[1,:])  #label=r"$t=1/4$"
    #ax_cond.scatter(posi_edges_1,cond_av_2[2,:])  #label=r"$t=1/2$"
    #ax_cond.scatter(posi_edges_1,cond_av_2[3,:])  #label=r"$t=3/4$"
    #ax_cond.scatter(posi_edges_1,cond_av_2[4,:])  #label=r"$t=1$"  

    # Reset the color cycle and plot normal over histogram for each N
    ax_cond.set_prop_cycle(None)

    # Interpolate the network values
    # ------
    for ii_t in range(num_time_indxs_to_plot):
        new_y_values_1 = network_2D.get_new_interpolated_point(table_x=posi_edges_1,table_y=cond_av_2[ii_t,:],new_x_value=posi_edges_1,type_clog="deposit")
        ax_cond.plot(posi_edges_1,new_y_values_1,ls=ls)



# Post process figures 
# -------------------------

# Velocity
plotting.thesisify_post_plot(ax=ax_velo,
                             x_label=r"$t$",
                             y_label=r"$u$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig_velo,fname=os.path.join(path_output,"velo_1__v__time_1.svg"), format="svg")

# Concentration
plotting.thesisify_post_plot(ax=ax_conc,
                             x_label=r"$x^1$",
                             y_label=r"$c$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)


plotting.save_fig(fig=fig_conc,fname=os.path.join(path_output,"conc_2__v__posi_1.svg"), format="svg")

# Conductance
plotting.thesisify_post_plot(ax=ax_cond,
                             x_label=r"$x^1$",
                             y_label=r"$k^{11}$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig_cond,fname=os.path.join(path_output,"perm_2__v__posi_1.svg"), format="svg")

# MAE
ax_mae.scatter(para_1,mae_1)

para_fine_1 = numpy.linspace(0,1,100)
new_y_values_1 = network_2D.get_new_interpolated_point(table_x=para_1,table_y=mae_1,new_x_value=para_fine_1,type_clog="deposit")

ax_mae.plot(para_fine_1,new_y_values_1)

plotting.thesisify_post_plot(ax=ax_mae,
                             x_label=r"$\epsilon$",
                             y_label=r"$\mathrm{MAE}$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig_mae,fname=os.path.join(path_output,"mae_1__v__epsi_1.svg"), format="svg")
