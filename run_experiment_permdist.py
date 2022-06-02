import numpy
import os
import datetime

import run_preprocess_2D
import configure

begin_time = datetime.datetime.now()

# Parameters 
# ------
num_reps = 10_000 # number of times to repeat a test

num_nodes_list = [1] # List of num nodes in cells to get distribution for

num_tests = len(num_nodes_list) # Nuber of different cell sizes to test



# Main
# -----
perm_effe_2 = numpy.zeros(shape=(num_tests, num_reps)) # place to store result
# perm_effe_2[t,r] = effective permeability for repeat repeats[r] of test tests[t]

for t in range(num_tests):
    for r in range(num_reps):  
        
        # Get effective permeability in 0,0 direction
        # -----
        perm_3, depo_2, conc_max_disc_1 = run_preprocess_2D.main(configure=configure)

        perm_effe = perm_3[0,0,0]

        perm_effe_2[t,r] = perm_effe

end_time = datetime.datetime.now()
print("sim_time:\n {}".format(end_time-begin_time))

# Save results 
# -----
path_results = os.path.join(".","results_experiment_permdist")
if not os.path.exists(path_results):
    os.mkdir(path_results)
    
numpy.save(file=os.path.join(path_results,"perm_effe_2.npy"), arr=perm_effe_2, allow_pickle=True, fix_imports=True)





