import argparse
import json
import numpy 
import os



def parse_any_given_args()->dict:
    """Parse all parser arguments. Arguments that were not given are parsed as with None as value. 
    Remove these from the dictionary of arguments.

    Returns
    -------
    dict
        Dictionary of all specified parser arguments.
    """
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-pr",   "--path_results",   type=str,     required=False, help="Path to results")
    parser.add_argument("-N",    "--num_nodes",      type=int,     required=False, help="Number of nodes in cell")
    parser.add_argument("-init", "--initialisation", type=str,     required=False, help="Structure of cell")
    parser.add_argument("-a",    "--alph",           type=float,   required=False, help="alpha")
    parser.add_argument("-b",    "--beta",           type=float,   required=False, help="beta")
    
    args = parser.parse_args() 
    dict_args = vars(args) # convert args to dictionary
    dict_args_no_nones = remove_none_items_from_dict(d=dict_args)
    return dict_args_no_nones



def remove_none_items_from_dict(d:dict)->dict:
    """Given a dictionary, remove the items (i.e., key-value pairs) that consist of 
    a None value, and return the dictionary.

    Parameters
    ----------
    d : dict
        Dictionary to check for None values.

    Returns
    -------
    dict
        Dictionary with key and values corresponding to None values removed.
    """
    del_keys = []
    for key, value in d.items():
        if value == None:
            del_keys.append(key)
    for key in del_keys:
        d.pop(key)
    return d 



def load_parameters_not_given(parameters_required: list, parameters_given: dict, parameters_default: dict)->dict:
    """Given a lists of parameters that are required, parameters that have actually been given, and 
    parameters that are used as default (i.e., when alternative values are not specified), 
    return a list of parameters to be used.

    Parameters
    ----------
    parameters_required : list
        List of strings that are names of parameters that are required for a function.
    parameters_given : dict
        Dictionary of parameters that have been given (e.g., in the parser).
    parameters_default : dict
        Dictionary of parmaeters to be used if alternatives are not given.

    Returns
    -------
    parameters_used: dict
        Dictionary of parameters to be used, consisting of parameters that are given 
        and default values for those that are not.
    """
    parameters_used = parameters_given 
    for parameter_name in parameters_required:
        if parameter_name not in list(parameters_given.keys()):
            parameters_used[parameter_name] = parameters_default[parameter_name]
    return parameters_used



def load_json_as_dict(path_json:str)->dict:
    """Load a json file as a dictionary.

    Parameters
    ----------
    path_json : str
        Path to json file to be used.

    Returns
    -------
    d : dict
        Dictionary corresponding to given json file.
    """
    with open(path_json) as json_file:
        d = json.load(json_file)
    return d



def save_dict_as_json(d:dict, path_json:str):
    """Save a dictionary as a json file.

    Parameters
    ----------
    d : dict
        Dictonary to be used.
    path_json : str
        Path at which to save json file.
    """
    with open(path_json, 'w') as json_file:
        json.dump(d, json_file, sort_keys=True, indent=4, separators=(',', ': '))



def load_required_parameters(parameters_required:list, path_parameters_default:str="./muffin/parameters.json")->dict:
    """Given a list of names of parameters that are requried (e.g., for a simulation), 
    and dictionary of default parameters, return a dictionary containing values for all parameters required,
    using parsed argument as parameter values if they are given and default parameter values if they are not.

    Parameters
    ----------
    parameters_required : list
        List of strings that are names of parameters that are required for a function.
    path_parameters_default : str, optional
        Path to a json file containing a dictionary of default parameters, by default "./muffin/parameters.json"

    Returns
    -------
    parameters_used: dict
        Dictionary of parameters to be used, consisting of parameters that are given 
        and default values for those that are not.
    """
    parameters_default = load_json_as_dict(path_json=path_parameters_default)

    # Unpack any parameters given in parser
    parameters_given = parse_any_given_args()

    # Add default values for any other required parameters
    parameters_used = load_parameters_not_given(parameters_required=parameters_required, 
                                                parameters_given=parameters_given, 
                                                parameters_default=parameters_default)
    return parameters_used



def save_nparray_as_npy(path_results:str, a:numpy.ndarray, name:str):
    """Save a numpy array at a specified path with a given name.

    Parameters
    ----------
    path_results : str
        Path at which to save array.
    a : numpy.ndarray
        Array to be saved.
    name : str
        Name under which to save the array.
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