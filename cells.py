import numpy
import scipy
from scipy import spatial
import random



class Cell_2D_four_reg():
    """
    Class for the cell of a 2D grid network.
    In cell, we form the intra adjacency matrix, which is the cell adjacency matrix, 
    and intra volume matrices. 
    These are then passed to the network, which 
    forms an intercell adjacency matrix, and intercell edge volume matrix, 
    and then uses these and the intracell matrices to form network ones.
    """
    def __init__(self, num_rows_cell,
                       num_cols_cell):
        """
        """
        # Parameters
        self.num_rows_cell: int = num_rows_cell
        self.num_cols_cell: int = num_cols_cell
        self.num_nodes_cell: int = self.num_rows_cell*self.num_cols_cell

        # Make intracell adjacency matrix
        self.adj_intra_2 = self.make_adj_intra_2()
   
    def make_adj_intra_2(self):
        """
        Make anetwork that is a grid.

        n_row: number of nodes in row
        n_col: number of nodes in col
        n_grid: number of nodes in grid (must be n_row*n_col)

        REVISIT THIS FUNCTION AND USE numpy.kron
        TO MAKE INTRAROW and INTERROW CONNECTIONS 
        EXPLICIT. This will be more generalisable 
        to more random networks.
        """
        n_row = self.num_rows_cell
        n_col = self.num_cols_cell
        # --------
        n_grid = n_row*n_col

        # Form block
        diagonals = [numpy.ones(n_col-1), numpy.ones(n_col-1)]
        A = scipy.sparse.diags(diagonals=diagonals, offsets=[1,-1], shape=(n_col, n_col)).toarray()
        #print(A)

        # Form block diagonal
        tup = n_row*(A,)
        B = scipy.linalg.block_diag(*tup)
        #print(B)

        # Form outer diagonals
        more_diagonals = [numpy.ones(n_grid-n_col), numpy.ones(n_grid-n_col)]
        C = scipy.sparse.diags(diagonals=more_diagonals, offsets=[n_col, -n_col], shape=(n_grid, n_grid)).toarray()
        #print(C)

        adj = B + C

        return adj


  

