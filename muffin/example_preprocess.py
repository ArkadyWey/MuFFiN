import muffin.parameters.parameters as parameters
import muffin.cells.four_regular as four_regular
import muffin.cells.six_regular as six_regular
import muffin.cells.six_irregular as six_irregular
import muffin.equations_preprocess.equations_preprocess as equations_preprocess
import muffin.solvers.solvers as solvers
import muffin.models.models as models

import matplotlib.pyplot as plt
import numpy
import sys
sys.path.append("/home/user/utils_python")
import plotting
import os

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

    print(parameters.dictionary)

    cell = four_regular.FourRegular(parameters=parameters)

    equations = equations_preprocess.Deposition(parameters=parameters)

    model = models.Model(parameters=parameters, cell=cell, equations_preprocess=equations)
    
    #model.solver.solve() or
    model.solve()

    print(model.solution.cond_5[100,:,:,0,0])


    #solver = solvers.Explicit(parameters=parameters, cell=cell, equations_preprocess=equations)

    #solver.solve()
    # model = models.Model(parameters, cell, equations, solver)

    # model.solver.solve()

    # model.solution.plot()

    # model.solution.save()

    # model.solution.load()



    # Plot permeability 
    # -----
    plotting.thesisify_pre_ax_creation()
    fig, ax = plt.subplots(1,1)

    # Choose dimensions to plot
    m = 0
    n = 0

    tlik_1 = parameters.tlik_1

    ax.plot(tlik_1, model.solution.perm_3[:,m,n], color="tab:blue", ls="-")
    ax.plot(tlik_1, 4/((parameters.alph*parameters.beta*tlik_1+2)**2), color="tab:orange", ls="--")

    plotting.thesisify_post_plot(ax=ax,
                                 x_label=r"$s$",
                                 y_label=r"$k^{11}$",
                                 x_left=0,
                                 x_right=1000,
                                 y_bottom=0,
                                 y_top=1)

    plotting.save_fig(fig=fig,fname=os.path.join(parameters.path,"perm_prep__3__v__s_1.svg"), format="svg")




    # Plot adhesivity 
    # -----
    # TODO: Add plotting as subpackage
    plotting.thesisify_pre_ax_creation()
    fig, ax = plt.subplots(1,1)

    # Choose dimensions to plot
    m = 0

    tlik_1 = parameters.tlik_1

    ax.plot(tlik_1, model.solution.depo_2[:,m], color="tab:blue", ls="-")
    ax.plot(tlik_1, 4/((parameters.alph*parameters.beta*tlik_1+2)**2), color="tab:orange", ls="--")

    plotting.thesisify_post_plot(ax=ax,
                                 x_label=r"$s$",
                                 y_label=r"$j^{1}$",
                                 x_left=0,
                                 x_right=parameters.tlik_max,
                                 y_bottom=0,
                                 y_top=1)

    plotting.save_fig(fig=fig,fname=os.path.join(parameters.path,"depo_prep__2__v__s_1.svg"), format="svg")