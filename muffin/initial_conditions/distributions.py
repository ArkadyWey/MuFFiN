import numpy
import inspect
import types

# Define different initial condition distributions 
# -----

def delta(mu:float):
    """
    """
    sample = mu
    return sample
    
def lognormal(mu:float, sigma:float):
    """
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

def get_sample(dist:str, **kwargs):
    name_to_args = map_function_name_to_args()
    name_to_func = map_function_name_to_func()
    
    if dist not in name_to_args.keys():
        raise Exception("{} is not an implemented distribution.".format(dist))
    else :
        # Execute function with parameters 
        func = name_to_func[dist]
        sample = func(**kwargs)
        return sample
    

if __name__ == "__main__": 

    sample = get_sample(dist="lognormal", mu=0.5, sigma=0.3)
    print(sample)