class Cell_2D_six_ireg():
    """
    """ 
    def __init__(self, num_nodes: int,
                       num_refs: int, 
                       num_dims: int,
                       mean: float,
                       leng_1: numpy.ndarray,
                       mu: float, 
                       sigma: float):
        """
        Parameters 
        # -------
        - mean: float 
            The mean of the lognormal distribution from which the conductance is drawn. 
            This is the conductance per unit length of the edges in the resulting cell. 

        """
        # Parameters
        self.num_nodes = num_nodes
        self.num_refs  = num_refs
        self.num_dims  = num_dims
        self.mean      = mean
        self.leng_1    = leng_1
        self.mu        = mu
        self.sigma     = sigma
        
        self.l1 = leng_1[0]
        self.l2 = leng_1[1]

        (self.pts_x_0, self.pts_y_0, self.pts_x_1, self.pts_y_1, self.pts_x_m1, self.pts_y_m1) = self.get_node_coordinates()

        self.pts_4 = self.get_points_tensor()

        self.dist_6 = self.get_distance_between_points()

        (self.simplices, self.key) = self.get_simplices_of_triangulation()

        self.edges = self.get_edges()

        self.cond_init_4 = self.get_conductance()


    def get_node_coordinates(self):
        """
        Get x and y coordinates of each point.
        
        Returns
        -------
        - pts_x_0: numpy.ndarray
            pts_x_0[i] is x coordinate of node i in cell with r = 0.
        - pts_y_0: numpy.ndarray
            pts_y_0[i] is y coordinate of node i in cell with s = 0.
        - pts_x_1: numpy.ndarray
            pts_x                                                                                                                                                       _1[i] is x coordinate of node i in cell with r = 1.
        - pts_y_1: numpy.ndarray
            pts_y_1[i] is y coordinate of node i in cell with s = 1.
        - pts_x_m1: numpy.ndarray
            pts_x_m1[i] is x coordinate of node i in cell with r = -1.
        - pts_y_m1: numpy.ndarray
            pts_y_m1[i] is y coordinate of node i in cell with s = -1.
        """
        # Parameters 
        num_nodes = self.num_nodes
        l1        = self.l1
        l2        = self.l2


        # Get unit cell points
        pts_x_0 = numpy.random.uniform(low=0.0, high=l1, size=num_nodes) #*l1 
        pts_y_0 = numpy.random.uniform(low=0.0, high=l2, size=num_nodes) #*l2 

        # Right and up components
        pts_x_1 = l1*numpy.ones_like(pts_x_0) + pts_x_0 
        pts_y_1 = l2*numpy.ones_like(pts_y_0) + pts_y_0

        ## Left and down components
        pts_x_m1 = -l1*numpy.ones_like(pts_x_0) + pts_x_0
        pts_y_m1 = -l2*numpy.ones_like(pts_y_0) + pts_y_0

        return (pts_x_0, 
                pts_y_0,
                pts_x_1,
                pts_y_1,
                pts_x_m1,
                pts_y_m1)


    def get_points_tensor(self):
        """
        Put node coordinates into tensor.

        Returns
        -------
        - pts_4: numpy.ndarray
            pts_4[i,m,r,s] is the x^m (either x or y) component of node i in cell at reference r,s.
        """
        # Parameters 
        num_nodes = self.num_nodes 
        num_refs  = self.num_refs
        num_dims  = self.num_dims

        pts_x_0   = self.pts_x_0
        pts_y_0   = self.pts_y_0
        pts_x_1   = self.pts_x_1
        pts_y_1   = self.pts_y_1
        pts_x_m1   = self.pts_x_m1
        pts_y_m1   = self.pts_y_m1

        # Make empty array
        pts_4 = numpy.zeros(shape=(num_nodes,num_dims,num_refs,num_refs))
        
        for r in range(num_refs):
            for s in range(num_refs):
                for i in range(num_nodes):

                    if r == 0:
                        pts_x = pts_x_0
                    elif r == 1:
                        pts_x = pts_x_1
                    elif r == 2: 
                        pts_x = pts_x_m1

                    if s == 0:
                        pts_y = pts_y_0
                    elif s == 1:
                        pts_y = pts_y_1
                    elif s == 2: 
                        pts_y = pts_y_m1

                    pts_4[i,0,r,s] = pts_x[i]
                    pts_4[i,1,r,s] = pts_y[i]      

        return pts_4


    def get_distance_between_points(self):
        """
        For each pair of points (i,r,s) in the points tensor,
        get their x and y coordinates and calculate the euclidean distance between them.

        Returns 
        --------

        """
        # Parameters
        num_nodes = self.num_nodes
        num_refs  = self.num_refs 

        pts_4     = self.pts_4
        
        dist_6 = numpy.zeros(shape=(num_nodes,num_refs,num_refs,num_nodes,num_refs,num_refs))
        # dist_6[i,r_i,s_i, j,r_j,s_j] = distance between node (i,r_i,s_i) and (j,r_j,s_j)
        for r_i in range(num_refs):
            for s_i in range(num_refs):
                for r_j in range(num_refs):
                    for s_j in range(num_refs):
                        for i in range(num_nodes):
                            for j in range(num_nodes):
                                # Get x,y coordinates corresponding to nodes
                                p_i = pts_4[i,:,r_i,s_i]
                                p_j = pts_4[j,:,r_j,s_j]
                                # Get distance between points
                                dist_6[i,r_i,s_i,j,r_j,s_j] = numpy.linalg.norm(p_i-p_j)

        return dist_6


    def get_simplices_of_triangulation(self):
        """
        Get all points in points tensor in correct form to use triangulation 
        method. 
        Then Triangulate all points using Delaunay triangulation.

        Returns 
        -------- 
        - simplices: list of lists.
            simplices[s] = [p_s_1,p_s_2,p_s_3] where p_s_i is the ith point on the s^th simplex.
            I.e. each simplex is a list of three points that make a triangle.
            These are indexed by p, hence we need a key between p and our indexing system (i,r,s).
        - key: list
            key[p] = [i,r,s] triple corresponding to point p. That is, a triple 
            that tells us the index, and r,s cell position of the point p. 
            We use this to map between two indexings, p, and (i,r,s).
        """
        # Parameters 
        num_refs  = self.num_refs
        num_nodes = self.num_nodes

        pts_4     = self.pts_4

        # Make empty lists
        # -----
        pts_to_tri_2 = []
        key = []
        # pts_to_tri_2[p,m] = mth (x or y) component of point p - need in this form for Delaunay algorithm.
        # key[p] = [i,r,s] triple corresponding to point p
        
        # Get all points in correct form
        # -----
        for r in range(num_refs):
            for s in range(num_refs):
                for i in range(num_nodes):
                    i_x = pts_4[i,0,r,s] # x component of point corresponding to node i in cell r,s
                    i_y = pts_4[i,1,r,s] # y component of point corresponding to node i in cell r,s

                    pts_to_tri_2.append([i_x,i_y]) 
                    key.append([i,r,s])

        pts_to_tri_2 = numpy.array(pts_to_tri_2)

        # Triangulate points
        tri = spatial.Delaunay(points=pts_to_tri_2)
        
        # Get simplices
        simplices = tri.simplices
        # simplices[s] = [p_s_1,p_s_2,p_s_3] where p_s_i is the ith point on the s^th simplex.

        self.key = key
        self.simplices = simplices
        self.pts_to_tri_2 = pts_to_tri_2
        return (simplices, key)


    def get_edges(self):
        """
        Turn each simplex into a loop, then extract the three edges from that loop. 
        
        Returns
        -------
        - edges: list
            Unstructured list of edges, such that edges[e] = (p_1,p_2).
            Note that indexing is still done via p here.
        
        """
        # Parameters 
        # -----------
        simplices = self.simplices

        loops = []
        for simplex in simplices: 
            path = list(simplex)

            # Close the path into a loop by adding the first element at the end
            path.append(path[0])
            loops.append(path)


        edges = []
        for loop in loops:
            # Add the three edges contained in the triangular loop
            # NB there are always three becuase it's a triangle
            edge_1 = [loop[0], loop[1]]
            edge_2 = [loop[1], loop[2]]
            edge_3 = [loop[2], loop[3]]

            edges.append(edge_1)
            edges.append(edge_2)
            edges.append(edge_3)

        return edges


    def get_conductance(self):
        """
        Get the initial conductance tensor.
        For each edge: 
            - Get the points on either end of the edge 
            in terms of the index p. 
            - Convert each p index to a (i,r,s) triple  using key.
            - Check if the edge has an end inside the unit cell. 
            - If it does, then define the edge conductance in terms of the length of the edge.
            - If it doesn't, then do not add the edge to the conductance tensor.
        
        Returns
        -------
        - cond_init_4: numpy.ndarray
            cond_init_4[i,j,r,s] = conductance between node i in unit cell 
            and node j in cell at position (r,s) relative to unit cell.
        """
        # Parameters 
        # ----------
        num_nodes = self.num_nodes
        num_refs  = self.num_refs

        edges     = self.edges
        key       = self.key
        dist_6    = self.dist_6

        cond_init_4 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_refs))

        edge_lengs = []
        edge_conds   = []
        for edge in edges:
            # Get points that edge involves
            p_i = edge[0]
            p_j = edge[1]

            # Get i,r,s triples that edge involves, by using key
            [i_i, r_i, s_i] = key[p_i]
            [i_j, r_j, s_j] = key[p_j]

            ireg_like_reg = False
            if ireg_like_reg == False:
                # Keep edge if involves unit cell
                # Either i or j is in unit cell, such that r==0==s.
                if (r_i == 0 and s_i == 0):
                    #print("i_i={},r_i={},s_i={},i_j={},r_j={},s_j={}".format(i_i,r_i,s_i,i_j,r_j,s_j))
                    # i is in unit cell
                    cond_init_4[i_i,i_j,r_j,s_j]   = self.mean/dist_6[i_i,r_i,s_i,i_j,r_j,s_j] #(1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_i,r_i,s_i,i_j,r_j,s_j])
                    cond_init_4[i_j,i_i,-r_j,-s_j] = self.mean/dist_6[i_i,r_i,s_i,i_j,r_j,s_j] #(1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_i,r_i,s_i,i_j,r_j,s_j]) 
                    #print("d={}".format(dist_6[i_i,r_i,s_i,i_j,r_j,s_j]))
                    edge_lengs.append(dist_6[i_i,r_i,s_i,i_j,r_j,s_j])
                    edge_conds.append(cond_init_4[i_i,i_j,r_j,s_j])
                elif (r_j == 0 and s_j == 0):
                    # j is in unit cell
                    #print("i_i={},r_i={},s_i={},i_j={},r_j={},s_j={}".format(i_i,r_i,s_i,i_j,r_j,s_j))
                    cond_init_4[i_j,i_i,r_i,s_i]   = self.mean/dist_6[i_i,r_i,s_i,i_j,r_j,s_j] #(1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_j,r_j,s_j,i_i,r_i,s_i])
                    cond_init_4[i_i,i_j,-r_i,-s_i] = self.mean/dist_6[i_i,r_i,s_i,i_j,r_j,s_j] #(1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_j,r_j,s_j,i_i,r_i,s_i])
                    #print("d={}".format(dist_6[i_i,r_i,s_i,i_j,r_j,s_j]))
                    edge_lengs.append(dist_6[i_i,r_i,s_i,i_j,r_j,s_j])
                    edge_conds.append(cond_init_4[i_j,i_i,r_i,s_i])
                    #g.append(cond_init_4[i_j,i_i,-r_j,-s_j])

            elif ireg_like_reg == True:
                self.scale_factor = numpy.sqrt(2.0)/numpy.sqrt(numpy.sqrt(3.0))
                if (r_i == 0 and s_i == 0):
                    # i is in unit cell
                    sample = numpy.random.lognormal(mean=self.mu, sigma=self.sigma)
                    cond_init_4[i_i,i_j,r_j,s_j]   = sample/self.scale_factor
                    cond_init_4[i_j,i_i,-r_j,-s_j] = sample/self.scale_factor 
                    edge_conds.append(cond_init_4[i_i,i_j,r_j,s_j])
                elif (r_j == 0 and s_j == 0):
                    # j is in unit cell
                    sample = numpy.random.lognormal(mean=self.mu, sigma=self.sigma)
                    cond_init_4[i_j,i_i,r_i,s_i]   = sample/self.scale_factor
                    cond_init_4[i_i,i_j,-r_i,-s_i] = sample/self.scale_factor
                    edge_conds.append(cond_init_4[i_j,i_i,r_i,s_i])
            else: 
                # neither i or j in unit cell so this edge is not in conductance
                pass
        
        #l = 3*self.l1
        #dd = numpy.sqrt(2*l**2)
        #ll = (1.0/15.0)*(l**3/l**2 + l**3/l**2 + dd*(3.0-1-1) + (5.0/2.0)*(l*numpy.log((l+dd)/l) + l*numpy.log((l+dd)/l)) )
        #print("ll:",ll)
        #print("average_cond:",numpy.mean(numpy.array(g)))
        #print("average_dist:",numpy.mean(numpy.array(d)))
        #print("avdist:",numpy.mean(dist_6[:,:,:,:,:,:]))
        #print("mean/average_dist:",self.mean/numpy.mean(numpy.array(d)))
        self.edge_lengs = edge_lengs
        self.edge_conds = edge_conds

        conns = numpy.zeros(shape=num_nodes) # conns[i] = number of edges from ndoe i in unit cell
        for i in range(num_nodes):
            conns[i] = numpy.count_nonzero(a=cond_init_4[i,:,:,:],axis=None)
        self.conns = conns
        print(conns)
        print(numpy.mean(conns))
        if numpy.mean(conns) != 6.0:
            raise Exception
        return cond_init_4





