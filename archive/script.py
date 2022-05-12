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

def interp(table_x,table_y,new_point):
    tck = interpolate.splrep(x=table_x,y=table_y,k=3)
    return interpolate.splev(x=new_point, tck=tck)

def get_velo(perm_1,posi_1,dx):
    """
    """
    num_1 = numpy.ones(shape=perm_1.shape)
    den_1 = perm_1
    integrand_1 = num_1/den_1
    
    integral = integrate.simps(y=integrand_1,x=posi_1,dx=dx,even="avg")

    velo = 1/integral
    return velo


begin_time = datetime.datetime.now()
print(datetime.datetime.now())


refs_1  = numpy.array([0,1,-1]) # TODO: needs to include all possible r

num_refs  = len(refs_1)
num_concs = 6 
num_nodes = 4
length    = 1.0
alpha     = 1.0
v         = 2.0
phi       = 0.5 # TODO: Define this properly

# PREPROCESSING -------------------------------------------------------------------------------------

conc_max_discs_1 = numpy.linspace(0,1,num_concs) # discrete list of possible concentrations
#print("conc_max_discs_1: \n {}".format(conc_max_discs_1))

# Conductance and adhesivity 
cond_init_3 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs)) # initial condition should be random

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


cond_tabl_4 = numpy.repeat(a=cond_init_3[numpy.newaxis,:,:,:], repeats=num_concs, axis=0) # create conductance table
# cond_tabl_4[k,i,j,r] = G_ij^r at c[k]

adhe_tabl_4 = numpy.zeros(shape=(num_concs,num_nodes,num_nodes,num_refs))
# adhe_tabl_4[k,i,j,r] = A_ij^r at c[k]

for k in range(num_concs):
    conc_disc = conc_max_discs_1[k] # discrete concentration
    # set conductance and adhesivity for each possible conc value
    for i in range(num_nodes):
        for j in range(num_nodes):
            for l in range(num_refs):            
                cond = cond_tabl_4[k,i,j,l]
                if cond != 0: # we don't need to worry about G_ij==0
                    if conc_disc < alpha*cond or numpy.allclose(a=conc_disc,b=alpha*cond,rtol=1e-5,atol=1e-8):
                        pass
                    elif conc_disc > alpha*cond:
                        #pass
                        cond_tabl_4[k,i,j,l] = 0
                        adhe_tabl_4[k,i,j,l] = 1
                    else: 
                        raise Exception
#print("cond_tabl_4[k,:,:,l]: \n",cond_tabl_4[0,:,:,0])
#print("adhe_tabl_4[k,:,:,l]: \n",adhe_tabl_4[0,:,:,0])
# line of three nodes
# plt.plot(conc_max_discs_1,cond_tabl_4[:,0,1,0])
# plt.plot(conc_max_discs_1,cond_tabl_4[:,1,0,0])
# plt.plot(conc_max_discs_1,cond_tabl_4[:,1,2,0])
# plt.plot(conc_max_discs_1,cond_tabl_4[:,2,1,0])
# plt.plot(conc_max_discs_1,cond_tabl_4[:,2,0,1])
# plt.plot(conc_max_discs_1,cond_tabl_4[:,0,2,2])
# plt.show()

# Cell problem
csol_2 = numpy.zeros(shape=(num_concs,num_nodes)) # cell solution W[k,i], is W_i at the k^th concentration

# ---- assemble cell problem ----
refs_2 = numpy.repeat(a=refs_1[numpy.newaxis,:], repeats=num_nodes, axis=0) # add j axis 
refs_3 = numpy.repeat(a=refs_2[numpy.newaxis,:,:], repeats=num_nodes, axis=0) # add i axis
refs_4 = numpy.repeat(a=refs_3[numpy.newaxis,:,:,:], repeats=num_concs, axis=0) # add k axis
# refs_4[k,i,j,r] = r (repeated for multiplication)

rhs_4 = length*numpy.multiply(refs_4,cond_tabl_4) # inside of sum on rhs of cell problem
rhs_3 = numpy.sum(a=rhs_4,axis=3) # sum over r

