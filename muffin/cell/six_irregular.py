import numpy
import scipy

import muffin.initial_conditions.initial_conditions as initial_conditions

class SixIrregular():
    """
    Class for six irregular cell. 

    Info
    -----
    Nodes are connected to other nodes using a Delaunay triangulation. 
    Average node coordination number is six. 
    Conductance distribution is set to empty since the conductance of each edge is 
    its inverse length, scaled by the desired conductnace per unit length (for example, 
    the mean conductance per unit length in a cell with which we with to compare).
    Thus conductancedistribution is specified as a delta distribition
    with parameter 1/edge_length in self.fill_edges(), which is different for each edge.
    """ 
    def __init__(self, num_nodes:int=4, 
                       mean:float=1.529590,
                       ):
        """
        Parameters 
        -----
        - num_nodes: int 
            The number of nodes in the cell. Any integer.

        - mean: float 
            The desired edge conductance per unit length. 
            To compare to four-regular cell, this should be the mean of the distribuiton 
            from which conductances in the four-regular cell are drawn. 
            For exmaple, if dist_cond == lognormal(mu,sigma), then mean=exp(mu+sigma**2/2)        
        """

    # Attributes
    # -----
        self.initialisation = "6-ireg"
        self.num_nodes:int  = num_nodes
        self.check_valid_num_nodes()
        self.n:int          = int(numpy.sqrt(num_nodes)) # number of rows or cols in square cell
        self.dist_cond:dict = {} # specified for each edge in self.fill_edges()
        self.dist_adhe:dict = {"name":"delta", "mu":1.0}
        self.mean:float     = mean
        self.num_refs:int   = 3

        self.num_dims:int = 2
        self.scale_factor = self.mean

        self.l1 = self.n*1.0
        self.l2 = self.n*1.0
    
        self.conn_4:numpy.ndarray = self.make_conn_4()
        self.cond_4:numpy.ndarray = self.fill_edges(dist=self.dist_cond)*self.scale_factor
        self.adhe_4:numpy.ndarray = self.fill_edges(dist=self.dist_adhe)


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
                            self.dist_cond["name"] = "delta"
                            self.dist_cond["mu"] = 1.0/self.dist_6[i,0,0,j,r,s]
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
        # -----
        pts_x_0 = numpy.random.uniform(low=0.0, high=l1, size=num_nodes) #*l1 
        pts_y_0 = numpy.random.uniform(low=0.0, high=l2, size=num_nodes) #*l2 

        # Get right and up components
        # -----
        pts_x_1 = l1*numpy.ones_like(pts_x_0) + pts_x_0 
        pts_y_1 = l2*numpy.ones_like(pts_y_0) + pts_y_0

        # Get left and down components
        # ------
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
        # ------
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
        tri = scipy.spatial.Delaunay(points=pts_to_tri_2)
        
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
        dist_6    = self.dist_6

        cond_init_4 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_refs))

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
                cond_init_4[i_i,i_j,r_j,s_j]   = 1 #self.mean/dist_6[i_i,r_i,s_i,i_j,r_j,s_j] #(1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_i,r_i,s_i,i_j,r_j,s_j])
                cond_init_4[i_j,i_i,-r_j,-s_j] = 1 #self.mean/dist_6[i_i,r_i,s_i,i_j,r_j,s_j] #(1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_i,r_i,s_i,i_j,r_j,s_j]) 
            elif (r_j == 0 and s_j == 0):
                # j is in unit cell
                cond_init_4[i_j,i_i,r_i,s_i]   = 1 #self.mean/dist_6[i_i,r_i,s_i,i_j,r_j,s_j] #(1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_j,r_j,s_j,i_i,r_i,s_i])
                cond_init_4[i_i,i_j,-r_i,-s_i] = 1 #self.mean/dist_6[i_i,r_i,s_i,i_j,r_j,s_j] #(1.72461)*(1/numpy.sqrt(num_nodes))*(1/dist_6[i_j,r_j,s_j,i_i,r_i,s_i])
        return cond_init_4


    def check_valid_num_nodes(self):
        """
        Raise no Exception. Any integer is a valid number of nodes for a six irregular cell.
        """
        pass

if __name__ == "__main__":
    num_nodes = 4 
    cell = SixIrregular(num_nodes=num_nodes, 
                        )
    print(cell.cond_4[:,:,0,0])
    for i in range(num_nodes):
        for j in range(num_nodes):
            for r in [0,1,-1]:
                for s in [0,1,-1]:
                    if cell.cond_4[i,j,r,s] != cell.cond_4[j,i,-r,-s]:
                        raise Exception()