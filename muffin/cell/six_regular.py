import numpy
import scipy

import muffin.initial_conditions.initial_conditions as initial_conditions

class SixRegular():
    """
    """ 
    def __init__(self, num_nodes:int=2, 
                       dist_cond:dict={"name":"lognormal", "mu":0.5, "sigma":0.3},
                       dist_adhe:dict={"name":"delta",     "mu":0.5}
                       ):
        """
        """
    # Attributes
    # -----
        self.initialisation:str   = "6-reg"
        self.num_nodes:int        = num_nodes
        self.n:int                = int(numpy.sqrt(num_nodes/2)) # number of rows or cols in square cell
        self.dist_cond:dict       = dist_cond
        self.dist_adhe:dict       = dist_adhe
        self.num_refs:int         = 3
        self.num_dims:int         = 2
        
        self.scale_factor:float   = numpy.sqrt(2.0)/numpy.sqrt(numpy.sqrt(3.0))
        self.l1:float             = self.n*self.scale_factor
        self.l2:float             = self.n*numpy.sqrt(3.0)*self.scale_factor
        self.leng_1:numpy.ndarray = self.get_leng_1()

        self.check_valid_num_nodes()

        self.conn_4:numpy.ndarray = self.make_conn_4()
        self.cond_4:numpy.ndarray = self.fill_edges(dist=self.dist_cond)/self.scale_factor
        self.adhe_4:numpy.ndarray = self.fill_edges(dist=self.dist_adhe)/self.scale_factor


    # Methods 
    # -----
    def get_sample(self,dist):
        sample = initial_conditions.get_sample(**dist)
        return sample

    def fill_edges(self,dist):
        """
        """
        a_4 = numpy.zeros_like(self.conn_4)
        for r in [0,1,-1]:
            for s in [0,1,-1]:
                for i in numpy.arange(start=0,stop=self.num_nodes,step=1):
                    for j in numpy.arange(start=i,stop=self.num_nodes,step=1):
                        if self.conn_4[i,j,r,s] != 0.0 and a_4[i,j,r,s] == 0:
                            sample = self.get_sample(dist=dist)
                            a_4[i,j,r,s]   = sample
                            a_4[j,i,-r,-s] = sample
        return a_4


    def make_conn_4(self):
        """
        """
        (self.pts_x_0, 
         self.pts_y_0, 
         self.pts_x_1, 
         self.pts_y_1, 
         self.pts_x_m1, 
         self.pts_y_m1) = self.get_node_coordinates()

        self.pts_4  = self.get_points_tensor()
        self.dist_6 = self.get_distance_between_points()

        (self.simplices, 
         self.key, 
         self.pts_to_tri_2) = self.get_simplices_of_triangulation()

        self.edges  = self.get_edges()
        self.conn_4 = self.connect_edges()

        return self.conn_4
        

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


        # Get central-cell components
        # ------
        pts_x_0 = []
        for i in range(num_rows_or_cols):
            # Fill the coordinates with the correct number of
            # construction cell points
            pts_x_0.append(pts_x_constr[0]+i) # get x coord of all 0 points to right
            pts_x_0.append(pts_x_constr[1]+i) # get x coord of all 1/2 points to right
        pts_x_0 = numpy.array(pts_x_0)           

        # We now need x points above and y points to the right, 
        # which are identical to those already made
        pts_x_0 = numpy.tile(A=pts_x_0, reps=num_rows_or_cols)

        pts_y_0_tile = list(numpy.tile(A=pts_y_constr, reps=num_rows_or_cols))
        
        pts_y_0 = []
        for i in range(num_rows_or_cols):
            for el in pts_y_0_tile:
                pts_y_0.append(el+i*numpy.sqrt(3.0)*self.scale_factor) # get y coord of all 0,1 points above
        
        pts_y_0 = numpy.array(pts_y_0)

        # Get right/up components
        # -----
        pts_x_1 = num_rows_or_cols*numpy.ones_like(pts_x_0)*self.scale_factor + pts_x_0 
        pts_y_1 = num_rows_or_cols*numpy.sqrt(3.0)*self.scale_factor*numpy.ones_like(pts_y_0) + pts_y_0

        # Get left/down components
        # -----
        pts_x_m1 = -num_rows_or_cols*numpy.ones_like(pts_x_0)*self.scale_factor + pts_x_0
        pts_y_m1 = -num_rows_or_cols*numpy.sqrt(3.0)*self.scale_factor*numpy.ones_like(pts_y_0) + pts_y_0

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
        # ----- 
        num_nodes = self.num_nodes 
        num_refs  = self.num_refs

        pts_x_0   = self.pts_x_0
        pts_y_0   = self.pts_y_0
        pts_x_1   = self.pts_x_1
        pts_y_1   = self.pts_y_1
        pts_x_m1   = self.pts_x_m1
        pts_y_m1   = self.pts_y_m1

        num_dims = self.num_dims

        # Make empty array
        # ------
        pts_4 = numpy.zeros(shape=(num_nodes,num_dims,num_refs,num_refs))

        # Fill array
        # ------     
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
        # -----
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
                                # -----
                                p_i = pts_4[i,:,r_i,s_i]
                                p_j = pts_4[j,:,r_j,s_j]
                                # Get distance between points
                                # -----
                                dist_6[i,r_i,s_i,j,r_j,s_j] = numpy.linalg.norm(p_i-p_j)

        return dist_6


    def get_simplices_of_triangulation(self):
        """
        Get all points in points tensor in correct form to use triangulation 
        method. 
        Then triangulate all points using Delaunay triangulation.

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
        # -----
        num_refs  = self.num_refs
        num_nodes = self.num_nodes

        pts_4     = self.pts_4

        # Make empty lists
        # -----
        pts_to_tri_2 = []
        key = []
        # pts_to_tri_2[p,m] = mth (x or y) component of point p 
        # Need in this form for Delaunay algorithm.
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
        # ------
        tri = scipy.spatial.Delaunay(points=pts_to_tri_2)
        
        # Get simplices
        # ------
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


    def connect_edges(self):
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

        conn_4 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_refs))

        for edge in edges:
            # Get points that edge involves
            p_i = edge[0]
            p_j = edge[1]

            # Get i,r,s triples that edge involves, by using key
            [i_i, r_i, s_i] = key[p_i]
            [i_j, r_j, s_j] = key[p_j]

            # Keep edge if it involves unit cell i.e., either i or j is in unit cell such that r==0==s.
            if (r_i == 0 and s_i == 0):
                # i is in unit cell
                conn_4[i_i,i_j,r_j,s_j]   = 1
                conn_4[i_j,i_i,-r_j,-s_j] = 1 
            elif (r_j == 0 and s_j == 0):
                # j is in unit cell
                conn_4[i_j,i_i,r_i,s_i]   = 1 
                conn_4[i_i,i_j,-r_i,-s_i] = 1 
            else: 
                # neither i or j in unit cell so this edge is not in cell
                pass

        return conn_4


    def check_valid_num_nodes(self):
        """
        Raise Exception if n=sqrt(num_nodes/2) is not square.

        Parameters
        -----
        - num_nodes: int 
            Number of nodes in the cell. 
            n = sqrt(num_nodes/2) must be square.     
        """
        N = self.num_nodes
        n = numpy.sqrt(N/2)
        
        if n-int(n) != 0.0:
            raise Exception("""A six regular cell cannot be constructed using num_nodes={} \\
                               because it required that n=sqrt(num_nodes/2) is square.""".format(self.num_nodes))
        else: 
            pass

    def get_leng_1(self):
        """
        """
        leng_1 = numpy.array([self.l1,self.l2])
        return leng_1


if __name__ == "__main__":
    num_nodes = 8
    mu = 0.5 
    sigma = 0.3 
    cell = SixRegular(num_nodes=num_nodes, 
                      dist_cond={"name":"lognormal", "mu":mu, "sigma":sigma},
                      dist_adhe={"name":"delta", "mu":1},
                        )
    print(cell.cond_4[:,:,1,0])
    for i in range(num_nodes):
        for j in range(num_nodes):
            for r in [0,1,-1]:
                for s in [0,1,-1]:
                    if cell.cond_4[i,j,r,s] != cell.cond_4[j,i,-r,-s]:
                        raise Exception()