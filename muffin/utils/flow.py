import scipy.interpolate as interpolate 

def get_new_interpolated_point(table_x,table_y,new_x_values_1):
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
    """_
    #if type_clog == "deposit":
    interpolated_function = interpolate.splrep(x=table_x,y=table_y,k=3)
    new_y_values_1 = interpolate.splev(x=new_x_values_1, tck=interpolated_function)
    # elif type_clog == "block":
    #     step_fun = interpolate.interp1d(table_x, table_y, kind='next') 
    #     #print("new_x_value:\n{}".format(new_x_value))
    #     new_y_value = step_fun(new_x_value)
    # else: 
    #     raise Exception("type_clog must be either 'block' or 'deposit'.")
    return new_y_values_1