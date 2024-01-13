import numpy

import muffin.parameters.parameters as parameters
import muffin.cells.cells as cells


class Solution():
    """_summary_
    """
    def __init__(self, parameters:parameters.Parameters,
                       ): 
        """_summary_
        """

    # Attributes
    # -----
        S = parameters.num_concs
        N = parameters.num_nodes
        R = parameters.num_refs
        D = parameters.num_dims
        
        # Define solution variables to fill
        # ------
        self.cond_5 = numpy.empty(shape=(S,N,N,R,R))
        self.csol_3 = numpy.empty(shape=(S,N,D))
        self.delt_5 = numpy.empty(shape=(S,N,N,R,D))
        self.heav_5 = numpy.empty(shape=(S,N,N,R,D))
        self.perm_3 = numpy.empty(shape=(S,D,D))
        self.depo_2 = numpy.empty(shape=(S,D))
