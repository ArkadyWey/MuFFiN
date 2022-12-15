from matplotlib import pyplot as plt
import os
import numpy
from scipy import interpolate

import utils_sl
import network_2D

import sys
sys.path.append("/home/user/utils_python")
import plotting


def get_new_interpolated_point(table_x,table_y,new_x_value,type_clog):
    """
    Given a list of x values, and corresponding y values, and
    a new x value, approximate the corresponding function, 
    and use this function to return the new y value 
    corresponding to the new x value.

    Parameters 
    ----------
    - table_x: numpy.ndarray
        1-dimensional list of x values.
    - table_y: numpy.ndarray
        1-dimensional list of y values.
    - new_x_value: float
        New x value for which the corresponding y value is to be approximated.
    
    Returns
    -------
    - new_y_value: float
        Interpolated y value corresponding to new_x_value
    """
    if type_clog == "deposit":
        interpolated_function = interpolate.splrep(x=table_x,y=table_y,k=3)
        new_y_value = interpolate.splev(x=new_x_value, tck=interpolated_function)
        #print(new_x_value)
    elif type_clog == "block":
        step_fun = interpolate.interp1d(table_x, table_y, kind='next') 
        #print("new_x_value:\n{}".format(new_x_value))
        new_y_value = step_fun(new_x_value)
    else: 
        raise Exception("type_clog must be either 'block' or 'deposit'.")
    return new_y_value



# Parameters 
# -----
path_results = os.path.join(".","results/results_network")





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
epsi = parameters["epsi"]
gamm = parameters["gamm"]
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


print(conc_4.shape)
            

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


n = int(numpy.sqrt(num_nodes))
# Get average values of solution down columns that can be plotted against  
# position
# -------
conc_2 = numpy.zeros(shape=(num_time_indxs_to_plot,num_posis))
volu_2 = numpy.zeros(shape=(num_time_indxs_to_plot,num_posis))

cond_2 = numpy.zeros(shape=(num_time_indxs_to_plot,num_posis-1)) # one less edge col than node col
adhe_2 = numpy.zeros(shape=(num_time_indxs_to_plot,num_posis-1)) # one less edge col than node col
for ii_t,i_t in enumerate(reshape_times_1):
    for j_c in range(num_cols):
        for sub_col in range(n):
            # we are now in a particular sub_col aka column of nodes
            # get the indexes of nodes that can appear in this sub col
            indxs_in_sub_col = numpy.linspace(start=0.0+sub_col,stop=num_nodes-n+sub_col,num=n,dtype=int)
            
            # Get mean conc and volu down each node column
            # -------
            concs_in_this_sub_col_1 = []
            volus_in_this_sub_col_1 = []
            for i_c in range(num_rows):
                for i in indxs_in_sub_col:
                    conc = conc_4[ii_t,i,i_c,j_c]
                    concs_in_this_sub_col_1.append(conc)

                    volu = volu_4[ii_t,i,i_c,j_c]
                    volus_in_this_sub_col_1.append(volu)
            
            mean_conc_in_this_sub_col = numpy.mean(concs_in_this_sub_col_1)
            conc_2[ii_t,sub_col+j_c*n] = mean_conc_in_this_sub_col
            
            mean_volu_in_this_sub_col = numpy.mean(volus_in_this_sub_col_1)
            volu_2[ii_t,sub_col+j_c*n] = mean_volu_in_this_sub_col

            # Get cond and adhe in each edge column
            # --------
            if (j_c==num_cols-1 and sub_col==n-1)==False:
                # If we're not in the last node column
                # Get mean cond and adhe down each edge column
                # ------
                if sub_col!=n-1:
                    # If not last ndoe col in cell, 
                    # then there is another to the right
                    sub_col_to_right = sub_col+1
                    indxs_in_sub_col_to_right = numpy.linspace(start=0.0+sub_col_to_right,stop=num_nodes-n+sub_col_to_right,num=n,dtype=int)   
                elif sub_col==n-1:
                    # In last col of nodes in cell, 
                    # col to the right is 0th col of the next cell
                    sub_col_to_right = 0
                    indxs_in_sub_col_to_right = numpy.linspace(start=0.0+sub_col_to_right,stop=num_nodes-n+sub_col_to_right,num=n,dtype=int)   
                else: 
                    raise Exception("Current node column does not exist.")

                conds_in_this_sub_col_1 = []
                adhes_in_this_sub_col_1 = []
                for i_c in range(num_rows):
                    for ii in range(len(indxs_in_sub_col)):
                        i = indxs_in_sub_col[ii]
                        j = indxs_in_sub_col_to_right[ii]

                        if sub_col!=n-1:
                            # Not in last col so j is in same cell as i
                            r0 = 0
                            r1 = 0
                        elif sub_col==n-1:
                            # In last col so j in celll to right of i
                            r0=1
                            r1=0
                        else: 
                            raise Exception("Current node column does not exist.")
                        cond = cond_7[ii_t,i,j,r0,r1,i_c,j_c]
                        conds_in_this_sub_col_1.append(cond)

                        adhe = cond_7[ii_t,i,j,r0,r1,i_c,j_c]
                        adhes_in_this_sub_col_1.append(adhe)

                mean_cond_in_this_sub_col = numpy.mean(conds_in_this_sub_col_1)
                cond_2[ii_t,sub_col+j_c*n] = mean_cond_in_this_sub_col

                mean_adhe_in_this_sub_col = numpy.mean(adhes_in_this_sub_col_1)
                adhe_2[ii_t,sub_col+j_c*n] = mean_adhe_in_this_sub_col
            elif (j_c==num_cols-1 and sub_col==n-1)==True:
                pass
            else:
                raise Exception("Current node column does not exist.")