class Cell_2D_six_reg():
    """
    """ 
    def __init__(self, num_nodes: int,
                       num_refs: int, 
                       num_dims: int, 
                       mu: float, 
                       sigma: float):
        """
        """
        # Parameters
        self.num_nodes = num_nodes
        self.num_refs  = num_refs
        self.num_dims  = num_dims
        self.mu        = mu
        self.sigma     = sigma
        self.scale_factor = numpy.sqrt(2.0)/numpy.sqrt(numpy.sqrt(3.0))

        (self.pts_x_0, self.pts_y_0, self.pts_x_1, self.pts_y_1, self.pts_x_m1, self.pts_y_m1) = self.get_node_coordinates()

        self.pts_4 = self.get_points_tensor()

        self.dist_6 = self.get_distance_between_points()

        (self.simplices, self.key, self.pts_to_tri_2) = self.get_simplices_of_triangulation()

        self.edges = self.get_edges()

        self.cond_init_4 = self.get_conductance()

    def get_node_coordinates(self):
        """
        """
        # Parameters 
        num_nodes = self.num_nodes 
        num_construction_cells = int(num_nodes/2)
        num_rows_or_cols = int(numpy.sqrt(num_construction_cells))

        
        # Get constructing points
        pts_x_constr = numpy.array([0.0,0.5])*self.scale_factor 
        pts_y_constr = numpy.array([0.0,numpy.sqrt(3.0)/2.0])*self.scale_factor 


        # Get unit cell points
        pts_x_0 = []
        for i in range(num_rows_or_cols):
            # Fill the coordinates with the correct number of
            # construction cell points
            pts_x_0.append(pts_x_constr[0]+i) # get x coord of all 0 points to right
            pts_x_0.append(pts_x_constr[1]+i) # get x coord of all 1/2 points to right
        pts_x_0 = numpy.array(pts_x_0)           
        # We now need x points above and y points to the right, which are identical to those already made
        pts_x_0 = numpy.tile(A=pts_x_0, reps=num_rows_or_cols)

        pts_y_0_tile = list(numpy.tile(A=pts_y_constr, reps=num_rows_or_cols))
        #print(pts_y_0_tile)
        
        pts_y_0 = []
        for i in range(num_rows_or_cols):
            for el in pts_y_0_tile:
                pts_y_0.append(el+i*numpy.sqrt(3.0)*self.scale_factor) # get y coord of all 0,1 points above
        
        #print(pts_y_0)

        pts_y_0 = numpy.array(pts_y_0)

        

        # Right and up components
        pts_x_1 = num_rows_or_cols*numpy.ones_like(pts_x_0)*self.scale_factor + pts_x_0 
        pts_y_1 = num_rows_or_cols*numpy.sqrt(3.0)*self.scale_factor*numpy.ones_like(pts_y_0) + pts_y_0

        ## Left and down components
        pts_x_m1 = -num_rows_or_cols*numpy.ones_like(pts_x_0)*self.scale_factor + pts_x_0
        pts_y_m1 = -num_rows_or_cols*numpy.sqrt(3.0)*self.scale_factor*numpy.ones_like(pts_y_0) + pts_y_0

        #print(pts_y_m1)

        return (pts_x_0, 
                pts_y_0,
                pts_x_1,
                pts_y_1,
                pts_x_m1,
                pts_y_m1)


    def get_points_tensor(self):
        """
        Put node coordinates into tensor.

        Returns
        -------
        - pts_4: numpy.ndarray
            pts_4[i,m,r,s] is the x^m (either x or y) component of node i in cell at reference r,s.
        """
        # Parameters 
        num_nodes = self.num_nodes 
        num_refs  = self.num_refs
        num_dims  = self.num_dims

        pts_x_0   = self.pts_x_0
        pts_y_0   = self.pts_y_0
        pts_x_1   = self.pts_x_1
        pts_y_1   = self.pts_y_1
        pts_x_m1   = self.pts_x_m1
        pts_y_m1   = self.pts_y_m1

        # Make empty array
        pts_4 = numpy.zeros(shape=(num_nodes,num_dims,num_refs,num_refs))
        
        for r in range(num_refs):
            for s in range(num_refs):
                for i in range(num_nodes):
                    if r == 0:
                        pts_x = pts_x_0
                    elif r == 1:
                        pts_x = pts_x_1
                    elif r == 2: 
                        pts_x = pts_x_m1

                    if s == 0:
                        pts_y = pts_y_0
                    elif s == 1:
                        pts_y = pts_y_1
                    elif s == 2: 
                        pts_y = pts_y_m1

                    pts_4[i,0,r,s] = pts_x[i]
                    pts_4[i,1,r,s] = pts_y[i]      

        return pts_4

    def get_distance_between_points(self):
        """
        For each pair of points (i,r,s) in the points tensor,
        get their x and y coordinates and calculate the euclidean distance between them.

        Returns 
        --------

        """
        # Parameters
        num_nodes = self.num_nodes
        num_refs  = self.num_refs 

        pts_4     = self.pts_4
        
        dist_6 = numpy.zeros(shape=(num_nodes,num_refs,num_refs,num_nodes,num_refs,num_refs))
        # dist_6[i,r_i,s_i, j,r_j,s_j] = distance between node (i,r_i,s_i) and (j,r_j,s_j)
        
        for r_i in range(num_refs):
            for s_i in range(num_refs):
                for r_j in range(num_refs):
                    for s_j in range(num_refs):
                        for i in range(num_nodes):
                            for j in range(num_nodes):
                                # Get x,y coordinates corresponding to nodes
                                p_i = pts_4[i,:,r_i,s_i]
                                p_j = pts_4[j,:,r_j,s_j]
                                # Get distance between points
                                dist_6[i,r_i,s_i,j,r_j,s_j] = numpy.linalg.norm(p_i-p_j)

        return dist_6


    def get_simplices_of_triangulation(self):
        """
        Get all points in points tensor in correct form to use triangulation 
        method. 
        Then Triangulate all points using Delaunay triangulation.

        Returns 
        -------- 
        - simplices: list of lists.
            simplices[s] = [p_s_1,p_s_2,p_s_3] where p_s_i is the ith point on the s^th simplex.
            I.e. each simplex is a list of three points that make a triangle.
            These are indexed by p, hence we need a key between p and our indexing system (i,r,s).
        - key: list
            key[p] = [i,r,s] triple corresponding to point p. That is, a triple 
            that tells us the index, and r,s cell position of the point p. 
            We use this to map between two indexings, p, and (i,r,s).
        """
        # Parameters 
        num_refs  = self.num_refs
        num_nodes = self.num_nodes

        pts_4     = self.pts_4

        # Make empty lists
        # -----
        pts_to_tri_2 = []
        key = []
        # pts_to_tri_2[p,m] = mth (x or y) component of point p - need in this form for Delaunay algorithm.
        # key[p] = [i,r,s] triple corresponding to point p
        
        # Get all points in correct form
        # -----
        for r in range(num_refs):
            for s in range(num_refs):
                for i in range(num_nodes):
                    i_x = pts_4[i,0,r,s] # x component of point corresponding to node i in cell r,s
                    i_y = pts_4[i,1,r,s] # y component of point corresponding to node i in cell r,s

                    pts_to_tri_2.append([i_x,i_y]) 
                    key.append([i,r,s])

        pts_to_tri_2 = numpy.array(pts_to_tri_2)

        # Triangulate points
        tri = spatial.Delaunay(points=pts_to_tri_2)
        
        # Get simplices
        simplices = tri.simplices
        # simplices[s] = [p_s_1,p_s_2,p_s_3] where p_s_i is the ith point on the s^th simplex.

        return (simplices, key, pts_to_tri_2)


    def get_edges(self):
        """
        Turn each simplex into a loop, then extract the three edges from that loop. 
        
        Returns
        -------
        - edges: list
            Unstructured list of edges, such that edges[e] = (p_1,p_2).
            Note that indexing is still done via p here.
        
        """
        # Parameters 
        # -----------
        simplices = self.simplices

        loops = []
        for simplex in simplices: 
            path = list(simplex)

            # Close the path into a loop by adding the first element at the end
            path.append(path[0])
            loops.append(path)


        edges = []
        for loop in loops:
            # Add the three edges contained in the triangular loop
            # NB there are always three becuase it's a triangle
            edge_1 = [loop[0], loop[1]]
            edge_2 = [loop[1], loop[2]]
            edge_3 = [loop[2], loop[3]]

            edges.append(edge_1)
            edges.append(edge_2)
            edges.append(edge_3)

        return edges


    def get_conductance(self):
        """
        Get the initial conductance tensor.
        For each edge: 
            - Get the points on either end of the edge 
            in terms of the index p. 
            - Convert each p index to a (i,r,s) triple  using key.
            - Check if the edge has an end inside the unit cell. 
            - If it does, then define the edge conductance in terms of the length of the edge.
            - If it doesn't, then do not add the edge to the conductance tensor.
        
        Returns
        -------
        - cond_init_4: numpy.ndarray
            cond_init_4[i,j,r,s] = conductance between node i in unit cell 
            and node j in cell at position (r,s) relative to unit cell.
        """
        # Parameters 
        # ----------
        num_nodes = self.num_nodes
        num_refs  = self.num_refs

        edges     = self.edges
        key       = self.key

        cond_init_4 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_refs))

        edge_conds = []
        edge_lengs = []
        for edge in edges:
            # Get points that edge involves
            p_i = edge[0]
            p_j = edge[1]

            # Get i,r,s triples that edge involves, by using key
            [i_i, r_i, s_i] = key[p_i]
            [i_j, r_j, s_j] = key[p_j]

            # Keep edge if involves unit cell
            # Either i or j is in unit cell, such that r==0==s.
            if (r_i == 0 and s_i == 0):
                # i is in unit cell
                sample = numpy.random.lognormal(mean=self.mu, sigma=self.sigma)
                cond_init_4[i_i,i_j,r_j,s_j]   = sample/self.scale_factor#numpy.sqrt(numpy.sqrt(3.0))*sample/numpy.sqrt(2.0)#numpy.sqrt(numpy.sqrt(3.0))*1.72461/numpy.sqrt(2.0)#1.72461/1.07456993182#sample#(1.72461)*1.0/dist_6[i_i,r_i,s_i,i_j,r_j,s_j] #(1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_i,r_i,s_i,i_j,r_j,s_j])
                cond_init_4[i_j,i_i,-r_j,-s_j] = sample/self.scale_factor#numpy.sqrt(numpy.sqrt(3.0))*sample/numpy.sqrt(2.0)#numpy.sqrt(numpy.sqrt(3.0))*1.72461/numpy.sqrt(2.0)#1.72461/1.07456993182#sample#(1.72461)*1.0/dist_6[i_i,r_i,s_i,i_j,r_j,s_j] #(1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_i,r_i,s_i,i_j,r_j,s_j]) 
                edge_conds.append(cond_init_4[i_i,i_j,r_j,s_j])
            elif (r_j == 0 and s_j == 0):
                # j is in unit cell
                sample = numpy.random.lognormal(mean=self.mu, sigma=self.sigma)
                cond_init_4[i_j,i_i,r_i,s_i]   = sample/self.scale_factor#numpy.sqrt(numpy.sqrt(3.0))*sample/numpy.sqrt(2.0)#numpy.sqrt(numpy.sqrt(3.0))*1.72461/numpy.sqrt(2.0)#1.72461/1.07456993182#sample#(1.72461)*1.0/dist_6[i_i,r_i,s_i,i_j,r_j,s_j] #(1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_j,r_j,s_j,i_i,r_i,s_i])
                cond_init_4[i_i,i_j,-r_i,-s_i] = sample/self.scale_factor#numpy.sqrt(numpy.sqrt(3.0))*sample/numpy.sqrt(2.0)#numpy.sqrt(numpy.sqrt(3.0))*1.72461/numpy.sqrt(2.0)#1.72461/1.07456993182#sample#(1.72461)*1.0/dist_6[i_i,r_i,s_i,i_j,r_j,s_j] #(1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_j,r_j,s_j,i_i,r_i,s_i])
                edge_conds.append(cond_init_4[i_j,i_i,r_i,s_i])
            else: 
                # neither i or j in unit cell so this edge is not in conductance
                pass
        self.edge_conds = edge_conds
        self.edge_lengs = edge_lengs

        conns = numpy.zeros(shape=num_nodes) # conns[i] = number of edges from ndoe i in unit cell
        conns_intra = numpy.zeros(shape=num_nodes)
        conns_inter = numpy.zeros(shape=num_nodes)
        for i in range(num_nodes):
            conns[i] = numpy.count_nonzero(a=cond_init_4[i,:,:,:],axis=None)
            conns_intra[i] = numpy.count_nonzero(a=cond_init_4[i,:,0,0],axis=None)
            conns_inter[i] = conns[i]-conns_intra[i]

        mean_conns = numpy.mean(conns)
        mean_conns_intra = numpy.mean(conns_intra)
        mean_conns_inter = numpy.mean(conns_inter)
        #print("conns:{}, mean_conns:{}".format(conns,numpy.mean(conns)))
        #print("conns_intra:{}, mean_conns_intra:{}".format(conns_intra,numpy.mean(conns_intra)))
        #print("conns_inter:{}, mean_conns_inter:{}".format(conns_inter,numpy.mean(conns_inter)))
        #print(numpy.mean(conns))

        self.mean_conns = mean_conns
        self.mean_conns_intra = mean_conns_intra
        self.mean_conns_inter = mean_conns_inter
        return cond_init_4






