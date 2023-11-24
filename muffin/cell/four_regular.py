import numpy 
import scipy

import muffin.initial_conditions.initial_conditions as initial_conditions

class FourRegular():
    """
    """
    def __init__(self, num_nodes:int=4, 
                       dist_cond:dict={"name":"lognormal", "mu":0.5, "sigma":0.3},
                       dist_adhe:dict={"name":"delta",     "mu":0.5}
                       ):
        """
        """

    # Attributes
    # -----
        self.num_nodes:int  = num_nodes
        self.check_valid_num_nodes()
        self.n:int          = int(numpy.sqrt(num_nodes)) # number of rows or cols in square cell
        self.dist_cond:dict = dist_cond
        self.dist_adhe:dict = dist_adhe
        
        self.num_refs:int = 3


        self.conn_4:numpy.ndarray = self.make_conn_4()
        self.cond_4:numpy.ndarray = self.fill_edges(dist=self.dist_cond)
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
                            sample = self.get_sample(dist=dist)
                            a_4[i,j,r,s]   = sample
                            a_4[j,i,-r,-s] = sample
        return a_4

    def make_conn_4(self):
        """
        Get cell initial connectivity tensor.

        Parameters
        -----
        - num_nodes: int
            Number of nodes in the cell. Must be a square number.
        - num_refs: int
            Number of lengths in the reference set. 
            For example, if reference set is {-1,0,+1} then num_refs==3.
        - mu: float 
            Mean of the normal distribution from which the lognormal distribution is derived. 
            Must be non-negative. 
        - sigma: float: 
            Standard deviation of the normal distribution from which the lognormal distribution is derived. 
            Must be non-negative. 
    
        Returns 
        -----
        - conn_4: numpy.ndarray
            Connectivity tensor of the cell.
            conn_4[i,j,r1,r2] = 1 if edge exists between node i in reference cell and node j in the cell 
            at position r1,r2.

        """
        
        # Get parameters
        # -----
        num_nodes = self.num_nodes
        num_refs  = self.num_refs
        n         = self.n
        
        # Make empty connectivity tensor
        # -----
        conn_4 = numpy.zeros(shape=(num_nodes, num_nodes, num_refs, num_refs))

        # Add intra-cell edges
        # -----
        # Form block
        diagonals = [numpy.ones(n-1), numpy.ones(n-1)]
        a_2 = scipy.sparse.diags(diagonals=diagonals, offsets=[1,-1], shape=(n, n)).toarray()

        # Form block diagonal
        tup = n*(a_2,)
        b_2 = scipy.linalg.block_diag(*tup)

        # Form outer diagonals
        more_diagonals = [numpy.ones(num_nodes-n), numpy.ones(num_nodes-n)]
        c_2 = scipy.sparse.diags(diagonals=more_diagonals, offsets=[n, -n], shape=(num_nodes, num_nodes)).toarray()

        # Form adjacency matrix
        adj_intra_2 = b_2 + c_2

        # Add intra-cell edges to cell
        conn_4[:,:,0,0] = adj_intra_2


        # Add inter-cell edges
        # -----

        # Get all node indices
        nodes = numpy.linspace(0,n**2-1,n**2)

        # Get indices of nodes on outside of cell
        left_nodes   = nodes[0::n]
        right_nodes  = nodes[n-1::n]
        top_nodes    = nodes[0:n]
        bottom_nodes = nodes[self.num_nodes-n::]

        # Add inter-cell edges to cell
        for i in range(n):
            left_node   = int(left_nodes[i])
            right_node  = int(right_nodes[i])
            top_node    = int(top_nodes[i])
            bottom_node = int(bottom_nodes[i])
 
            conn_4[left_node,right_node,-1,0] = 1 
            conn_4[right_node,left_node,+1,0] = 1 
            conn_4[bottom_node,top_node,0,-1] = 1 
            conn_4[top_node,bottom_node,0,+1] = 1

        return conn_4

    def check_valid_num_nodes(self):
        """
        Raise Exception if n=sqrt(num_nodes) is not square.

        Parameters
        -----
        - num_nodes: int 
            Number of nodes in the cell. 
            n = sqrt(num_nodes) must be square.     
        """
        N = self.num_nodes
        n = numpy.sqrt(N)
        
        if n-int(n) != 0.0:
            raise Exception("""A four regular cell cannot be constructed using num_nodes={}.
                               because it requires that n=sqrt(num_nodes) is square.""".format(self.num_nodes))
        else: 
            pass




if __name__ == "__main__":
    num_nodes = 4
    mu = 0.5 
    sigma = 0.3 
    cell = FourRegular(num_nodes=num_nodes, 
                        dist_cond={"name":"lognormal", "mu":mu, "sigma":sigma},
                        dist_adhe={"name":"delta", "mu":1},
                        )
    print(cell.cond_4[:,:,0,0])
    for i in range(num_nodes):
        for j in range(num_nodes):
            for r in [0,1,-1]:
                for s in [0,1,-1]:
                    if cell.cond_4[i,j,r,s] != cell.cond_4[j,i,-r,-s]:
                        raise Exception()