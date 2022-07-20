import numpy 

def count_num_edges_blocked(adhe_tabl_5, heav_5):
    """
    Count the number of edges that are blocked 
    in particular run.
    """
    # Parameters 
    adhe_tabl_4 = adhe_tabl_5[-1,:,:,:,:]
    # adhe_tabl_4[i,j,r,s]

    num_refs    = len(adhe_tabl_4[0,0,:,0])

    m = 0
    heav_4      = heav_5[-1,:,:,:,:]
    # heav_4[i,j,r,m]
    #heav_4 = numpy.repeat(a=heav_3[:,:,:,numpy.newaxis], repeats=num_refs, axis=3)
    
    
    count_adhe = 0
    for r in range(num_refs):
        for s in range(num_refs):

            ## Take upper triangle so that edges are unique
            #a = adhe_wo_reps_2 = numpy.triu(adhe_tabl_4[:,:,r,s])

            a = adhe_tabl_4[:,:,r,s]*(numpy.ones_like(heav_4[:,:,r,m]) - heav_4[:,:,r,m])
            # Count number of unique edges where adhesivity is 1
            count_adhe = count_adhe + numpy.count_nonzero(a=a, axis=None, keepdims=False)
    
    return count_adhe
