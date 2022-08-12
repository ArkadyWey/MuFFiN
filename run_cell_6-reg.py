import cells
import numpy
import os

import configure

# Parameters 
# -----
path_results = os.path.join(".","results/results_6-reg")

if not os.path.exists(os.path.join(".",path_results)):
    os.mkdir(path_results)

num_nodes = 18
num_refs  = 3
num_dims  = 2

initialisation = "6-reg"
sigma          = 0.3

conf = configure.Configure(num_nodes=N,
                           initialisation=initialisation,
                           sigma=sigma)

cell = cells.Cell_2D_six_reg(num_nodes=num_nodes,
                             num_refs=num_refs, 
                             num_dims=num_dims, 
                             mu=conf.mu,
                             sigma=conf.sigma)



# Save arrays for triangulation plot
# -------------------------------
# Send results to arrays for storage
key = numpy.array(cell.key)

numpy.save(file=os.path.join(path_results,"pts_to_tri_2.npy"), arr=cell.pts_to_tri_2, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_results,"simplices.npy"), arr=cell.simplices, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_results,"key.npy"), arr=key, allow_pickle=True, fix_imports=True)

# Save arrays for initial conductance plot
# -------------------------------
numpy.save(file=os.path.join(path_results,"cond_init_4.npy"), arr=cell.cond_init_4, allow_pickle=True, fix_imports=True)
numpy.save(file=os.path.join(path_results,"pts_4.npy"), arr=cell.pts_4, allow_pickle=True, fix_imports=True)