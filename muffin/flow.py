from scipy import interpolate
from scipy import integrate
import numpy


def get_new_interpolated_point(table_x,table_y,new_x_value,type_clog):
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
    if type_clog == "deposit":
        interpolated_function = interpolate.splrep(x=table_x,y=table_y,k=3)
        new_y_value = interpolate.splev(x=new_x_value, tck=interpolated_function)
        #print(new_x_value)
    elif type_clog == "block":
        step_fun = interpolate.interp1d(table_x, table_y, kind='next') 
        #print("new_x_value:\n{}".format(new_x_value))
        new_y_value = step_fun(new_x_value)
    else: 
        raise Exception("type_clog must be either 'block' or 'deposit'.")
    return new_y_value


def get_concentration_at_time_and_position(conc_2,velo_1,psi_2,phi,conc_in,dt,dx,i_t,i_x):
    """
    A step of the advection-reaction equation. 
    Uses values of the parameter arrays from the last or to the left to get the concentration value at the current time 
    and position.
    Given the concentration, velocity, reactivity, porosity, and boundary concentration-value, 
    and the temporal and spatial time steps, 
    and the position and time indices, 
    return the concentration at the time and position corresponding to this position and time index.

    if t=0:
        if x=0:
            conc = 1
        elif x>0:
            conc = 0
    elif t>0:
        if x=0:
            conc = 1
        elif x>0:
            conc[t,x] = func_of[t-1,x], func_of[t-1,x-1]...

    Parameters 
    -----------
    - conc_2: numpy.ndarray
        2-dimensional concentration as function of position and time, such that conc_2[i_x,i_t] = concentration at posi_1[i_x] and time_1[i_t].
    - velo_1: numpy.ndarray
        1-dimensional velocity as a function of time, such that velo_1[i_t] = velocity at time_1[i_t].
    - psi_2: numpy.ndarray
        2-dimensional reactivity as function of position and time, such that psi_2[i_x,i_t] = reactivity at posi_1[i_x] and time_1[i_t].
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
        The current position index.

    Returns
    -------
    - conc: float 
        The concentration at the current position and time, such that conc = concentration at time[i_t] 
        and position[i_x].
    """

    if i_t == 0: # initial time
        if i_x == 0: # boundary point
            conc = conc_in # enforce initial boundary condition
        elif i_x > 0: # inner points
            conc = 0.0 # enforce initial inner condition
        
    elif i_t > 0: # later times 
        if i_x == 0: # boundary point
            conc = conc_in # enfore later time boundary condition
        elif i_x > 0: # inner points
            conc_prev    = conc_2[i_x,i_t-1]
            conc_prev_m1 = conc_2[i_x-1,i_t-1]
            psi_prev     = psi_2[i_x,i_t-1]
            velo_prev    = velo_1[i_t-1] 
            
            conc = conc_prev - (dt/dx)*(velo_prev/phi)*(conc_prev-conc_prev_m1) - dt*(psi_prev/phi)*conc_prev
            
            #print("conc_prev: \n{}".format(conc_prev))
            #print("reaction: \n{}".format(psi_prev))
            #if psi_prev*dt*conc_prev < 0:
            #    sys.exit()
    
    return conc


def get_maximum_or_total_concentration_at_time_and_position(conc_2,dpdx_2,time_1,i_t,i_x,type_clog):
    """
    Get the maximum concentration at the current position up to and including the current time.
    Given the concentration at all positions and times, the current position, and the current time, 
    return the maximum concentration a the current position up to and including the current time.

    Parameters 
    -----------
    - conc_2: numpy.ndarray
        2-dimensional concentration as function of position and time, such that conc_2[i_x,i_t] = concentration at posi_1[i_x] and time_1[i_t].
    - dpdx_2: numpy.ndarray
        2-dimensional pressure gradient as function of position and time, such that dpdx_2[i_x,i_t] = pressure gradient at posi_1[i_x] and time_1[i_t].
    - i_t: int 
        The time current time index.
    - i_x: int
        The current position index.

    Returns
    -------
    - conc_max_or_tot: float 
        Scaler value that is the maximum concentration at position_1[i_x] over times up to and including time_1[i_t].
    """
    #print("i_x:\n{}".format(i_x))
    #print("i_t:\n{}".format(i_t))
    #print("conc_2[i_x,0:i_t+1]:\n{}".format(conc_2[i_x,0:i_t+1]))
    if type_clog == "block":
        conc_at_posi_1 = conc_2[i_x,0:i_t+1] # concentration at current position up to (and including) current time
        conc_max_or_tot = numpy.amax(a=conc_at_posi_1, axis=0)
    elif type_clog == "deposit":
        conc_at_posi_1 = conc_2[i_x,0:i_t+1]
        dpdx_at_posi_1 = dpdx_2[i_x,0:i_t+1]
        integrand_1 = conc_at_posi_1*abs(dpdx_at_posi_1)
        dt = time_1[1]-time_1[0]
        conc_max_or_tot = integrate.simps(y=integrand_1,x=time_1[0:i_t+1],dx=dt,even="avg")
    return conc_max_or_tot


