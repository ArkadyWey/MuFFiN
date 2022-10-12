import numpy 
import cells
import configure 
import os
import argparse

path_results = os.path.join(".","results/results_cond-dist")

# Make results directories 
# --------
if not os.path.exists(path_results):
    os.makedirs(path_results)

sigma          = 0.3
initialisation = "6-ireg"

parser = argparse.ArgumentParser(description="Input parameters")
parser.add_argument("-N", "--num_nodes", dest="num_nodes", required=True,
                    help="num_nodes value.", type=int)

parser.add_argument("-r", "--num_reps", dest="num_reps", required=True,
                    help="number of repeats at each N", type=int)

args = parser.parse_args()

num_nodes = args.num_nodes
num_reps  = args.num_reps

conf = configure.Configure(num_nodes=num_nodes,
                           initialisation=initialisation,
                           sigma=sigma,
                           type_alpha="none")
edge_lengs = []
edge_conds = []
for r in range(num_reps):
    print("r={}".format(r))
    cell = cells.Cell_2D_six_ireg(num_nodes=conf.num_nodes,
                                  num_refs=3, 
                                  num_dims=2,
                                  mean=conf.mean,
                                  leng_1=conf.leng_1,
                                  mu=0.5,
                                  sigma=0.3)
    
    for edge_leng in cell.edge_lengs:
        edge_lengs.append(edge_leng)

    for edge_cond in cell.edge_conds:
        edge_conds.append(edge_cond)


numpy.save(file=os.path.join(path_results,"edge_lengs_N-{}.npy".format(num_nodes)), arr=numpy.array(edge_lengs), allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_results,"edge_conds_N-{}.npy".format(num_nodes)), arr=numpy.array(edge_conds), allow_pickle=True, fix_imports=True)

median_edge_lengs = numpy.median(a=numpy.array(edge_lengs),axis=None)
median_edge_conds = numpy.median(a=numpy.array(edge_conds),axis=None)

mean_edge_lengs = numpy.mean(a=numpy.array(edge_lengs),axis=None)
mean_edge_conds = numpy.mean(a=numpy.array(edge_conds),axis=None)

var_edge_lengs = numpy.var(a=numpy.array(edge_lengs),axis=None)
var_edge_conds = numpy.var(a=numpy.array(edge_conds),axis=None)

print("median_edge_lengs:\n{}".format(median_edge_lengs))
print("median_edge_conds:\n{}".format(median_edge_conds))

print("mean_edge_lengs:\n{}".format(mean_edge_lengs))
print("mean_edge_conds:\n{}".format(mean_edge_conds))

print("var_edge_lengs:\n{}".format(var_edge_lengs))
print("var_edge_conds:\n{}".format(var_edge_conds))

v = var_edge_conds
l = numpy.sqrt(2.0)/numpy.sqrt(numpy.sqrt(3.0))
c = numpy.exp(2.0*0.5)
sig_squ = numpy.log((v*l**2)/c+1.0)
sig = numpy.sqrt(sig_squ)
print("sig:\n{}".format(sig))