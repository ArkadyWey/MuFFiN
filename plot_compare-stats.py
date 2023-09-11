from matplotlib import pyplot as plt
import os 
import numpy 
import scipy.interpolate as interpolate

import configure
import utils_plot_exp_param_dist


import sys
sys.path.append("/home/user/utils_python")
import plotting

# Parameters 
# -------
sigma = 0.3 
type_alpha = "mean"
dist = "depo" # depo or perm

path_results = "/home/user/projects/papers/2023_homogenisation/figures/poly/esbl_prep"

# Define init possibilites 
inits = ["4-reg", "6-reg", "6-ireg"]
colors = ["tab:blue","tab:orange", "tab:green"] # number of connections
markers = ["s", "h", "x"]

plotting.thesisify_pre_ax_creation()
fig_mean, ax_mean = plt.subplots(1,1)

plotting.thesisify_pre_ax_creation()
fig_sd, ax_sd = plt.subplots(1,1)

for i_init,initialisation in enumerate(inits):

    # Define fits
    # ------
    if initialisation == "4-reg":
        num_nodes_list = [1,4,9,16,25,36,49,64,81,100]

        if dist == "perm":
            fit_mean = 1
            fit_sd = 0.291
            label_mean = r"$\bar{k}_4$"

        elif dist == "depo": 
            fit_mean = 1
            fit_sd = 0.315
            label_mean = r"$\bar{j}_4$"
        else: 
            raise Exception("dist must be perm or depo.")
        
        
    elif initialisation == "6-reg":
        num_nodes_list = [2,8,18,32,50,72,98]

        if dist == "perm":
            fit_mean = 1.73205081
            fit_sd = 0.341
            label_mean = r"$\bar{k}_6$"

        elif dist == "depo":
            fit_mean = 2.14913986
            fit_sd = 0.369
            label_mean = r"$\bar{j}_6$"

        else: 
            raise Exception("dist must be perm or depo.")

    elif initialisation == "6-ireg":
        num_nodes_list =  [4,16,36,64]#,100]  # 6-ireg


        if dist == "perm":
            fit_mean = 1.73205081
            fit_sd = 0.621
            label_mean = r"$\bar{k}_6$"

        elif dist == "depo": 
            fit_mean = 2.14913986
            fit_sd = 0.44#0.391
            label_mean = r"$\bar{j}_6$"

        else: 
            raise Exception("dist must be perm or depo.")

    else: 
        raise Exception("initialisation must be 4-reg, 6-reg, or 6-ireg.")


    if dist == "perm": 
        if initialisation == "4-reg":
            stat_mean = "4-regular"
            stat_sd = "4-regular"
        elif initialisation == "6-reg":
            stat_mean = "6-regular"
            stat_sd = "6-regular"
        elif initialisation == "6-ireg":
            stat_mean = "6-irregular"
            stat_sd = "6-irregular"
        #stat_mean = initialisation#r"$\mathbb{E}[k]$"
        #stat_sd   = initialisation#r"$\mathbb{S}[k]$"
        label_mean_limit = r"$\bar{k}_{N\rightarrow\infty}$"  
    elif dist == "depo": 
        #stat_mean = initialisation#r"$\mathbb{E}[j]$"
        #stat_mean = initialisation#r"$\mathbb{E}[j]$"
        stat_mean = None#r"$\mathbb{E}[j]$"
        stat_sd   = None#r"$\mathbb{S}[j]$"
        label_mean_limit = r"$\bar{j}_{N\rightarrow\infty}$"  
    else:
        raise Exception("dist must be perm or depo.")


    # Get mean and standard deviation at each N
    # ----
    num_tests = len(num_nodes_list)

    mean_1 = numpy.zeros(shape=num_tests)
    sd_1   = numpy.zeros(shape=num_tests)
    for t in range(num_tests):
        N = num_nodes_list[t]
        path_stats = "/home/user/projects/papers/2023_homogenisation/figures/poly/esbl_prep/init-{}/N-{}/fulls_init-{}_N-{}".format(initialisation,N,initialisation,N)

        # Get parameter to histogram
        # ------
        if dist == "perm":
            param_effe_1 = numpy.load(os.path.join(path_stats, "perm_prep_4.npy".format(N)))
            param_effe_1 = param_effe_1[:,0,0,0]
        elif dist == "depo":
            param_effe_1 = numpy.load(os.path.join(path_stats, "depo_prep_3.npy".format(N)))
            param_effe_1 = param_effe_1[:,0,0]
        else: 
            raise Exception("{} is not a valid distribution parameter.".format(dist))

        mean_1[t] = numpy.mean(a=param_effe_1, axis=0)
        sd_1[t]   = numpy.std(a=param_effe_1, axis=0 )



    # Plot scatter of means and SDs
    # -----
    if initialisation == "4-reg" or initialisation == "6-ireg":
        num_nodes=4
    elif initialisation == "6-reg":
        num_nodes=2

    conf = configure.Configure(num_nodes=num_nodes,
                            initialisation=initialisation,
                            sigma=sigma, type_alpha=type_alpha)

    ax_mean.scatter(num_nodes_list,mean_1, color=colors[i_init], marker=markers[i_init],label=stat_mean)
    ax_sd.scatter(num_nodes_list,sd_1,   color=colors[i_init], marker=markers[i_init])#,label=stat_sd  ) 

    # Plot guide lines
    # ------
    N_smooth =  numpy.linspace(1,100,500)

    #ax.plot(N_smooth, (conf.mean)*numpy.ones_like(N_smooth), color="tab:blue", ls="-", label=r"$\bar{G}$")
    ax_mean.plot(N_smooth, fit_mean*numpy.ones_like(N_smooth), color=colors[i_init], ls="--")  #, label=label_mean)
    ax_mean.plot(N_smooth, (mean_1[-1])*numpy.ones_like(N_smooth), color=colors[i_init],ls=":")  # , label=label_mean_limit)
    ax_sd.plot(N_smooth, fit_sd*numpy.power(N_smooth,-0.5), color=colors[i_init], ls="-", label=str(fit_sd)+r"$N^{-\frac{1}{2}}$")

    #print("init:{}, dist:{}, large_cell:{}".format(initialisation,dist,mean_1[-1]))
    #print("init:{}, dist:{}, large_cell:{}".format(initialisation,dist,mean_1[-1]))
    print("init:{}, dist:{}, error:{}".format(initialisation,dist,1-abs(mean_1[1]-mean_1[-1])/mean_1[-1]))

