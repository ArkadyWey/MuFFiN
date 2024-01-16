import muffin.equations_preprocess.equations_preprocess as equations_preprocess
import muffin.parameters.parameters as parameters
import muffin.solutions.solutions as solutions
import muffin.solvers.solvers as solvers
import muffin.plotters.plotters as plotters

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
        
        self.solution = self.get_solution()
        self.solver   = self.get_solver(option_solver=option_solver)
        self.plotter  = self.get_plotter()
        

    def get_solver(self, option_solver):
        if option_solver == "explicit":
            solver = solvers.Explicit(parameters = self.parameters, 
                                      cell = self.cell, 
                                      equations_preprocess = self.equations_preprocess, 
                                      solution=self.solution)
        
        else: 
            # TODO: Add other solvers
            raise Exception("option_solver must be 'explicit'. option_solver=={} is not implemented.".format(option_solver))
        return solver


    def get_solution(self):
        solution = solutions.Solution(parameters=self.parameters)
        return solution


    def get_plotter(self):
        plotter = plotters.Plotter(parameters = self.parameters, 
                                  solution=self.solution)
        return plotter


    def solve(self):
        """Call self.solver.solve() to solve self.equations_preprocess 
        given self.parameters and self.cell.
        """
        self.solver.solve()


    def plot(self, type_plot:str="all", variable_name:str="conductance", indices:dict={"i":0,"j":1,"r0":0,"r1":0,"r":0,"m":0,"n":0}):
        """Produce figures of the solution.

        Parameters
        ----------
        type_plot : str, optional
            The type of plots to produce, by default "all". Options are "all", "single", or "distributions".
            "all" produces a plot of each solution variable as a function of the time-like variable.
            "single" produces a plot of the specified solution variable as a function of the time-like variable.
            "distributions" produces plots for the distributions of the initial permeability and adhesivity.
        y : str, optional
            The variable to plot when type_plot==single, by default "conductance".
        indices : dict, optional
            The indices of the variables to be plotted, by default {"i":0,"j":1,"r0":0,"r1":0,"m":0,"n":0}.

        Raises
        ------
        Exception
            Non-implemented type_plot choices.
        """
        if type_plot == "all":
            self.plotter.plot_all(indices=indices)
        elif type_plot == "single":
            self.plotter.plot_single(variable_name=variable_name, indices=indices)
        elif type_plot == "distributions":
            self.plotter.plot_distributions(indices=indices)
        else: 
            raise Exception("type_plot must be 'all' or 'single'. type_plot=={} is not implemented.".format(type_plot))


    def save(self, type_save:str="all", variable_name:str="conductance"):
        if type_save == "all":
            self.solution.save_all()
        elif type_save == "single":
            self.solution.save_single(variable_name=variable_name)
        else: 
            raise Exception("type_save must be 'all' or 'single'. type_save=={} is not implemented.".format(type_save))


    def load(self, type_load:str="all", variable_name:str="conductance"):
        if type_load == "all":
            self.solution.load_all()
        elif type_load == "single":
            self.solution.load_single(variable_name=variable_name)
        else: 
            raise Exception("type_load must be 'all' or 'single'. type_load=={} is not implemented.".format(type_load))
