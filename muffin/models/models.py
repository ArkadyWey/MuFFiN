import muffin.equations_preprocess.equations_preprocess as equations_preprocess
import muffin.equations_flow.equations_flow as equations_flow
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
                       equations_flow,
                       option_solver:str="explicit", 
                       show_on:bool=False): 
        """_summary_
        """

    # Attributes
    # -----
        self.parameters = parameters
        self.cell       = cell
        self.equations_preprocess = equations_preprocess
        self.equations_flow = equations_flow
        self.show_on:bool = show_on
        
        self.solution, self.solution_flow = self.get_solution()
        self.solver = self.get_solver(option_solver=option_solver)
        self.plotter_preprocess, self.plotter_flow = self.get_plotter()
        

    def get_solver(self, option_solver):
        if option_solver == "explicit":
            solver = solvers.Explicit(parameters = self.parameters, 
                                      cell = self.cell, 
                                      equations_preprocess = self.equations_preprocess, 
                                      solution=self.solution, 
                                      equations_flow=self.equations_flow, 
                                      solution_flow=self.solution_flow)
        
        else: 
            # TODO: Add other solvers
            raise Exception("option_solver must be 'explicit'. {} is not implemented.".format(option_solver))
        return solver


    def get_solution(self, type_solution:str="all"):
        if type_solution=="all":
            solution      = solutions.Solution(parameters=self.parameters)
            solution_flow = solutions.Solution_Flow(parameters=self.parameters)
        elif type_solution=="preprocess":
            solution      = solutions.Solution(parameters=self.parameters)
            solution_flow = None
        elif type_solution=="flow":
            solution = None
            solution_flow = solutions.Solution_Flow(parameters=self.parameters)
        else: 
            raise Exception("typle_solution must be 'all' or 'preprocess' or 'flow'. {} is not implemented.".format(type_solution))
        return solution, solution_flow


    def get_plotter(self, type_plotter:str="all"):

        if type_plotter=="all":
            plotter_preprocess = plotters.Plotter_Preprocess(parameters = self.parameters, 
                                                             solution=self.solution, 
                                                             show_on=self.show_on)
            plotter_flow = plotters.Plotter_Flow(parameters = self.parameters, 
                                                 solution_flow=self.solution_flow, 
                                                 show_on=self.show_on)
        elif type_plotter=="preprocess":
            plotter_preprocess = plotters.Plotter_Preprocess(parameters = self.parameters, 
                                                             solution=self.solution, 
                                                             show_on=self.show_on)
            plotter_flow = None
        elif type_plotter=="flow":
            plotter_preprocess = None
            plotter_flow = plotters.Plotter_Flow(parameters = self.parameters, 
                                                 solution_flow=self.solution_flow, 
                                                 show_on=self.show_on)

        return plotter_preprocess, plotter_flow


    def solve(self, type_solve:str="all"):
        """Call self.solver.solve() to solve self.equations_preprocess 
        given self.parameters and self.cell.
        """
        if type_solve=="preprocess":
            self.solver.solve_preprocess()
        elif type_solve=="flow":
            self.solver.solve_flow()
        elif type_solve=="all":
            self.solver.solve_preprocess()
            self.solver.solve_flow()
        else:
            raise Exception("type_solve must be 'preprocess' or 'flow' or 'all'. {} is not implemented".format(type_solve))


    def plot(self, type_solution:str="all", type_plot:str="all", y_name:str="conductance", 
                   indices:dict={"i":0,"j":1,"r0":0,"r1":0,"r":0,"m":0,"n":0}):
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
        if type_solution == "preprocess":
            if type_plot == "all":
                self.plotter_preprocess.plot_all(indices=indices)
            elif type_plot == "single":
                self.plotter_preprocess.plot_single(y_name=y_name, indices=indices)
            else: 
                raise Exception("type_plot must be 'all' or 'single'. {} is not implemented.".format(type_plot))

        elif type_solution == "flow":
            if type_plot == "all":
                self.plotter_flow.plot_all()
            elif type_plot == "single":
                self.plotter_flow.plot_single(y_name=y_name)
            else: 
                raise Exception("type_plot must be 'all' or 'single'. {} is not implemented.".format(type_plot))

        elif type_solution == "all":
            if type_plot == "all":
                self.plotter_preprocess.plot_all(indices=indices)
                self.plotter_flow.plot_all()
            elif type_plot == "single":
                self.plotter_preprocess.plot_single(y_name=y_name, indices=indices)
                self.plotter_flow.plot_single(y_name=y_name)
            else: 
                raise Exception("type_plot must be 'all' or 'single'. {} is not implemented.".format(type_plot))

        else: 
            raise Exception("type_solution must be 'all' or 'preprocess' or 'flow'. {} is not implemented.".format(type_plot))



    def save(self, type_save:str="all", variable_name:str="conductance"):
        if type_save == "all":
            self.solution.save_all()
            self.solution_flow.save_all()
        elif type_save == "single":
            self.solution.save_single(variable_name=variable_name)
        else: 
            raise Exception("type_save must be 'all' or 'single'. {} is not implemented.".format(type_save))


    def load(self, type_load:str="all", variable_name:str="conductance"):
        if type_load == "all":
            self.solution.load_all()
        elif type_load == "single":
            self.solution.load_single(variable_name=variable_name)
        else: 
            raise Exception("type_load must be 'all' or 'single'. {} is not implemented.".format(type_load))
