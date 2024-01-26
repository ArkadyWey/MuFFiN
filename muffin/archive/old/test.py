#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy 
import scipy
import matplotlib.pyplot as plt

import casadi

"""
"""

def ode(x,z):
    """
    """
    ic0 = 0
    ic1 = 1
    ic2 = 2

    iu = 0

    psi = 1    
    phi = 1
    u   = z[iu]
    dx  = 0.1

    result = casadi.SX(3,1)

    dc01 = x[ic1]-x[ic0]
    dc12 = x[ic2]-x[ic1]

    result[ic0] = 0
    result[ic1] = -(u/phi)*(dc01/dx)-psi*x[ic1]
    result[ic2] = -(u/phi)*(dc12/dx)-psi*x[ic2]

    return result


def alg(x,z):
    """
    """
    iu = 0
    u=z[iu]

    result = casadi.SX(1,1)

    result[iu]  = u - 1

    return result

# set up casadi problem
x = casadi.SX.sym("x", (3, 1))
z = casadi.SX.sym("z", (1, 1))

problem = {"x": x, 
           "ode": ode(x, z), 
           "z": z, 
           "alg": alg(x, z)} # dae consisting of ode variables, their eqaution, de variables, their equation 


# integrator (needs to be setup with solution times to return )
t_eval = numpy.linspace(0, 1, 101)

options =   {"grid": t_eval,
             "reltol": 1e-8,
             "abstol": 1e-8,
             "output_t0": True,
            }

integrator = casadi.integrator("F","idas", problem, options) # create function with name "F", arguments "idas", problem, and options=options

# solving 
x0  = [1,0,0]
z0  = [1] # works with bad initial condition
sol = integrator(x0=x0, z0=z0)

# plotting
t = t_eval
y = numpy.concatenate([sol["xf"].full(), sol["zf"].full()])

c0 = y[0,:]
c1 = y[1,:]
c2 = y[2,:]
u  = y[3,:]

plt.plot(t,c0)
plt.plot(t,c1)
plt.plot(t,c2)
plt.plot(t,u)
# plt.show()

#for i in range(len(Vus)):
#   # solve
#   x0  = [0, 0, 1, 0, 1, Vus[i], Vls[i], 1]
#   z0  = [1, 0, 0, 0] # bad initial condition
#   sol = integrator(x0=x0, z0=z0)
#   # plotting
#   t = t_eval
#   y = numpy.concatenate([sol["xf"].full(), sol["zf"].full()])
#   C0 = y[0,:]
#   C1 = y[1,:] 
#   Cin = y[2,:]
#   Cou = y[3,:]
#   Vin0 = y[4,:]
#   Vu = y[5,:]
#   Vl = y[6,:]
#   V1ou = y[7,:]
#   p0 = y[8,:]
#   p1 = y[9,:]
#   pin = y[10,:]
#   pou = y[11,:]
#   Qin0 = (Vin0**2)*(pin - p0)
#   Q1ou = (V1ou**2)*(p1 - pou)
#   Qu   = (Vu**2)*(p0 - p1)
#   Ql   = (Vl**2)*(p0 - p1)
#   T = numpy.zeros_like(t)
#   for it in range(len(t)):
#       T_it = numpy.sum(Qin0[0:it+1])*(t[1]-t[0])
#       T[it] = T_it
#   #print(T[-1])
#   print(T[0])
#   #print(Ql[0]+Qu[0])
#   #plt.plot(t, Qin0)
#   #plt.plot(t, Q1ou)
#   #plt.plot(t, Qu + Ql)
#   #plt.plot(t, p0-p1)
#   #plt.plot(t, Ql)
#    #plt.plot(t, Cin*Qin0)
#    #plt.plot(t, C1*Q1ou)
#    plt.plot(T, 1-(C1*Q1ou)/(Cin*Qin0))
#    #plt.plot(t, T)
#
#plt.show()
#   #plt.plot(t, C0, label=r"$C_0$")
#   #plt.plot(t, C1, label=r"$C_1$")
#   #plt.plot(t, Cin, label=r"$C_{in}$")
#   ##plt.plot(t, Cou, label=r"$C_{ou}$")
#   #plt.legend()
#   #plt.show()
#
#   #plt.plot(t, Vin0, label=r"$V_{in0}$")
#   #plt.plot(t, Vu,   label=r"$V_{u}$")
#   #plt.plot(t, Vl,   label=r"$V_{l}$")
#   #plt.plot(t, V1ou, label=r"$V_{1ou}$")
#   #plt.legend()
#   #plt.show()
#
#   #plt.plot(t, p0,  label=r"$p_{0}$")
#   #plt.plot(t, p1,  label=r"$p_{1}$")
#   #plt.plot(t, pin, label=r"$p_{in}$")
#   #plt.plot(t, pou, label=r"$p_{ou}$")
#   #plt.legend()
#   #plt.show()