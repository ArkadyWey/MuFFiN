import numpy 
import scipy.linalg as linalg

import muffin.parameters.parameters as parameters
import muffin.cells.cells as cells

class Base():
    """_summary_
    """
    def __init__(self, parameters:parameters.Parameters, 
                       cell): # TODO: :cells.Base - Make base class for cells
        """_summary_
        """

    # Attributes
    # -----        
        self.parameters = parameters
        self.cell = cell    
    
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
        leng_1 = self.cell.leng_1
        

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

    # ---- Submethods ----
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
        pass
        ## Get params
        ## -----
        #num_nodes = parameters.num_nodes
        #num_refs  = parameters.num_refs # 3
        #num_dims  = parameters.num_dims # 2
        #
        #
        ## Make array to be filled
        ## -----
        #delt_4 = numpy.zeros(shape=(num_nodes,num_nodes,num_refs,num_dims))
        #
        #
        ## Fill using definition of delta
        ## -----
        #for i in range(num_nodes):
        #    for j in range(num_nodes):
        #        for r in range(num_refs):
        #            for m in range(num_dims):
        #                delt_4[i,j,r,m] = csol_2[i,m] - (csol_2[j,m] + refs_1[r]*leng_1[m])
        # return delt_4
    
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


        
class Deposition(Base):
    """_summary_

    """
    def __init__(self, parameters:parameters.Parameters,
                       cell):
        """_summary_
        """
        super().__init__(parameters=parameters, cell=cell)
        pass

    # Attributes
    # -----        

    # Methods
    # -----      
    def get_conductance_problem(self, cond_4, adhe_4, effe_4, delt_4):
        rhs_4 = effe_4*adhe_4*delt_4*cond_4**(3/2)
        return rhs_4

    def step_conductance_problem(self, cond_4, rhs_4, diff_tlik):
        cond_new_4 = cond_4  - diff_tlik*rhs_4
        return cond_new_4