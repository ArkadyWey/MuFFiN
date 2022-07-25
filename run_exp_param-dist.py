import numpy
import os
import datetime
import argparse
import json 

import run_preprocess_2D
import utils_preprocess_2D

"""
To run in parallel: 
parallel python3 run_exp_param-dist.py -Ns ::: 2 8 18 etc...
"""

begin_time = datetime.datetime.now()

# Parameters 
# ------
file_parameters = open("parameters.json")
parameters      = json.load(file_parameters)

parser = argparse.ArgumentParser(description="Input parameters")
parser.add_argument("-Ns", "--num_nodes_list", dest="num_nodes_list", nargs="+", required=True,
                    help="num_nodes values for exp_param-dist", type=int)

parser.add_argument("-r", "--num_reps", dest="num_reps", required=True,
                    help="number of repeats at each N", type=int)

args = parser.parse_args()

num_nodes_list = args.num_nodes_list
#num_nodes_list = [2,8,18]
#num_nodes_list = numpy.linspace(1,10,10,dtype=int)**2 # List of num nodes in cells to get distribution for

num_reps = args.num_reps#100 # number of times to repeat a test


path_results = os.path.join(".","results/results_exp_param-dist_4-reg_reps-{}_sigma-{}".format(num_reps,parameters["sigma"]))
if not os.path.exists(path_results):
    os.makedirs(path_results)

#if not os.path.exists(os.path.join(path_results,"cond")):
#    os.makedirs(os.path.join(path_results,"cond"))
#
#if not os.path.exists(os.path.join(path_results,"adhe")):
#    os.makedirs(os.path.join(path_results,"adhe"))


num_tests = len(num_nodes_list) # Number of different cell sizes to test

l1_list = []
l2_list = []
for N in num_nodes_list:
    l1_list.append(numpy.sqrt(N)) #1.07456993183*
    l2_list.append(numpy.sqrt(N)) #1.86120971822* 

num_tests = len(num_nodes_list) # Number of different cell sizes to test
# Main
# -----
perm_effe_2 = numpy.zeros(shape=(num_tests, num_reps)) # place to store result
# perm_effe_2[t,r] = effective permeability for repeat repeats[r] of test tests[t]
depo_effe_2 = numpy.zeros(shape=(num_tests, num_reps)) # place to store result
# depo_effe_2[t,r] = effective deposition for repeat repeats[r] of test tests[t]

count_adhe_2 = numpy.zeros(shape=(num_tests, num_reps))
# count_adhe_2[t,r] = number of edges blocked for repeat repeats[r] of test tests[t]

for t in range(num_tests):
    num_nodes = num_nodes_list[t]
    print("Running for N={}.".format(num_nodes))
    l1 = l1_list[t]
    l2 = l2_list[t]

    for r in range(num_reps):  
        print("Running for N={}. Repeat {} of {}.".format(num_nodes,r,num_reps))
        # Get correct number of nodes 
        # -----
        
        # Get effective permeability in 0,0 direction and adhesivity in 0 diresction
        # -----
        perm_3, depo_2, conc_max_disc_1, cond_init_4, adhe_tabl_5, heav_5, delt_5 = run_preprocess_2D.main(num_nodes=num_nodes, 
                                                                                                   l1=l1,
                                                                                                   l2=l2)
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

        count_adhe = utils_preprocess_2D.count_num_edges_blocked(adhe_tabl_5=adhe_tabl_5, heav_5=heav_5, delt_5=delt_5, cond_init_4=cond_init_4)
        count_adhe_2[t,r] = count_adhe

    mean_perm = numpy.mean(perm_effe_2[t,:])
    mean_depo = numpy.mean(depo_effe_2[t,:])
    print("mean_perm:{}".format(mean_perm))
    print("mean_depo:{}".format(mean_depo))

    # Get array for this N
    # -----
    perm_effe_1 = perm_effe_2[t,:]
    depo_effe_1 = depo_effe_2[t,:]

    count_adhe_1 = count_adhe_2[t,:]

    # Save results at current N
    # -----   
    numpy.save(file=os.path.join(path_results,"perm_effe_1_N-{}.npy".format(num_nodes)), arr=perm_effe_1, allow_pickle=True, fix_imports=True)
    numpy.save(file=os.path.join(path_results,"depo_effe_1_N-{}.npy".format(num_nodes)), arr=depo_effe_1, allow_pickle=True, fix_imports=True)
    
    numpy.save(file=os.path.join(path_results,"count_adhe_1_N-{}.npy".format(num_nodes)), arr=count_adhe_1, allow_pickle=True, fix_imports=True)

end_time = datetime.datetime.now()
print("sim_time:\n {}".format(end_time-begin_time))






