from scipy import interpolate
from scipy import integrate
import numpy

# temporary
import sys


def get_new_interpolated_point(table_x,table_y,new_x_value):
    """
    Given a list of x values, and corresponding y values, and
    a new x value, approximate the corresponding function, 
    and use this function to return the new y value 
    corresponding to the new x value.

    Parameters 
    ----------
    - table_x: numpy.ndarray
        1-dimensional list of x values.
    - table_y: numpy.ndarray
        1-dimensional list of y values.
    - new_x_value: float
        New x value for which the corresponding y value is to be approximated.
    
    Returns
    -------
    - new_y_value: float
        Interpolated y value corresponding to new_x_value
    """
    interpolated_function = interpolate.splrep(x=table_x,y=table_y,k=3)
    new_y_value = interpolate.splev(x=new_x_value, tck=interpolated_function)
    return new_y_value



def get_permeability_and_deposition_at_time_and_position(conc_max_discs_1,perm_1,depo_1,conc_2,i_x,i_t):
    """
    Given a discrete list of concentrations, and the lists of corresponding permeability 
    and deposition-parameter values, return the permeability and deposition parameter 
    corresponding to a new concentration.

    Parameters
    ----------
    - conc_max_discs_1: numpy.ndarray 
        1-dimensional list of concentration values.
    - perm_1: numpy.ndarray
        1-dimensional list of permeability values corresponding to the concentration values.
    - depo_1: numpy.ndarray 
        1-dimensional list of deposition-parameter values corresponding to the concentration values.
    - conc_1: float
        1-dimensional list of concentrations, such that conc[i_x] = concentration at position[i_x].
    - i_x: int
        Index of the position at which the permeability and deposition parameter are desired.
    
    Returns
    -------
    - perm: float
        The permeability corresponding to the concentration conc,
    - depo: float
        The deposition parameter corresponding to the new concentration conc.
    """
    #conc = conc_2[i_x,i_t]

    # Get max of concentration 
    # -----
    conc_max_1 = numpy.amax(a=conc_2,axis=0)
    # conc_max_1[i_x] = the max concentration that position[i_x] has seen up to time[i_t].
    conc_max = conc_max_1[i_x]

    perm = get_new_interpolated_point(table_x=conc_max_discs_1,table_y=perm_1,new_x_value=conc_max)
    depo = get_new_interpolated_point(table_x=conc_max_discs_1,table_y=depo_1,new_x_value=conc_max)

    #conc = conc_2[i_x,i_t]
    #print("conc: \n{}".format(conc))
    #print("conc_max: \n{}".format(conc_max))
    #print("perm: \n{}".format(perm))
    return (perm, depo)


def get_velocity_at_time(perm_solver_1,posi_1,dx):
    """
    Given a list of positions and the permeabilities corresponding to these 
    positions, and a spatial step, return the velocity.

    Parameters
    ----------
    - perm_solver_1: numpy.ndarray 
        1-dimensional list of true permeabilities at the corresponsing positions.
    - posi_1: numpy.ndarray 
        1-dimensional list of positions at which the permeabilities have been calculated.
    - dx: float
        Spatial step. I.e., should be posi_1[1]-posi[0] if positions are equally spaced.
    
    Returns
    --------
    - velo: float 
        The Darcy velocity corresponding to the given permeabilities.
    """
    num_1 = numpy.ones(shape=perm_solver_1.shape)
    den_1 = perm_solver_1
    integrand_1 = num_1/den_1
    
    integral = integrate.simps(y=integrand_1,x=posi_1,dx=dx,even="avg")

    velo = 1/integral
    return velo


