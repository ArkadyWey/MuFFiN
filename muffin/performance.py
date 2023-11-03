import scipy
from scipy import integrate 
import numpy

def get_lifetime(velo_1,time_1,tau):
    """
    """
    lamb = scipy.integrate.simpson(y=velo_1[0:tau+1], 
                                   x=time_1[0:tau+1], 
                                   dx=time_1[1]-time_1[0], 
                                   axis=-1, 
                                   even="avg")
    return lamb

def get_throughput(velo_1,time_1,t):
    """
    """
    thet = scipy.integrate.trapezoid(y=velo_1[0:t+1],
                                     x=time_1[0:t+1],
                                     dx=time_1[1]-time_1[0],
                                     axis=0)
    
    return thet

def get_efficiency(conc_2):
    """
    """
    eta_1 = conc_2[0,:] - conc_2[-1,:]
    return eta_1

def get_termination(velo_1,time_1,mu):
    """
    """
    indx_crit_1 = [i for i in range(len(velo_1)) if velo_1[i]<mu]
    indx_crit = indx_crit_1[0]
    
    tau = time_1[indx_crit]
    return int(tau)


def get_pressure(dpdx_2,posi_1,tau):
    """
    """
    pres_2 = numpy.ones_like(dpdx_2)
    for i_t in numpy.linspace(0,tau,tau+1,endpoint=True,dtype=int):
        dpdx_1 = dpdx_2[:,i_t]
        for i_x in numpy.linspace(1,100,100,endpoint=True,dtype=int):
            pres = integrate.trapezoid(y=dpdx_1[0:i_x],x=posi_1[0:i_x],dx=posi_1[1]-posi_1[0])
            pres_2[i_x,i_t] = pres
    return pres_2