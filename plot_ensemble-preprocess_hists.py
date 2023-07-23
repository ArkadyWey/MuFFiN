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
initialisation = "4-reg"

dist = "perm"

path_results = "/home/user/projects/papers/2023_homogenisation/figures/poly/esbl_prep/init-{}".format(initialisation)

#path_results = /home/user/projects/papers/2023_homogenisation/figures/poly/esbl_prep/init-4-reg/N-4/fulls_init-4-reg_N-4

# Plot histogram clearer method
# -----------------------    
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

if initialisation == "4-reg":     
    num_nodes_list = [4,16,36,64,100]     # 4-reg

    x_left   = 0.5
    x_right  = 1.5
    y_bottom = 0.0 
    y_top    = 14.0

elif initialisation == "6-reg":
    num_nodes_list = [2,8,18,32,50,72,98]  # 6-reg

    x_left   = 1.0
    x_right  = 3.0
    y_bottom = 0.0
    y_top    = 12.0

elif initialisation == "6-ireg":
    num_nodes_list =  [4,16,36,64]#,100]  # 6-ireg

    x_left   = 1.0
    x_right  = 2.5
    y_bottom = 0.0
    y_top    = 10.0

else: 
    raise Exception("Need N for this initilisation...")


colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink"]
for t, N in enumerate(num_nodes_list):

    path_stats = "/home/user/projects/papers/2023_homogenisation/figures/poly/esbl_prep/init-{}/N-{}/fulls_init-{}_N-{}".format(initialisation,N,initialisation,N)

    # Plot parameter distribution
    # ----------------------------
    # Get parameters
    # --------
    conf = configure.Configure(num_nodes=N,
                               initialisation=initialisation,
                               sigma=sigma, type_alpha=type_alpha)


    num_bins = 100
    #min_val = 0.0
    #max_val = conf.mean*2

    min_val = x_left
    max_val = x_right

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
    

    # Get bin edges of histogram
    # ------
    bin_edges = utils_plot_exp_param_dist.GetBinEdges(num_bins=num_bins,
                                                      min_val=min_val, 
                                                      max_val=max_val)
    
    # Plot histogram
    # ------
    count_param_1, bins_param, _ignored = ax.hist(x=param_effe_1, 
                                                  bins=bin_edges.bin_edges, 
                                                  density=True, 
                                                  align='mid', 
                                                  label=r"$N={}$".format(num_nodes_list[t]), 
                                                  alpha=0.4, color=colors[t])
   
    
    # Interpolate histogram
    # ------
    bin_centres = numpy.linspace(start=min_val, stop=max_val, num=num_bins, endpoint=True)
    spl = interpolate.splrep(bin_centres, count_param_1, k=3)
    x2 = numpy.linspace(bin_centres[0], bin_centres[-1], 10*num_bins)
    y2 = interpolate.splev(x2, spl)
    ax.plot(x2,y2,color=colors[t], 
                  linewidth=2.0, 
                  linestyle="-", 
                  alpha=1.0)

# Plot 
# ----
if dist == "perm":
    dist_character = r"$k$"
elif dist == "depo": 
    dist_character = r"$j$"
else:
    raise Exception("dist must be perm or depo.") 


plotting.thesisify_post_plot(ax=ax,
                             x_label=dist_character,
                             y_label=r"Probability density",
                             x_left=x_left,
                             x_right=x_right,
                             y_bottom=y_bottom,
                             y_top=y_top)


plotting.save_fig(fig=fig,fname=os.path.join(path_results,"{}__v__prob__init-{}.svg".format(dist,initialisation)), format="svg")



# Get mean and standard deviation of each histogram 
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
        fit_sd = 0.391
        label_mean = r"$\bar{j}_6$"

    else: 
        raise Exception("dist must be perm or depo.")

else: 
    raise Exception("initialisation must be 4-reg, 6-reg, or 6-ireg.")


if dist == "perm": 
    stat_mean = r"$\mathbb{E}[k]$"
    stat_sd   = r"$\mathbb{S}[k]$"
    label_mean_limit = r"$\bar{k}_{N\rightarrow\infty}$"  
elif dist == "depo": 
    stat_mean = r"$\mathbb{E}[j]$"
    stat_sd   = r"$\mathbb{S}[j]$"
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
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)


conf = configure.Configure(num_nodes=4,
                           initialisation=initialisation,
                           sigma=sigma, type_alpha=type_alpha)

ax.scatter(num_nodes_list,mean_1, label=stat_mean)
ax.scatter(num_nodes_list,sd_1,   label=stat_sd)

# Plot guide lines
# ------
N_smooth =  numpy.linspace(1,100,500)

