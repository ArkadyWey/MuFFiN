from matplotlib import pyplot as plt
import os 
import numpy 
import copy 

import muffin.utils.utils_preprocess as utils_preprocess
import muffin.configure.configure as configure
import muffin.flow.flow as flow 
import muffin.utils.load_and_save

import muffin.plotters.plotting as plotting

# Parameters 
# -----
#path_data = os.path.join(".","results/results_preprocess")
#path_data = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/results_preprocess") # paper
#path_data = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/mono/prep") # paper
#path_data = os.path.join("/home/user/home_temp/projects/papers/2023_homogenisation/figures/mono/beta-0.01/prep") # paper
#path_data = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/mono/prep")
#path_data = os.path.join("./examples/preprocess/init-4-reg/N-4/r-0/data")
#path_data = os.path.join("./examples/preprocess/data")
path_data = os.path.join("./test/test-2")

path_data_dir  = os.path.dirname(path_data)
print(path_data_dir)
path_plot = os.path.join(path_data_dir,"svg")
muffin.utils.load_and_save.check_and_make_dir(path_plot)

type_clog = "deposit"

# Load variables
# -----
conc_max_or_tot_1 = numpy.load(os.path.join(path_data, "conc_max_or_tot_1.npy"))
perm_prep_3       = numpy.load(os.path.join(path_data, "perm_prep_3.npy"))
depo_prep_2       = numpy.load(os.path.join(path_data, "depo_prep_2.npy"))
cond_tabl_5       = numpy.load(os.path.join(path_data, "cond_tabl_5.npy"))
adhe_tabl_5       = numpy.load(os.path.join(path_data, "adhe_tabl_5.npy"))
heav_5            = numpy.load(os.path.join(path_data, "heav_5.npy"))
delt_5            = numpy.load(os.path.join(path_data, "delt_5.npy"))


alph = 0.3
beta = 0.01

# Plot permeability 
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

# Choose dimensions to plot
m = 0
n = 0

#ax.scatter(conc_max_or_tot_1, perm_prep_3[:,m,n], color="tab:blue",   marker="o"  ) # label=r"$k^{11}$"
#ax.scatter(conc_max_or_tot_1, depo_prep_2[:,m]  , color="tab:orange", marker="o") # label=r"$j^{1}$" 

f = numpy.linspace(0.0,conc_max_or_tot_1[-1],1000)

#ax.plot(f, flow.get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=perm_prep_3[:,m,n],new_x_value=f,type_clog=type_clog), color="tab:blue") # , label=r"$\hat{k}^{11}$"
ax.plot(conc_max_or_tot_1, perm_prep_3[:,m,n])
ax.plot(conc_max_or_tot_1, 4/((alph*beta*conc_max_or_tot_1+2)**2), color="tab:orange", ls="--")

#plt.rcParams['text.latex.preamble'] = r"\usepackage{bm}"
plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$s$",
                             y_label=r"$k^{11}$",
                             x_left=0,
                             x_right=1000,
                             y_bottom=0,
                             y_top=1)

plotting.save_fig(fig=fig,fname=os.path.join(path_plot,"perm_prep__3__v__s_1.svg"), format="svg")









# Plot deposition parameter
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

# Choose dimensions to plot
m = 0
n = 0


#ax.scatter(conc_max_or_tot_1, perm_prep_3[:,m,n], color="tab:blue",   marker="o"  ) # label=r"$k^{11}$"
#ax.scatter(conc_max_or_tot_1, depo_prep_2[:,m]  , color="tab:orange", marker="o") # label=r"$j^{1}$" 

f = numpy.linspace(0.0,conc_max_or_tot_1[-1],1000)

ax.plot(f, flow.get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=depo_prep_2[:,m]  ,new_x_value=f,type_clog=type_clog), color="tab:blue") # label=r"$\hat{j}^{1}$ "

ax.plot(conc_max_or_tot_1, alph*4/((alph*beta*conc_max_or_tot_1+2)**2), color="tab:orange", ls="--")

#plt.rcParams['text.latex.preamble'] = r"\usepackage{bm}"
plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$s$",
                             y_label=r"$j^{1}$",
                             x_left=0,
                             x_right=1000,
                             y_bottom=0,
                             y_top=1)

plotting.save_fig(fig=fig,fname=os.path.join(path_plot,"depo_prep__2__v__s_1.svg"), format="svg")





