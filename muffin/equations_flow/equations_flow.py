import numpy

import muffin.parameters.parameters as parameters

class Base():
    """_summary_
    """
    def __init__(self, parameters:parameters.Parameters):
        """_summary_
        """

    # Attributes
    # -----        
        self.parameters = parameters
    

    # Methods
    # -----        
    def get_concentration_problem(self, conc_1, psi_1, velo, phi, diff_posi):

        rhs_1 = numpy.zeros(shape=(X))
        for i_x in range(X):
            
            if i_x==0:
                rhs = 0.0 # boundary condition
            elif i_x!=0:
                rhs = (1/diff_posi)*(velo/phi)*(conc_1[i_x]-conc_1[i_x-1]) - (psi_1[i_x]/phi)*conc_1[i_x]
            
            rhs_1[i_x] = rhs
        
        return rhs_1

    def step_concentration_problem(self, conc_1, rhs_1, diff_time):
        conc_new_1 = conc_1 - diff_time*rhs_1
        return conc_new_1




