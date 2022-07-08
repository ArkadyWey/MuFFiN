from inspect import Parameter
import numpy
import json

import preprocess_2D
import initial_conditions_2D


class Configure():
    """
    """ 
    def __init__(self, num_nodes: int):
        """
        """      

        # Get class parameters 
        # -----
        self.num_nodes    = num_nodes
        
        
        # Get input parameters from parameters dictionary or class parameters
        # -----
        file = open("parameters.json", "r")
        parameters = json.load(file)
        
        self.max_ref_dist   = parameters["max_ref_dist"]
        self.num_dims       = parameters["num_dims"]
        self.num_concs      = parameters["num_concs"]
        self.alpha          = parameters["alpha"]
        self.v              = parameters["v"]    # 2.0 # Sum of volumes of nodes in cell
        self.phi            = parameters["phi"]  # TODO: Define this properly
        self.l1             = parameters["l1"]
        self.l2             = parameters["l2"]
        self.mean           = parameters["mean"] 
        self.sd             = parameters["sd"]
        self.initialisation = parameters["initialisation"]


        # Do secondary configuration 
        # -----
        self.leng_1          = numpy.array([self.l1, self.l2])
        self.conc_max_disc_1 = numpy.linspace(0, 1.0, self.num_concs)
        self.refs_2          = preprocess_2D.get_reference(max_ref_dist=self.max_ref_dist,
                                                           num_dims=self.num_dims)



        # Get initial conditions: conductance and adhesivity 
        # -----
        self.num_refs = len(self.refs_2[:,0])

        self.adhe_init_4 = numpy.zeros(shape=(self.num_nodes, self.num_nodes, self.num_refs, self.num_refs)) 

        self.cond_init_4 = self.get_initial_conductance()


    def get_initial_conductance(self):
        """
        The initial conductance depends on the parameter 
        initialisation, which is prescribed in the parameters 
        dictionary.
        """
        if self.initialisation == "square-struc_prescribed":
            cond_init_4 = initial_conditions_2D.grid_prescribed(num_nodes=self.num_nodes,
                                                                     num_refs=self.num_refs)
        elif self.initialisation == "square-struc":
            cond_init_4 = initial_conditions_2D.grid_log_normal(num_nodes=self.num_nodes, 
                                                                     num_refs=self.num_refs, 
                                                                     mean=self.mean,
                                                                     sd=self.sd)
        elif self.initialisation == "rand-struc":
            cond_init_4 = initial_conditions_2D.random_structure_uniform(num_nodes=self.num_nodes,
                                                                         num_refs=self.num_refs)

        elif self.initialisation == "hexag-struc":
            cond_init_4 = initial_conditions_2D.hexag_struc(num_nodes=self.num_nodes, 
                                                            num_refs=self.num_refs, 
                                                            mean=self.mean, 
                                                            sd=self.sd)

        else: 
            raise Exception("""initialisation must be: square-struc_prescribed or \
                               square-struc or rand-struc or hexag-struc.""")

        return cond_init_4


if __name__ == "__main__":

    num_nodes = 1


    conf = Configure(num_nodes=num_nodes)
