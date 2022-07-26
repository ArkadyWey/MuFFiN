import numpy 

def count_num_edges_blocked(cond_tabl_5, adhe_tabl_5, delt_5, heav_5):
    """
    Count the number of edges that are blocked in particular run.
    Also count the number of these that are horizontal and vertical. 
    I think the latter part of this method only works for 4-reg structure.

    
    """
    # Parameters 
    # -----------
    m         = 0 # interested in flow in horizontal direction
    num_refs  = len(cond_tabl_5[0,0,0,:,0])
    num_nodes = len(cond_tabl_5[0,:,0,0,0])
    n         = int(numpy.sqrt(num_nodes)) # num_rows_or_cols


    count_adhe = 0
    count_adhe_hori = 0
    for r in range(num_refs):
        for s in range(num_refs):
            
            # All edges
            # ---------
            # Get integrand of adhesivity
            a = cond_tabl_5[0,:,:,r,s]*(-delt_5[0,:,:,r,m])*adhe_tabl_5[-1,:,:,r,s]*heav_5[0,:,:,r,m]
            
            # Count number of unique edges where adhesivity is 1
            count_adhe = count_adhe + numpy.count_nonzero(a=a, axis=None, keepdims=False)

            # Horizontal edges 
            # -----------------
            # Count number oghorizontal edges
            if s == 0: # Only hozizontal if s==0
                for b in range(n):
                    # Get integrand of adhesivity
                    a_hori = cond_tabl_5[0,b*n:(b+1)*n,b*n:(b+1)*n,r,s]*(-delt_5[0,b*n:(b+1)*n,b*n:(b+1)*n,r,m])*adhe_tabl_5[-1,b*n:(b+1)*n,b*n:(b+1)*n,r,s]*heav_5[0,b*n:(b+1)*n,b*n:(b+1)*n,r,m]
                    
                    # Count number of horizontal edges where adhesivity is 1
                    # This is number of non zeros in block diagonals
                    count_adhe_hori = count_adhe_hori + numpy.count_nonzero(a=a_hori, axis=None, keepdims=False)

    # Count vertical edges 
    count_adhe_vert = count_adhe-count_adhe_hori

    return count_adhe, count_adhe_hori, count_adhe_vert
