import numpy
import scipy



class Cell_2D_Grid:
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


  