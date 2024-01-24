import os
import matplotlib.pyplot as plt
import numpy

import muffin.parameters.parameters as parameters
import muffin.solutions.solutions as solutions
import muffin.plotters.plotting as plotting
import muffin.utils.load_and_save as load_and_save


class Plotter():
    """_summary_
    """
    def __init__(self, parameters:parameters.Parameters): 
        """_summary_
        """


    # Attributes
    # -----
        self.parameters = parameters
        self.path_save = os.path.join(self.parameters.path, "plots")
        load_and_save.check_and_make_dir(path=self.path_save)


    # Methods
    # -----
    def plot(self, x_value:numpy.ndarray, y_value:numpy.ndarray, 
                   color:str="tab:blue", linestyle:str="-", 
                   x_label:str=None, y_label:str=None,
                   x_left:str=None, x_right:str=None, 
                   y_bottom:str=None, y_top:str=None, 
                   x_name:str=None, y_name:str=None):
        
        # Define
        plotting.thesisify_pre_ax_creation()
        fig, ax = plt.subplots(1,1)

        # Plot
        ax.plot(x_value, y_value, color=color, ls=linestyle)

        # Format
        plotting.thesisify_post_plot(ax=ax,
                                     x_label=x_label,
                                     y_label=y_label,
                                     x_left=x_left,
                                     x_right=x_right,
                                     y_bottom=y_bottom,
                                     y_top=y_top)

        # Save
        fig_name = "{}__V__{}.svg".format(x_name,y_name)
        plotting.save_fig(fig=fig, fname=os.path.join(self.path_save, fig_name), format="svg")
        
        # Close to save memory
        plt.close()


    def plot_sweep(self, x_value:numpy.ndarray, y_values:numpy.ndarray, 
                         color:str="tab:blue", linestyle:str="-", 
                         x_label:str=None, y_label:str=None,
                         x_left:str=None, x_right:str=None, 
                         y_bottom:str=None, y_top:str=None, 
                         x_name:str=None, y_name:str=None):
        # y_values second axis is different arrays 

        # Define
        plotting.thesisify_pre_ax_creation()
        fig, ax = plt.subplots(1,1)

        # Plot
        for t in range(len(y_values[0,:])):
            ax.plot(x_value, y_values[:,t], color=color, ls=linestyle)

        # Format
        plotting.thesisify_post_plot(ax=ax,
                                     x_label=x_label,
                                     y_label=y_label,
                                     x_left=x_left,
                                     x_right=x_right,
                                     y_bottom=y_bottom,
                                     y_top=y_top)

        # Save
        fig_name = "{}__V__{}.svg".format(x_name,y_name)
        plotting.save_fig(fig=fig, fname=os.path.join(self.path_save, fig_name), format="svg")
        
        # Close to save memory
        plt.close()


class Plotter_Preprocess(Plotter):
    """_summary_
    """
    def __init__(self, parameters:parameters.Parameters,
                       solution:solutions.Solution): 
        """_summary_
        """


    # Attributes
    # -----
        super().__init__(parameters=parameters)

        self.solution = solution
        self.parameters = parameters


    # Methods
    # -----
    def plot_single(self, y_name:str="conductance", indices:dict={"i":0,"j":1,"r0":0,"r1":0,"r":0,"m":0,"n":0}):
        x_meta = self.solution.dictionary["time_like"]
        y_meta = self.solution.dictionary[y_name]

        # Get correct indices of array
        y_value = y_meta["value"] # array of some shape  
        count = 0      
        for index in list(indices.keys()):
            if index in y_meta["indices"]:
                axis = y_meta["indices"].index(index)
                y_value = numpy.take(a=y_value, indices=indices[index], axis=axis-count) # count since decrease shape each time I take
                count=count+1

        self.plot(x_value=x_meta["value"], y_value=y_value, 
                  color="tab:blue", linestyle="-", 
                  x_label=x_meta["label"], y_label=y_meta["label"],
                  x_left=x_meta["value"][0,...], x_right=x_meta["value"][-1,...], 
                  y_bottom=y_meta["value"].min(), y_top=y_meta["value"].max(), 
                  x_name=x_meta["name"], y_name=y_meta["name"])


    def plot_all(self, indices:dict={"i":0,"j":1,"r0":0,"r1":0,"r":0,"m":0,"n":0}):
        for variable_name in self.solution.variable_names:
            y_meta = self.solution.dictionary[variable_name]
            self.plot_single(y_name=y_meta["name"], indices=indices)



class Plotter_Flow(Plotter):
    """_summary_
    """
    def __init__(self, parameters:parameters.Parameters,
                       solution_flow:solutions.Solution_Flow): 
        """_summary_
        """
    
    # Attributes
    # -----
        super().__init__(parameters=parameters)

        self.solution_flow = solution_flow
        self.parameters = parameters

    def plot_single(self, y_name:str="permeability"):
        y_meta = self.solution_flow.dictionary[y_name]
        
        if "i_t" in y_meta["indices"] and "i_x" not in y_meta["indices"]:
            # Plot vs time
            x_name = "time"
            x_meta = self.solution_flow.dictionary[x_name]

            y_value = y_meta["value"]
            self.plot(x_value=x_meta["value"], y_value=y_value, 
                      color="tab:blue", linestyle="-", 
                      x_label=x_meta["label"], y_label=y_meta["label"],
                      x_left=x_meta["value"][0,...], x_right=x_meta["value"][-1,...], 
                      y_bottom=y_meta["value"].min(), y_top=y_meta["value"].max(), 
                      x_name=x_meta["name"], y_name=y_meta["name"])
        
        elif "i_x" in y_meta["indices"] and "i_t" not in y_meta["indices"]:
            pass

        elif "i_t" in y_meta["indices"] and "i_x" in y_meta["indices"]:
            x_name = "position"
            x_meta = self.solution_flow.dictionary[x_name]

            y_values = []
            T = self.parameters.time_max
            step = int(T/10)
            indxs_to_sweep = self.solution_flow.dictionary["time"]["value"][0:None:step]
            y_values = numpy.empty(shape=(self.parameters.num_posis, len(indxs_to_sweep)))
            for i,t in enumerate(indxs_to_sweep):
                t = int(t)
                print(t)
                y_value = y_meta["value"][t,:]
                y_values[:,i] = y_value
            self.plot_sweep(x_value=x_meta["value"], y_values=y_values, 
                           color="tab:blue", linestyle="-", 
                           x_label=x_meta["label"], y_label=y_meta["label"],
                           x_left=x_meta["value"][0,...], x_right=x_meta["value"][-1,...], 
                           y_bottom=y_meta["value"].min(), y_top=y_meta["value"].max(), 
                           x_name=x_meta["name"], y_name=y_meta["name"])

        else:
            raise Exception("Number of axes of flow solution variable must be 1 or 2.")

    def plot_all(self):
        for variable_name in self.solution_flow.variable_names:
            y_meta = self.solution_flow.dictionary[variable_name]
            self.plot_single(y_name=y_meta["name"])