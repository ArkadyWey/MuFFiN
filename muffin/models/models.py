import muffin.equations_preprocess.equations_preprocess as equations_preprocess
import muffin.parameters.parameters as parameters
import muffin.solutions.solutions as solutions
import muffin.solvers.solvers as solvers

class Model():
    """_summary_
    """
    def __init__(self, parameters:parameters.Parameters,
                       cell,
                       equations_preprocess, 
                       option_solver="explicit"): 
        """_summary_
        """

    # Attributes
    # -----
        self.parameters = parameters
        self.cell       = cell
        self.equations_preprocess = equations_preprocess
        
        self.solution = solutions.Solution(parameters=self.parameters)
        self.solver = self.get_solver(option_solver=option_solver)
        

    def get_solver(self, option_solver):
        if option_solver == "explicit":
            solver = solvers.Explicit(parameters = self.parameters, 
                                      cell = self.cell, 
                                      equations_preprocess = self.equations_preprocess, 
                                      solution=self.solution)
        
        else: 
            raise Exception("Solver option_solver must be 'explicit', {} is not implemented.".format(option_solver))
        
        return solver
    
    def solve(self):
        """Call self.solver.solve() to solve self.equations_preprocess 
        given self.parameters and self.cell.
        """
        self.solver.solve()
