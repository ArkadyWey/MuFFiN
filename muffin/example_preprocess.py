

parameters = muffin.parameters.Parameters()
cell = muffin.cells.FourRegular(parameters)
equations_preprocess = muffin.equations.preprocess.deposition_flux_dependent.Deposition_FluxDependent(parameters)

problem = muffin.problem.Problem(parameters, cell,equations_preprocess)

problem.solve(problem_type="preprocess")

solution = problem.solution(problem_type="preprocess")

solution.plot() # plot all variables against s

pressure = solution.pressure

pressure.plot()