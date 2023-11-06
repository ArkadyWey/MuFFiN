import numpy

def ones(num_samples:int):
    """
    """
    return numpy.ones(num_samples)
    
def lognormal(num_samples:int, mu:float, sigma:float):
    """
    """
    return numpy.random.lognormal(mean=mu, sigma=sigma, size=num_samples)