class Cell_2D_six_ireglikereg():
    """
    """ 
    def __init__(self, num_nodes: int,
                       num_refs: int, 
                       num_dims: int,
                       leng_1: numpy.ndarray,
                       mu: float, 
                       sigma: float):
        """
        Parameters 
        # -------
        - mean: float 
            The mean of the lognormal distribution from which the conductance is drawn. 
            This is the conductance per unit length of the edges in the resulting cell. 

        """
        # Parameters
        self.num_nodes = num_nodes
        self.num_refs  = num_refs
        self.num_dims  = num_dims
        self.leng_1    = leng_1
        self.mu        = mu
        self.sigma     = sigma

        self.scale_factor = numpy.sqrt(2.0)/numpy.sqrt(numpy.sqrt(3.0))
        
        self.l1 = leng_1[0]
        self.l2 = leng_1[1]

        (self.pts_x_0, self.pts_y_0, self.pts_x_1, self.pts_y_1, self.pts_x_m1, self.pts_y_m1) = self.get_node_coordinates()

        self.pts_4 = self.get_points_tensor()

        (self.simplices, self.key) = self.get_simplices_of_triangulation()

        self.edges = self.get_edges()

        self.cond_init_4 = self.get_conductance()


    def get_node_coordinates(self):
        """
        Get x and y coordinates of each point.
        
        Returns
        -------
        - pts_x_0: numpy.ndarray
            pts_x_0[i] is x coordinate of node i in cell with r = 0.
        - pts_y_0: numpy.ndarray
            pts_y_0[i] is y coordinate of node i in cell with s = 0.
        - pts_x_1: numpy.ndarray
            pts_x                                                                                                                                                       _1[i] is x coordinate of node i in cell with r = 1.
        - pts_y_1: numpy.ndarray
            pts_y_1[i] is y coordinate of node i in cell with s = 1.
        - pts_x_m1: numpy.ndarray
            pts_x_m1[i] is x coordinate of node i in cell with r = -1.
        - pts_y_m1: numpy.ndarray
            pts_y_m1[i] is y coordinate of node i in cell with s = -1.
        """
        # Parameters 
        num_nodes = self.num_nodes
        l1        = self.l1
        l2        = self.l2


        # Get unit cell points
        pts_x_0 = numpy.random.uniform(low=0.0, high=l1, size=num_nodes) #*l1 
        pts_y_0 = numpy.random.uniform(low=0.0, high=l2, size=num_nodes) #*l2 

        # Right and up components
        pts_x_1 = l1*numpy.ones_like(pts_x_0) + pts_x_0 
        pts_y_1 = l2*numpy.ones_like(pts_y_0) + pts_y_0

        ## Left and down components
        pts_x_m1 = -l1*numpy.ones_like(pts_x_0) + pts_x_0
        pts_y_m1 = -l2*numpy.ones_like(pts_y_0) + pts_y_0

        return (pts_x_0, 
                pts_y_0,
                pts_x_1,
                pts_y_1,
                pts_x_m1,
                pts_y_m1)


    def get_points_tensor(self):
        """
        Put node coordinates into tensor.

        Returns
        -------
        - pts_4: numpy.ndarray
            pts_4[i,m,r,s] is the x^m (either x or y) component of node i in cell at reference r,s.
        """
        # Parameters 
        num_nodes = self.num_nodes 
        num_refs  = self.num_refs
        num_dims  = self.num_dims

        pts_x_0   = self.pts_x_0
        pts_y_0   = self.pts_y_0
        pts_x_1   = self.pts_x_1
        pts_y_1   = self.pts_y_1
        pts_x_m1   = self.pts_x_m1
        pts_y_m1   = self.pts_y_m1

        # Make empty array
        pts_4 = numpy.zeros(shape=(num_nodes,num_dims,num_refs,num_refs))
        
        for r in range(num_refs):
            for s in range(num_refs):
                for i in range(num_nodes):

                    if r == 0:
                        pts_x = pts_x_0
                    elif r == 1:
                        pts_x = pts_x_1
                    elif r == 2: 
                        pts_x = pts_x_m1

                    if s == 0:
                        pts_y = pts_y_0
                    elif s == 1:
                        pts_y = pts_y_1
                    elif s == 2: 
                        pts_y = pts_y_m1

                    pts_4[i,0,r,s] = pts_x[i]
                    pts_4[i,1,r,s] = pts_y[i]      

        return pts_4


    def get_simplices_of_triangulation(self):
        """
        Get all points in points tensor in correct form to use triangulation 
        method. 
        Then Triangulate all points using Delaunay triangulation.

        Returns 
        -------- 
        - simplices: list of lists.
            simplices[s] = [p_s_1,p_s_2,p_s_3] where p_s_i is the ith point on the s^th simplex.
            I.e. each simplex is a list of three points that make a triangle.
            These are indexed by p, hence we need a key between p and our indexing system (i,r,s).
        - key: list
            key[p] = [i,r,s] triple corresponding to point p. That is, a triple 
            that tells us the index, and r,s cell position of the point p. 
            We use this to map between two indexings, p, and (i,r,s).
        """
        # Parameters 
        num_refs  = self.num_refs
        num_nodes = self.num_nodes

        pts_4     = self.pts_4

        # Make empty lists
        # -----
        pts_to_tri_2 = []
        key = []
        # pts_to_tri_2[p,m] = mth (x or y) component of point p - need in this form for Delaunay algorithm.
        # key[p] = [i,r,s] triple corresponding to point p
        
        # Get all points in correct form
        # -----
        for r in range(num_refs):
            for s in range(num_refs):
                for i in range(num_nodes):
                    i_x = pts_4[i,0,r,s] # x component of point corresponding to node i in cell r,s
                    i_y = pts_4[i,1,r,s] # y component of point corresponding to node i in cell r,s

                    pts_to_tri_2.append([i_x,i_y]) 
                    key.append([i,r,s])

        pts_to_tri_2 = numpy.array(pts_to_tri_2)

        # Triangulate points
        tri = spatial.Delaunay(points=pts_to_tri_2)
        
        # Get simplices
        simplices = tri.simplices
        # simplices[s] = [p_s_1,p_s_2,p_s_3] where p_s_i is the ith point on the s^th simplex.

        self.key = key
        self.simplices = simplices
        self.pts_to_tri_2 = pts_to_tri_2
        return (simplices, key)


    def get_edges(self):
        """
        Turn each simplex into a loop, then extract the three edges from that loop. 
        
        Returns
        -------
        - edges: list
            Unstructured list of edges, such that edges[e] = (p_1,p_2).
            Note that indexing is still done via p here.
        
        """
        # Parameters 
        # -----------
        simplices = self.simplices

        loops = []
        for simplex in simplices: 
            path = list(simplex)

            # Close the path into a loop by adding the first element at the end
            path.append(path[0])
            loops.append(path)


        edges = []
        for loop in loops:
            # Add the three edges contained in the triangular loop
            # NB there are always three becuase it's a triangle
            edge_1 = [loop[0], loop[1]]
            edge_2 = [loop[1], loop[2]]
            edge_3 = [loop[2], loop[3]]

            edges.append(edge_1)
            edges.append(edge_2)
            edges.append(edge_3)

        return edges


    def get_conductance(self):
        """
        Get the initial conductance tensor.
        For each edge: 
            - Get the points on either end of the edge 
            in terms of the index p. 
            - Convert each p index to a (i,r,s) triple  using key.
            - Check if the edge has an end inside the unit cell. 
            - If it does, then define the edge conductance in terms of the length of the edge.
            - If it doesn't, then do not add the edge to the conductance tensor.
        
        Returns
        -------
        - cond_init_4: numpy.ndarray
            cond_init_4[i,j,r,s] = conductance between node i in unit cell 
            and node j in cell at position (r,s) relative to unit cell.
        """
        # Parameters 
        # ----------
        num_nodes = self.num_nodes
        num_refs  = self.num_refs

        edges     = self.edges
        key       = self.key

        cond_init_4 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_refs))

        edge_lengs = []
        edge_conds   = []
        for edge in edges:
            # Get points that edge involves
            p_i = edge[0]
            p_j = edge[1]

            # Get i,r,s triples that edge involves, by using key
            [i_i, r_i, s_i] = key[p_i]
            [i_j, r_j, s_j] = key[p_j]
            
            if (r_i == 0 and s_i == 0):
                # i is in unit cell
                sample = numpy.random.lognormal(mean=self.mu, sigma=self.sigma)
                cond_init_4[i_i,i_j,r_j,s_j]   = sample/self.scale_factor
                cond_init_4[i_j,i_i,-r_j,-s_j] = sample/self.scale_factor 
                edge_conds.append(cond_init_4[i_i,i_j,r_j,s_j])
            elif (r_j == 0 and s_j == 0):
                # j is in unit cell
                sample = numpy.random.lognormal(mean=self.mu, sigma=self.sigma)
                cond_init_4[i_j,i_i,r_i,s_i]   = sample/self.scale_factor
                cond_init_4[i_i,i_j,-r_i,-s_i] = sample/self.scale_factor
                edge_conds.append(cond_init_4[i_j,i_i,r_i,s_i])
            else: 
                # neither i or j in unit cell so this edge is not in conductance
                pass

        self.edge_lengs = edge_lengs
        self.edge_conds = edge_conds

        conns = numpy.zeros(shape=num_nodes) # conns[i] = number of edges from ndoe i in unit cell
        conns_intra = numpy.zeros(shape=num_nodes)
        conns_inter = numpy.zeros(shape=num_nodes)
        for i in range(num_nodes):
            conns[i] = numpy.count_nonzero(a=cond_init_4[i,:,:,:],axis=None)
            conns_intra[i] = numpy.count_nonzero(a=cond_init_4[i,:,0,0],axis=None)
            conns_inter[i] = conns[i]-conns_intra[i]

        mean_conns = numpy.mean(conns)
        mean_conns_intra = numpy.mean(conns_intra)
        mean_conns_inter = numpy.mean(conns_inter)
        print("conns:{}, mean_conns:{}".format(conns,numpy.mean(conns)))
        print("conns_intra:{}, mean_conns_intra:{}".format(conns_intra,numpy.mean(conns_intra)))
        print("conns_inter:{}, mean_conns_inter:{}".format(conns_inter,numpy.mean(conns_inter)))
        print(numpy.mean(conns))

        self.mean_conns = mean_conns
        self.mean_conns_intra = mean_conns_intra
        self.mean_conns_inter = mean_conns_inter
        
        return cond_init_4











