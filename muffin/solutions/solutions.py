import numpy
import os

import muffin.parameters.parameters as parameters
import muffin.utils.load_and_save as load_and_save



class Base():
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
    
    # Methods 
    # -----
    def save(self, d:dict=None, path_file:str=None):
        load_and_save.save_dict_of_array(d=d, path_file=path_file)


    def save_single(self, variable_name:str="conductance"):
        y_meta = self.dictionary[variable_name]
        self.save(d=y_meta, path_file=os.path.join(self.path_save,"{}.npy".format(y_meta["name"])))


    def save_all(self):
        for variable_name in self.variable_names:
            self.save_single(variable_name=variable_name)


    def load(self, path_file:str=None):
        d = load_and_save.load_dict_of_array(path_file=path_file)
        return d


    def load_single(self, variable_name:str="conductance"):
        d = self.load(path_file=os.path.join(self.path_save,"{}.npy".format(variable_name)))
        return d
    

    def load_all(self):
        self.dictionary = {}
        for variable_name in self.variable_names:
            d = self.load_single(variable_name=variable_name)
            self.dictionary[variable_name] = d



class Solution(Base):
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
        self.parameters = parameters
        self.path_save = os.path.join(self.parameters.path, "solution")
        load_and_save.check_and_make_dir(path=self.path_save)

        self.variable_names = [
            "time_like",
            "conductance",
            "cell_solution",
            "cell_solution_difference",
            "cell_solution_direction",
            "permeability",
            "adhesivity"
        ]

        # Define solution variables to fill
        # ------
        S = parameters.num_tliks
        N = parameters.num_nodes
        R = parameters.num_refs
        D = parameters.num_dims
        
        self.tlik_1 = parameters.tlik_1
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



class Solution_Flow(Base):
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
        self.parameters = parameters
        self.path_save = os.path.join(self.parameters.path, "solution_flow")
        load_and_save.check_and_make_dir(path=self.path_save)

        self.variable_names = [
            "time",
            "position",
            "concentration",
            "time_like",
            "permeability",
            "adhesivity",
            "velocity",
            "pressure_gradient",
            "reactivity"
        ]

        # Define solution variables to fill
        # ------
        T = parameters.num_times_solv
        X = parameters.num_posis

        self.time_solv_1 = parameters.time_solv_1
        self.time_save_1 = parameters.time_save_1
        self.posi_1 = parameters.posi_1
        self.conc_2 = numpy.empty(shape=(T,X))
        self.tlik_2 = numpy.empty(shape=(T,X))
        self.perm_2 = numpy.empty(shape=(T,X))
        self.depo_2 = numpy.empty(shape=(T,X))
        self.velo_1 = numpy.empty(shape=(T))
        self.dpdx_2 = numpy.empty(shape=(T,X))
        self.psi_2  = numpy.empty(shape=(T,X))


    # Methods
    # ------
    def get_dictionary(self):
        self.dictionary = {}

        self.dictionary["time"] = {}
        self.dictionary["time"]["name"] = "time"
        self.dictionary["time"]["variable"] = "time_1"
        self.dictionary["time"]["label"] = r"$t$"
        self.dictionary["time"]["value"] = self.time_save_1
        self.dictionary["time"]["indices"] = ["i_t"]

        self.dictionary["position"] = {}
        self.dictionary["position"]["name"] = "position"
        self.dictionary["position"]["variable"] = "posi_1"
        self.dictionary["position"]["label"] = r"$x$"
        self.dictionary["position"]["value"] = self.posi_1
        self.dictionary["position"]["indices"] = ["i_x"]
  
        self.dictionary["concentration"] = {}
        self.dictionary["concentration"]["name"] = "concentration"
        self.dictionary["concentration"]["variable"] = "conc_2"
        self.dictionary["concentration"]["label"] = r"$c$"
        self.dictionary["concentration"]["value"] = self.conc_2
        self.dictionary["concentration"]["indices"] = ["i_t","i_x"]

        self.dictionary["time_like"] = {}
        self.dictionary["time_like"]["name"] = "time_like"
        self.dictionary["time_like"]["variable"] = "tlik_2"
        self.dictionary["time_like"]["label"] = r"$s$"
        self.dictionary["time_like"]["value"] = self.tlik_2
        self.dictionary["time_like"]["indices"] = ["i_t","i_x"]
    
        self.dictionary["permeability"] = {}
        self.dictionary["permeability"]["name"] = "permeability"
        self.dictionary["permeability"]["variable"] = "perm_2"
        self.dictionary["permeability"]["label"] = r"$k$"
        self.dictionary["permeability"]["value"] = self.perm_2
        self.dictionary["permeability"]["indices"] = ["i_t","i_x"]

        self.dictionary["adhesivity"] = {}
        self.dictionary["adhesivity"]["name"] = "adhesivity"
        self.dictionary["adhesivity"]["variable"] = "depo_2"
        self.dictionary["adhesivity"]["label"] = r"$j$"
        self.dictionary["adhesivity"]["value"] = self.depo_2
        self.dictionary["adhesivity"]["indices"] = ["i_t","i_x"]

        self.dictionary["velocity"] = {}
        self.dictionary["velocity"]["name"] = "velocity"
        self.dictionary["velocity"]["variable"] = "velo_1"
        self.dictionary["velocity"]["label"] = r"$u$"
        self.dictionary["velocity"]["value"] = self.velo_1
        self.dictionary["velocity"]["indices"] = ["i_t"]

        self.dictionary["pressure_gradient"] = {}
        self.dictionary["pressure_gradient"]["name"] = "pressure_gradient"
        self.dictionary["pressure_gradient"]["variable"] = "dpdx_2"
        self.dictionary["pressure_gradient"]["label"] = r"$\partial p/\partial x$"
        self.dictionary["pressure_gradient"]["value"] = self.dpdx_2
        self.dictionary["pressure_gradient"]["indices"] = ["i_t","i_x"]

        self.dictionary["reactivity"] = {}
        self.dictionary["reactivity"]["name"] = "reactivity"
        self.dictionary["reactivity"]["variable"] = "psi_2"
        self.dictionary["reactivity"]["label"] = r"$\psi$"
        self.dictionary["reactivity"]["value"] = self.psi_2
        self.dictionary["reactivity"]["indices"] = ["i_t","i_x"]
