import numpy

import muffin.parameters.parameters as parameters


class Solution():
    """_summary_
    """
    def __init__(self, parameters:parameters.Parameters,
                       ): 
        """_summary_
        """

    # Attributes
    # -----
        # Load variables from parameters 
        # ------
        self.tlik_1 = parameters.tlik_1

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


    # Methods
    # ------
    def get_dictionary(self):
        self.dictionary = {}

        self.dictionary["time_like"] = {}
        self.dictionary["time_like"]["name"] = "time_like"
        self.dictionary["time_like"]["variable"] = "tlik_1"
        self.dictionary["time_like"]["label"] = r"$s$" #r"$G_{ij}^{\bm{r}}$"
        self.dictionary["time_like"]["value"] = self.tlik_1
        self.dictionary["time_like"]["indices"] = []

        self.dictionary["conductance"] = {}
        self.dictionary["conductance"]["name"] = "conductance"
        self.dictionary["conductance"]["variable"] = "cond_5"
        self.dictionary["conductance"]["label"] = r"$G_{ij}^r$" #r"$G_{ij}^{\bm{r}}$"
        self.dictionary["conductance"]["value"] = self.cond_5
        self.dictionary["conductance"]["indices"] = ["s","i","j","r0","r1"]

        self.dictionary["cell_solution"] = {}
        self.dictionary["cell_solution"]["name"] = "cell_solution"
        self.dictionary["cell_solution"]["variable"] = "csol_3"
        self.dictionary["cell_solution"]["label"] = r"$W_i^m$"
        self.dictionary["cell_solution"]["value"] = self.csol_3
        self.dictionary["cell_solution"]["indices"] = ["s","i","m"]

        self.dictionary["cell_solution_difference"] = {}
        self.dictionary["cell_solution_difference"]["name"] = "cell_solution_difference"
        self.dictionary["cell_solution_difference"]["variable"] = "delt_5"
        self.dictionary["cell_solution_difference"]["label"] = r"$\Delta_{ij}^{rm}$"
        self.dictionary["cell_solution_difference"]["value"] = self.delt_5
        self.dictionary["cell_solution_difference"]["indices"] = ["s","i","j","r","m"]

        self.dictionary["cell_solution_direction"] = {}
        self.dictionary["cell_solution_direction"]["name"] = "cell_solution_direction"
        self.dictionary["cell_solution_direction"]["variable"] = "heav_5"
        self.dictionary["cell_solution_direction"]["label"] = r"$H_{ij}^{rm}$"
        self.dictionary["cell_solution_direction"]["value"] = self.heav_5
        self.dictionary["cell_solution_direction"]["indices"] = ["s","i","j","r","m"]

        self.dictionary["permeability"] = {}
        self.dictionary["permeability"]["name"] = "permeability"
        self.dictionary["permeability"]["variable"] = "perm_3"
        self.dictionary["permeability"]["label"] = r"$k$"
        self.dictionary["permeability"]["value"] = self.perm_3
        self.dictionary["permeability"]["indices"] = ["s","m","n"]

        self.dictionary["adhesivity"] = {}
        self.dictionary["adhesivity"]["name"] = "adhesivity"
        self.dictionary["adhesivity"]["variable"] = "depo_2"
        self.dictionary["adhesivity"]["label"] = r"$j$"
        self.dictionary["adhesivity"]["value"] = self.depo_2
        self.dictionary["adhesivity"]["indices"] = ["s","m"]
