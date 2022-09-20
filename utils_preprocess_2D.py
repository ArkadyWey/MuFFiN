import numpy 

def count_num_edges_blocked(initialisation, cond_tabl_5, adhe_tabl_5, delt_5, heav_5):
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
    #sum_a = 0]
    cnt = 0
    for r in range(num_refs):
        for s in range(num_refs):
            
            # All edges
            # ---------
            # Get integrand of adhesivity
            a = cond_tabl_5[0,:,:,r,s]*(-delt_5[0,:,:,r,m])*adhe_tabl_5[-1,:,:,r,s]*heav_5[0,:,:,r,m]
            b = cond_tabl_5[0,:,:,r,s]*(-delt_5[0,:,:,r,m])
            #sum_a = sum_a + numpy.sum(a)
            #print(b)
            cnt = cnt + numpy.count_nonzero(a=b, axis=None, keepdims=False)
            
            # Count number of unique edges where adhesivity is 1
            count_adhe = count_adhe + numpy.count_nonzero(a=a, axis=None, keepdims=False)

            #print("r={},s={}".format(r,s))
            #print("a:\n{}".format(a))
            #print("delt:\n{}".format((-delt_5[0,:,:,r,m])*adhe_tabl_5[-1,:,:,r,s]*heav_5[0,:,:,r,m]))
            #print("cond:\n{}".format(cond_tabl_5[0,:,:,r,s]))

            if initialisation=="4-reg":
                """
                If initialisation=="4-reg" then get the number of horizontal edges that are blocked.
                """
                # NOTE: Below is only valid  fpr 4-reg:
                # Horizontal edges 
                # -----------------
                # Count number of horizontal edges
                if s == 0: # Only hozizontal if s==0
                    for b in range(n):
                        # Get integrand of adhesivity
                        a_hori = cond_tabl_5[0,b*n:(b+1)*n,b*n:(b+1)*n,r,s]*(-delt_5[0,b*n:(b+1)*n,b*n:(b+1)*n,r,m])*adhe_tabl_5[-1,b*n:(b+1)*n,b*n:(b+1)*n,r,s]*heav_5[0,b*n:(b+1)*n,b*n:(b+1)*n,r,m]

                        # Count number of horizontal edges where adhesivity is 1
                        # This is number of non zeros in block diagonals
                        count_adhe_hori = count_adhe_hori + numpy.count_nonzero(a=a_hori, axis=None, keepdims=False)

            elif initialisation == "6-reg":
                """
                If initialisation=="6-reg, then check if how many horizontal edges are blocked. 
                To do this, get the list of pairs of indices that we know will 
                be between horizontal edges. 
                Then for each horizontal edge pair, check whether this is blocked 
                by checking whether there is a non-zero entry in a at this index pair.
                """
                horizontal_edge_pairs = get_horizontal_index_pairs(num_nodes=num_nodes)
                for pair in horizontal_edge_pairs:
                    left_index = pair[0]
                    right_index = pair[1]
                    #print(a[left_index,right_index])
                    if a[left_index,right_index] != 0.0:
                        count_adhe_hori = count_adhe_hori + 1
                    else: 
                        pass

            elif initialisation == "6-ireg":
                count_adhe_hori = None 
            
            else: 
                raise Exception("initilisation must be 4-reg, 6-reg, or 6-ireg.")


    if initialisation=="4-reg":
        """
        If initialisation=="4-reg" then get the number of vertical edges that are blocked.
        Use horizontal count to save computational time.
        """
        # Count vertical edges 
        count_adhe_not_hori = count_adhe-count_adhe_hori
    
    if initialisation=="6-reg":
        """
        If initialisation=="6-reg" then get the number of diagonal edges that are blocked. 
        This is the total number of edges that are blocked minus the number of horizontal edges 
        that are blocked.
        """
        # Count diagonal edges 
        count_adhe_not_hori = count_adhe-count_adhe_hori
    elif initialisation=="6-ireg":
        count_adhe_not_hori = None 
    else:
        raise Exception("Initialisation must be 4-reg,6-reg, or 6-ireg.")

    #print(count_adhe, count_adhe_hori, count_adhe_not_hori)
    #print(sum_a/numpy.sqrt(3))
    #if -sum_a/numpy.sqrt(3) > 4.0:
    #    exit()
    print("cnt: {}".format(cnt))
    return count_adhe, count_adhe_hori, count_adhe_not_hori



def get_horizontal_index_pairs(num_nodes):
    """
    Get a list of all pairs of node indices that are either end 
    of a horizontal edge in a 6-reg structure with a cell containing num_nodes
    nodes.
    Each pair is itself a list.

    """
    N = num_nodes
    n = int(numpy.sqrt(N/2))

    if num_nodes == 2: 
        """
        This is a special case, but luckily 
        pairs are easy to identify, since there 
        are only two.
        """
        pairs = [[0,0],[1,1]]

    else: 
        """
        For every other case there is an algorithm. 
        See notes from 7.8.22 for details.
        """

        # Define index list 
        # -------
        """
        index_list is a list of constructor indices that make up a constructor 
        set from which all index pairs are derived. 
        This should be the set [0,1,2,...,n-1,0]
        The zero on the end is there because we need a cycle.
        """
        index_list = list(numpy.linspace(start=0,stop=n,num=n,dtype=int,endpoint=False)) # use argument unpacker
        index_list.append(0)

        """
        Given the set of constructor indices above, 
        the below algorithm defines all possible pairs.
        """
        pairs = []
        for k in range(n): # [0,...,n-1]
            for i in range(n): # [0,...,n-1]
                index_left = index_list[i]
                index_right = index_list[i+1]

                # Even pair
                # ------
                even_left_node_index  = k*2*n + 2*index_left
                even_right_node_index = k*2*n + 2*index_right

                even_pair = [even_left_node_index, even_right_node_index]

                pairs.append(even_pair)
                

                # Odd pair
                # -----
                odd_left_node_index  = k*2*n + 2*index_left + 1
                odd_right_node_index = k*2*n + 2*index_right + 1

                odd_pair = [odd_left_node_index, odd_right_node_index]

                #print("odd_pair:{}".format(odd_pair))

                pairs.append(odd_pair)
    
    return pairs
        


