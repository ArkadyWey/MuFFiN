import numpy
import datetime
import os 

import flow

begin_time = datetime.datetime.now()
print(datetime.datetime.now())


def main(conc_max_or_tot_1,perm_prep_1,depo_prep_1,
         posi_1,time_1,
         phi,conc_in,
         dt,dx,
         type_clog):
    """
    """
    # Parameters 
    # ------
    num_positions = len(posi_1)
    num_times     = len(time_1)

    # Storage for solution
    # ---------------------
    conc_2     = numpy.zeros(shape=(num_positions,num_times))
    conc_max_or_tot_2 = numpy.zeros(shape=(num_positions,num_times))
    perm_2     = numpy.zeros(shape=(num_positions,num_times))
    depo_2     = numpy.zeros(shape=(num_positions,num_times))
    depo_pre_2 = numpy.zeros(shape=(num_positions,num_times))
    velo_1     = numpy.zeros(shape=(num_times))
    dpdx_2     = numpy.zeros(shape=(num_positions,num_times))
    psi_2      = numpy.zeros(shape=(num_positions,num_times))

    # Initial and boundary conditions are enforced inside solver

    for i_t in range(num_times):
        print("Calculating solution at time step {} of {}".format(i_t, num_times-1))
        for i_x in range(num_positions): 
            #conc_2,conc_max_or_tot_2,perm_2,depo_2,velo_1,dpdx_2,psi_2 = flow.step(conc_2=conc_2,conc_max_or_tot_2=conc_max_or_tot_2,perm_2=perm_2,depo_2=depo_2,velo_1=velo_1,dpdx_2=dpdx_2,psi_2=psi_2,
            #                                                                conc_max_or_tot_1=conc_max_or_tot_1,perm_prep_1=perm_prep_1,depo_prep_1=depo_prep_1,
            #                                                                posi_1=posi_1,
            #                                                                phi=phi,conc_in=conc_in,
            #                                                                dt=dt,dx=dx,
            #                                                                i_x=i_x,i_t=i_t)

            conc_2[i_x,i_t] = flow.get_concentration_at_time_and_position(conc_2=conc_2,
                                                                          velo_1=velo_1,
                                                                          psi_2=psi_2,
                                                                          phi=phi,
                                                                          conc_in=conc_in,
                                                                          dt=dt,
                                                                          dx=dx,
                                                                          i_t=i_t,
                                                                          i_x=i_x)

            conc_max_or_tot_2[i_x,i_t] = flow.get_maximum_or_total_concentration_at_time_and_position(conc_2=conc_2,
                                                                                                      dpdx_2=dpdx_2,
                                                                                                      time_1=time_1,
                                                                                                      i_t=i_t,
                                                                                                      i_x=i_x,
                                                                                                      type_clog=type_clog)

            # replace depo_2[i_x,i_t] with depo_pre_2[i_x,i_t] if blocking
            perm_2[i_x,i_t], depo_2[i_x,i_t] = flow.get_permeability_and_deposition_at_time_and_position(conc_max_or_tot_1=conc_max_or_tot_1,
                                                                                                         perm_prep_1=perm_prep_1,
                                                                                                         depo_prep_1=depo_prep_1,
                                                                                                         conc_2=conc_2,
                                                                                                         dpdx_2=dpdx_2,
                                                                                                         time_1=time_1,
                                                                                                         i_t=i_t,
                                                                                                         i_x=i_x,
                                                                                                         type_clog=type_clog)
            if type_clog == "block":
                """
                If adhesivity value is not new, then this deposition value has already removed necessary
                particles and reaction should be turned off until next time it is new.
                """
                #for ii_t in range(i_t+1):
                if i_t != 0:
                    if depo_pre_2[i_x,i_t] <= depo_pre_2[i_x,i_t-1]:
                        depo_2[i_x,i_t] = 0
                    else:                   
                        depo_2[i_x,i_t] = depo_pre_2[i_x,i_t]                                                                   
            elif type_clog == "deposit":
                #print("depo")
                pass 
            else: 
                raise Exception("type_clog must be either 'block' or 'deposit'.")
            
        velo_1[i_t] = flow.get_velocity_at_time(perm_2=perm_2,posi_1=posi_1,i_t=i_t,dx=dx)

        for i_x in range(num_positions): 
            dpdx_2[i_x,i_t] = flow.get_pressure_gradient_at_time_and_position(perm_2=perm_2,velo_1=velo_1,i_t=i_t,i_x=i_x)

            psi_2[i_x,i_t] = flow.get_reactivity_at_time_and_position(depo_2=depo_2,dpdx_2=dpdx_2,i_t=i_t,i_x=i_x)
        
        #print("psi_2[:,i_t]:\n{}".format(psi_2[:,i_t])) 

    return (conc_2,conc_max_or_tot_2,perm_2,depo_2,velo_1,dpdx_2,psi_2)

