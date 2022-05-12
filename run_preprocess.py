from turtle import shape
import numpy
import scipy 
from scipy import optimize
from scipy import sparse
import datetime
import matplotlib
from matplotlib import pyplot as plt
from scipy import interpolate
from scipy import integrate


import preprocess

def main(conc_max_discs_1,cond_init_3,adhe_init_3,alpha,refs_1,length,v):
    """
    """

    # Preprocess
    # ------------
    # Get conductance and adhesivity 
    # -----
    cond_tabl_4, adhe_tabl_4 = preprocess.get_conductance_and_adhesivity(conc_max_discs_1=conc_max_discs_1, 
                                                                         cond_init_3=cond_init_3, 
                                                                         adhe_init_3=adhe_init_3, 
                                                                         alpha=alpha)
    #print("cond_tabl_4[k,:,:,l]: \n",cond_tabl_4[3,:,:,-1])
    #print("adhe_tabl_4[k,:,:,l]: \n",adhe_tabl_4[3,:,:,-1])


    # Get lhs and rhs of cell problem 
    # ------
    lhs_3, rhs_3 = preprocess.get_cell_problem(refs_1=refs_1, 
                                               cond_tabl_4=cond_tabl_4,
                                               length=length)
    #print("lhs_3[k,:,:]: \n", lhs_3[0,:,:])
    #print("rhs_3[k,:,:]: \n", rhs_3[0,:,:])


    # Get solution of cell problem
    # ------
    csol_2 = preprocess.get_cell_solution(lhs_3=lhs_3,
                                          rhs_3=rhs_3)
    #print("csol_2[k,:]: \n", csol_2[0,:])


    # Get delta
    # ------
    # Form delt_4 where delta_4[k,i,j,r] = W_i-W_j-rl at the kth concentration 
    delt_4 = preprocess.get_delta(csol_2=csol_2, 
                                  refs_1=refs_1, 
                                  length=length)
    print("delt_4[k,:,:,l]: \n", delt_4[3,:,:,1])



    # Get heaviside 
    # -----
    # Use delt_4 to form heavisude which is H(delta)
    heav_4 = preprocess.get_heaviside(delt_4=delt_4)
    #print("heav_4[k,:,:,l]: \n", heav_4[0,:,:,-1])



    # Get local permeability and deposition parameter
    # ------ 
    perm_1, depo_1 = preprocess.get_permeability_and_deposition(cond_tabl_4=cond_tabl_4, 
                                                                 adhe_tabl_4=adhe_tabl_4, 
                                                                 refs_1=refs_1, 
                                                                 delt_4=delt_4, 
                                                                 heav_4=heav_4, 
                                                                 cond_init_3=cond_init_3, 
                                                                 v=v)
    #print("perm_1[k]: \n{}".format(perm_1[3]))
    #print("depo_1[k]: \n{}".format(depo_1[3]))
    return (perm_1,depo_1)


if __name__ == "__main__":

    begin_time = datetime.datetime.now()
    print(datetime.datetime.now())
    
    # Parameters
    # ------------
    refs_1  = numpy.array([0,1,-1]) # TODO: needs to include all possible r
    #print("refs_1: \n {}".format(refs_1))
    
    num_refs  = len(refs_1)
    num_concs = 1001
    num_nodes = 4
    length    = 1.0
    alpha     = 1.0
    v         = 2.0 # Sum of volumes of nodes in cell
    phi       = 0.5 # TODO: Define this properly
    
    # Concentrations to tabulate 
    conc_max_discs_1 = numpy.linspace(0,1,num_concs) # discrete list of possible concentrations
    #print("conc_max_discs_1: \n {}".format(conc_max_discs_1))
    
    # Conductance and adhesivity 
    cond_init_3 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs)) 
    adhe_init_3 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs)) 
    # TODO: initial condition should be random
    
    # line of three nodes
    #cond_init_3[0,1,0] = 1
    #cond_init_3[1,0,0] = 1
    #cond_init_3[1,2,0] = 1
    #cond_init_3[2,1,0] = 1
    #cond_init_3[2,0,1] = 1
    #cond_init_3[0,2,2] = 1
    
    # grid of four nodes
    cond_init_3[0,1,0] = 0.8 #1.0
    cond_init_3[1,0,0] = 0.8 #1.0
    cond_init_3[1,3,0] = 0.2 #1.0
    cond_init_3[3,1,0] = 0.2 #1.0
    cond_init_3[2,3,0] = 0.4 #1.0
    cond_init_3[3,2,0] = 0.4 #1.0
    cond_init_3[0,2,0] = 0.6 #1.0
    cond_init_3[2,0,0] = 0.6 #1.0
    cond_init_3[1,0,1] = 1.0 #1.0
    cond_init_3[0,1,2] = 1.0 #1.0
    cond_init_3[3,2,1] = 1.0 #1.0
    cond_init_3[2,3,2] = 1.0 #1.0


    # Get permeability and deposition parameter tables
    # -----
    perm_1, depo_1 = main(conc_max_discs_1=conc_max_discs_1,
                          cond_init_3=cond_init_3,
                          adhe_init_3=adhe_init_3,
                          alpha=alpha,
                          refs_1=refs_1,
                          length=length,
                          v=v)
    

    # Save results 
    # -----
    numpy.save(file="./perm_1.npy", arr=perm_1, allow_pickle=True, fix_imports=True)
    numpy.save(file="./depo_1.npy", arr=depo_1, allow_pickle=True, fix_imports=True)
    numpy.save(file="./conc_max_discs_1.npy", arr=conc_max_discs_1, allow_pickle=True, fix_imports=True)

    #print(conc_max_discs_1)
    #print(perm_1)
    #print(depo_1)


    plt.plot(conc_max_discs_1,perm_1, label=r"$k$", color="red")
    plt.plot(conc_max_discs_1,depo_1, label=r"$j$", color="blue")
    plt.xlabel("c")
    plt.legend()
    plt.show()

        




