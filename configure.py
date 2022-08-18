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
                       initialisation: str,
                       sigma: float):
        """
        """      

        # Get class parameters 
        # -----
        self.num_nodes      = num_nodes
        self.initialisation = initialisation
        self.sigma          = sigma

        # Get input parameters from parameters dictionary or class parameters
        # -----
        file = open("parameters.json", "r")
        parameters = json.load(file)
        
        self.max_ref_dist   = parameters["max_ref_dist"]
        self.num_dims       = parameters["num_dims"]
        self.num_concs      = parameters["num_concs"]
        self.v              = parameters["v"]    # 2.0 # Sum of volumes of nodes in cell
        self.mu             = parameters["mu"] 


        # Do secondary configuration 
        # -----
        self.l1, self.l2    = self.get_lengths()        
        self.leng_1          = numpy.array([self.l1, self.l2])
        self.conc_max_disc_1 = numpy.linspace(0, 1.0, self.num_concs)
        self.refs_2          = preprocess_2D.get_reference(max_ref_dist=self.max_ref_dist,
                                                           num_dims=self.num_dims)
        self.phi             = self.v/(numpy.prod(self.leng_1))


        # Get params
        # -----
        self.mean = self.get_mean()
        self.median = self.get_median()
        
        self.scaled_mean = self.get_scaled_mean()
        self.alpha = self.get_alpha()

        # Get initial conditions: conductance and adhesivity 
        # -----
        self.num_refs = len(self.refs_2[:,0])

        self.adhe_init_4 = numpy.zeros(shape=(self.num_nodes, self.num_nodes, self.num_refs, self.num_refs)) 

        self.cond_init_4 = self.get_initial_conductance()

    def get_lengths(self):
        """
        The length of the cell depends on the initialisation and the 
        number of nodes in the cell, because of scalings.
        """
        num_nodes = self.num_nodes
        initialisation = self.initialisation

        if initialisation == "4-reg":
            n = int(numpy.sqrt(num_nodes))
            l1 = n*1.0
            l2 = n*1.0
        elif initialisation == "6-reg":
            n  = int(numpy.sqrt(num_nodes/2))    
            #l1 = n*1.0
            #l2 = n*numpy.sqrt(3.0)
            scale_factor = numpy.sqrt(2.0)/numpy.sqrt(numpy.sqrt(3.0))
            l1 = n*scale_factor
            l2 = n*numpy.sqrt(3.0)*scale_factor
        elif initialisation == "6-ireg":
            n = int(numpy.sqrt(num_nodes))
            l1 = n*1.0
            l2 = n*1.0
            #n  = int(numpy.sqrt(num_nodes/2))    
            #scale_factor = numpy.sqrt(2.0)/numpy.sqrt(numpy.sqrt(3.0))
            #l1 = n*scale_factor
            #l2 = n*numpy.sqrt(3.0)*scale_factor
        else: 
            raise Exception("initialisation must be '4-reg', '6-reg', or '6-ireg'.")

        return (l1, l2)

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

    def get_scaled_mean(self):
        """
        The mean above is not the mean unless the structure is 4-reg, 
        since otherwise the conductances are scaled for a fair test. 
        Here we scale the mean by the correct scale factor.
        """
        if self.initialisation == "4-reg_prescribed":
            scaled_mean = self.mean
        elif self.initialisation == "4-reg":
            scaled_mean = self.mean
        elif self.initialisation == "6-reg":
            # Scale factor is length of edge
            scale_factor = numpy.sqrt(2.0)/numpy.sqrt(numpy.sqrt(3.0))
            scaled_mean = self.mean/scale_factor
        elif self.initialisation == "6-ireg":
            #scale_factor = 2.0/self.l1#self.l1/2.0 # edge length is uniform so average is half
            #scale_factor = numpy.sqrt(numpy.sqrt(3.0))/numpy.sqrt(2.0)
            # Scale factor is average length of edge
            # See https://math.stackexchange.com/questions/208666/average-distance-between-random-points-in-a-rectangle
            
            lw = 3*self.l1
            lh = 3*self.l2
            
            d = numpy.sqrt(lw**2+lh**2)
            t1 = (lw**3)/(lh**2) + (lh**3)/(lw**2)
            t2 = d*(3.0 - (lw**2)/(lh**2) - (lh**2)/(lw**2) )
            t3 = (5.0/2.0)*( (lh**2/lw)*numpy.log((lw + d)/self.l2) + (lw**2/lh)*numpy.log((lh + d)/lw)  )
            scale_factor = (1.0/15.0)*(t1+t2+t3)
            #scale_factor = numpy.sqrt(2.0)/numpy.sqrt(numpy.sqrt(3.0))
            scale_factor = 1.0
            scaled_mean = self.mean/scale_factor # mean/length for length uniformly distributed
        else: 
            raise Exception("initialisation must be '4-reg', '6-reg', or '6-ireg'.")


        return scaled_mean

    def get_alpha(self):
        """
        Given the conductance distribution's mu and sigma variables, 
        get alpha. 
        At the moment, we calculate alpha such that the incominig concentration, 
        which is 1, blocks an edge with 50% chance. 
        """
        # Parameters 
        # -----------
        alpha = 1.0/self.scaled_mean
        #print("threshold:",1.0/alpha)

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
        elif self.initialisation == "6-reg":
            cond_init_4 = initial_conditions_2D.six_reg(num_nodes=self.num_nodes, 
                                                        num_refs=self.num_refs, 
                                                        mu=self.mu, 
                                                        sigma=self.sigma)
        elif self.initialisation == "6-ireg":
            cond_init_4 = initial_conditions_2D.six_ireg(num_nodes=self.num_nodes,
                                                         num_refs=self.num_refs,
                                                         mean=self.mean, 
                                                         leng_1=self.leng_1)

        else: 
            raise Exception("""initialisation must be: 4-reg_prescribed or \
                               4-reg or 6-ireg or 6-reg.""")

        return cond_init_4



if __name__ == "__main__":

    num_nodes = 1


    conf = Configure(num_nodes=num_nodes)