def get_permeability_and_deposition_at_time_and_position(conc_max_or_tot_1,perm_prep_1,depo_prep_1,conc_2,dpdx_2,time_1,i_t,i_x,type_clog):
    """
    Find the permeabiltiy and adhesivity at the current time and position.
    Given a discrete list of maximum concentrations, and the lists of corresponding permeability 
    and adhesivity values, find the maximum concentration value at the current position at times up to and inclusing the current time, 
    and return the permeability and deposition parameter 
    corresponding to a new maximum concentration.

    Parameters
    ----------
    - conc_max_or_tot_1: numpy.ndarray 
        1-dimensional list of pre-determined maximum concentration values. For example, an evenly distributed list 
        of numbers between 0 and 1.
    - perm_prep_1: numpy.ndarray
        1-dimensional list of permeability values corresponding to the maximum concentration values.
    - depo_prep_1: numpy.ndarray 
        1-dimensional list of adhesivity values corresponding to the maximum concentration values.
    - conc_2: numpy.ndarray
        2-dimensional concentration as function of position and time, such that conc_2[i_x,i_t] = concentration at posi_1[i_x] and time_1[i_t].
    - i_t: int 
        The time current time index.
    - i_x: int
        The current position index.
    
    Returns
    -------
    - perm: float
        The permeability corresponding to the maximum concentration conc_max_or_tot at position posi_1[i_x] and time_1[i_t].
    - depo: float
        The adhesivity corresponding to the maximum concentration conc_max_or_tot at position posi_1[i_x] and time_1[i_t].
    """

    # Find max concentration at current position up to and including current time 
    # -----
    conc_max_or_tot = get_maximum_or_total_concentration_at_time_and_position(conc_2,dpdx_2,time_1,i_t,i_x,type_clog)
    #print("conc_max_or_tot:\n{}".format(conc_max_or_tot))

    # Get permeability and adhesivity corresponding to new max concentration
    # -----
    perm = get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=perm_prep_1,new_x_value=conc_max_or_tot,type_clog=type_clog)
    depo = get_new_interpolated_point(table_x=conc_max_or_tot_1,table_y=depo_prep_1,new_x_value=conc_max_or_tot,type_clog=type_clog)
    #print(depo)
    return (perm, depo)


def get_velocity_at_time(perm_2,posi_1,i_t,dx):
    """
    Given a list of positions and the permeabilities corresponding to these 
    positions, and a spatial step, and a time point, return the velocity at this time point.

    Parameters
    ----------
    - perm_2: numpy.ndarray
        2-dimensional list of permeabilities, so that perm_2[i_x,i_t] = the permeability corresponding 
        to the maximum concentration conc_max_or_tot at posi_1[i_x] and time_1[i_t].
    - posi_1: numpy.ndarray 
        1-dimensional list of positions at which the permeabilities have been calculated.
    - i_t: int 
        The time current time index.
    - dx: float
        Spatial step. I.e., should be posi_1[1]-posi[0] if positions are equally spaced.
    
    Returns
    --------
    - velo: float 
        The Darcy velocity corresponding to the permeability at time_1[i_t].
    """

    # Parameters
    # ----------
    num_posi  = len(posi_1)

    # Define intergrand
    # -----
    num_1 = numpy.ones(shape=num_posi)
    den_1 = perm_2[:,i_t]
    integrand_1 = num_1/den_1
    
    integral = integrate.simps(y=integrand_1,x=posi_1,dx=dx,even="avg")
    # TODO: check if result depends on even=...

    velo = 1.0/integral
    return velo


