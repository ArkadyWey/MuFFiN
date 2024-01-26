import numpy
import inspect
import types

# Define different initial condition distributions 
# -----

def delta(mu:float=0.5)->float:
    """Dirac-delta distribution sampler.

    Parameters
    ----------
    mu : float
        Parameter of the Dirac-delta distribution, by default 0.5.

    Returns
    -------
    sample : float
        A sample value of the distribution.
    """
    sample = mu
    return sample
    

def lognormal(mu:float=-0.045, sigma:float=0.3)->float:
    """Lognormal distribution sampler.

    Parameters
    ----------
    mu : float, optional
        Mean of the normal distribution corresponding to the log-normal conductance/adherence 
        distribution, by default -0.045.
    sigma : float, optional
        Standard deviation of the normal distribution corresponding to the log-normal conductance/adherence 
        distribution, by default 0.3.

    Returns
    -------
    sample : float
        A sample value of the distribution.
    """
    sample = numpy.random.lognormal(mean=mu, sigma=sigma)
    return sample


# Utils
# -----
def get_functions():
    functions_1 = [function for function in globals().values() if type(function) == types.FunctionType]
    return functions_1

def map_function_name_to_args():
    functions_1 = get_functions() # local functions list
    name_to_args = {func.__name__: inspect.getfullargspec(func).args for func in functions_1}
    return name_to_args

def map_function_name_to_func():
    functions_1 = get_functions() # local functions list
    name_to_func = {func.__name__: func for func in functions_1}
    return name_to_func

def get_sample(**dist):
    name_to_args = map_function_name_to_args()
    name_to_func = map_function_name_to_func()
    
    if "name" in dist.keys():
        func_name = dist.pop("name")
    else: 
        raise Exception("Distribution dictionary {} is missing the key 'name'.".format(dist))
    
    if func_name not in name_to_args.keys():
        raise Exception("{} is not an implemented distribution.".format(func_name))
    else :
        # Execute function with parameters 
        func = name_to_func[func_name]
        
        # If kwargs match required arguments then use them
        sample = func(**dist)
        return sample
    

if __name__ == "__main__": 

    sample = get_sample(dist="lognormal", mu=0.5, sigma=0.3)
    print(sample)




