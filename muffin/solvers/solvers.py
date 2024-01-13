import muffin.equations_preprocess.equations_preprocess as equations_preprocess
import muffin.parameters.parameters as parameters
import muffin.solutions.solutions as solutions

class Explicit():
    """_summary_
    """
    def __init__(self, parameters:parameters.Parameters,
                       cell,
                       equations_preprocess, 
                       solution): 
        """_summary_
        """

    # Attributes
    # -----
        self.parameters = parameters 
        self.cell = cell
        self.equations_preprocess = equations_preprocess
        self.solution = solution 

    # Methods 
    # -----
    def solve(self):
        for s in range(self.parameters.tlik_max):
            if s==0:
                self.solution.cond_5[s,:,:,:,:] = self.cell.cond_4
            elif s!=0:
                # Conductance problem 
                # -----
                rhs_4 = self.equations_preprocess.get_conductance_problem(cond_4=self.solution.cond_5[s-1,:,:,:,:], 
                                                                          adhe_4=self.cell.adhe_4, 
                                                                          effe_4=self.cell.effe_4, 
                                                                          delt_4=self.solution.delt_5[s-1,:,:,:,:])

                self.solution.cond_5[s,:,:,:,:] = self.equations_preprocess.step_conductance_problem(cond_4=self.solution.cond_5[s-1,:,:,:,:], 
                                                                                                     rhs_4=rhs_4, 
                                                                                                     diff_tlik=self.parameters.diff_tlik)
        
            # Cell problem 
            # -----
            (lhs_cpro_2, rhs_cpro_3) = self.equations_preprocess.get_cell_problem(cond_4=self.solution.cond_5[s,:,:,:,:])
            self.solution.csol_3[s,:,:] = self.equations_preprocess.step_cell_problem(lhs_cpro_2=lhs_cpro_2, rhs_cpro_3=rhs_cpro_3)    
        
            # Other 
            # -----
            self.solution.delt_5[s,:,:,:,:] = self.equations_preprocess.get_delta(csol_2=self.solution.csol_3[s,:,:], 
                                                                                  refs_1=self.parameters.refs_1, 
                                                                                  leng_1=self.cell.leng_1)
            
            self.solution.heav_5[s,:,:,:,:] = self.equations_preprocess.get_heaviside(delt_4=self.solution.delt_5[s,:,:,:,:])

            (self.solution.perm_3[s,:,:], self.solution.depo_2[s,:]) = self.equations_preprocess.get_permeability_and_adhesivity(adhe_4=self.cell.adhe_4, 
                                                                                                                               cond_4=self.solution.cond_5[s,:,:,:,:], 
                                                                                                                               delt_4=self.solution.delt_5[s,:,:,:,:], 
                                                                                                                               heav_4=self.solution.heav_5[s,:,:,:,:], 
                                                                                                                               refs_1=self.parameters.refs_1, 
                                                                                                                               leng_1=self.cell.leng_1)
