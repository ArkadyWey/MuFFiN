import numpy 
import scipy.sparse.linalg as linalg

import muffin.parameters.parameters as parameters

class Base():
    """Get base equations for the preprocessing step of the solver.

    Equations for the preprocessing step are equations that involve microscale variables 
    but not macroscale variables. 
    Base equations in this step are equations that do not depend on the particle
    deposition method.
    Equations that do depend on the particle deposition method then inherit from this 
    base class.
    """
    def __init__(self, parameters:parameters.Parameters): # TODO: :cells.Base - Make base class for cells
        """Define parameters as attributes.

        Parameters
        ----------
        parameters : parameters.parameters.Parameters
            Parameters of the problem, held in the Parameters class.
        """

    # Attributes
    # -----        
        self.parameters:parameters.Parameters = parameters
    
    # Methods
    # -----        
    def get_cell_problem(self, cond_4:numpy.ndarray)->tuple:
        """Get the left hand side and right hand side of the cell problem.
        The cell problem is a linear equation of the form Ax=b.

        Parameters
        ----------
        cond_4 : numpy.ndarray
            Conductance of edges in the cell. 
            Note that cond_4[i,j,r0,r1] is the conductance of the edge 
            between node i and node j in the cell at position r0, r1 relative to the cell containing node i.

        Returns
        -------
        (lhs_cpro_2, rhs_cpro_3) : tuple(numpy.ndarray, numpy.ndarray)
            Left hand side and right hand side of cell problem. 
            Note that lhs_cpro_2[i,j] is the element of the left hand matrix for nodes i and j, 
            and rhs_cpro_3[i,j,m] is the element of the right hand matrix for nodes i and j in direction m.
        """
        
        
        # Define readable parameters 
        # -----
        N = self.parameters.num_nodes
        R = self.parameters.num_refs
        D = self.parameters.num_dims
        
        refs_1 = self.parameters.refs_1
        leng_1 = self.parameters.leng_1
        

        # Define arrays to fill
        # -----
        rhs_cpro_inte_5 = numpy.empty(shape=(N,N,R,R,D))
        # rhs_cpro_inte_5[i,j,r0,r1,m].
        
        lhs_inte_4 = numpy.empty(shape=(N,N,R,R))
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


    def step_cell_problem(self, lhs_cpro_2:numpy.ndarray, rhs_cpro_3:numpy.ndarray)->numpy.ndarray:
        """Solve the cell problem.
        The cell problem is a linear equation of the form Ax=b.

        Parameters
        ----------
        lhs_cpro_2 : numpy.ndarray
            Left hand side of the cell problem.
            Note that lhs_cpro_2[i,j] is the element of the left hand matrix for nodes i and j.
        rhs_cpro_3 : numpy.ndarray
            Right hand side of cell problem. 
            Note that rhs_cpro_3[i,j,m] is the element of the right hand matrix for nodes i and j 
            in direction m.
        
        Returns
        -------
        csol_2 : numpy.ndarray
            Cell solution. 
            Note that csol_2[i,m] is the cell solution at node i in direction m.
        """

        # Define readable parameters 
        # -----
        N = self.parameters.num_nodes
        D = self.parameters.num_dims 


        # Define arrays to fill
        # -----
        csol_2 = numpy.empty(shape=(N,D))
        # csol_2[i,m]


        # Get solution
        # -----
        a_2 = lhs_cpro_2[:,:]
        for m in range(D):
            b_1 = numpy.sum(a=rhs_cpro_3[:,:,m], axis=1) # sum over j
            csol_2[:,m] = linalg.lsqr(A=a_2, b=b_1)[0]

            # TODO: Consider -- 
            #sol = optimize.lsq_linear(A=a_2,b=b_1)
            #csol_3[k,:,m] = sol.x

        return csol_2


    def get_delta(self, csol_2:numpy.ndarray, refs_1:numpy.ndarray, leng_1:numpy.ndarray)->numpy.ndarray:
        """Get delta. 
        Delta is a tensor that holds information about the difference between cell solutions
        at different nodes.

        Parameters
        ----------
        csol_2 : numpy.ndarray
            Cell solution. 
            Note that csol_2[i,m] is the cell solution at node i in direction m.
        refs_1 : numpy.ndarray
            Reference indices that describe the displacement the cell that contains one node from the cell
            that contains another node. For example, the edge between node i in one cell and node j in a cell 
            one cell to the right and one cell below the cell containing i is indexed by i,j,r0=1,r1=-1.
            Thus the reference indices are r=1 and r=-1.
            Note refs_1[r] is reference at index r in [0,1,-1]
        leng_1 : numpy.ndarray
            The lengths of the edges of the recangular macroscale domain.
            Note that leng_1[m] is the length in direction m.

        Returns
        -------
        delt_4 : numpy.ndarray
            The cell solution difference.
            Note that delt_4[i,j,r,m] is difference in cell solutions at nodes i and j 
            in direction m with reference r.
        """


        # Define readable parameters 
        # -----
        N = self.parameters.num_nodes
        D = self.parameters.num_dims 
        R = self.parameters.num_refs 
        

        # Make array to be filled
        # -----
        delt_4 = numpy.empty(shape=(N,N,R,D))
        
        
        # Fill using definition of delta
        # -----
        for i in range(N):
            for j in range(N):
                for r in range(R):
                    for m in range(D):
                        delt_4[i,j,r,m] = csol_2[i,m] - (csol_2[j,m] + refs_1[r]*leng_1[m])
        return delt_4
    

    def get_heaviside(self, delt_4:numpy.ndarray)->numpy.ndarray:
        """Get the Heaviside function. 
        Heaviside is a tensor that holds information about the sign of the difference between cell solutions
        at different nodes. This is positive only when the difference tensor indicates 
        that information is conducted in the direction of the pressure gradient. 
        Note that the tolerance is arbitrarily set at 1E-5 so delt_4 values smaller than this 
        result in zero contribution to adhesivity.

        Parameters
        ----------
        delt_4 : numpy.ndarray
            The cell solution difference.
            Note that delt_4[i,j,r,m] is difference in cell solutions at nodes i and j 
            in direction m with reference r.
            

        Returns
        -------
        heav_4 : numpy.ndarray
            The cell solution difference sign. An indicator for flow along an edge with a component 
            in the direction of the pressure gradient.
            Note that heav_4[i,j,r,m] == 1 if the difference in cell solutions at nodes i and j 
            in direction m with reference r is positive (i.e., above the tolerance), and zero otherwise. 
        """
        tol = 1E-5
        heav_4 = (delt_4>tol).astype(int)
        return heav_4


    def get_permeability_and_adhesivity(self, adhe_4:numpy.ndarray, cond_4:numpy.ndarray, 
                                              delt_4:numpy.ndarray, heav_4:numpy.ndarray, 
                                              refs_1:numpy.ndarray, leng_1:numpy.ndarray)->tuple:
        """Get the permeability and adhesivity. 
        These are the two parameters of the macroscale system.

        Parameters
        ----------
        adhe_4 : numpy.ndarray
            Adherence of edges in the cell. 
            Note that adhe_4[i,j,r0,r1] is the adherence of the edge 
            between node i and node j in the cell at position r0, r1 relative to the cell containing node i.

        cond_4 : numpy.ndarray
            Conductance of edges in the cell. 
            Note that cond_4[i,j,r0,r1] is the conductance of the edge 
            between node i and node j in the cell at position r0, r1 relative to the cell containing node i.

        delt_4 : numpy.ndarray
            The cell solution difference.
            Note that delt_4[i,j,r,m] is difference in cell solutions at nodes i and j 
            in direction m with reference r.

        heav_4 : numpy.ndarray
            The cell solution difference sign. An indicator for flow along an edge with a component 
            in the direction of the pressure gradient.
            Note that heav_4[i,j,r,m] == 1 if the difference in cell solutions at nodes i and j 
            in direction m with reference r is positive (i.e., above the tolerance), and zero otherwise. 

        refs_1 : numpy.ndarray
            Reference indices that describe the displacement the cell that contains one node from the cell
            that contains another node. For example, the edge between node i in one cell and node j in a cell 
            one cell to the right and one cell below the cell containing i is indexed by i,j,r0=1,r1=-1.
            Thus the reference indices are r=1 and r=-1.
            Note refs_1[r] is reference at index r in [0,1,-1].

        leng_1 : numpy.ndarray
            The lengths of the edges of the recangular macroscale domain.
            Note that leng_1[m] is the length in direction m.

        Returns
        -------
        (perm_2, depo_1) : tuple(numpy.ndarray,numpy.ndarray)
            The permeability, which is the effective conductance, and the adhesivity, which is the effective adherence.
            Note that perm_2[m,n] is the permeability in the n direction of the face in the m direction.
            Note that depo_1[m] is the adhesivity in the m direction.
        """
        
        # Define readable parameters 
        # -----
        N = self.parameters.num_nodes 
        R = self.parameters.num_refs  
        D = self.parameters.num_dims  


        # Make arrays to fill
        # -----
        perm_inte_6 = numpy.empty(shape=(N,N,R,R,D,D))
        # perm_inte_7[i,j,r0,r1,m,n]

        depo_inte_5 = numpy.empty(shape=(N,N,R,R,D))
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
    """Get non-base equations for the preprocessing step of the solver.

    Equations for the preprocessing step are equations that involve microscale variables 
    but not macroscale variables. 
    Non-base equations in this step are equations that do depend on the particle
    deposition method.
    In this class, we implement those for deposition that is proportional to the cross-sectional area  
    of the edge, which results in a conductnace decrfease that is proportional to conductance to the 
    power of 3/4.
    Note that this class inherits base methods from the base class for the equations of the preprocessing step.
    """
    def __init__(self, parameters:parameters.Parameters):
        """Inherit from base class.
        """
        super().__init__(parameters=parameters)


    # Attributes
    # -----        

    # Methods
    # -----      
    def get_conductance_problem(self, cond_4:numpy.ndarray, adhe_4:numpy.ndarray, effe_4:numpy.ndarray, delt_4:numpy.ndarray)->numpy.ndarray:
        """Get the right hand side of the equation that describes 
        how the conductance decreases as particle adhering occurs. 

        Parameters
        ----------
        adhe_4 : numpy.ndarray
            Adherence of edges in the cell. 
            Note that adhe_4[i,j,r0,r1] is the adherence of the edge 
            between node i and node j in the cell at position r0, r1 relative to the cell containing node i. 

        cond_4 : numpy.ndarray
            Conductance of edges in the cell. 
            Note that cond_4[i,j,r0,r1] is the conductance of the edge 
            between node i and node j in the cell at position r0, r1 relative to the cell containing node i.

        delt_4 : numpy.ndarray
            The cell solution difference.
            Note that delt_4[i,j,r,m] is difference in cell solutions at nodes i and j 
            in direction m with reference r.    

        effe_4 : numpy.ndarray
            Reactance of edges in the cell.
            Note that effe_4[i,j,r0,r1] is the reactance of the edge 
            between node i and node j in the cell at position r0, r1 relative to the cell containing node i.   

        Returns
        -------
        rhs_4 : numpy.ndarray
            The right hand side of the conductance equation.
            Note that rhs_4[i,j,r0,r1] is the right hand side of the equation that describes the change 
            of conductance of the edge between node i and node j in the cell at position r0, r1 relative 
            to the cell containing node i.   
        """
        
        # Define readable parameters 
        # -----
        N = self.parameters.num_nodes
        R = self.parameters.num_refs


        # Make arrays to fill
        # -----
        rhs_4 = numpy.empty(shape=(N,N,R,R))
        # rhs_4[i,j,r0,r1]
        

        # Get rhs of conductance equation
        # -----
        for r0 in range(R):
            for r1 in range(R): 
                rhs_4[:,:,r0,r1] = effe_4[:,:,r0,r1]*adhe_4[:,:,r0,r1]*abs(delt_4[:,:,r0,0])*cond_4[:,:,r0,r1]**(3.0/2.0) 

        return rhs_4


    def step_conductance_problem(self, cond_4:numpy.ndarray, rhs_4:numpy.ndarray, diff_tlik:float)->numpy.ndarray:
        """Execute one step of the equation for the change of conductance due to adhering particles.

        Parameters
        ----------
        cond_4 : numpy.ndarray
            Conductance of edges in the cell. 
            Note that cond_4[i,j,r0,r1] is the conductance of the edge 
            between node i and node j in the cell at position r0, r1 relative to the cell containing node i.
            Note that this is the current (as opposed to future) conductance.
        rhs_4 : numpy.ndarray
            The right hand side of the conductance equation.
            Note that rhs_4[i,j,r0,r1] is the right hand side of the equation that describes the change 
            of conductance of the edge between node i and node j in the cell at position r0, r1 relative 
            to the cell containing node i.   
        diff_tlik : float
            The difference between time points, that is, 'delta t'.

        Returns
        -------
        cond_new_4 : numpy.ndarray
            Conductance of edges in the cell. 
            Note that cond_4[i,j,r0,r1] is the conductance of the edge 
            between node i and node j in the cell at position r0, r1 relative to the cell containing node i.
            Note that this is the future (as opposed to current) conductance.
        """
        cond_new_4 = cond_4 - diff_tlik*rhs_4
        return cond_new_4