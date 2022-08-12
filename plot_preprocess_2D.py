from matplotlib import pyplot as plt
import os 
import numpy 
import copy 

import utils_preprocess_2D
import configure

# Parameters 
# -----
path_results = os.path.join(".","results/results_preprocess_2D")


# Load variables
# -----
conc_max_disc_1 = numpy.load(os.path.join(path_results, "conc_max_disc_1.npy"))
perm_prep_3     = numpy.load(os.path.join(path_results, "perm_prep_3.npy"))
depo_prep_2     = numpy.load(os.path.join(path_results, "depo_prep_2.npy"))
cond_tabl_5     = numpy.load(os.path.join(path_results, "cond_tabl_5.npy"))
adhe_tabl_5     = numpy.load(os.path.join(path_results, "adhe_tabl_5.npy"))
heav_5          = numpy.load(os.path.join(path_results, "heav_5.npy"))
delt_5          = numpy.load(os.path.join(path_results, "delt_5.npy"))


# Plot permeability and deposition parameter values on one axis 
# -----
fig, ax = plt.subplots(1,1)

# Choose dimensions to plot
m = 0
n = 0


ax.plot(conc_max_disc_1, perm_prep_3[:,m,n], label=r"$k$", color="red")
ax.plot(conc_max_disc_1, depo_prep_2[:,m],   label=r"$j$", color="blue")
ax.set_xlabel("c")
ax.legend()
plt.savefig(fname=os.path.join(path_results,"perm_prep_3__depo_prep_2__v__conc_max_disc_1.svg"), format="svg")



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


count, count_hori, count_not_hori = utils_preprocess_2D.count_num_edges_blocked(initialisation="6-reg",
                                                                                cond_tabl_5=cond_tabl_5, 
                                                                                adhe_tabl_5=adhe_tabl_5, 
                                                                                delt_5=delt_5, 
                                                                                heav_5=heav_5)
print(count, count_hori, count_not_hori)

r = -1
s = 0
m = 0
#print("heav_5[0,:,:,r,m]:\n{}".format(heav_5[0,:,:,r,m]))
print("-delt_5[0,:,:,r,m]:\n{}".format(-delt_5[0,:,:,r,m]))
print("cond_tabl_5[-1,:,:,r,s]:\n{}".format(cond_tabl_5[0,:,:,r,s]))
#print("adhe_tabl_5[-1,:,:,r,s]:\n{}".format(adhe_tabl_5[-1,:,:,r,s]))

conf = configure.Configure(num_nodes=2,initialisation="6-reg",sigma=0.3)
print(conf.mean)
print(conf.scaled_mean)