# I should be able to build this lhs without looking through k
# TODO: do this without k loop
lhs_4 = numpy.zeros_like(rhs_4)
for k in range(num_concs):
    for l in range(num_refs):
        cond_2 = cond_tabl_4[k,:,:,l]
        cond_sum_1 = numpy.sum(a=cond_2,axis=1)
        cond_sum_2 = numpy.diag(cond_sum_1)
        lhs_2 = cond_2 - numpy.multiply(numpy.eye(N=num_nodes,M=num_nodes), cond_sum_2)
        lhs_4[k,:,:,l] = lhs_2
lhs_3 = numpy.sum(a=lhs_4,axis=3) # sum over r
        
# solve the cell problem for each possible conc value
for k in range(num_concs):
    a_2 = lhs_3[k,:,:]
    b_1 = numpy.sum(a=rhs_3[k,:,:],axis=1)
    #if k==5:
    #    print("a_2: \n{}".format(a_2))
    #    print("b_1: \n{}".format(b_1))
    # ---- solve ----
    #print("k: \n{}".format(k))
    #print("a_2: \n{}".format(a_2))
    #print("b_1: \n{}".format(b_1))
    #csol_1 = numpy.linalg.solve(a=a_2,b=b_1)
    #csol_1 = optimize.lsq_linear(A=a_2,b=b_1)
    csol_1 = sparse.linalg.lsqr(A=a_2,b=b_1)
    
    #csol_2[k,:] = csol_1
    #csol_2[k,:] = csol_1.x
    csol_2[k,:] = csol_1[0]
    
    #print(csol_1.x)
    #print("csol_1: \n{}".format(csol_1[0]))

# form delt_4 where delta_4[k,i,j,r] = W_i-W_j-rl at the kth concentration 
# use delt_4 to form heavisude which is H(delta)

delt_4 = numpy.zeros(shape=(num_concs,num_nodes,num_nodes,num_refs)) 
# delt_4[k,i,j,l] is delta_ij^r[l] at concentration c[k]
# Note that we'll need delta_ji^{-r}, which is the negative of this object

for k in range(num_concs):
    csol_1 = csol_2[k,:]
    csol_iway_2 = numpy.repeat(a=csol_1[:,numpy.newaxis],repeats=num_nodes,axis=1)
    csol_jway_2 = numpy.repeat(a=csol_1[numpy.newaxis,:],repeats=num_nodes,axis=0)
    csol_diff_2 = csol_iway_2 - csol_jway_2
    for l in range(num_refs):
        ref = refs_1[l]
        ref_2 = ref*numpy.ones(shape=(num_nodes,num_nodes))
        delt_2 = csol_diff_2 - length*ref_2
        delt_4[k,:,:,l] = delt_2

# Use delta to make heaviside         
heav_4 = (delt_4>0).astype(int)

#print("delt_4[k,:,:,l]: \n{}".format(delt_4[3,:,:,0]))


# TODO: Make heav_4 properly once we know node pressures -- this is now done, we dont need pressure we need delta
#heav_3 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs)) # we can't know what this is without pressure
#heav_3[0,1,0] = 1
#heav_3[2,0,0] = 1
#heav_3[1,3,0] = 1
#heav_3[2,3,0] = 1
#heav_3[1,0,1] = 1
#heav_3[3,2,1] = 1
#heav_4 = numpy.repeat(a=heav_3[numpy.newaxis,:,:,:],repeats=num_concs,axis=0)
#print("heav_4[k,:,:,l]: \n{}".format(heav_4[2,:,:,0]))

# so for now zeros so we end up with ones
#print("csol_iway_2: \n{}".format(csol_iway_2))
#print("csol_jway_2: \n{}".format(csol_jway_2))
#print("csol_diff_2: \n{}".format(csol_diff_2))
#print("delt_4[k,:,:,l]: \n{}".format(delt_4[0,:,:,2]))

# Form k and j 
perm_inte_4 = cond_tabl_4*delt_4 # the inside of the sum for k, which is G_ij^r[l]*delta_ij^r[l] at c[k]

