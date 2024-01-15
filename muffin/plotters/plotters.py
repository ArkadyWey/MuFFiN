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
    def __init__(self, parameters:parameters.Parameters,
                       solution:solutions.Solution): 
        """_summary_
        """


    # Attributes
    # -----
        self.solution = solution
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
        

    def plot_single(self, variable_name:str="conductance", indices:dict={"i":0,"j":1,"r0":0,"r1":0,"r":0,"m":0,"n":0}):
        x_meta = self.solution.dictionary["time_like"]
        y_meta = self.solution.dictionary[variable_name]

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
            self.plot_single(variable_name=y_meta["name"], indices=indices)