#perm_1 = 0.5*         # perm_1[k] = permeability at conc_max_discs_1[k]



#plt.plot(conc_max_discs_1, cond_tabl_4[:,0,1,0],label=r"$G_{01}^{0}$")
##plt.plot(conc_max_discs_1, cond_tabl_4[:,1,0,0])
#plt.plot(conc_max_discs_1, cond_tabl_4[:,1,3,0],label=r"$G_{13}^{0}$")
##plt.plot(conc_max_discs_1, cond_tabl_4[:,3,1,0])
#plt.plot(conc_max_discs_1, cond_tabl_4[:,2,3,0],label=r"$G_{23}^{0}$")
##plt.plot(conc_max_discs_1, cond_tabl_4[:,3,2,0])
#plt.plot(conc_max_discs_1, cond_tabl_4[:,0,2,0],label=r"$G_{02}^{0}$")
##plt.plot(conc_max_discs_1, cond_tabl_4[:,2,0,0],label=r"$G_{20}^{0}$")
#plt.plot(conc_max_discs_1, cond_tabl_4[:,1,0,1],label=r"$G_{10}^{1}$")
##plt.plot(conc_max_discs_1, cond_tabl_4[:,0,1,2])
#plt.plot(conc_max_discs_1, cond_tabl_4[:,3,2,1],label=r"$G_{32}^{1}$")
##plt.plot(conc_max_discs_1, cond_tabl_4[:,2,3,2])
#plt.legend()
#plt.show()
#
#plt.plot(conc_max_discs_1, adhe_tabl_4[:,0,1,0],label=r"$G_{01}^{0}$")
##plt.plot(conc_max_discs_1, adhe_tabl_4[:,1,0,0])
#plt.plot(conc_max_discs_1, adhe_tabl_4[:,1,3,0],label=r"$G_{13}^{0}$")
##plt.plot(conc_max_discs_1, adhe_tabl_4[:,3,1,0])
#plt.plot(conc_max_discs_1, adhe_tabl_4[:,2,3,0],label=r"$G_{23}^{0}$")
##plt.plot(conc_max_discs_1, adhe_tabl_4[:,3,2,0])
#plt.plot(conc_max_discs_1, adhe_tabl_4[:,0,2,0],label=r"$G_{02}^{0}$")
##plt.plot(conc_max_discs_1, adhe_tabl_4[:,2,0,0],label=r"$G_{20}^{0}$")
#plt.plot(conc_max_discs_1, adhe_tabl_4[:,1,0,1],label=r"$G_{10}^{1}$")
##plt.plot(conc_max_discs_1, adhe_tabl_4[:,0,1,2])
#plt.plot(conc_max_discs_1, adhe_tabl_4[:,3,2,1],label=r"$G_{32}^{1}$")
##plt.plot(conc_max_discs_1, adhe_tabl_4[:,2,3,2])
#plt.legend()
#plt.show()
#
#plt.plot(conc_max_discs_1,csol_2[:,0],label=r"$W_0$")
#plt.plot(conc_max_discs_1,csol_2[:,1],label=r"$W_1$")
#plt.plot(conc_max_discs_1,csol_2[:,2],label=r"$W_2$")
#plt.plot(conc_max_discs_1,csol_2[:,3],label=r"$W_3$")
#plt.legend()
#plt.show()
#
#plt.plot(conc_max_discs_1,csol_2[:,0]-csol_2[:,1],label=r"$W_0-W_1$")
#plt.plot(conc_max_discs_1,csol_2[:,2]-csol_2[:,3],label=r"$W_2-W_3$")
#plt.plot(conc_max_discs_1,csol_2[:,2]-csol_2[:,0],label=r"$W_2-W_0$")
#plt.plot(conc_max_discs_1,csol_2[:,1]-csol_2[:,3],label=r"$W_1-W_3$")
#plt.legend()
#plt.show()