# Plot concentration
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.scatter(posi_nodes_1,conc_2[0,:], label=r"$t=0$")
ax.scatter(posi_nodes_1,conc_2[1,:], label=r"$t=1/4$")
ax.scatter(posi_nodes_1,conc_2[2,:], label=r"$t=1/2$")
ax.scatter(posi_nodes_1,conc_2[3,:], label=r"$t=3/4$")
ax.scatter(posi_nodes_1,conc_2[4,:], label=r"$t=1$")

# Interpolate the network values
# ------
for ii_t in range(num_time_indxs_to_plot):
    new_y_values_1 = get_new_interpolated_point(table_x=posi_nodes_1,table_y=conc_2[ii_t,:],new_x_value=posi_nodes_1,type_clog="deposit")
    ax.plot(posi_nodes_1,new_y_values_1)

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$\bar{C}_i$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"conc_2__v__posi_nodes_1.svg"), format="svg")




# Plot conductance
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.scatter(posi_edges_1,cond_2[0,:], label=r"$t=0$")
ax.scatter(posi_edges_1,cond_2[1,:], label=r"$t=1/4$")
ax.scatter(posi_edges_1,cond_2[2,:], label=r"$t=1/2$")
ax.scatter(posi_edges_1,cond_2[3,:], label=r"$t=3/4$")
ax.scatter(posi_edges_1,cond_2[4,:], label=r"$t=1$")

# Interpolate the network values
# ------
for ii_t in range(num_time_indxs_to_plot):
    new_y_values_1 = get_new_interpolated_point(table_x=posi_edges_1,table_y=cond_2[ii_t,:],new_x_value=posi_edges_1,type_clog="deposit")
    ax.plot(posi_edges_1,new_y_values_1)

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$\bar{G}_{ij}^{(r^1,0)^\top}$",
                             x_left=-0.05,
                             x_right=+1.05,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"cond_2__v__posi_edges_1.svg"), format="svg")



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
                                                   epsi=epsi, 
                                                   gamm=gamm)
    flux_out_1[i_t] = flux_out
    # reset the first flux to be the second one, since vlocity is artificially zero initially
    flux_out_1[0] = flux_out_1[1]


plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.plot(time_1,flux_out_1)

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$T$",
                             y_label=r"$\bar{Q}_{i\mathrm{out}}$",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"flux_out_1__v__time_1.svg"), format="svg")