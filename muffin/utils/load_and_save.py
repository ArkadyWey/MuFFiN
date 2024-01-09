import argparse
import json
import numpy 
import os

def parse_any_given_args():
    """
    If a valid arg was given to parser, then save it.
    path_parameters : str
        Path to parameters file in json format.
    """
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-pr",   "--path_results",   type=str,     required=False, help="Path to results")
    parser.add_argument("-N",    "--num_nodes",      type=int,     required=False, help="Number of nodes in cell")
    parser.add_argument("-init", "--initialisation", type=str,     required=False, help="Structure of cell")
    parser.add_argument("-a",    "--alph",           type=float,   required=False, help="alpha")
    parser.add_argument("-b",    "--beta",           type=float,   required=False, help="beta")
    
    args = parser.parse_args()

    return args

def load_parameters_not_given(parameters_required: list, parameters_given: dict, parameters_default: dict):
    """
    """
    parameters_used = parameters_given 
    for parameter_name in parameters_required:
        if parameter_name not in list(parameters_given.keys()):
            parameters_used[parameter_name] = parameters_default[parameter_name]
    return parameters_used

def load_json_as_dict(path_json):
    with open(path_json) as json_file:
        d = json.load(json_file)
    return d

def save_dict_as_json(d, path_json):
    with open(path_json, 'w') as json_file:
        json.dump(d, json_file, sort_keys=True, indent=4, separators=(',', ': '))

def load_required_parameters(parameters_required:list):
    """
    """
    
    # Load default parameters
    path_parameters_default = "./muffin/parameters.json" 
    parameters_default      = load_json_as_dict(path_json=path_parameters_default)

    # Unpack any parameters given in parser
    args = parse_any_given_args() # use parameter_value = args.name
    parameters_given = vars(args) # convert args to dictionary

    # Add default values for any other required parameters
    parameters_used = load_parameters_not_given(parameters_required=parameters_required, 
                                                parameters_given=parameters_given, 
                                                parameters_default=parameters_default)
    return parameters_used


def save_nparray_as_npy(path_results, a, name):
    """
    """
    numpy.save(file=os.path.join(path_results, name), arr=a, allow_pickle=True, fix_imports=True)

def check_and_make_dir(path:str):
    """Check if directory exists and make it if it does not.

    Parameters
    ----------
    path : str
        String to directory to be checked and made.
    """
    if not os.path.exists(path):
        os.mkdir(path)