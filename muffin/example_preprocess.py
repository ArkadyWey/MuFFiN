import muffin.parameters.parameters as parameters
import muffin.cells.four_regular as four_regular
import muffin.cells.six_regular as six_regular
import muffin.cells.six_irregular as six_irregular
import muffin.equations_preprocess.equations_preprocess as equations_preprocess

# parameters = muffin.parameters.Parameters()

# cell = muffin.cells.FourRegular(parameters)
# equations_preprocess = muffin.equations.preprocess.deposition_flux_dependent.Deposition_FluxDependent(parameters)

# problem = muffin.problem.Problem(parameters, cell,equations_preprocess)

# problem.solve(problem_type="preprocess")

# solution = problem.solution(problem_type="preprocess")

# solution.plot() # plot all variables against s

# pressure = solution.pressure

# pressure.plot()

# problem.save() # save sims and plots, just sims, or just plots

if __name__ == "__main__":

    parameters = parameters.Parameters()

    cell = four_regular.FourRegular(parameters=parameters)

    equations = equations_preprocess.Deposition(parameters=parameters, cell=cell)

    # solver = solvers.Explicit()

    # model = models.Model(parameters, cell, equations, solver)

    # model.solver.solve()

    # model.solution.plot()

    # model.solution.save()

    # model.solution.load()
    