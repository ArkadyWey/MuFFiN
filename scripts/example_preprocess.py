import muffin.parameters.parameters as parameters
import muffin.cells.four_regular as four_regular
import muffin.cells.six_regular as six_regular
import muffin.cells.six_irregular as six_irregular
import muffin.equations_preprocess.equations_preprocess as equations_preprocess
import muffin.equations_flow.equations_flow as equations_flow
import muffin.solvers.solvers as solvers
import muffin.models.models as models
import muffin.plotters.plotting as plotting

import matplotlib.pyplot as plt
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

    
    print("Getting Parameters...") 
    parameters = parameters.Parameters()

    #print(parameters.dictionary)

    print("Getting Cell...") 
    cell = four_regular.FourRegular(parameters=parameters)

    print("Getting Equations (Preprocess)...") 
    equations = equations_preprocess.Deposition(parameters=parameters)
    
    print("Getting Equations (Flow)...") 
    equations_flow = equations_flow.Base(parameters=parameters)

    print("Getting Model...") 
    model = models.Model(parameters=parameters, cell=cell, equations_preprocess=equations, equations_flow=equations_flow)
    
    #solver = solvers.Explicit(parameters=parameters, cell=cell, equations_preprocess=equations)
    #solver.solve()

    #model.solver.solve() or
    print("Solving (Preprocess and Flow)...") 
    model.solve(type_solve="all")
    
    #print("Solving (Flow)...") 
    #model.solve(type_solve="flow")

    # print("Saving...")
    # model.save(type_save="preprocess")
    # model.save(type_save="all")
    #model.load(type_load="all", y="permeability")
    
    print("Plotting...") 
    model.plot(type_solution="all")# , y_name="permeability")

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
                                 y_top=1, 
                                 legend_on=False)

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
    ax.plot(tlik_1, parameters.alph*4/((parameters.alph*parameters.beta*tlik_1+2)**2), color="tab:orange", ls="--")

    plotting.thesisify_post_plot(ax=ax,
                                 x_label=r"$s$",
                                 y_label=r"$j^{1}$",
                                 x_left=0,
                                 x_right=parameters.tlik_max,
                                 y_bottom=0,
                                 y_top=1)

    plotting.save_fig(fig=fig,fname=os.path.join(parameters.path,"depo_prep__2__v__s_1.svg"), format="svg")


    # Plot concentration 
    # -----
    plotting.thesisify_pre_ax_creation()
    fig, ax = plt.subplots(1,1)

    posi_1 = parameters.posi_1

    ax.plot(posi_1, model.solution_flow.conc_2[2,:], color="tab:blue", ls="-")
    print(model.solution_flow.conc_2[0,:])
    print(model.solution_flow.conc_2[1,:])
    print(model.solution_flow.conc_2[2,:])
    print(model.solution_flow.conc_2[3,:])
    print(model.solution_flow.conc_2[4,:])
    print(model.solution_flow.conc_2[5,:])

    plotting.thesisify_post_plot(ax=ax,
                                 x_label=r"$x$",
                                 y_label=r"$c$",
                                 x_left=0,
                                 x_right=1,
                                 y_bottom=0,
                                 y_top=1)

    plotting.save_fig(fig=fig,fname=os.path.join(parameters.path,"conc_2__v__time_1.svg"), format="svg")