def get_pressure_gradient_at_time(perm_solver_1,velo_1,i_t):
    """
    Given the velocity at and the true permeabilities at a set of positions, 
    return the pressure gradient at the same set of positions, 
    by using Darcy's law such that dpdx[i_x] = - u/k[i_x].

    Parameters
    ------------
    - perm_solver_1: numpy.ndarray
        1-dimensional list of true permeabilities correspnding to a set of positions, 
        so that perm_solver_1[i_x] = permeability at position[i_x].
    - velo_1: float
        The velocity as a function of time, so that velo_1[i_t] = velocity at time[i_t].
        Note that velo_1[i_t] is the velocity corresponding to the set of permeabilities perm_solver_1
        above.
    
    Returns
    -------
    - dpdx_1: numpy.ndarray
        The pressure gradient as a function of position, so that dpdx_1[i_x]
        is the pressure gradient at position[i_x].
    """
    velo = velo_1[i_t]
    dpdx_1 = - velo*numpy.ones(shape=perm_solver_1.shape)/perm_solver_1
    return dpdx_1

def get_reaction_parameter_at_time(depo_solver_1,dpdx_1):
    """
    Given the deposition parameter at a set of positions, 
    and the pressure gradient at the same set of positions, 
    return the reaction parameter.

    Parameters 
    ----------
    - depo_solver_1: numpy.ndarray
        The deposition parameter at a set of positions, so that 
        depo_solver_1[i_x] = the deposition parameter at position[i_x].
    - dpdx_1: numpy.ndarray
        The pressure gradient as a function of position, so that dpdx_1[i_x]
        is the pressure gradient at position[i_x].

    Returns
    -------
    - psi_1: numpy.ndarray
        The reaction parameter at a set of positions, 
        so that psi_1[i_x] = reaction parameter psi at position[i_x] = j[i_x]*dpdx[i_x].
    """
    psi_1 = depo_solver_1*dpdx_1
    return psi_1


def get_concentration_at_time_and_position(conc_2,velo_1,psi_2,phi,conc_in,dt,dx,i_x,i_t):
    """
    A step of the advection-reaction equation. Given the concentration, velocity, reaction parameter, 
    porosity, and boundary condition, and the spatial and temporal time steps, and the position and time 
    index, return the concentration at this position at the current time index.

    If t=0, then concentration is the initial condition, which is already contained in 
    conc_2.
    For all other t, if x=0 then concentration is the value in the boundary condition, conc_in.
    For all other x, return a step of the advection reaction equation, by using the 
    previous concentration and other parameters, to find the current concentration.



    Parameters 
    -----------
    - conc_1: numpy.ndarray
        1-dimensional concentration as function of position, such that conc_1[i_x] = concentration at position[i_x].
    - velo_1: numpy.ndarray
        1-dimensional velocity as a function of time, such that velo_1[i_t] = velocity at time[i_t].
    - psi_1: numpy.ndarray
        1-dimensional reaction parameter as a function of position, such that psi_1[i_x] is the reaction parameter at
        position[i_x].
    - phi: float
        The constant porosity, which is the ratio of volume of nodes to volume of filter.
    -conc_in: float 
        The concentration at the inlet. This should be bounded by zero and one.
    - dt: float 
        The timestep.
    - dx: float
        The spatial step.
    - i_t: int 
        The time current time index.
    - i_x: int
        the current position index.

    Returns
    -------
    - conc_now: float 
        The future concentration at the current positions, such that conc_now = concentration at time[i_t+1] 
        and position[i_x].
    """

    # Parameters 
    # ----------
    if i_t==0: 
        conc = conc_2[i_x,i_t] # enforce initial condition

    else: 
    # Step 
    # -----
        if i_x == 0:
            conc = conc_in # enforce boundary condition
        
        else:
            conc_prev    = conc_2[i_x,i_t-1]
            conc_prev_m1 = conc_2[i_x-1,i_t-1]
            psi_prev     = psi_2[i_x,i_t-1]
            velo_prev    = velo_1[i_t-1] 
            
            conc = conc_prev - (velo_prev/phi)*(dt/dx)*(conc_prev-conc_prev_m1) - psi_prev*dt*conc_prev
            #print("conc_prev: \n{}".format(conc_prev))
            #print("reaction: \n{}".format(psi_prev))
            #if psi_prev*dt*conc_prev < 0:
            #    sys.exit()
    
    return conc