from scipy import interpolate
import numpy
import os 
from matplotlib import pyplot as plt

def get_new_interpolated_point(table_x,table_y,new_x_value):
    """
    Given a list of x values, and corresponding y values, and
    a new x value, approximate the corresponding function, 
    and use this function to return the new y value 
    corresponding to the new x value.
    Parameters 
    ----------
    - table_x: numpy.ndarray
        1-dimensional list of x values.
    - table_y: numpy.ndarray
        1-dimensional list of y values.
    - new_x_value: float
        New x value for which the corresponding y value is to be approximated.

    Returns
    -------
    - new_y_value: float
        Interpolated y value corresponding to new_x_value
    """
    interpolated_function = interpolate.splrep(x=table_x,y=table_y,k=3)
    new_y_value = interpolate.splev(x=new_x_value, tck=interpolated_function)

    return new_y_value


class PlotParameterDistribution():
    def __init__(self, parameter_name,
                       num_nodes_list,
                       num_bins_in_range,
                       num_pts_to_interp,
                       path_results,
                       ax):
        """
        """
        self.parameter_name = parameter_name

        (self.count_hist, self.bins_hist) = self.get_histograms(num_bins_in_range=num_bins_in_range, 
                                                                num_nodes_list=num_nodes_list, 
                                                                path_results=path_results)

        (self.counts_int_1, self.bins_int_1) = self.plot_histograms(bins_hist=self.bins_hist, 
                                                                    num_nodes_list=num_nodes_list, 
                                                                    path_results=path_results, 
                                                                    ax=ax)

        # Reset the color cycle and plot interpolation of histogram for each N
        plt.gca().set_prop_cycle(None)


        self.ax = self.plot_interpolated_histograms(num_nodes_list=num_nodes_list, 
                                                    counts_int_1=self.counts_int_1, 
                                                    bins_int_1=self.bins_int_1, 
                                                    path_results=path_results,
                                                    num_pts_to_interp=num_pts_to_interp, 
                                                    ax=ax)






    def get_histograms(self,num_bins_in_range, num_nodes_list, path_results):
        """
        """
        # Parameters 
        # -----------
        num_tests = len(num_nodes_list)

        # Build the tuple of perms so all hists are built at same time
        list_of_perms = []

        for t in range(num_tests):

            # Get perm for this N
            N = num_nodes_list[t]

            if self.parameter_name == "perm":
                param_effe_2 = numpy.load(os.path.join(path_results, "perm_effe_1_N-{}.npy".format(N)))
            elif self.parameter_name == "depo":
                # For square-struc
                param_effe_2 = numpy.load(os.path.join(path_results, "depo_effe_1_N-{}.npy".format(N))) #/numpy.sqrt(N)
                # for other strucs
                #param_effe_2 = -numpy.load(os.path.join(path_results, "depo_effe_2_N-{}.npy".format(N)))
            elif self.parameter_name == "adhe":
                param_effe_2 = numpy.load(os.path.join(path_results, "count_adhe_1_N-{}.npy".format(N))) 
            else: 
                raise Exception("parameter_name must be either perm or depo or adhe.")
            
            param_effe_1 = param_effe_2[:]

            # Add this perm to list of perms
            list_of_perms.append(param_effe_1)

        # Make all hists
        tuple_of_perms = tuple(list_of_perms)
        count_hist, bins_hist = numpy.histogram(numpy.hstack(tup=tuple_of_perms), bins=num_bins_in_range)

        return (count_hist, bins_hist) 


    def plot_histograms(self, bins_hist, num_nodes_list, path_results, ax):
        """
        """
        # Parameters 
        num_tests = len(num_nodes_list)

        # Plot histograms and get bins and count for each for interpolation
        counts_int_1 = []
        bins_int_1 = []
        for t in range(num_tests):
            N = num_nodes_list[t]

            # Unpack perm for this N
            if self.parameter_name == "perm":
                param_effe_2 = numpy.load(os.path.join(path_results, "perm_effe_1_N-{}.npy".format(N)))
            elif self.parameter_name == "depo":
                # For square-struc
                param_effe_2 = numpy.load(os.path.join(path_results, "depo_effe_1_N-{}.npy".format(N))) #/numpy.sqrt(N)
                # for other strucs
                #param_effe_2 = -numpy.load(os.path.join(path_results, "depo_effe_2_N-{}.npy".format(N)))
            elif self.parameter_name == "adhe":
                param_effe_2 = numpy.load(os.path.join(path_results, "count_adhe_1_N-{}.npy".format(N))) 
            else: 
                raise Exception("parameter_name must be either perm or depo or adhe.")
                
            param_effe_1 = param_effe_2[:]

            # Plot hist for this N (using histogram bins we found above)
            #count, bins, ignored = ax.hist(param_effe_1, bins_hist)
            count_int, bins_int, ignored = ax.hist(x=param_effe_1, bins=bins_hist, density=True, align='mid', label=r"$N={}$".format(num_nodes_list[t]), alpha=0.4)

            # Add to interpolation bins list
            counts_int_1.append(count_int)
            bins_int_1.append(bins_int)

        return (counts_int_1, bins_int_1)

    def plot_interpolated_histograms(self, num_nodes_list, counts_int_1, bins_int_1, path_results,num_pts_to_interp, ax):
        """
        """
        # Parameters 
        num_tests = len(num_nodes_list)

        for t in range(num_tests):
            N = num_nodes_list[t]

            # Get interpolation count and bins for this N
            count = counts_int_1[t]
            bins  = bins_int_1[t]

            # Interpolate histogram
            dist_interp_1 = get_new_interpolated_point(table_x=numpy.linspace(min(bins), max(bins), len(count)), 
                                                       table_y=count, 
                                                       new_x_value=numpy.linspace(min(bins), max(bins), num_pts_to_interp))

            ax.plot(numpy.linspace(min(bins), max(bins), num_pts_to_interp), dist_interp_1)

        return ax