# Cleanup graph 
# -------------
x_right_stats = 102
y_top_stats = 2.5


if dist == "perm":
    y_label = r"$\mathbb{E}[k]$"
elif dist == "depo":
    y_label = r"$\mathbb{E}[j]$"

plotting.thesisify_post_plot(ax=ax_mean,
                             x_label=r"$N$",
                             y_label=y_label,
                             x_left=0,
                             x_right=x_right_stats,
                             y_bottom=0.5,
                             y_top=y_top_stats)


plotting.save_fig(fig=fig_mean,fname=os.path.join(path_results,"stats__v__N__stat-mean_dist-{}.svg".format(dist)), format="svg")

# Sd
# ------

x_right_stats = 102
y_top_stats = 0.5

if dist == "perm":
    y_label = r"$\mathbb{S}[k]$"
elif dist == "depo":
    y_label = r"$\mathbb{S}[j]$"

plotting.thesisify_post_plot(ax=ax_sd,
                             x_label=r"$N$",
                             y_label=y_label,
                             x_left=0,
                             x_right=x_right_stats,
                             y_bottom=0,
                             y_top=y_top_stats)


plotting.save_fig(fig=fig_sd,fname=os.path.join(path_results,"stats__v__N__stat-sd_dist-{}.svg".format(dist)), format="svg")