class Cell_2D_six_reglikeireg():
    """
    """ 
    def __init__(self, num_nodes: int,
                       num_refs: int, 
                       num_dims: int,
                       mean: float,
                       leng_1: numpy.ndarray,
                       mu: float, 
                       sigma: float):

                       
        """
        """
        # Parameters
        self.num_nodes = num_nodes
        self.num_refs  = num_refs
        self.num_dims  = num_dims
        self.mean      = mean
        self.leng_1    = leng_1
        self.mu        = mu
        self.sigma     = sigma
        self.scale_factor = numpy.sqrt(2.0)/numpy.sqrt(numpy.sqrt(3.0))

        (self.pts_x_0, self.pts_y_0, self.pts_x_1, self.pts_y_1, self.pts_x_m1, self.pts_y_m1) = self.get_node_coordinates()
        (self.ireg_pts_x_0, self.ireg_pts_y_0, self.ireg_pts_x_1, self.ireg_pts_y_1, self.ireg_pts_x_m1, self.ireg_pts_y_m1) = self.get_ireg_node_coordinates()

        self.pts_4      = self.get_points_tensor(self.pts_x_0, self.pts_y_0, self.pts_x_1, self.pts_y_1, self.pts_x_m1, self.pts_y_m1)
        self.ireg_pts_4 = self.get_points_tensor(self.ireg_pts_x_0, self.ireg_pts_y_0, self.ireg_pts_x_1, self.ireg_pts_y_1, self.ireg_pts_x_m1, self.ireg_pts_y_m1)

        #self.dist_6 = self.get_distance_between_points(pts_4=self.pts_4)
        self.ireg_dist_6 = self.get_distance_between_points(pts_4=self.ireg_pts_4)

        (self.simplices, self.key, self.pts_to_tri_2) = self.get_simplices_of_triangulation()

        self.edges = self.get_edges()

        self.cond_init_4 = self.get_conductance()

    def get_node_coordinates(self):
        """
        """
        # Parameters 
        num_nodes = self.num_nodes 
        num_construction_cells = int(num_nodes/2)
        num_rows_or_cols = int(numpy.sqrt(num_construction_cells))

        
        # Get constructing points
        pts_x_constr = numpy.array([0.0,0.5])*self.scale_factor 
        pts_y_constr = numpy.array([0.0,numpy.sqrt(3.0)/2.0])*self.scale_factor 


        # Get unit cell points
        pts_x_0 = []
        for i in range(num_rows_or_cols):
            # Fill the coordinates with the correct number of
            # construction cell points
            pts_x_0.append(pts_x_constr[0]+i) # get x coord of all 0 points to right
            pts_x_0.append(pts_x_constr[1]+i) # get x coord of all 1/2 points to right
        pts_x_0 = numpy.array(pts_x_0)           
        # We now need x points above and y points to the right, which are identical to those already made
        pts_x_0 = numpy.tile(A=pts_x_0, reps=num_rows_or_cols)

        pts_y_0_tile = list(numpy.tile(A=pts_y_constr, reps=num_rows_or_cols))
        #print(pts_y_0_tile)
        
        pts_y_0 = []
        for i in range(num_rows_or_cols):
            for el in pts_y_0_tile:
                pts_y_0.append(el+i*numpy.sqrt(3.0)*self.scale_factor) # get y coord of all 0,1 points above
        
        #print(pts_y_0)

        pts_y_0 = numpy.array(pts_y_0)

        

        # Right and up components
        pts_x_1 = num_rows_or_cols*numpy.ones_like(pts_x_0)*self.scale_factor + pts_x_0 
        pts_y_1 = num_rows_or_cols*numpy.sqrt(3.0)*self.scale_factor*numpy.ones_like(pts_y_0) + pts_y_0

        ## Left and down components
        pts_x_m1 = -num_rows_or_cols*numpy.ones_like(pts_x_0)*self.scale_factor + pts_x_0
        pts_y_m1 = -num_rows_or_cols*numpy.sqrt(3.0)*self.scale_factor*numpy.ones_like(pts_y_0) + pts_y_0

        #print(pts_y_m1)

        return (pts_x_0, 
                pts_y_0,
                pts_x_1,
                pts_y_1,
                pts_x_m1,
                pts_y_m1)

    def get_ireg_node_coordinates(self):
        """
        Get x and y coordinates of each point.
        
        Returns
        -------
        - pts_x_0: numpy.ndarray
            pts_x_0[i] is x coordinate of node i in cell with r = 0.
        - pts_y_0: numpy.ndarray
            pts_y_0[i] is y coordinate of node i in cell with s = 0.
        - pts_x_1: numpy.ndarray
            pts_x                                                                                                                                                       _1[i] is x coordinate of node i in cell with r = 1.
        - pts_y_1: numpy.ndarray
            pts_y_1[i] is y coordinate of node i in cell with s = 1.
        - pts_x_m1: numpy.ndarray
            pts_x_m1[i] is x coordinate of node i in cell with r = -1.
        - pts_y_m1: numpy.ndarray
            pts_y_m1[i] is y coordinate of node i in cell with s = -1.
        """
        # Parameters 
        num_nodes = self.num_nodes
        n = numpy.sqrt(num_nodes)
        l1 = n*1.0
        l2 = n*1.0
        print(l1)
        print(l2)


        # Get unit cell points
        pts_x_0 = numpy.random.uniform(low=0.0, high=l1, size=num_nodes) #*l1 
        pts_y_0 = numpy.random.uniform(low=0.0, high=l2, size=num_nodes) #*l2 

        # Right and up components
        pts_x_1 = l1*numpy.ones_like(pts_x_0) + pts_x_0 
        pts_y_1 = l2*numpy.ones_like(pts_y_0) + pts_y_0

        ## Left and down components
        pts_x_m1 = -l1*numpy.ones_like(pts_x_0) + pts_x_0
        pts_y_m1 = -l2*numpy.ones_like(pts_y_0) + pts_y_0

        return (pts_x_0, 
                pts_y_0,
                pts_x_1,
                pts_y_1,
                pts_x_m1,
                pts_y_m1)

    #def get_ireg_node_coordinates(self):
    #    """
    #    Get x and y coordinates of each point.
    #    
    #    Returns
    #    -------
    #    - pts_x_0: numpy.ndarray
    #        pts_x_0[i] is x coordinate of node i in cell with r = 0.
    #    - pts_y_0: numpy.ndarray
    #        pts_y_0[i] is y coordinate of node i in cell with s = 0.
    #    - pts_x_1: numpy.ndarray
    #        pts_x                                                                                                                                                       _1[i] is x coordinate of node i in cell with r = 1.
    #    - pts_y_1: numpy.ndarray
    #        pts_y_1[i] is y coordinate of node i in cell with s = 1.
    #    - pts_x_m1: numpy.ndarray
    #        pts_x_m1[i] is x coordinate of node i in cell with r = -1.
    #    - pts_y_m1: numpy.ndarray
    #        pts_y_m1[i] is y coordinate of node i in cell with s = -1.
    #    """
    #    # Parameters 
    #    num_nodes = self.num_nodes
    #    num_construction_cells = int(num_nodes/2)
    #    num_rows_or_cols = int(numpy.sqrt(num_construction_cells))
    #    nr = num_rows_or_cols
    #    sf = self.scale_factor
    #    srt = numpy.sqrt(3.0)