# Plot conductance as a function of f 
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

# non-random
## Choose components to plot
#i = 0 
#j = 1
#r1 = 0
#r2 = 0
#ax.plot(conc_max_or_tot_1, cond_tabl_5[:,i,j,r1,r2], color="tab:green", ls="-")


print(conc_max_or_tot_1.shape)
print(depo_prep_2[:,0])

##ax.scatter(conc_max_or_tot_1, cond_tabl_5[:,i,j,r1,r2], color="tab:blue", marker="o")
## random
#for i in [0,1,2,3]:
#    for j in [0,1,2,3]:
#        for r1 in [-1,0,1]:
#            for r2 in [-1,0,1]:
#                if r1==0 and r2==0:
#                    c = "tab:blue"
#                elif r2!=0:
#                    c="tab:orange"
#                elif r1!=0:
#                    c="tab:green"
#                else: 
#                    raise Exception("There is another scenario, we need another colour!")
#                ax.plot(conc_max_or_tot_1, cond_tabl_5[:,i,j,r1,r2], color=c, ls="-")
##ax.plot(conc_max_or_tot_1, cond_tabl_5[:,i,j,r1,r2], color="tab:blue", marker="o")
# r = 0
# -----



## hori
ax.plot(conc_max_or_tot_1, (cond_tabl_5[:,0,1,0,0]), color="tab:blue", ls="-")
#ax.plot(conc_max_or_tot_1, (cond_tabl_5[:,2,3,0,0]), color="tab:blue", ls="--")
## vert
#ax.plot(conc_max_or_tot_1, (cond_tabl_5[:,0,2,0,0]), color="tab:orange", ls="-")
#ax.plot(conc_max_or_tot_1, (cond_tabl_5[:,1,3,0,0]), color="tab:orange", ls="--")
## r = 1
## -----
## hori
#ax.plot(conc_max_or_tot_1, (cond_tabl_5[:,1,0,1,0]), color="tab:green", ls="-")
#ax.plot(conc_max_or_tot_1, (cond_tabl_5[:,3,2,1,0]), color="tab:green", ls="--")
## vert
#ax.plot(conc_max_or_tot_1, (cond_tabl_5[:,0,2,0,1]), color="tab:red", ls="-")
#ax.plot(conc_max_or_tot_1, (cond_tabl_5[:,1,3,0,1]), color="tab:red", ls="--")



#ax.plot(conc_max_or_tot_1, 4/((alph*beta*conc_max_or_tot_1+2)**2), color="black", ls="--")
#ax.plot(conc_max_or_tot_1, numpy.ones_like(conc_max_or_tot_1), color="black", ls=":")
ax.plot(conc_max_or_tot_1, 4/((alph*beta*conc_max_or_tot_1+2)**2), color="tab:orange", ls="--")


f = numpy.linspace(0.0,conc_max_or_tot_1[-1],1000)

#ax.plot(f, flow.get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=cond_tabl_5[:,i,j,r1,r2],new_x_value=f,type_clog=type_clog), color="tab:blue")
#ax.plot(conc_max_1, flow.get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=depo_prep_2[:,m]  ,new_x_value=conc_max_1,type_clog=type_clog), label=r"$\hat{j}^{1}$", color="blue")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$s$",
                             y_label=r"$G_{ij}^{\bm{r}}$",
                             x_left=0,
                             x_right=1000,
                             y_bottom=0,
                             y_top=1)

plotting.save_fig(fig=fig,fname=os.path.join(path_plot,"cond_5__v__s_1.svg"), format="svg")




# Plot delta as a function of f 
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

# Choose components to plot
f = numpy.linspace(0.0,conc_max_or_tot_1[-1],1000)

# non-random
# ----------------
#ax.scatter(conc_max_or_tot_1, abs(delt_5[:,0,1,0,0]), color="tab:blue", marker="o")
#ax.plot(   conc_max_or_tot_1, abs(delt_5[:,0,1,0,0]), color="tab:blue", ls="-")

#ax.scatter(conc_max_or_tot_1, abs(delt_5[:,0,1,0,1]), color="tab:orange", marker="o")
#ax.plot(   conc_max_or_tot_1, abs(delt_5[:,0,1,0,1]), color="tab:orange", ls="-")

#ax.plot(conc_max_or_tot_1, cond_tabl_5[:,i,j,r1,r2], color="tab:blue", marker="o")