cond_init_4 = numpy.repeat(a=cond_init_3[numpy.newaxis,:,:,:], repeats=num_concs, axis=0)
depo_inte_4 = cond_init_4*delt_4*adhe_tabl_4*(numpy.ones_like(heav_4)-heav_4) # the inside of the sum for j, which is G_ij^r[l]*delta_ij^r[l] at c[k]
#print("cond_tabl_4[k,:,:,l]: \n{}".format(cond_tabl_4[0,:,:,0]))
#print("perm_inte_4[k,:,:,l]: \n{}".format(perm_inte_4[0,:,:,0]))

perm_2 = numpy.zeros(shape=(num_concs,num_refs)) # perm_2[k,l] is the r[l] element of the permeability at concentration c[k]
perm_1 = numpy.zeros(shape=(num_concs)) # perm_1[k] is the permeability at concentration c[k]
depo_2 = numpy.zeros(shape=(num_concs,num_refs)) # perm_2[k,l] is the r[l] element of the permeability at concentration c[k]
depo_1 = numpy.zeros(shape=(num_concs)) # perm_1[k] is the permeability at concentration c[k]
for k in range(num_concs):
    for l in range(num_refs):
        ref = refs_1[l]
        #print(ref)
        perm_inte_2 = perm_inte_4[k,:,:,l]
        depo_inte_2 = depo_inte_4[k,:,:,l]
        #print("perm_inte_2:\n",perm_inte_2)
        perm_2[k,l] = ref*numpy.sum(a=numpy.sum(a=perm_inte_2,axis=0),axis=0) # sum over i then j
        depo_2[k,l] = numpy.sum(a=numpy.sum(a=depo_inte_2,axis=0),axis=0) # sum over i then j
perm_1[:] = -0.5*numpy.sum(a=perm_2,axis=1) # sum over r 
depo_1[:] = -(1/v)*numpy.sum(a=depo_2,axis=1) # sum over r 

#print("perm_1[k]: \n{}".format(perm_1[3]))
#print("depo_1[k]: \n{}".format(depo_1[3]))


        

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


# SIMULATION ----------------------------------------------------------------------------------------

num_times = 1001
time_1 = numpy.linspace(0,20,num_times)
dt = time_1[1] - time_1[0]

num_positions = 101
posi_1 = numpy.linspace(0,10,num_positions)
dx = posi_1[1]-posi_1[0]

# Storage for solution
conc_2 = numpy.zeros(shape=(num_positions,num_times))
velo_1 = numpy.zeros(shape=(num_times))
# Initial conditions
conc_2[:,0] = numpy.zeros(shape=num_positions)
conc_in = 1.0
conc_2[0,0] = conc_in
# Boundary conditions 
conc_2[0,:] = numpy.ones(shape=num_times)
conc_2[0,0] = conc_in

#print(conc_2)


