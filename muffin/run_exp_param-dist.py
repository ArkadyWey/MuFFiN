import numpy
import os
import datetime
import argparse
import json 

import muffin.run_preprocess_2D as run_preprocess_2D
import muffin.utils_preprocess_2D as utils_preprocess_2D

"""
To run in series:
python3 run_exp_param-dist.py --num_reps 1000 --num_nodes 4

To run in parallel: 
parallel python3 run_exp_param-dist.py --num_nodes ::: 2 8 18...
"""

begin_time = datetime.datetime.now()

# Parameters 
# ------
parser = argparse.ArgumentParser(description="Input parameters")
parser.add_argument("-Ns", "--num_nodes_list", dest="num_nodes_list", nargs="+", required=True,
                    help="num_nodes values for exp_param-dist", type=int)

parser.add_argument("-r", "--num_reps", dest="num_reps", required=True,
                    help="number of repeats at each N", type=int)

parser.add_argument("-i", "--initialisation", dest="initialisation", required=True,
                    help="structure of cell", type=str)

parser.add_argument("-s", "--sigma", dest="sigma", required=True,
                    help="sigma for lognormal disribution that conductance drawn from", type=float)

parser.add_argument("-a", "--type_alpha", dest="type_alpha", required=True,
                    help="type of alpha blocking rule, either mean or median", type=str)

args = parser.parse_args()

num_nodes_list = args.num_nodes_list
# or... 
# num_nodes_list = [2,8,18]
# num_nodes_list = numpy.linspace(1,10,10,dtype=int)**2 # List of num nodes in cells to get distribution for

num_reps = args.num_reps # number of times to repeat a test
#  or ...
# 100
initialisation = args.initialisation
sigma          = args.sigma
type_alpha     = args.type_alpha

path_results = os.path.join(".","results/results_exp_param-dist_{}_reps-{}_sigma-{}_alpha-{}".format(initialisation,num_reps,sigma,type_alpha))

# Make results directories 
# --------
if not os.path.exists(path_results):
    os.makedirs(path_results)

num_tests = len(num_nodes_list) # Number of different cell sizes to test



# Main
# -----
perm_effe_2 = numpy.zeros(shape=(num_tests, num_reps)) # place to store result
# perm_effe_2[t,r] = effective permeability for repeat repeats[r] of test tests[t]
depo_effe_2 = numpy.zeros(shape=(num_tests, num_reps)) # place to store result
# depo_effe_2[t,r] = effective deposition for repeat repeats[r] of test tests[t]

count_adhe_2 = numpy.zeros(shape=(num_tests, num_reps))
# count_adhe_2[t,r] = number of edges blocked for repeat repeats[r] of test tests[t]
count_adhe_hori_2 = numpy.zeros(shape=(num_tests, num_reps))
# count_adhe_2[t,r] = number of horizontal edges blocked for repeat repeats[r] of test tests[t]
count_adhe_not_hori_2 = numpy.zeros(shape=(num_tests, num_reps))
# count_adhe_2[t,r] = number of vertical edges blocked for repeat repeats[r] of test tests[t]

for t in range(num_tests):
    num_nodes = num_nodes_list[t]
    print("Running for N={}.".format(num_nodes))


    for r in range(num_reps):  
        print("Running for N={}. Repeat {} of {}.".format(num_nodes,r,num_reps))
        # Get correct number of nodes 
        # -----
        
        # Get effective permeability in 0,0 direction and adhesivity in 0 diresction
        # -----
        perm_3, depo_2, conc_max_disc_1, cond_tabl_5, adhe_tabl_5, delt_5, heav_5 = run_preprocess_2D.main(num_nodes=num_nodes, 
                                                                                                           initialisation=initialisation,
                                                                                                           sigma=sigma,
                                                                                                           type_alpha=type_alpha)
        # Get right direction
        perm_effe = perm_3[0,0,0]
        depo_effe = depo_2[-1,0]

        # Add to array
        perm_effe_2[t,r] = perm_effe
        depo_effe_2[t,r] = depo_effe

        # Save each cond and adhe and get count of blocked
        # ------
        #numpy.save(file=os.path.join(path_results+"/cond","cond_init_4_N-{}_R-{}.npy".format(num_nodes, r)), arr=cond_init_4, allow_pickle=True, fix_imports=True)
        #numpy.save(file=os.path.join(path_results+"/adhe","adhe_tabl_5_N-{}_R-{}.npy".format(num_nodes, r)), arr=adhe_tabl_5, allow_pickle=True, fix_imports=True)

        count_adhe, count_adhe_hori, count_adhe_not_hori = utils_preprocess_2D.count_num_edges_blocked(initialisation="6-reg",
                                                                                                       cond_tabl_5=cond_tabl_5, 
                                                                                                       adhe_tabl_5=adhe_tabl_5, 
                                                                                                       delt_5=delt_5, 
                                                                                                       heav_5=heav_5)
        count_adhe_2[t,r]          = count_adhe
        count_adhe_hori_2[t,r]     = count_adhe_hori
        count_adhe_not_hori_2[t,r] = count_adhe_not_hori
        #print(count_adhe)

    mean_perm = numpy.mean(perm_effe_2[t,:])
    mean_depo = numpy.mean(depo_effe_2[t,:])
    print("mean_perm:{}".format(mean_perm))
    print("mean_depo:{}".format(mean_depo))

    # Get array for this N
    # -----
    perm_effe_1 = perm_effe_2[t,:]
    depo_effe_1 = depo_effe_2[t,:]

    count_adhe_1 = count_adhe_2[t,:]
    count_adhe_hori_1 = count_adhe_hori_2[t,:]
    count_adhe_not_hori_1 = count_adhe_not_hori_2[t,:]
    

    # Save results at current N
    # -----   
    numpy.save(file=os.path.join(path_results,"perm_effe_1_N-{}.npy".format(num_nodes)), arr=perm_effe_1, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"depo_effe_1_N-{}.npy".format(num_nodes)), arr=depo_effe_1, allow_pickle=True, fix_imports=True)
    
    numpy.save(file=os.path.join(path_results,"count_adhe_1_N-{}.npy".format(num_nodes)), arr=count_adhe_1, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"count_adhe_hori_1_N-{}.npy".format(num_nodes)), arr=count_adhe_hori_1, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"count_adhe_not_hori_1_N-{}.npy".format(num_nodes)), arr=count_adhe_not_hori_1, allow_pickle=True, fix_imports=True)

end_time = datetime.datetime.now()
print("sim_time:\n {}".format(end_time-begin_time))