class PlotParameterMeanAndSD():
    """
    """
    def __init__(self, parameter_name,
                       paths_results,
                       num_nodes_lists,
                       markers,
                       labels_mean,
                       colors,
                       N_smooth,
                       labels_sd,
                       sd_constants_and_powers,
                       labels_sd_fit,
                       ax_mean,
                       ax_sd):
        """
        """
        self.parameter_name = parameter_name
        self.paths_results = paths_results
        self.num_nodes_lists = num_nodes_lists
        self.markers = markers
        self.labels_mean = labels_mean
        self.colors = colors
        self.N_smooth = N_smooth
        self.labels_sd = labels_sd
        self.sd_constants_and_powers = sd_constants_and_powers
        self.labels_sd_fit = labels_sd_fit

        self.ax_mean, self.ax_sd = self.plot_mean_and_sd(ax_mean=ax_mean, ax_sd=ax_sd)


        

    def get_mean_and_sd_for_each_N(self, parameter_name, num_nodes_list, path_results):
        """
        """
        # Parameters 
        num_tests = len(num_nodes_list)

        # Get mean and standard deviation for each N
        mean_1 = numpy.zeros(shape=num_tests)
        sd_1 = numpy.zeros(shape=num_tests)
        
        #print(parameter_name)
        for t in range(num_tests):
            N = num_nodes_list[t]

            if parameter_name == "perm":
                param_effe_2 = numpy.load(os.path.join(path_results, "perm_effe_2_N-{}.npy".format(N)))
            elif parameter_name == "depo":
                # For square-struc
                param_effe_2 = -numpy.load(os.path.join(path_results, "depo_effe_2_N-{}.npy".format(N)))/numpy.sqrt(N)
                # for other strucs
                #param_effe_2 = -numpy.load(os.path.join(path_results, "depo_effe_2_N-{}.npy".format(N)))
            else: 
                raise Exception("parameter_name must be either perm or depo.")

            mean_1[t] = numpy.mean(a=param_effe_2, axis=1)
            sd_1[t]   = numpy.std(a=param_effe_2, axis=1)

        return mean_1, sd_1


    def plot_mean_and_sd(self, ax_mean, ax_sd):

        # Parameters 
        # ------
        parameter_name = self.parameter_name
        paths_results = self.paths_results
        num_structures = len(paths_results)
        num_nodes_lists = self.num_nodes_lists
        markers = self.markers
        labels_mean = self.labels_mean
        colors = self.colors
        N_smooth = self.N_smooth
        labels_sd = self.labels_sd
        sd_constants_and_powers = self.sd_constants_and_powers
        labels_sd_fit = self.labels_sd_fit

        for i in range(num_structures):
            mean_1, sd_1 = self.get_mean_and_sd_for_each_N(parameter_name=parameter_name,
                                                           num_nodes_list=num_nodes_lists[i], 
                                                           path_results=paths_results[i])
        
            ax_mean.scatter(num_nodes_lists[i],mean_1, marker=markers[i], label=labels_mean[i], color=colors[i])
            ax_mean.plot(N_smooth, (mean_1[-1])*numpy.ones_like(N_smooth), color=colors[i], ls="--")
            
            ax_sd.scatter(num_nodes_lists[i],  sd_1,   marker=markers[i], label=labels_sd[i], color=colors[i])
            ax_sd.plot(N_smooth, sd_constants_and_powers[i][0]*numpy.power(N_smooth,sd_constants_and_powers[i][1]), color=colors[i], label=labels_sd_fit[i],ls="-")

        return ax_mean, ax_sd