# random
# -----------------
#for i in [0,1,2,3]:
#    for j in [0,1,2,3]:
#        for r in [-1,0,1]:
#            for m in [0]:
#                if r==-1:
#                    c="tab:blue"
#                    ls="-"
#                elif r==0:
#                    c="tab:orange"
#                    ls="--"
#                elif r==1:
#                    c="tab:green"
#                    ls=":"
#                ax.plot(   conc_max_or_tot_1, abs(delt_5[:,i,j,r,m]), color=c, ls=ls)
# r = 0
# -----
# hori
#ax.plot(conc_max_or_tot_1, (delt_5[:,1,0,0,0]), color="tab:blue", ls="-")
ax.plot(conc_max_or_tot_1, (delt_5[:,1,0,0,0]), color="tab:blue", ls="-")
#ax.plot(conc_max_or_tot_1, (delt_5[:,3,2,0,0]), color="tab:blue", ls="--")
ax.plot(conc_max_or_tot_1, (delt_5[:,3,2,0,0]), color="tab:blue", ls="-")
# vert
# ax.plot(conc_max_or_tot_1, (delt_5[:,2,0,0,0]), color="tab:orange", ls="-")
ax.plot(conc_max_or_tot_1, (delt_5[:,2,0,0,0]), color="tab:orange", ls="-")
# ax.plot(conc_max_or_tot_1, (delt_5[:,2,0,0,0]), color="tab:orange", ls="-")
ax.plot(conc_max_or_tot_1, (delt_5[:,3,1,0,0]), color="tab:orange", ls="-")
# r = 1
# -----
# hori
#ax.plot(conc_max_or_tot_1, (delt_5[:,0,1,-1,0]), color="tab:green", ls="-")
ax.plot(conc_max_or_tot_1, (delt_5[:,0,1,-1,0]), color="tab:blue", ls="-")
#ax.plot(conc_max_or_tot_1, (delt_5[:,2,3,-1,0]), color="tab:green", ls="--")
ax.plot(conc_max_or_tot_1, (delt_5[:,2,3,-1,0]), color="tab:blue", ls="-")
# vert
# ax.plot(conc_max_or_tot_1, (delt_5[:,0,2,0,0]), color="tab:red", ls="-")
ax.plot(conc_max_or_tot_1, (delt_5[:,0,2,0,0]), color="tab:orange", ls="-")
# ax.plot(conc_max_or_tot_1, (delt_5[:,1,3,0,0]), color="tab:red", ls="--")
ax.plot(conc_max_or_tot_1, (delt_5[:,1,3,0,0]), color="tab:orange", ls="-")


## r = 0
## -----
## hori
#ax.plot(conc_max_or_tot_1, (heav_5[:,1,0,0,0]), color="tab:blue", ls="-")
#ax.plot(conc_max_or_tot_1, (heav_5[:,3,2,0,0]), color="tab:blue", ls="--")
## vert
#ax.plot(conc_max_or_tot_1, (heav_5[:,0,2,0,0]), color="tab:orange", ls="-")
#ax.plot(conc_max_or_tot_1, (heav_5[:,1,3,0,0]), color="tab:orange", ls="--")
## r = 1
## -----
## hori
#ax.plot(conc_max_or_tot_1, (heav_5[:,0,1,-1,0]), color="tab:green", ls="-")
#ax.plot(conc_max_or_tot_1, (heav_5[:,2,3,-1,0]), color="tab:green", ls="--")
## vert
#ax.plot(conc_max_or_tot_1, (heav_5[:,2,0,0,0]), color="tab:red", ls="-")
#ax.plot(conc_max_or_tot_1, (heav_5[:,3,1,0,0]), color="tab:red", ls="--")
## r = -1
## -----
## hori
#ax.plot(conc_max_or_tot_1, abs(delt_5[:,0,1,-1,0]), color="tab:red", ls="-")
#ax.plot(conc_max_or_tot_1, abs(delt_5[:,2,3,-1,0]), color="tab:red", ls="--")


#f = numpy.linspace(0.0,20.0,1000)

#ax.plot(f, flow.get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=cond_tabl_5[:,i,j,r1,r2],new_x_value=f,type_clog=type_clog), color="tab:blue")
#ax.plot(conc_max_1, flow.get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=depo_prep_2[:,m]  ,new_x_value=conc_max_1,type_clog=type_clog), label=r"$\hat{j}^{1}$", color="blue")

