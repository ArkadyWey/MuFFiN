import json
import os
import argparse

import muffin.utils.load_and_save as load_and_save

class Parameters():
    """Parameters class. See __init__ for functionality.
    """
    def __init__(self, path:str           = "./examples/misc/meta", 
                       num_nodes:int      = 4,
                       initialisation:str = "4-reg",
                       alph:float         = 1.0,
                       beta:float         = 0.01,
                       max_ref_dist:int   = 1,
                       num_dims:int       = 2,
                       num_concs:int      = 1001,
                       num_refs           = 3,
                       v:float            = 0.5,  
                       dist_cond:dict     = {"name":"lognormal", "mu":-0.045, "sigma":0.3},
                       dist_adhe:dict     = {"name":"delta",     "mu":-0.045}
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
        self.dictionary_parser:dict = self.get_parameters_parser()
    
        # Get parameters where parser overwrites class instance
        self.dictionary:dict = self.overwrite_parameters_class_with_parser()    

    # Attributes
    # -----
        self.path:str           = self.dictionary["path"]
        self.num_nodes:int      = self.dictionary["num_nodes"]
        self.initialisation:str = self.dictionary["initialisation"]
        self.alph:float         = self.dictionary["alph"]
        self.beta:float         = self.dictionary["beta"]
        self.max_ref_dist:int   = self.dictionary["max_ref_dist"]
        self.num_dims:int       = self.dictionary["num_dims"]
        self.num_concs:int      = self.dictionary["num_concs"]
        self.num_refs:int       = self.dictionary["num_refs"]
        self.v:float            = self.dictionary["v"]
        self.dist_cond:dict     = self.dictionary_class["dist_cond"]
        self.dist_adhe:dict     = self.dictionary_class["dist_adhe"]

    # Do
    # -----
        self.save(path=self.path)

    # Methods 
    # -----
    def get_parameters_parser(self):
        """Get a dictionary of the parameters given by the parser.

        Returns
        -------
        dictionary_parser : dict
            Dictionary where keys are parameter names and values are
            parameter values.
        """        
        # Define parser
        parser = argparse.ArgumentParser()
            
        # Optionally add parameters from parser
        parser.add_argument("-pr",   "--path",           type=str,   required=False, help="Path to results")
        parser.add_argument("-N",    "--num_nodes",      type=int,   required=False, help="Number of nodes in cell")
        parser.add_argument("-init", "--initialisation", type=str,   required=False, help="Structure of cell")
        parser.add_argument("-a",    "--alph",           type=float, required=False, help="Adherence parameter")
        parser.add_argument("-b",    "--beta",           type=float, required=False, help="Reaction parameter")
        parser.add_argument("-mrd",  "--max_ref_dist",   type=float, required=False, help="Maximum number of cells between which adjacent nodes are connected")
        parser.add_argument("-nd",   "--num_dims",       type=float, required=False, help="Number of dimensions")
        parser.add_argument("-nc",   "--num_concs",      type=float, required=False, help="Number of mass flux points to discretise with, by default 1001")
        parser.add_argument("-v",    "--v",              type=float, required=False, help="Check definition")
        parser.add_argument("-nr",   "--num_refs",       type=int,   required=False, help="Number of cell reference numbers")
        parser.add_argument("-dc",   "--dist_cond",      type=str,   required=False, help="Conductance distribution")
        parser.add_argument("-da",   "--dist_adhe",      type=str,   required=False, help="Adherence distribution")
        
        # Remove nones from parameters not given
        parser_args = parser.parse_args() 
        dict_parser_args = vars(parser_args) # convert args to dictionary
        dictionary_parser = load_and_save.remove_none_items_from_dict(d=dict_parser_args) # remove nones
        
        # Convert distribution strings to dictionaries if given in parser
        if "dist_cond" in dictionary_parser.keys():
            dictionary_parser["dist_cond"] = json.loads(dictionary_parser["dist_cond"])
        if "dist_adhe" in dictionary_parser.keys():
            dictionary_parser["dist_adhe"] = json.loads(dictionary_parser["dist_adhe"])
        
        return dictionary_parser


    def overwrite_parameters_class_with_parser(self):
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
        



