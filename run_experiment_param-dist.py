import numpy
import os
import datetime

import run_preprocess_2D


begin_time = datetime.datetime.now()

# Parameters 
# ------
num_reps = 100 # number of times to repeat a test

#num_nodes_list = numpy.linspace(1,10,10,dtype=int)**2 # List of num nodes in cells to get distribution for
num_nodes_list = [2,8,18,32]

num_tests = len(num_nodes_list) # Number of different cell sizes to test


# Main
# -----
perm_effe_2 = numpy.zeros(shape=(num_tests, num_reps)) # place to store result
# perm_effe_2[t,r] = effective permeability for repeat repeats[r] of test tests[t]
depo_effe_2 = numpy.zeros(shape=(num_tests, num_reps)) # place to store result
# depo_effe_2[t,r] = effective deposition for repeat repeats[r] of test tests[t]

for t in range(num_tests):
    for r in range(num_reps):  
        print("Repeat {} of {}.".format(r,num_reps))
        # Get correct number of nodes 
        # -----
        num_nodes = num_nodes_list[t]


        # Get effective permeability in 0,0 direction
        # -----
        perm_3, depo_2, conc_max_disc_1 = run_preprocess_2D.main(num_nodes=num_nodes)

        perm_effe = perm_3[0,0,0]
        depo_effe = depo_2[-1,0]

        #print(perm_effe)
        #print(depo_effe)

        perm_effe_2[t,r] = perm_effe
        depo_effe_2[t,r] = depo_effe

    mean_perm = numpy.mean(perm_effe_2[t,:])
    mean_depo = numpy.mean(depo_effe_2[t,:])
    print("mean_perm:{}".format(mean_perm))
    print("mean_depo:{}".format(mean_depo))

    # Get array for this N
    # -----
    perm_effe_1 = perm_effe_2[t,:]
    depo_effe_1 = depo_effe_2[t,:]

    # Save results at current N
    # -----
    path_results = os.path.join(".","results_experiment_param-dist_hexag-structure_reps-p1k")
    if not os.path.exists(path_results):
        os.mkdir(path_results)

    N = num_nodes_list[t]
    
    numpy.save(file=os.path.join(path_results,"perm_effe_2_N-{}.npy".format(N)), arr=perm_effe_1, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"depo_effe_2_N-{}.npy".format(N)), arr=depo_effe_1, allow_pickle=True, fix_imports=True)


end_time = datetime.datetime.now()
print("sim_time:\n {}".format(end_time-begin_time))