if __name__ == "__main__":


    # Preprocess
    # ----------
    #path_results_preprocess = os.path.join(".","results/results_preprocess_2D") # thesis
    path_results_preprocess = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/results_preprocess") # paper


    conc_max_or_tot_1  = numpy.load(file=os.path.join(path_results_preprocess,"conc_max_or_tot_1.npy"), mmap_mode=None, allow_pickle=False, fix_imports=True, encoding='ASCII')
    perm_prep_3      = numpy.load(file=os.path.join(path_results_preprocess,"perm_prep_3.npy"),      mmap_mode=None, allow_pickle=False, fix_imports=True, encoding='ASCII')
    depo_prep_2      = numpy.load(file=os.path.join(path_results_preprocess,"depo_prep_2.npy"),      mmap_mode=None, allow_pickle=False, fix_imports=True, encoding='ASCII')

    perm_prep_1 = perm_prep_3[:,0,0]
    depo_prep_1 = depo_prep_2[:,0]


    # Parameters 
    # ----------
    num_times = 2001#1001#5001#10001 # 1001
    time_1 = numpy.linspace(0,1,num_times)
    dt = time_1[1] - time_1[0]

    num_positions = 1001#161#101#501#1001 # 101
    posi_1 = numpy.linspace(0,1,num_positions)
    dx = posi_1[1]-posi_1[0]

    conc_in = 1.0
    phi = 1.0 # TODO: Define this properly

    type_clog = "deposit"


    (conc_2,conc_max_or_tot_2,perm_2,depo_2,velo_1,dpdx_2,psi_2) = main(conc_max_or_tot_1=conc_max_or_tot_1,perm_prep_1=perm_prep_1,depo_prep_1=depo_prep_1,
                                                                        posi_1=posi_1,time_1=time_1,
                                                                        phi=phi,conc_in=conc_in,
                                                                        dt=dt,dx=dx,
                                                                        type_clog=type_clog)



    # Save results 
    # ----- 
    #path_results = os.path.join(".","results/results_flow") # thesis
    path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/results_flow") # paper
    if not os.path.exists(path_results):
        os.mkdir(path_results)

    numpy.save(file=os.path.join(path_results,"time_1.npy"), arr=time_1, allow_pickle=True, fix_imports=True) 
    numpy.save(file=os.path.join(path_results,"posi_1.npy"), arr=posi_1, allow_pickle=True, fix_imports=True)

    numpy.save(file=os.path.join(path_results,"conc_2.npy"),     arr=conc_2, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"conc_max_or_tot_2.npy"), arr=conc_max_or_tot_2, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"perm_2.npy"),     arr=perm_2, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"depo_2.npy"),     arr=depo_2, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"velo_1.npy"),     arr=velo_1, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"dpdx_2.npy"),     arr=dpdx_2, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"psi_2.npy"),      arr=psi_2, allow_pickle=True, fix_imports=True)



print(datetime.datetime.now() - begin_time)