def get_pressure_gradient_at_time_and_position(perm_2,velo_1,i_t,i_x):
    """
    Given the velocity and the permeability, and a time and spatial point, 
    return the pressure gradient at this position and time, 
    by using Darcy's law such that dpdx = - u/k.

    Parameters
    ------------
    - perm_2: numpy.ndarray
        2-dimensional list of permeabilities, so that perm_2[i_x,i_t] = the permeability corresponding 
        to the maximum concentration conc_max_or_tot at posi_1[i_x] and time_1[i_t].
    - velo_1: float 
        The Darcy velocity as a function of time, so that velo_1[i_t] = velocity at time[i_t].
        Note that velo_1[i_t] is the velocity corresponding to the set of permeabilities perm_2
        above.
    
    Returns
    -------
    - dpdx: float
        The pressure gradient at time time[i_t] and position posi_1[i_x].
    """
    perm = perm_2[i_x,i_t]
    velo = velo_1[i_t]
    dpdx = - velo/perm
    return dpdx


def get_reactivity_at_time_and_position(depo_2,dpdx_2,i_t,i_x):
    """
    Given the adhesivity at a set of positions and times, 
    and the pressure gradient at the same set of positions and times,
    and a particular position point and time point, 
    return the reaction parameter at this time and position.

    Parameters 
    ----------
    - depo_2: numpy.ndarray
        The adhesivity at a set of positions and times, so that 
        depo_1[i_x,i_t] = the adhesivity parameter j at position posi_1[i_x] and time time_1[i_t].
    - dpdx_2: numpy.ndarray
        The pressure gradient at a set of positions and times, so that 
        dpdx_1[i_x,i_t] = the pressure gradient dpdx at position posi_1[i_x] and time time_1[i_t].

    Returns
    -------
    - psi: float
        The reactivity at position posi_1[i_x] at time time_1[i_t].
    """
    depo = depo_2[i_x,i_t]
    dpdx = dpdx_2[i_x,i_t]
    psi = -depo*dpdx

    #depo_prev = depo_2[i_x,i_t-1]
    #psi = -(depo-depo_prev)*dpdx
    return psi


def step(conc_2,conc_max_2,perm_2,depo_2,velo_1,dpdx_2,psi_2,
         conc_max_or_tot_1,perm_prep_1,depo_prep_1,
         posi_1,
         phi,conc_in,
         dt,dx,
         i_x,i_t):
    """
    Given a position point and a time point, 
    return the solution at this position and time 
    by taking a step of the numerical scheme.
    """
    conc_2[i_x,i_t] = get_concentration_at_time_and_position(conc_2=conc_2,
                                                             velo_1=velo_1,
                                                             psi_2=psi_2,
                                                             phi=phi,
                                                             conc_in=conc_in,
                                                             dt=dt,
                                                             dx=dx,
                                                             i_t=i_t,
                                                             i_x=i_x)

    conc_max_2[i_x,i_t] = get_maximum_or_total_concentration_at_time_and_position(conc_2,dpdx_2,time_1,i_t,i_x,type_clog)

    perm_2[i_x,i_t], depo_2[i_x,i_t] = get_permeability_and_deposition_at_time_and_position(conc_max_or_tot_1=conc_max_or_tot_1,
                                                                                            perm_prep_1=perm_prep_1,
                                                                                            depo_prep_1=depo_prep_1,
                                                                                            conc_2=conc_2,
                                                                                            i_t=i_t,
                                                                                            i_x=i_x)
    
    velo_1[i_t] = get_velocity_at_time(perm_2=perm_2,posi_1=posi_1,i_t=i_t,dx=dx)

    dpdx_2[i_x,i_t] = get_pressure_gradient_at_time_and_position(perm_2=perm_2,velo_1=velo_1,i_t=i_t,i_x=i_x)

    psi_2[i_x,i_t] = get_reactivity_at_time_and_position(depo_2=depo_2,dpdx_2=dpdx_2,i_t=i_t,i_x=i_x)

    return (conc_2,conc_max_2,perm_2,depo_2,velo_1,dpdx_2,psi_2)