for i_t in range(num_times-1):
    i_t = i_t + 1 # because we already know initial values
    # sudocode
    # 1. Get k, j
    # -----------
    # for i_x in range(num_positions):
        # - Get the last c_new and call it c, at this position, c[i_x] and call it c. This is a proxy for x, 
        #       since if we want to know k(x) we find k(c_x)
        # - use spline to get k(c_x) and j(c_x)
    
    # 2. Stick all k(c_x), j(c_x) together to make vector k[i_x], j[i_x] (this can be done inside the space loop by appending)
    # 3. Use k[i_x] to get u using eq. (11) in 1-d problem notes
    # 4. Use darcy: dpdx[i_x] = - u/k[i_x]
    # 5. Get phi[i_x] = j[i_x]*dpdx[i_x]
    # 6. Build solver to get value of c at t[i_t+1]
    # --------------------------------------------
    # c_new[i_x] = c[i_x] - dt*( (u/dx*phi)*(c[i_x+1]-c[i_x])+phi[i_x]*c[i_x] )

    # 1. Get k, j
    conc_1 = conc_2[:,i_t-1] 

    perm_solver_1 = numpy.zeros(shape=num_positions)
    depo_solver_1 = numpy.zeros(shape=num_positions)
    for i_x in range(num_positions):
        # get previous concentration
        conc = conc_1[i_x]
        # use spline to get k, j
        perm = interp(table_x=conc_max_discs_1,table_y=perm_1,new_point=conc)
        depo = interp(table_x=conc_max_discs_1,table_y=depo_1,new_point=conc)
        
        # 2. Stick all together. i.e. fill the functions of x
        perm_solver_1[i_x] = perm
        depo_solver_1[i_x] = depo

    # 3. Use previous perm to get current u
    velo = get_velo(perm_1=perm_solver_1,posi_1=posi_1,dx=dx)
    velo_1[i_t] = velo
    #print(velo)

    # 4. Use darcy: dpdx[i_x] = - u/k[i_x]
    dpdx_1 = - velo*numpy.ones(shape=perm_solver_1.shape)/perm_solver_1

    # 5. Get psi[i_x] = j[i_x]*dpdx[i_x]
    psi_1 = depo_solver_1*dpdx_1

    # 6. Build solver to get value of c at t[i_t]
    conc_new_1 = numpy.zeros(shape=num_positions)
    conc_new_1[0] = conc_in # enforce boundary condition
    for i_x in range(num_positions-1): 
        i_x = i_x + 1 # since we know the boundary
        conc    = conc_1[i_x]
        conc_m1 = conc_1[i_x-1]
        psi = psi_1[i_x]

        conc_new = conc - (velo/phi)*(dt/dx)*(conc-conc_m1) - psi*dt*conc
        conc_new_1[i_x] = conc_new
    #print(conc_new_1)
    
    conc_2[:,i_t] = conc_new_1

start          = 0
first_quarter  = int(1*(num_times-1)/4)
second_quarter = int(2*(num_times-1)/4)
third_quarter  = int(3*(num_times-1)/4)
end            = -1

plt.plot(posi_1,conc_2[:,start])
plt.plot(posi_1,conc_2[:,first_quarter])
plt.plot(posi_1,conc_2[:,second_quarter])
plt.plot(posi_1,conc_2[:,third_quarter])
plt.plot(posi_1,conc_2[:,end])


#plt.plot(posi_1,conc_2[:,3])
plt.show()

plt.plot(time_1,velo_1)
plt.xlabel("t")
plt.ylabel("u")
plt.show()


print(datetime.datetime.now() - begin_time)







# Below is old code - i think new idea above is more complete and can probab;y get rid of below.

#    # for i_x in range(num_positions):
#        # At each position, find the permeability
#        # Fill A,G,W,k
#        # TODO Get best conc_dh
#        # Use best conc_dh to give required matrices
#        # output is perm_1, which has perm entry for each position so indexed by i_x
#        # TODO Find the k that corresponds to the current c
#    k = 1 # this is a placeholder for the real k
#
#    # Calculate velocity (not function of space so outside space loop)
#    velo = 1/(numpy.sum(a=1/perm_1,axis=0)*dx)    
#    # Calculate dp/dx
#    dpdx_1 = -velo/perm_1 # dpdx_1[i_x] is pressure gradient at point i_x 
#    
#    # Calculate node pressure
#    pres_2 = numpy.zeros(shape=(num_positions,num_nodes)) # pres_2[i_x,i] is the pressure of the ith node at position indexed by i_x
#    for i_x in range(num_positions): # i_x indexes the position 
#        # Find node pressure
#        dpdx = dpdx_1[i_x]
#        pres_1 = csol_1*dpdx
#        pres_2[i_x,:] = pres_1
#
#        # Find Heaviside
#        #for i_r in range(num_refs):
#            #pres_iway_2 = numpy.repeat(a=pres_1[:,numpy.newaxis],repeats=num_nodes,axis=1)
#            #pres_jway_2 = numpy.repeat(a=pres_1[numpy.newaxis,:],repeats=num_nodes,axis=0)
#            #pres_diff_2 = pres_iway_2 - pres_jway_2
#            #heav_2      = (pres_diff_2>0).astype(int)
#            #heav_2 = (delt_4[k,:,:,i_r]).astype(int)




































