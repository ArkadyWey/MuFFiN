import numpy
import scipy.integrate as integrate

import muffin.parameters.parameters as parameters
import muffin.utils.flow as flow


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

        conc_shft_1 = numpy.roll(a=conc_1, shift=1, axis=0) # get conc_1[i_x-1]
        rhs_1 = -(1.0/diff_posi)*(velo/phi)*(conc_1-conc_shft_1) - (psi_1/phi)*conc_1
        rhs_1[0] = 0.0 # boundary condition 
        return rhs_1

    def step_concentration_problem(self, conc_1, rhs_1, diff_time):
        conc_new_1 = conc_1 + diff_time*rhs_1
        return conc_new_1


    def get_time_like(self, conc_2, dpdx_2, time_1, diff_time):
        # conc_2 = conc_2[0:i_t,:]
        # dpdx_2 = dpdx_2[0:i_t,:]
        # time_1 = time_1[0:i_t]
        
        # Only take arrys up to i_t
        integrand_2 = conc_2*abs(dpdx_2)
        tlik_1 = integrate.simps(y=integrand_2, x=time_1, axis=0, dx=diff_time, even="avg") # tlik_1[i_x]
        return tlik_1

    
    def get_permeability_and_adhesivity(self, tlik_prep_1, perm_prep_1, depo_prep_1, tlik_1):
        perm_1 = flow.get_new_interpolated_point(table_x=tlik_prep_1, table_y=perm_prep_1, new_x_values_1=tlik_1)
        depo_1 = flow.get_new_interpolated_point(table_x=tlik_prep_1, table_y=depo_prep_1, new_x_values_1=tlik_1)
        return (perm_1,depo_1) # perm[i_x]


    def get_velocity(self, perm_1, posi_1, diff_posi):
        # perm_1 = perm_2[i_t,:]
        # Define intergrand
        # -----
        den_1 = perm_1
        num_1 = numpy.ones_like(a=den_1)

        integrand_1 = num_1/den_1

        integral = integrate.simps(y=integrand_1, x=posi_1, axis=0, dx=diff_posi, even="avg")

        velo = 1.0/integral
        return velo


    def get_pressure_gradient(self,perm_1,velo):
        # perm_1 = perm_2[i_t,:]
        # velo = velo_1[i_t]
        velo_1 = velo*numpy.ones_like(a=perm_1)
        dpdx_1 = -velo_1/perm_1
        return dpdx_1 #dpdx_1[i_x]


    def get_reactivity(self, depo_1, dpdx_1):
        psi_1 = -depo_1*dpdx_1
        return psi_1