#ax.plot(conc_max_or_tot_1, numpy.zeros_like(conc_max_or_tot_1), color="black", ls=":")
#ax.plot(conc_max_or_tot_1, numpy.ones_like(conc_max_or_tot_1), color="black", ls="--")


plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$s$",
                             y_label=r"$\Delta_{ij}^{r}$",
                             x_left=0,
                             x_right=1001,
                             y_bottom=-0.005,
                             y_top=1.01)
#                             y_bottom=-0.1,
#                             y_top=1.1)

plotting.save_fig(fig=fig,fname=os.path.join(path_plot,"delt_5__v__s_1.svg"), format="svg")


# Plot adhe distribution
# -----
fig, ax = plt.subplots(1,1)

# Count number of non zero in adhe
# -----
# get correct k array 
alpha = 1.0/1.72
# TODO Define alpha properly
 
count_cond = 0
count_adhe = 0
count_above_thresh = 0
num_refs = len( cond_tabl_5[0,0,0,:,0])
num_nodes = len(cond_tabl_5[0,:,0,0,0])

for r in range(num_refs):
    for s in range(num_refs):
        # Take upper triangle so that edges are unique
        cond_wo_reps_2 = numpy.triu(cond_tabl_5[0,:,:,r,s])
        adhe_wo_reps_2 = numpy.triu(adhe_tabl_5[-1,:,:,r,s])

        # Count number of unique non-zero edges
        count_cond = count_cond + numpy.count_nonzero(a=cond_wo_reps_2, axis=None, keepdims=False)

        # Count number of unique edges where adhesivity is 1
        count_adhe = count_adhe + numpy.count_nonzero(a=adhe_wo_reps_2, axis=None, keepdims=False)

        # Check above by counting number of edges that satisfy blocking condition
        for i in range(num_nodes):
            for j in range(num_nodes):
                if cond_wo_reps_2[i,j]<(1.0/alpha) and cond_wo_reps_2[i,j]>0.0:
                    count_above_thresh = count_above_thresh + 1

#print(count_cond)
#print(count_adhe)
#print(count_above_thresh)

# Count number of edges above threshold


def count_num_edges_blocked(adhe_tabl_5, heav_5, delt_5, cond_tanl_5):
    """
    Count the number of edges that are blocked 
    in particular run.
    """
    # Parameters 
    num_refs    = len(adhe_tabl_5[0,0,0,:,0])

    count_adhe = 0
    for r in range(num_refs):
        for s in range(num_refs):

            ## Take upper triangle so that edges are unique
            #a = adhe_wo_reps_2 = numpy.triu(adhe_tabl_4[:,:,r,s])
            a = adhe_tabl_5[-1,:,:,r,s]*heav_5[0,:,:,r,m]*cond_tabl_5[0,:,:,r,s]*(-delt_5[0,:,:,r,m])
            #print("a={}".format(a))
            # Count number of unique edges where adhesivity is 1
            #print("r={},s={},a=\n{}".format(r,s,a))
            #print("r={},s={},a=\n{}".format(r,s,a))
            count_adhe = count_adhe + numpy.count_nonzero(a=a, axis=None, keepdims=False)
    
    return count_adhe

count_adhe = count_num_edges_blocked(adhe_tabl_5, heav_5, delt_5, cond_tabl_5)
print(count_adhe)


count, count_hori, count_not_hori = utils_preprocess.count_num_edges_blocked(initialisation="6-ireg",
                                                                                cond_tabl_5=cond_tabl_5, 
                                                                                adhe_tabl_5=adhe_tabl_5, 
                                                                                delt_5=delt_5, 
                                                                                heav_5=heav_5)
print(count, count_hori, count_not_hori)

r = -1
s = 0
m = 0
#print("heav_5[0,:,:,r,m]:\n{}".format(heav_5[0,:,:,r,m]))
#print("-delt_5[0,:,:,r,m]:\n{}".format(-delt_5[0,:,:,r,m]))
#print("cond_tabl_5[-1,:,:,r,s]:\n{}".format(cond_tabl_5[0,:,:,r,s]))
#print("adhe_tabl_5[-1,:,:,r,s]:\n{}".format(adhe_tabl_5[-1,:,:,r,s]))
