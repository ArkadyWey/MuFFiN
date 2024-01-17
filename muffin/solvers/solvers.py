import muffin.equations_preprocess.equations_preprocess as equations_preprocess
import muffin.parameters.parameters as parameters
import muffin.solutions.solutions as solutions

class Explicit():
    """_summary_
    """
    def __init__(self, parameters:parameters.Parameters,
                       cell,
                       equations_preprocess:equations_preprocess.Deposition, # TODO: Implement abstract class since can be others
                       solution:solutions.Solution): 
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
    def solve_preprocess(self):
        for s in range(self.parameters.tlik_max):
            # Conductance problem 
            # -----
            if s==0:
                self.solution.cond_5[s,:,:,:,:] = self.cell.cond_4
            elif s!=0:
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
                                                                                                                            
        self.solution.get_dictionary()


    def solve_flow(self):
        for i_t in range(self.parameters.time_max):
            # Concentration problem 
            # -----
            if i_t==0: 
                self.solution.conc_2[i_t,:] = self.domain.conc_1 # initial condition
            elif i_t!=0:
                rhs_1 = self.equations_flow.get_concentration_problem(conc_1=self.solution_flow.conc_2[i_t-1,:], 
                                                                      psi_1=self.solution_flow.psi_2[i_t-1,:]
                                                                      velo=self.solution_flow.velo_1[i_t-1],
                                                                      phi=self.parameters.phi, 
                                                                      diff_posi=self.parameters.diff_posi)

                self.solution.conc_2[i_t,:] = self.equations_preprocess.step_conductance_problem(conc_1=self.solution_flow.conc_2[i_t-1,:], 
                                                                                                 rhs_1=rhs_1, 
                                                                                                 diff_time=self.parameters.diff_time)
        self.solution_flow.get_dictionary()