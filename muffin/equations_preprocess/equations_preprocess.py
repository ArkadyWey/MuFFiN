import numpy 
import scipy.sparse.linalg as linalg

import muffin.parameters.parameters as parameters

class Base():
    """_summary_
    """
    def __init__(self, parameters:parameters.Parameters): # TODO: :cells.Base - Make base class for cells
        """_summary_
        """

    # Attributes
    # -----        
        self.parameters = parameters
    
    # Methods
    # -----        
    def get_cell_problem(self, cond_4):
        pass
        # Define readable parameters 
        # -----
        N = self.parameters.num_nodes
        R = self.parameters.num_refs
        D = self.parameters.num_dims
        
        refs_1 = self.parameters.refs_1
        leng_1 = self.parameters.leng_1
        

        # Define arrays to fill
        # -----
        rhs_cpro_inte_5 = numpy.zeros(shape=(N,N,R,R,D))
        # rhs_cpro_inte_5[i,j,r0,r1,m].
        
        lhs_inte_4 = numpy.zeros(shape=(N,N,R,R))
        # lhs_inte_4[i,j,r0,r1].


        # Build lhs and rhs
        # ------
        for r0 in range(R):
            for r1 in range(R):

                # Get lhs integrand
                # -----
                lhs_inte_4[:,:,r0,r1] = cond_4[:,:,r0,r1] - numpy.diag(numpy.sum(a=cond_4[:,:,r0,r1], axis=1))

                # Get rhs integrand
                # -----                     
                for m in range(D):
                    if m==0: 
                        r=r0
                    elif m==1:
                        r=r1
                    else: 
                        raise Exception("m != 0,1. This is impossible, since num_dims={}".format(D))

                    rhs_cpro_inte_5[:,:,r0,r1,m] = cond_4[:,:,r0,r1]*refs_1[r]*leng_1[m]


        # Sum over references
        # -----
        rhs_cpro_3 = -numpy.sum(a=numpy.sum(a=rhs_cpro_inte_5, axis=3), axis=2) # sum over r1 then r0
        # NB: rhs of cell problem has minus sign by definition.

        lhs_cpro_2 =  numpy.sum(a=numpy.sum(a=lhs_inte_4, axis=3), axis=2) # sum over r1 then r0


        # Force a unique solution 
        # -------
        #lhs_cpro_2[-1,:] = numpy.zeros(num_nodes)
        #lhs_cpro_2[-1,-1] = 1
        #rhs_cpro_3[-1,:,0] = numpy.zeros(num_nodes)
        #rhs_cpro_3[-1,:,1] = numpy.zeros(num_nodes)

        return (lhs_cpro_2, rhs_cpro_3)


    def step_cell_problem(self, lhs_cpro_2, rhs_cpro_3):
        pass 
        """
        Parameters
        -----
        - lhs_2[i,j]
        - rhs_3[i,j,m]

        Returns 
        # -----
        - csol_2[i,m]
        """

        # Define readable parameters 
        # -----
        N = self.parameters.num_nodes
        D = self.parameters.num_dims 


        # Define arrays to fill
        # -----
        csol_2 = numpy.zeros(shape=(N,D))


        # Get solution
        # -----
        a_2 = lhs_cpro_2[:,:]
        for m in range(D):
            b_1 = numpy.sum(a=rhs_cpro_3[:,:,m], axis=1) # sum over j
            csol_2[:,m] = linalg.lsqr(A=a_2, b=b_1)[0]
            #sol = optimize.lsq_linear(A=a_2,b=b_1)
            #csol_3[k,:,m] = sol.x

        return csol_2


    def get_delta(self, csol_2, refs_1, leng_1)->numpy.ndarray:
        """Get delta.

        Parameters
        ----------
        csol_2 : numpy.ndarray
            csol_2[i,m] is cell solution at node i in direction m.
        refs_1 : numpy.ndarray
            refs_1[r] is reference at index r in {0,1,-1}.
        leng_1 : numpy.ndarray
            leng_1[m] is length in direction m.
        
        Returns
        -------
        delt_4 : numpy.ndarray
            delt_4[i,j,r,m] is difference in cell solutions at nodes i and j in direction m with weight r.
        """
        # Define readable parameters 
        # -----
        N = self.parameters.num_nodes
        D = self.parameters.num_dims 
        R = self.parameters.num_refs 
        

        # Make array to be filled
        # -----
        delt_4 = numpy.zeros(shape=(N,N,R,D))
        
        
        # Fill using definition of delta
        # -----
        for i in range(N):
            for j in range(N):
                for r in range(R):
                    for m in range(D):
                        delt_4[i,j,r,m] = csol_2[i,m] - (csol_2[j,m] + refs_1[r]*leng_1[m])
        return delt_4
    

    def get_heaviside(self, delt_4:numpy.ndarray)->numpy.ndarray:
        """_summary_

        Parameters
        ----------
        delt_4 : numpy.ndarray
            _description_

        Returns
        -------
        heav_4 : numpy.ndarray
            _description_
        """
        tol = 1E-5
        heav_4 = (delt_4>tol).astype(int)
        return heav_4


    def get_permeability_and_adhesivity(self, adhe_4, cond_4, delt_4, heav_4, refs_1, leng_1):
        # Define readable parameters 
        # -----
        N = self.parameters.num_nodes 
        R = self.parameters.num_refs  
        D = self.parameters.num_dims  


        # Make arrays to fill
        # -----
        perm_inte_6 = numpy.zeros(shape=(N,N,R,R,D,D))
        # perm_inte_7[i,j,r0,r1,m,n]
        depo_inte_5 = numpy.zeros(shape=(N,N,R,R,D))
        # depo_inte_6[i,j,r0,r1,m]


        # Get permeability and adhesivity integrands
        # ------
        for m in range(D):
            for n in range(D):
                for r0 in range(R):
                    for r1 in range(R):
                        if m==0: 
                            rm=r0
                        elif m==1:
                            rm=r1
                        else: 
                            raise Exception("m != 0,1. This is impossible, since the problem is 2D.")
                        if n==0: 
                            rn=r0
                        elif n==1:
                            rn=r1
                        else: 
                            raise Exception("n != 0,1. This is impossible, since the problem is 2D.")
                        # Get depo and perm
                        # -----
                        perm_inte_6[:,:,r0,r1,m,n] = refs_1[rm]*cond_4[:,:,r0,r1]*(-delt_4[:,:,rn,n])
                        depo_inte_5[:,:,r0,r1,m]   = adhe_4[:,:,r0,r1]*cond_4[:,:,r0,r1]*(-delt_4[:,:,rm,m])*heav_4[:,:,rm,m]
                        # TODO: Check heav definition and indexing


        # Sums
        # -----
        perm_5 = numpy.sum(a=perm_inte_6, axis=3) # sum over r1
        perm_4 = numpy.sum(a=perm_5, axis=2) # sum over r0
        perm_3 = numpy.sum(a=perm_4, axis=1) # sum over j
        perm_2 = numpy.sum(a=perm_3, axis=0) # sum over i
        # perm_2[m,n]    

        depo_4 = numpy.sum(a=depo_inte_5, axis=3) # sum over r1
        depo_3 = numpy.sum(a=depo_4, axis=2) # sum over r0
        depo_2 = numpy.sum(a=depo_3, axis=1) # sum over j
        depo_1 = numpy.sum(a=depo_2, axis=0) # sum over i
        # depo_2[m]


        # Multiply by prefactors
        # -----
        for m in range(D):
            for n in range(D):
                perm_2[m,n] = 0.5*(leng_1[m]/numpy.prod(leng_1))*perm_2[m,n]

        depo_1 = -(1/numpy.prod(leng_1))*depo_1

        return (perm_2, depo_1)


        
class Deposition(Base):
    """_summary_

    """
    def __init__(self, parameters:parameters.Parameters):
        """_summary_
        """
        super().__init__(parameters=parameters)
        pass

    # Attributes
    # -----        

    # Methods
    # -----      
    def get_conductance_problem(self, cond_4, adhe_4, effe_4, delt_4):
        N = self.parameters.num_nodes
        R = self.parameters.num_refs

        rhs_4 = numpy.zeros(shape=(N,N,R,R))
        for r0 in range(R):
            for r1 in range(R): 
                rhs_4[:,:,r0,r1] = effe_4[:,:,r0,r1]*adhe_4[:,:,r0,r1]*abs(delt_4[:,:,r0,0])*cond_4[:,:,r0,r1]**(3.0/2.0) 
        return rhs_4

    def step_conductance_problem(self, cond_4, rhs_4, diff_tlik):
        cond_new_4 = cond_4  - diff_tlik*rhs_4
        return cond_new_4