from inspect import Parameter
import numpy
import json
import math

import preprocess_2D
import initial_conditions_2D


class Configure():
    """
    """ 
    def __init__(self, num_nodes: int, 
                       l1: float, 
                       l2: float):
        """
        """      

        # Get class parameters 
        # -----
        self.num_nodes    = num_nodes
        self.l1           = l1
        self.l2           = l2
        
        # Get input parameters from parameters dictionary or class parameters
        # -----
        file = open("parameters.json", "r")
        parameters = json.load(file)
        
        self.max_ref_dist   = parameters["max_ref_dist"]
        self.num_dims       = parameters["num_dims"]
        self.num_concs      = parameters["num_concs"]
        self.v              = parameters["v"]    # 2.0 # Sum of volumes of nodes in cell
        self.mu             = parameters["mu"] 
        self.sigma          = parameters["sigma"]
        self.initialisation = parameters["initialisation"]


        # Do secondary configuration 
        # -----
        self.leng_1          = numpy.array([self.l1, self.l2])
        self.conc_max_disc_1 = numpy.linspace(0, 1.0, self.num_concs)
        self.refs_2          = preprocess_2D.get_reference(max_ref_dist=self.max_ref_dist,
                                                           num_dims=self.num_dims)
        self.phi             = self.v/(numpy.prod(self.leng_1))


        # Get initial conditions: conductance and adhesivity 
        # -----
        self.num_refs = len(self.refs_2[:,0])

        self.adhe_init_4 = numpy.zeros(shape=(self.num_nodes, self.num_nodes, self.num_refs, self.num_refs)) 

        self.cond_init_4 = self.get_initial_conductance()

        # Get params
        # -----
        self.mean = self.get_mean()
        self.median = self.get_median()
        
        self.alpha = self.get_alpha()

    def get_mean(self):
        """
        Get mean of resulting log-normal distribution.
        """
        mean = numpy.exp(self.mu+(self.sigma**2)/2)
        return mean

    def get_median(self):
        """
        Get mean of resulting log-normal distribution.
        """
        median = numpy.exp(self.mu)
        return median

    def get_pdf(self,x):
        """
        """
        pdf = (numpy.exp(-(numpy.log(x) - self.mu)**2 / (2 * self.sigma**2))  / (x * self.sigma * numpy.sqrt(2 * numpy.pi))) 
        return pdf

    def get_cdf(self,x):
        """
        """
        cdf = 0.5*(1 + math.erf( (numpy.log(x) - self.mu)/(self.sigma*numpy.sqrt(2))  ))
        return cdf

    def get_alpha(self):
        """
        Given the conductance distribution's mu and sigma variables, 
        get alpha. 
        At the moment, we calculate alpha such that the incominig concentration, 
        which is 1, blocks an edge with 50% chance. 
        """
        # Parameters 
        # -----------
        if self.initialisation == "4-reg_prescribed":
            alpha = 1.0/self.mean
        elif self.initialisation == "4-reg":
            alpha = 1.0/self.mean
        elif self.initialisation == "6-reg":
            alpha = (1.0/self.mean)*(numpy.sqrt(2.0)/numpy.sqrt(numpy.sqrt(3.0)))
        else: 
            raise Exception("Haven't checked what correct alpha is for this initialisation is yet. Check scale factor in cell.")

        return alpha
    def get_initial_conductance(self):
        """
        The initial conductance depends on the parameter 
        initialisation, which is prescribed in the parameters 
        dictionary.
        """
        if self.initialisation == "4-reg_prescribed":
            cond_init_4 = initial_conditions_2D.four_reg_prescribed(num_nodes=self.num_nodes,
                                                                    num_refs=self.num_refs)
        elif self.initialisation == "4-reg":
            cond_init_4 = initial_conditions_2D.four_reg(num_nodes=self.num_nodes, 
                                                         num_refs=self.num_refs, 
                                                         mu=self.mu,
                                                         sigma=self.sigma)
        elif self.initialisation == "6-ireg":
            cond_init_4 = initial_conditions_2D.six_ireg(num_nodes=self.num_nodes,
                                                         num_refs=self.num_refs)

        elif self.initialisation == "6-reg":
            cond_init_4 = initial_conditions_2D.six_reg(num_nodes=self.num_nodes, 
                                                        num_refs=self.num_refs, 
                                                        mu=self.mu, 
                                                        sigma=self.sigma)

        else: 
            raise Exception("""initialisation must be: 4-reg_prescribed or \
                               4-reg or 6-ireg or 6-reg.""")

        return cond_init_4



if __name__ == "__main__":

    num_nodes = 1


    conf = Configure(num_nodes=num_nodes)
