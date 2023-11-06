from turtle import shape
import numpy
import scipy 
from scipy import optimize
from scipy import sparse
import datetime
import matplotlib
from matplotlib import pyplot as plt
import os 

import muffin.flow as flow


begin_time = datetime.datetime.now()
print(datetime.datetime.now())


def main(time_1, posi_1, conc_max_disc_1, perm_prep_1, depo_prep_1, dt, dx, conc_in, phi):
    """
    """
    # Get temp parameters 
    # -----
    num_positions = len(posi_1)
    num_times = len(time_1)

    # Storage for solution
    # ---------------------
    conc_2 = numpy.zeros(shape=(num_positions,num_times)) 
    velo_1 = numpy.zeros(shape=(num_times))
    psi_2  = numpy.zeros(shape=(num_positions,num_times))
    perm_2 = numpy.zeros(shape=(num_positions,num_times))
    depo_2 = numpy.zeros(shape=(num_positions,num_times))
    dpdx_2 = numpy.zeros(shape=(num_positions,num_times))
    # conc_2[i_x,i_t] = concentraton at position[i_x] at time[i_t]
    # velo_1[i_t] = velocity at time[i_t]


    # Initial conditions
    # --------------------
    conc_2[:,0] = numpy.zeros(shape=num_positions)
    conc_2[0,0] = conc_in


    # Boundary conditions 
    # --------------------
    # This is enforced in the advection-reaction equation step

    #print("conc_2: \n{}".format(conc_2))

    for i_t in range(num_times):
    # predict values now using previous time step
        print("Calculating conc at time step {} of {}".format(i_t, num_times))
        # Get concentration at this time using conc and parameters from previous step
        # -----
        conc_1 = numpy.zeros(shape=num_positions)
        for i_x in range(num_positions): 
            conc = flow.get_concentration_at_time_and_position(conc_2=conc_2,
                                                               velo_1=velo_1,
                                                               psi_2=psi_2,
                                                               phi=phi,
                                                               conc_in=conc_in,
                                                               dt=dt,
                                                               dx=dx,
                                                               i_x=i_x,
                                                               i_t=i_t)

            conc_1[i_x] = conc
        #print("conc_1: \n{}".format(conc_1))

        conc_2[:,i_t] = conc_1


        # Get permeability and deposition at this time using current concentration just calculated
        # -----
        perm_1 = numpy.zeros(shape=num_positions)
        depo_1 = numpy.zeros(shape=num_positions)
        for i_x in range(num_positions):

            # Get permeability and deposition parameter at this time and all positions
            # -----
            perm, depo = flow.get_permeability_and_deposition_at_time_and_position(conc_max_disc_1=conc_max_disc_1,
                                                                                                 perm_prep_1=perm_prep_1,
                                                                                                 depo_prep_1=depo_prep_1,
                                                                                                 conc_2=conc_2,
                                                                                                 i_x=i_x,
                                                                                                 i_t=i_t)
            perm_1[i_x] = perm
            depo_1[i_x] = depo

        perm_2[:,i_t] = perm_1
        depo_2[:,i_t] = depo_1


        # Get velocity at this time 
        # -----
        velo = flow.get_velocity_at_time(perm_1=perm_1,posi_1=posi_1,dx=dx)
        velo_1[i_t] = velo


        # Get pressure gradient at this time (using Darcy: dpdx[i_x] = - u/k[i_x])
        # -----
        dpdx_1 = flow.get_pressure_gradient_at_time(perm_1=perm_1,
                                                    velo_1=velo_1,
                                                    i_t=i_t)
        dpdx_2[:,i_t] = dpdx_1


        # Get reaction parameter at this time
        # -----
        psi_1 = flow.get_reaction_parameter_at_time(depo_1=depo_1,
                                                    dpdx_1=dpdx_1)
        psi_2[:,i_t] = psi_1

    return (conc_2, velo_1, psi_2, perm_2, depo_2, dpdx_2)

if __name__ == "__main__":


    # Preprocess
    # ----------
    path_results_preprocess = os.path.join(".","results/results_preprocess_1D")

    conc_max_disc_1      = numpy.load(file=os.path.join(path_results_preprocess,"conc_max_disc_1.npy"), mmap_mode=None, allow_pickle=False, fix_imports=True, encoding='ASCII')
    perm_prep_1           = numpy.load(file=os.path.join(path_results_preprocess,"perm_prep_1.npy"), mmap_mode=None, allow_pickle=False, fix_imports=True, encoding='ASCII')
    depo_prep_1           = numpy.load(file=os.path.join(path_results_preprocess,"depo_prep_1.npy"), mmap_mode=None, allow_pickle=False, fix_imports=True, encoding='ASCII')

    # Parameters 
    # ----------
    num_times = 1001 # 1001
    time_1 = numpy.linspace(0,1,num_times)
    dt = time_1[1] - time_1[0]

    num_positions = 101 # 101
    posi_1 = numpy.linspace(0,1,num_positions)
    dx = posi_1[1]-posi_1[0]

    conc_in = 0.7 # 0.8

    phi = 1.0 # TODO: Define this properly


    (conc_2, velo_1, psi_2, perm_2, depo_2, dpdx_2) = main(time_1=time_1, 
                                                           posi_1=posi_1, 
                                                           conc_max_disc_1=conc_max_disc_1, 
                                                           perm_prep_1=perm_prep_1, 
                                                           depo_prep_1=depo_prep_1, 
                                                           dt=dt, 
                                                           dx=dx, 
                                                           conc_in=conc_in, 
                                                           phi=phi)



    # Save results 
    # ----- 
    path_results = os.path.join(".","results/results_flow_1D")
    if not os.path.exists(path_results):
        os.mkdir(path_results)

    numpy.save(file=os.path.join(path_results,"time_1.npy"), arr=time_1, allow_pickle=True, fix_imports=True) 
    numpy.save(file=os.path.join(path_results,"posi_1.npy"), arr=posi_1, allow_pickle=True, fix_imports=True)
    
    numpy.save(file=os.path.join(path_results,"conc_2.npy"), arr=conc_2, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"velo_1.npy"), arr=velo_1, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"psi_2.npy"), arr=psi_2, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"perm_2.npy"), arr=perm_2, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"depo_2.npy"), arr=depo_2, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"dpdx_2.npy"), arr=dpdx_2, allow_pickle=True, fix_imports=True)


print(datetime.datetime.now() - begin_time)