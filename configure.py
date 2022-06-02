from inspect import Parameter
import numpy

import preprocess_2D
import initial_conditions_2D


class Parameters():
    """
    """ 
    def __init__(self):
        """
        """      
        self.max_ref_dist = 1
        self.num_dims     = 2
        self.num_concs    = 11
        self.num_nodes    = 1

        self.alpha        = 1.0
        self.v            = 1.0#2.0 # Sum of volumes of nodes in cell
        #self.phi          = 0.5 # TODO: Define this properly

        self.l1           = 1.0
        self.l2           = 1.0

        self.mean = 0.5 
        self.sd = 0.3





def main(Parameters):

    # Parameters 
    # -----
    max_ref_dist = Parameters.max_ref_dist
    num_dims     = Parameters.num_dims
    num_concs    = Parameters.num_concs
    num_nodes    = Parameters.num_nodes
    alpha        = Parameters.alpha
    v            = Parameters.v
    #phi         = Parameters.phi 
    l1           = Parameters.l1
    l2           = Parameters.l2
    mean         = Parameters.mean 
    sd           = Parameters.sd


    # Secondary configure 
    # -----
    leng_1          = numpy.array([l1,l2])
    conc_max_disc_1 = numpy.linspace(0,1,num_concs)
    refs_2 = preprocess_2D.get_reference(max_ref_dist=max_ref_dist,
                                         num_dims=num_dims)



    # Initial conditions: conductance and adhesivity 
    # -----
    num_refs = len(refs_2[:,0])

    adhe_init_4 = numpy.zeros(shape=(num_nodes, num_nodes, num_refs, num_refs)) 

    #cond_init_4 = initial_conditions_2D.grid_prescribed(num_nodes=num_nodes, num_refs=num_refs)
    cond_init_4 = initial_conditions_2D.grid_log_normal(num_nodes=num_nodes, 
                                                        num_refs=num_refs, 
                                                        mean=mean,
                                                        sd=sd)


    return (conc_max_disc_1, cond_init_4, adhe_init_4, alpha, refs_2, leng_1, v)

if __name__ == "__main__":

    conc_max_disc_1, cond_init_4, adhe_init_4, alpha, refs_2, leng_1, v = main(Parameters=Parameters())