#
    #    l1        = nr*srt*sf
    #    l2        = sf
#
#
    #    # Get unit cell points
    #    pts_x_0 = numpy.random.uniform(low=0.0, high=l1, size=num_nodes) 
    #    pts_y_0 = numpy.random.uniform(low=0.0, high=l2, size=num_nodes) 
#
    #    # Right and up components
    #    pts_x_1 = l1*numpy.ones_like(pts_x_0) + pts_x_0 
    #    pts_y_1 = l2*numpy.ones_like(pts_y_0) + pts_y_0
#
    #    ## Left and down components
    #    pts_x_m1 = -l1*numpy.ones_like(pts_x_0) + pts_x_0
    #    pts_y_m1 = -l2*numpy.ones_like(pts_y_0) + pts_y_0
#
    #    return (pts_x_0, 
    #            pts_y_0,
    #            pts_x_1,
    #            pts_y_1,
    #            pts_x_m1,
    #            pts_y_m1)

    def get_points_tensor(self,pts_x_0,pts_y_0,pts_x_1,pts_y_1,pts_x_m1,pts_y_m1):
        """
        Put node coordinates into tensor.

        Returns
        -------
        - pts_4: numpy.ndarray
            pts_4[i,m,r,s] is the x^m (either x or y) component of node i in cell at reference r,s.
        """
        # Parameters 
        num_nodes = self.num_nodes 
        num_refs  = self.num_refs
        num_dims  = self.num_dims

        # Make empty array
        pts_4 = numpy.zeros(shape=(num_nodes,num_dims,num_refs,num_refs))
        
        for r in range(num_refs):
            for s in range(num_refs):
                for i in range(num_nodes):
                    if r == 0:
                        pts_x = pts_x_0
                    elif r == 1:
                        pts_x = pts_x_1
                    elif r == 2: 
                        pts_x = pts_x_m1

                    if s == 0:
                        pts_y = pts_y_0
                    elif s == 1:
                        pts_y = pts_y_1
                    elif s == 2: 
                        pts_y = pts_y_m1

                    pts_4[i,0,r,s] = pts_x[i]
                    pts_4[i,1,r,s] = pts_y[i]      

        return pts_4

    def get_distance_between_points(self, pts_4):
        """
        For each pair of points (i,r,s) in the points tensor,
        get their x and y coordinates and calculate the euclidean distance between them.

        Returns 
        --------

        """
        # Parameters
        num_nodes = self.num_nodes
        num_refs  = self.num_refs 
       
        dist_6 = numpy.zeros(shape=(num_nodes,num_refs,num_refs,num_nodes,num_refs,num_refs))
        # dist_6[i,r_i,s_i, j,r_j,s_j] = distance between node (i,r_i,s_i) and (j,r_j,s_j)
        for r_i in range(num_refs):
            for s_i in range(num_refs):
                for r_j in range(num_refs):
                    for s_j in range(num_refs):
                        for i in range(num_nodes):
                            for j in range(num_nodes):
                                # Get x,y coordinates corresponding to nodes
                                p_i = pts_4[i,:,r_i,s_i]
                                p_j = pts_4[j,:,r_j,s_j]
                                # Get distance between points
                                dist_6[i,r_i,s_i,j,r_j,s_j] = numpy.linalg.norm(p_i-p_j)
        return dist_6

    
    def get_simplices_of_triangulation(self):
        """
        Get all points in points tensor in correct form to use triangulation 
        method. 
        Then Triangulate all points using Delaunay triangulation.

        Returns 
        -------- 
        - simplices: list of lists.
            simplices[s] = [p_s_1,p_s_2,p_s_3] where p_s_i is the ith point on the s^th simplex.
            I.e. each simplex is a list of three points that make a triangle.
            These are indexed by p, hence we need a key between p and our indexing system (i,r,s).
        - key: list
            key[p] = [i,r,s] triple corresponding to point p. That is, a triple 
            that tells us the index, and r,s cell position of the point p. 
            We use this to map between two indexings, p, and (i,r,s).
        """
        # Parameters 
        num_refs  = self.num_refs
        num_nodes = self.num_nodes

        pts_4     = self.pts_4

        # Make empty lists
        # -----
        pts_to_tri_2 = []
        key = []
        # pts_to_tri_2[p,m] = mth (x or y) component of point p - need in this form for Delaunay algorithm.
        # key[p] = [i,r,s] triple corresponding to point p
        
        # Get all points in correct form
        # -----
        for r in range(num_refs):
            for s in range(num_refs):
                for i in range(num_nodes):
                    i_x = pts_4[i,0,r,s] # x component of point corresponding to node i in cell r,s
                    i_y = pts_4[i,1,r,s] # y component of point corresponding to node i in cell r,s

                    pts_to_tri_2.append([i_x,i_y]) 
                    key.append([i,r,s])

        pts_to_tri_2 = numpy.array(pts_to_tri_2)

        # Triangulate points
        tri = spatial.Delaunay(points=pts_to_tri_2)
        
        # Get simplices
        simplices = tri.simplices
        # simplices[s] = [p_s_1,p_s_2,p_s_3] where p_s_i is the ith point on the s^th simplex.

        return (simplices, key, pts_to_tri_2)


    def get_edges(self):
        """
        Turn each simplex into a loop, then extract the three edges from that loop. 
        
        Returns
        -------
        - edges: list
            Unstructured list of edges, such that edges[e] = (p_1,p_2).
            Note that indexing is still done via p here.
        
        """
        # Parameters 
        # -----------
        simplices = self.simplices

        loops = []
        for simplex in simplices: 
            path = list(simplex)

            # Close the path into a loop by adding the first element at the end
            path.append(path[0])
            loops.append(path)


        edges = []
        for loop in loops:
            # Add the three edges contained in the triangular loop
            # NB there are always three becuase it's a triangle
            edge_1 = [loop[0], loop[1]]
            edge_2 = [loop[1], loop[2]]
            edge_3 = [loop[2], loop[3]]

            edges.append(edge_1)
            edges.append(edge_2)
            edges.append(edge_3)

        return edges


    def get_conductance(self):
        """
        Get the initial conductance tensor.
        For each edge: 
            - Get the points on either end of the edge 
            in terms of the index p. 
            - Convert each p index to a (i,r,s) triple  using key.
            - Check if the edge has an end inside the unit cell. 
            - If it does, then define the edge conductance in terms of the length of the edge.
            - If it doesn't, then do not add the edge to the conductance tensor.
        
        Returns
        -------
        - cond_init_4: numpy.ndarray
            cond_init_4[i,j,r,s] = conductance between node i in unit cell 
            and node j in cell at position (r,s) relative to unit cell.
        """
        # Parameters 
        # ----------
        num_nodes = self.num_nodes
        num_refs  = self.num_refs

        edges       = self.edges
        key         = self.key
        ireg_dist_6 = self.ireg_dist_6

        cond_init_4 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_refs))

        edge_lengs = []
        edge_conds   = []
        for edge in edges:
            # Get points that edge involves
            p_i = edge[0]
            p_j = edge[1]

            # Get i,r,s triples that edge involves, by using key
            [i_i, r_i, s_i] = key[p_i]
            [i_j, r_j, s_j] = key[p_j]
            
            # Keep edge if involves unit cell
            # Either i or j is in unit cell, such that r==0==s.
            if (r_i == 0 and s_i == 0):
                #print("i_i={},r_i={},s_i={},i_j={},r_j={},s_j={}".format(i_i,r_i,s_i,i_j,r_j,s_j))
                # i is in unit cell
                cond_init_4[i_i,i_j,r_j,s_j]   = self.mean/ireg_dist_6[i_i,r_i,s_i,i_j,r_j,s_j] #(1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_i,r_i,s_i,i_j,r_j,s_j])
                cond_init_4[i_j,i_i,-r_j,-s_j] = self.mean/ireg_dist_6[i_i,r_i,s_i,i_j,r_j,s_j] #(1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_i,r_i,s_i,i_j,r_j,s_j]) 
                #print("d={}".format(dist_6[i_i,r_i,s_i,i_j,r_j,s_j]))
                edge_lengs.append(ireg_dist_6[i_i,r_i,s_i,i_j,r_j,s_j])
                edge_conds.append(cond_init_4[i_i,i_j,r_j,s_j])
                #g.append(cond_init_4[i_j,i_i,-r_j,-s_j])
            elif (r_j == 0 and s_j == 0):
                # j is in unit cell
                #print("i_i={},r_i={},s_i={},i_j={},r_j={},s_j={}".format(i_i,r_i,s_i,i_j,r_j,s_j))
                cond_init_4[i_j,i_i,r_i,s_i]   = self.mean/ireg_dist_6[i_i,r_i,s_i,i_j,r_j,s_j] #(1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_j,r_j,s_j,i_i,r_i,s_i])
                cond_init_4[i_i,i_j,-r_i,-s_i] = self.mean/ireg_dist_6[i_i,r_i,s_i,i_j,r_j,s_j] #(1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_j,r_j,s_j,i_i,r_i,s_i])
                #print("d={}".format(dist_6[i_i,r_i,s_i,i_j,r_j,s_j]))
                edge_lengs.append(ireg_dist_6[i_i,r_i,s_i,i_j,r_j,s_j])
                edge_conds.append(cond_init_4[i_j,i_i,r_i,s_i])
                #g.append(cond_init_4[i_j,i_i,-r_j,-s_j])

            else: 
                # neither i or j in unit cell so this edge is not in conductance
                pass

        self.edge_lengs = edge_lengs
        self.edge_conds = edge_conds
        return cond_init_4