#ax.plot(N_smooth, (conf.mean)*numpy.ones_like(N_smooth), color="tab:blue", ls="-", label=r"$\bar{G}$")
ax.plot(N_smooth, fit_mean*numpy.ones_like(N_smooth), color="tab:blue", ls="-", label=label_mean)
ax.plot(N_smooth, (mean_1[-1])*numpy.ones_like(N_smooth), color="tab:blue",ls="--", label=label_mean_limit)
ax.plot(N_smooth, fit_sd*numpy.power(N_smooth,-0.5), color="tab:orange", label=str(fit_sd)+r"$N^{-\frac{1}{2}}$",ls="-")

#aprx = conf.mean*conf.get_cdf(conf.mean)
#rslt = mean_1[-1]
#pcnt = aprx/rslt*100
#print("pcnt:{}".format(pcnt))

if initialisation == "4-reg":
    x_right_stats = 102
    y_top_stats = 1.1
elif initialisation == "6-reg":
    x_right_stats = 102
    y_top_stats = 2.2


# Cleanup graph 
# -------------
plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$N$",
                             y_label=r"Statistics",
                             x_left=0,
                             x_right=x_right_stats,
                             y_bottom=0,
                             y_top=y_top_stats)


plotting.save_fig(fig=fig,fname=os.path.join(path_results,"stats__v__N__dist-{}_init-{}.svg".format(dist,initialisation)), format="svg")




# Plot scatter accuracy
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.scatter(num_nodes_list,numpy.ones_like(mean_1)-abs(mean_1-mean_1[-1]))

# Cleanup graph 
# -------------
plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$N$",
                             y_label=r"Accuracy",
                             x_left=0,
                             x_right=102,
                             y_bottom=0.95,
                             y_top=1.001)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"accu__v__N__dist-{}_init-{}.svg".format(dist,initialisation)), format="svg")




# Sweep s 
# --------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)


N = 4
colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink"]
eses   = ["0","50","100","150","200"]
for ss,s in enumerate([0,1,2,3,4]):
    
    path_stats = "/home/user/projects/papers/2023_homogenisation/figures/poly/esbl_prep/init-{}/N-{}/fulls_init-{}_N-{}".format(initialisation,N,initialisation,N)
    
    # Plot parameter distribution
    # ----------------------------
    
    # Get parameters
    # --------
    conf = configure.Configure(num_nodes=N,
                               initialisation=initialisation,
                               sigma=sigma, 
                               type_alpha=type_alpha)
    
    num_bins = 100
    x_left = 0 
    #x_right = 1.25
    min_val = x_left
    max_val = x_right

    # Get parameter to histogram
    # ------
    if dist == "perm":
        param_effe_1 = numpy.load(os.path.join(path_stats, "perm_prep_4.npy"))
        param_effe_1 = param_effe_1[:,s,0,0]
    elif dist == "depo":
        param_effe_1 = numpy.load(os.path.join(path_stats, "depo_prep_3.npy"))
        param_effe_1 = param_effe_1[:,s,0]
    else: 
        raise Exception("{} is not a valid distribution parameter.".format(dist))
    
    # Get bin edges of histogram
    # ------
    bin_edges = utils_plot_exp_param_dist.GetBinEdges(num_bins=num_bins,
                                                      min_val=min_val, 
                                                      max_val=max_val)
    # Plot histogram
    # ------
    count_param_1, bins_param, _ignored = ax.hist(x=param_effe_1, 
                                                  bins=bin_edges.bin_edges, 
                                                  density=True, 
                                                  align='mid', 
                                                  alpha=0.4, 
                                                  color=colors[ss], 
                                                  label=r"$s={}$".format(eses[ss]))

    # Interpolate histogram
    # ------
    bin_centres = numpy.linspace(start=min_val, stop=max_val, num=num_bins, endpoint=True)
    spl = interpolate.splrep(bin_centres, count_param_1, k=3)
    x2 = numpy.linspace(bin_centres[0], bin_centres[-1], 5*num_bins)
    y2 = interpolate.splev(x2, spl)
    ax.plot(x2,y2,color=colors[ss], 
                  linewidth=2.0, 
                  linestyle="-", 
                  alpha=1.0)

# Plot 
# ----
if dist == "perm":
    dist_character = r"$k$"
    if initialisation == "4-reg":
        y_top = 40
    elif initialisation == "6-reg":
        y_top = 20
elif dist == "depo": 
    dist_character = r"$j$"
    if initialisation == "4-reg":
        y_top = 12
    elif initialisation == "6-reg":
        y_top = 12
else:
    raise Exception("dist must be perm or depo.") 


plotting.thesisify_post_plot(ax=ax,
                             x_label=dist_character,
                             y_label=r"Probability density",
                             x_left=x_left,
                             x_right=x_right,
                             y_bottom=y_bottom,
                             y_top=y_top)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"{}__v__prob__init-{}_sweep-s.svg".format(dist,initialisation)), format="svg")

