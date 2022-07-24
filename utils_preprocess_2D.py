import numpy 
import copy

def count_num_edges_blocked(adhe_tabl_5, heav_5, delt_5, cond_init_4):
    """
    Count the number of edges that are blocked 
    in particular run.
    """
    # Parameters 
    m = 0
    num_refs    = len(adhe_tabl_5[-1,0,0,:,0])

    adhe_tabl_4 = adhe_tabl_5[-1,:,:,:,:]
    # adhe_tabl_4[i,j,r,s]

    heav_4      = heav_5[0,:,:,:,:]
    
    delt_4 = delt_5[0,:,:,:,:]
    delt_ind_4 = copy.copy(delt_4)
    delt_ind_4[delt_ind_4!=0]
    
    # Indicators
    cond_init_ind_4 = copy.copy(cond_init_4)
    cond_init_ind_4[cond_init_ind_4!=0.0]


    
    count_adhe = 0
    for r in range(num_refs):
        for s in range(num_refs):

            ## Take upper triangle so that edges are unique
            #a = adhe_wo_reps_2 = numpy.triu(adhe_tabl_4[:,:,r,s])

            a = cond_init_4[:,:,r,s]*adhe_tabl_4[:,:,r,s]*heav_4[:,:,r,m]*delt_ind_4[:,:,r,m] #*cond_init_ind_4[:,:,r,s]
            # Count number of unique edges where adhesivity is 1
            count_adhe = count_adhe + numpy.count_nonzero(a=a, axis=None, keepdims=False)
    
    return count_adhe