class Cell_2D_six_rand():
    """
    """ 
    def __init__(self, num_nodes: int,
                       num_refs: int, 
                       num_dims: int,
                       mean: float,
                       leng_1: numpy.ndarray,
                       mu: float, 
                       sigma: float):
        """
        Parameters 
        # -------
        - mean: float 
            The mean of the lognormal distribution from which the conductance is drawn. 
            This is the conductance per unit length of the edges in the resulting cell. 

        """
        # Parameters
        self.num_nodes = num_nodes
        self.num_refs  = num_refs
        self.num_dims  = num_dims
        self.mean      = mean
        self.leng_1    = leng_1
        self.mu        = mu
        self.sigma     = sigma
        
        self.l1 = leng_1[0]
        self.l2 = leng_1[1]

        (self.pts_x_0, self.pts_y_0, self.pts_x_1, self.pts_y_1, self.pts_x_m1, self.pts_y_m1) = self.get_node_coordinates()

        self.pts_4 = self.get_points_tensor()

        self.dist_6 = self.get_distance_between_points()

        self.edges = self.get_edges()

        self.cond_init_4 = self.get_conductance()


    def get_node_coordinates(self):
        """
        Get x and y coordinates of each point.
        
        Returns
        -------
        - pts_x_0: numpy.ndarray
            pts_x_0[i] is x coordinate of node i in cell with r = 0.
        - pts_y_0: numpy.ndarray
            pts_y_0[i] is y coordinate of node i in cell with s = 0.
        - pts_x_1: numpy.ndarray
            pts_x                                                                                                                                                       _1[i] is x coordinate of node i in cell with r = 1.
        - pts_y_1: numpy.ndarray
            pts_y_1[i] is y coordinate of node i in cell with s = 1.
        - pts_x_m1: numpy.ndarray
            pts_x_m1[i] is x coordinate of node i in cell with r = -1.
        - pts_y_m1: numpy.ndarray
            pts_y_m1[i] is y coordinate of node i in cell with s = -1.
        """
        # Parameters 
        num_nodes = self.num_nodes
        l1        = self.l1
        l2        = self.l2


        # Get unit cell points
        pts_x_0 = numpy.random.uniform(low=0.0, high=l1, size=num_nodes) #*l1 
        pts_y_0 = numpy.random.uniform(low=0.0, high=l2, size=num_nodes) #*l2 

        # Right and up components
        pts_x_1 = l1*numpy.ones_like(pts_x_0) + pts_x_0 
        pts_y_1 = l2*numpy.ones_like(pts_y_0) + pts_y_0

        ## Left and down components
        pts_x_m1 = -l1*numpy.ones_like(pts_x_0) + pts_x_0
        pts_y_m1 = -l2*numpy.ones_like(pts_y_0) + pts_y_0

        return (pts_x_0, 
                pts_y_0,
                pts_x_1,
                pts_y_1,
                pts_x_m1,
                pts_y_m1)


    def get_points_tensor(self):
        """
        Put node coordinates into tensor.

        Returns
        -------
        - pts_4: numpy.ndarray
            pts_4[i,m,r,s] is the x^m (either x or y) component of node i in cell at reference r,s.
        """
        # Parameters 
        num_nodes = self.num_nodes 
        num_refs  = self.num_refs
        num_dims  = self.num_dims

        pts_x_0   = self.pts_x_0
        pts_y_0   = self.pts_y_0
        pts_x_1   = self.pts_x_1
        pts_y_1   = self.pts_y_1
        pts_x_m1   = self.pts_x_m1
        pts_y_m1   = self.pts_y_m1

        # Make empty array
        pts_4 = numpy.zeros(shape=(num_nodes,num_dims,num_refs,num_refs))
        
        for r in range(num_refs):
            for s in range(num_refs):
                for i in range(num_nodes):

                    if r == 0:
                        pts_x = pts_x_0
                    elif r == 1:
                        pts_x = pts_x_1
                    elif r == 2: 
                        pts_x = pts_x_m1

                    if s == 0:
                        pts_y = pts_y_0
                    elif s == 1:
                        pts_y = pts_y_1
                    elif s == 2: 
                        pts_y = pts_y_m1

                    pts_4[i,0,r,s] = pts_x[i]
                    pts_4[i,1,r,s] = pts_y[i]      

        return pts_4


    def get_distance_between_points(self):
        """
        For each pair of points (i,r,s) in the points tensor,
        get their x and y coordinates and calculate the euclidean distance between them.

        Returns 
        --------

        """
        # Parameters
        num_nodes = self.num_nodes
        num_refs  = self.num_refs 

        pts_4     = self.pts_4
        
        dist_6 = numpy.zeros(shape=(num_nodes,num_refs,num_refs,num_nodes,num_refs,num_refs))
        # dist_6[i,r_i,s_i, j,r_j,s_j] = distance between node (i,r_i,s_i) and (j,r_j,s_j)
        
        for r_i in range(num_refs):
            for s_i in range(num_refs):
                for r_j in range(num_refs):
                    for s_j in range(num_refs):
                        for i in range(num_nodes):
                            for j in range(num_nodes):
                                # Get x,y coordinates corresponding to nodes
                                p_i = pts_4[i,:,r_i,s_i]
                                p_j = pts_4[j,:,r_j,s_j]
                                # Get distance between points
                                dist_6[i,r_i,s_i,j,r_j,s_j] = numpy.linalg.norm(p_i-p_j)

        return dist_6


    def get_edges(self):
        """
        Get edges. Note that an edge here is NOT the same form 
        as the edges in the other cell classes above.
        We return a list of edges = 
        [[[node_i,r_i,s_i],[node_j,r_j,s_j]],..], 
        where each [[node_i,r_i,s_i],[node_j,r_j,s_j]]
        is the edge from node_i 
        in cell r_i,s_i to node_j in cell r_j,s_j.
        Note that edges have r_i,s_i=0,0 or r_j,s_j=0,0, 
        but this is fine, because we only ever need edges 
        that have at least one node inside the unit cell.
        """
        # Parameters 
        num_nodes = self.num_nodes
        connectivity = numpy.random.binomial(12, 0.5)#6
        print(connectivity)

        edges = []
        e = list(connectivity*numpy.ones(num_nodes,dtype=int))
        for i in range(num_nodes):
            while e[i] > 0:
                if e[i]==1.0 and (e.count(0)==num_nodes-1):
                    # if there are no nodes left to fill and we have one left on the end...
                    # then break and accept that connectivity is slightly below.
                    print(e)
                    break
                else: 
                    j = random.randint(0, num_nodes-1)
                    r = random.randint(-1, +1)
                    s = random.randint(-1, +1)
                    edge = [[i,0,0],[j,r,s]]
                    # if edge already exists then guess again, if not then we've found an edge
                    if (edge not in edges) and (edge[0]!=edge[1]) and ((e[i]==1 and edge[0][0]==edge[1][0])==False) and (e[j]>0): 
                        # no edges created twice
                        # no loop edges 
                        # no edges created that lead to themself when no room for 2 new edges
                        # no edges created when they lead to an end which has no room for periodic edge to be made
                        #print(edge)

                        # reverse it 
                        edge_reverse = [edge[1],edge[0]]
                        # get the related edge for periodicity
                        edge_other = [[edge[0][0],-edge[1][1],-edge[1][2]],[edge[1][0],-edge[0][1],-edge[0][2]]]
                        # add the reverse of the periodic edge
                        edge_other_reverse = [edge_other[1],edge_other[0]]

                        edges.append(edge)
                        edges.append(edge_other)
                        # Decrease number of edges needed for nodes in unit cell 
                        e[i]=e[i]-1 # the node that we're leaving 
                        e[j]=e[j]-1 # the node that we're going to, since 
                            # either the periodic edge will lead to j in the unit cell
                            # or the edge itself will lead to j in the unit cell
                        #print(e)
                        edges.append(edge_reverse)
                        edges.append(edge_other_reverse)

        return edges


    def get_conductance(self):
        """
        Get the initial conductance tensor.
        For each edge: 
            - Get the points on either end of the edge 
            in terms of the index p. 
            - Convert each p index to a (i,r,s) triple  using key.
            - Check if the edge has an end inside the unit cell. 
            - If it does, then define the edge conductance in terms of the length of the edge.
            - If it doesn't, then do not add the edge to the conductance tensor.
        
        Returns
        -------
        - cond_init_4: numpy.ndarray
            cond_init_4[i,j,r,s] = conductance between node i in unit cell 
            and node j in cell at position (r,s) relative to unit cell.
        """
        # Parameters 
        # ----------
        num_nodes = self.num_nodes
        num_refs  = self.num_refs

        edges     = self.edges
        dist_6    = self.dist_6

        cond_init_4 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_refs))

        edge_lengs = []
        edge_conds   = []
        for edge in edges:
            # Get i,r,s triples that edge involves, by using key
            [i_i, r_i, s_i] = edge[0]
            [i_j, r_j, s_j] = edge[1]
            
            # Keep edge if involves unit cell
            # Either i or j is in unit cell, such that r==0==s.
            if (r_i == 0 and s_i == 0):
                #print("i_i={},r_i={},s_i={},i_j={},r_j={},s_j={}".format(i_i,r_i,s_i,i_j,r_j,s_j))
                # i is in unit cell
                cond_init_4[i_i,i_j,r_j,s_j]   = self.mean/dist_6[i_i,r_i,s_i,i_j,r_j,s_j] #(1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_i,r_i,s_i,i_j,r_j,s_j])
                cond_init_4[i_j,i_i,-r_j,-s_j] = self.mean/dist_6[i_i,r_i,s_i,i_j,r_j,s_j] #(1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_i,r_i,s_i,i_j,r_j,s_j]) 
                #print("d={}".format(dist_6[i_i,r_i,s_i,i_j,r_j,s_j]))
                edge_lengs.append(1.0/dist_6[i_i,r_i,s_i,i_j,r_j,s_j])
                edge_conds.append(cond_init_4[i_i,i_j,r_j,s_j])
                #g.append(cond_init_4[i_j,i_i,-r_j,-s_j])
            elif (r_j == 0 and s_j == 0):
                # j is in unit cell
                #print("i_i={},r_i={},s_i={},i_j={},r_j={},s_j={}".format(i_i,r_i,s_i,i_j,r_j,s_j))
                cond_init_4[i_j,i_i,r_i,s_i]   = self.mean/dist_6[i_i,r_i,s_i,i_j,r_j,s_j] #(1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_j,r_j,s_j,i_i,r_i,s_i])
                cond_init_4[i_i,i_j,-r_i,-s_i] = self.mean/dist_6[i_i,r_i,s_i,i_j,r_j,s_j] #(1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_j,r_j,s_j,i_i,r_i,s_i])
                #print("d={}".format(dist_6[i_i,r_i,s_i,i_j,r_j,s_j]))
                edge_lengs.append(1.0/dist_6[i_i,r_i,s_i,i_j,r_j,s_j])
                edge_conds.append(cond_init_4[i_j,i_i,r_i,s_i])
                #g.append(cond_init_4[i_j,i_i,-r_j,-s_j])
            else: 
                # neither i or j in unit cell so this edge is not in conductance
                pass
        
        self.edge_lengs = edge_lengs
        self.edge_conds = edge_conds
        return cond_init_4