class GetBinEdges():
    """
    Get parameters for probability distribution of 
    the deposition parameter.
    """
    def __init__(self, num_bins,
                       min_val,
                       max_val):
        """
        Parameters 
        ------
        num_bins: int
            - Number of bins we want the histogram to have.
        min_val: float 
            - Centre of the left-most bin. 
        max_val: float 
            - Centre of the right-most bin.
        """

        self.left_bin_edge, self.right_bin_edge = self.get_bin_edge_limits(min_val=min_val,
                                                                           max_val=max_val,
                                                                           num_bins=num_bins)

        self.bin_edges = self.get_bin_edges(left_bin_edge=self.left_bin_edge,
                                            right_bin_edge=self.right_bin_edge,
                                            num_bins=num_bins)


    def get_bin_edge_limits(self, min_val, max_val, num_bins):
        """
        Get bin edge limits so that we can define bins in next function. 

        Parameters
        -------
        - min_val: float 
            Min value that the distribution can achieve. 
            For example, in the case of the depositiion parameter distriburion, this is  zero. 
        - max_val: float 
            Max value the histogram can achieve. 
            For example, in the case of the deposition parameter distribution, this is
            the mean of the undferlying conductance distribution.
        
        Returns 
        ------
        left_bin_edge: float 
            - Left side of first bin. Use zero minus half the width of a bin, so that
            first bin is centred about zero. 
        right_bin_edge: float 
            - Right edge of last bin. We use the mean of the conductance distribution plus 
            half the width, so that the last bin is centred about the mean, since we know that 
            is the maximal value that the histogram can achieve.
        """
        # Get bin width
        # ----------
        dx = (max_val-min_val)/num_bins
        left_bin_edge  = min_val-dx/2.0
        right_bin_edge = max_val+dx/2.0

        return (left_bin_edge, right_bin_edge)

    def get_bin_edges(self, left_bin_edge, right_bin_edge, num_bins):
        """
        Get an array of the limits of the bins, 
        in the form bin_edges = [left-side-of-first bin, right-side-of-first-bin, 
            .... right-side-of-last-bin], 
        so that len(bin_edges) = num_bins + 1.

        Parameters 
        -------
        left_bin_edge: float 
            - Left side of first bin. Use zero minus half the width of a bin, so that
            first bin is centred about zero. 
        right_bin_edge: float 
            - Right edge of last bin. We use the mean of the conductance distribution plus 
            half the width, so that the last bin is centred about the mean, since we know that 
            is the maximal value that the histogram can achieve.

        Returns 
        # -----
        - bin_edges: numpy.ndarray
            List of values at which bin edges occur.
            bin_edges = [left-side-of-first bin, right-side-of-first-bin, 
                .... right-side-of-last-bin], 
        """
        bin_edges = numpy.linspace(start=left_bin_edge, stop=right_bin_edge, num=num_bins+1, endpoint=True)
        return bin_edges






class Plot_DepoAprx_vs_Density():
    """
    """
    def __init__(self, num_nodes,
                       num_bins,
                       conf, 
                       count_adhe_1, 
                       max_height):
        """
        """


        self.x_adhe_1, self.height_adhe_1 = self.get_x_and_y(count_adhe_1=count_adhe_1, 
                                                             mean=conf.mean,
                                                             num_nodes=num_nodes)

        self.x_j_aprx_1 = self.get_scaled_x_for_j(x_adhe_1=self.x_adhe_1, 
                                                  mean=conf.mean, 
                                                  num_nodes=num_nodes)

        self.width = self.get_bin_width(min_val=0.0, 
                                        max_val=conf.mean, 
                                        num_nodes=num_nodes)

    def get_x_and_y(self,count_adhe_1, mean, num_nodes):
        """
        - Take the a 1-d variable that is the count of 
        either number of edges blocoed, number of horizontal edges blocked, 
        or number of vertical edges blocked. 
        - Bin these.
        - Get correct density by dividing by number of samples. 
        - Scale density to match j density. 
        - Get number of bins and use this to get x values.

        Return
        - x values of density plot for number of edges blocked. 
        - height values for density plot for number of edges blocked.
        """
        # Bin number of edges blocked 
        # -----
        self.bincount_adhe = numpy.bincount(list(count_adhe_1.astype(dtype=int)))

        # Get probability density of each bin
        # --------
        height_adhe = self.bincount_adhe/max(self.bincount_adhe)*num_nodes/mean#*max_height  #sum(bincount_adhe_hori)  #/width_approx

        # Get number of bins 
        # ------
        num_bins_adhe = len(self.bincount_adhe)

        # Get x for density of blocked edges
        x_adhe = range(num_bins_adhe)

        return (x_adhe, height_adhe)

    def get_scaled_x_for_j(self, x_adhe_1, mean, num_nodes):
        """
        Scale the values on x axis of density v number of edges 
        blocked to make them fit to density v j plot.
        """
        # Get x for j approx
        # x = B*mean/N
        # -----
        x_j_aprx_1 = list(numpy.array(list(x_adhe_1))/num_nodes*mean)

        return x_j_aprx_1


    def get_bin_width(self, min_val, max_val, num_nodes):
        # Get bin width
        # ----------
        width = (max_val-min_val)/num_nodes
        return width

