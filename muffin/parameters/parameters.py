import json
import os
import argparse
import numpy

import muffin.utils.load_and_save as load_and_save

class Parameters():
    """Parameters class. See __init__ for functionality.
    """
    def __init__(self, path:str           = "./tests/test-2", 
                       initialisation:str = "4-reg",
                       num_nodes:int      = 4,
                       dist_cond:dict     = {"name":"lognormal", "mu":-0.045, "sigma":0.3},
                       dist_adhe:dict     = {"name":"delta",     "mu":1.0}, 
                       dist_effe:dict     = {"name":"delta",     "mu":0.01},
                       num_tliks:int      = 1001,
                       tlik_max:int       = 2000,
                       num_posis:int      = 101,
                       time_max:int       = 500,
                       parser_on:bool     = False
                ):
        """Add parameters as attributes and save dictionary of parameters at path.

        Parameters
        ----------
        path : str, optional
            Path at which parameter dictionary is save, by default "./muffin/examples/misc".
        num_nodes : int, optional
            Number of nodes in the cell, by default 4.
        initialisation : str, optional
            Name of the connectivity structure of the cell, by default "4-reg".
        alph : float, optional
            Adherence parameter, by default 1.0.
            A number between zero and one that determines how 'sticky' and edge is, 
            and therefore the proportion of particles that are removed on an edge they travel down it. 
            If alph=0 then no particles are removed, while if alph=1 then all particles are removed.
        beta : float, optional
            Reaction parameter, by default 0.01. 
            A number that determines the how much deposition decreases the conductance of an edge. 
            If beta=O(1) then we expect O(1) conductance decrease over the time it takes for fludi to traverse the
            network.
        max_ref_dist : int, optional
            Maximum number of cells between which adjacent nodes are connected, by default 1. 
            # TODO: Depricate
        num_dims : int, optional
            Number of dimensions, by default 2.
            # TODO: Depricate
        num_concs : int, optional
            Number of mass flux points to discretise with, by default 1001. 
            # TODO: Improve explanation.
        v : float, optional
            # TODO: Check definition, by default 0.5
        dict_cond : dict
            Initial conductance distribution. Dictionary with key "name" as well as keys for any 
            parameters of the named distribution. See muffin/initial_conditions/initial_conditions.py 
            for options.
        dict_adhe : dict
            Initial adherence distribution. Dictionary with key "name" as well as keys for any 
            parameters of the named distribution. See muffin/initial_conditions/initial_conditions.py 
            for options.
        """
        # Get parameters given in class instance
        self.dictionary_class:dict = locals()
        self.dictionary_class.pop("self") # remove self as parameter

        # Get parameters given in parser
        self.dictionary_parser:dict = self.get_parameters_parser(parser_on=parser_on)
    
        # Get parameters where parser overwrites class instance
        self.dictionary:dict = self.overwrite_default_parameters_with_parser()    


    # Attributes
    # -----
        # Primary parameters
        # -----
        self.path:str           = self.dictionary["path"]
        self.initialisation:str = self.dictionary["initialisation"]
        self.num_nodes:int      = self.dictionary["num_nodes"]
        self.dist_cond:dict     = self.dictionary_class["dist_cond"]
        self.dist_adhe:dict     = self.dictionary_class["dist_adhe"]
        self.dist_effe:dict     = self.dictionary_class["dist_effe"]
        self.num_tliks:int      = self.dictionary["num_tliks"]
        self.tlik_max:int       = self.dictionary["tlik_max"]
        self.num_posis          = self.dictionary["num_posis"]
        self.time_max           = self.dictionary["time_max"]
        self.phi                = 1.0 # TODO: Fix phi

        # Secondary parameters
        # -----
        self.alph:float = self.dist_adhe["mu"]
        self.beta:float = self.dist_effe["mu"]
        
        self.max_ref_dist:int = 1 # maximum number of cells between adjacent nodes
        self.refs_1:numpy.ndarray = self.get_references(max_ref_dist=self.max_ref_dist) # reference numbers : {0,,1,-1,...,K,-K} when max_ref_dist=K
        self.num_refs:int = len(self.refs_1) # number of reference numbers

        self.leng_1:numpy.ndarray = self.get_leng_1(initialisation=self.initialisation) # dimensions of cell

        self.tlik_1 = numpy.linspace(start=0, stop=self.tlik_max, num=self.num_tliks, endpoint=True) # time-like variable discretisation
        self.diff_tlik = self.tlik_1[1] - self.tlik_1[0] # step size for time-like variable discretisation

        self.num_dims:int = 2 # number of dimensions of cell

        self.path_save = os.path.join(self.path, "parameters")
    
        # Macroscale
        # -----
        self.posi_max = 1.0 # TODO: Change to self.leng_1[0]
        self.posi_1   = numpy.linspace(start=0, stop=self.posi_max, num=self.num_posis, endpoint=True)
        self.diff_posi = self.posi_1[1]-self.posi_1[0]

        self.num_times_solv = self.time_max*2*(self.num_posis-1)+1 
        self.time_solv_1 = numpy.linspace(start=0, stop=self.time_max, num=self.num_times_solv, endpoint=True)
        self.diff_time_solv = self.time_solv_1[1]-self.time_solv_1[0]

        self.incr_time = int((self.num_times_solv-1)/self.time_max) # time increment to reduce num times saved
        self.time_save_1 = self.time_solv_1[0::self.incr_time]
        self.num_times_save = len(self.time_save_1)

        self.conc_1 = self.get_initial_concentration_distribution(num_posis=self.num_posis)

        # TODO: Implement at what times to save

    # Do
    # -----
        self.save(path=self.path_save)


    # Methods 
    # -----
    def get_parameters_parser(self, parser_on):
        """Get a dictionary of the parameters given by the parser.

        Returns
        -------
        dictionary_parser : dict
            Dictionary where keys are parameter names and values are
            parameter values.
        """        
        if parser_on == True:
            # Define parser
            parser = argparse.ArgumentParser()

            # Optionally add parameters from parser
            parser.add_argument("-p",  "--path",           type=str, required=False, help="Path to simulation")
            parser.add_argument("-i",  "--initialisation", type=str, required=False, help="Structure of cell")
            parser.add_argument("-N",  "--num_nodes",      type=int, required=False, help="Number of nodes in cell")
            parser.add_argument("-dc", "--dist_cond",      type=str, required=False, help="Conductance distribution")
            parser.add_argument("-da", "--dist_adhe",      type=str, required=False, help="Adherence distribution")
            parser.add_argument("-de", "--dist_effe",      type=str, required=False, help="Effectance distribution")
            parser.add_argument("-nc", "--num_tliks",      type=int, required=False, help="Number of timelike variable point to discretise with")
            parser.add_argument("-tm", "--time_like_max",  type=int, required=False, help="Maximum value of timelike variable")
            parser.add_argument("-np", "--num_posis",      type=int, required=False, help="Number of spatial points to discretise with")
            parser.add_argument("-T",  "--time_max",       type=int, required=False, help="Maximum value of time variable")

            # Remove nones from parameters not given
            parser_args = parser.parse_args() 
            #parser_args, unknown = parser.parse_known_args()
            #parser_args = parser.parse_args("")
            dict_parser_args = vars(parser_args) # convert args to dictionary
            dictionary_parser = load_and_save.remove_none_items_from_dict(d=dict_parser_args) # remove nones

            # Convert distribution strings to dictionaries if given in parser
            if "dist_cond" in dictionary_parser.keys():
                dictionary_parser["dist_cond"] = json.loads(dictionary_parser["dist_cond"])
            if "dist_adhe" in dictionary_parser.keys():
                dictionary_parser["dist_adhe"] = json.loads(dictionary_parser["dist_adhe"])
            if "dist_effe" in dictionary_parser.keys():
                dictionary_parser["dist_effe"] = json.loads(dictionary_parser["dist_effe"])
        
        elif parser_on == False:
                dictionary_parser = {}

        return dictionary_parser


    def overwrite_default_parameters_with_parser(self):
        """Get a dictionary of all the parameters, where 
        any parameters that are given by the parser have overwritten 
        parameters given by the calss instance.

        Returns
        -------
        dict_parameters_after_parser : dict
            Dictionary where keys are parameter names and values are
            parameter values.
        """    
        # Get dictionary of parameters given by class instance
        dict_parameters_before_parser = self.dictionary_class
        dict_parser = self.dictionary_parser

        # Overwrite default/class-defined parameters with any from parser
        dict_parameters_after_parser  = dict_parameters_before_parser
        for parameter_name in dict_parameters_before_parser:
            if parameter_name in list(dict_parser.keys()):
                dict_parameters_after_parser[parameter_name] = dict_parser[parameter_name]
        
        return dict_parameters_after_parser


    def save(self, path:str=None):
        """Save dictionary of parameters as json at specified path.

        Parameters
        ----------
        path : str, optional
            Location at which to save parameter dictionary as json, by default None. 
            If none then saves at default path.
        """
        if path is None:
            print("Saving at default path: {}".format(self.path))
            path = self.path

        load_and_save.check_and_make_dir(path=path)

        with open(os.path.join(path,"parameters.json"), 'w') as json_file:
            d = self.dictionary
            json.dump(d, json_file, sort_keys=True, indent=4, separators=(',', ': '))


    def get_leng_1(self, initialisation):
        """
        """
        if initialisation == "4-reg":
            self.n:int                 = int(numpy.sqrt(self.num_nodes)) # number of rows or cols in square cell
            self.scale_factor:None     = None
            self.l1:float              = self.n*1.0
            self.l2:float              = self.n*1.0
        
        elif initialisation == "6-reg":
            self.n:int                = int(numpy.sqrt(self.num_nodes/2)) # number of rows or cols in square cell
            self.scale_factor:float   = numpy.sqrt(2.0)/numpy.sqrt(numpy.sqrt(3.0))
            self.l1:float             = self.n*self.scale_factor
            self.l2:float             = self.n*numpy.sqrt(3.0)*self.scale_factor
        
        elif initialisation == "6-ireg":
            self.n:int                = int(numpy.sqrt(self.num_nodes)) 
            self.scale_factor:float   = self.get_mean()
            self.l1:float             = self.n*1.0
            self.l2:float             = self.n*1.0
        
        else:
            raise Exception("The cell structure 'initialisation' must be '4-reg', '6-reg', or '6-ireg', and initialisation=={} is not implemented.".format(initialisation))
        
        leng_1 = numpy.array([self.l1,self.l2])
        
        # TODO: Add 'from file'
        return leng_1
        

    def get_mean(self)->float:
        if self.dist_cond["name"]=="lognormal":
            mean = numpy.exp(self.dist_cond["mu"]+self.dist_cond["sigma"]**2/2) 
        return mean
    # TODO: Move this to distribution
    

    def get_references(self, max_ref_dist:int)->numpy.ndarray:
        if max_ref_dist == 1:
            refs_1 = numpy.array([0,1,-1])
        else: 
            raise Exception("max_ref_dist != 1 is not implemented.")
            # TODO: Implement
        return refs_1


    def get_initial_concentration_distribution(self, num_posis:int)->numpy.ndarray:
        conc_1 = numpy.empty(shape=(num_posis))
        conc_1[:] = numpy.zeros_like(conc_1)
        conc_1[0] = 1.0
        return conc_1
    