from matplotlib import pyplot as plt
import os 
import numpy
from scipy import interpolate
import math

import muffin.configure.configure as configure
import muffin.utils.utils_plot_exp_param_dist as utils_plot_exp_param_dist

import muffin.plotters.plotting as plotting

# Parameters 
# -----
initialisation = "4-reg"
num_reps       = 10000
type_alpha     = "mean"

path_results = os.path.join(".","results/results_exp_param-dist_{}_kj_inf__vs__sigma_reps-{}_alpha-{}".format(initialisation,num_reps,type_alpha))

# Make results directory
# --------
if not os.path.exists(path_results):
    os.makedirs(path_results)







# Plot mean at large N for each sigma: permeability
# -----------------------
plotting.thesisify_pre_ax_creation(fig_type="full_page")
fig, ax = plt.subplots(1,1)

num_nodes_list = [36]
num_tests = len(num_nodes_list)

sigma_list = [0.03,0.06,0.09,0.12,0.15,0.18,0.21,0.24,0.27,0.30]
num_sigmas = len(sigma_list)

mean_at_each_sigma_1 = numpy.zeros(shape=num_sigmas)
g_bar_at_each_sigma_1 = numpy.zeros(shape=num_sigmas)

for i_sigma,sigma in enumerate(sigma_list): 

    path_results_sigma = os.path.join(".","results/results_exp_param-dist_{}_reps-{}_sigma-{}_alpha-{}".format(initialisation,num_reps,sigma,type_alpha))

    # Get mean and standard deviation for each N
    mean_1 = numpy.zeros(shape=num_tests)
    sd_1   = numpy.zeros(shape=num_tests)


    for t in range(num_tests):
        N = num_nodes_list[t]

        conf = configure.Configure(num_nodes=N,
                                   initialisation=initialisation,
                                   sigma=sigma,
                                   type_alpha=type_alpha)
        
        count_adhe_hori_1 = numpy.load(os.path.join(path_results_sigma, "perm_effe_1_N-{}.npy".format(N)))
        mean_1[t]   = numpy.mean(a=count_adhe_hori_1, axis=0)
        sd_1[t]     = numpy.std( a=count_adhe_hori_1, axis=0)

    mean_at_each_sigma = mean_1[0]
    mean_at_each_sigma_1[i_sigma] = mean_at_each_sigma
    g_bar_at_each_sigma_1[i_sigma] = conf.mean
    
# Plot scatter for distribution means
ax.scatter(sigma_list, mean_at_each_sigma_1, label=r"$\bar{k}^{11}|_{N \rightarrow \infty}$")
#ax.scatter(sigma_list, g_bar_at_each_sigma_1, label=r"$\bar{G}$")

# Plot guide lines
sigma_smooth = numpy.linspace(0,0.4,1000)
ax.plot(sigma_smooth, numpy.exp(conf.mu+0.5*sigma_smooth**2), color="tab:blue", ls="-",label=r"$\bar{G}$")
ax.plot(sigma_smooth, numpy.exp(conf.mu)*numpy.ones(shape=sigma_smooth.shape), color="tab:blue", ls="--", label=r"$\bar{G}|_{\sigma = 0.03}$")

ax.vlines(x=mean_1[0], 
          ymin=0.0, 
          ymax=1.0, 
          color="tab:green", 
          linewidth=2.0, 
          linestyle=(3,(3,3)), 
          alpha=1.0, 
          label=r"$\mathbb{E}[k^{11}]$")


plotting.thesisify_post_plot(ax=ax,
                             fig_type="full_page",
                             x_label=r"$\sigma$",
                             y_label=None,
                             x_left=0.00,
                             x_right=0.33,
                             y_bottom=None,
                             y_top=None)



plotting.save_fig(fig=fig,fname=os.path.join(path_results,"k_infty__vs__sigma.svg"), format="svg")











# Plot LOG-LOG difference in mean at large N for each sigma: permeability
# -----------------------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

num_nodes_list = [36]
num_tests = len(num_nodes_list)

sigma_list = [0.03,0.06,0.09,0.12,0.15,0.18,0.21,0.24,0.27,0.30]
num_sigmas = len(sigma_list)

mean_at_each_sigma_1 = numpy.zeros(shape=num_sigmas)
g_bar_at_each_sigma_1 = numpy.zeros(shape=num_sigmas)

for i_sigma,sigma in enumerate(sigma_list): 

    path_results_sigma = os.path.join(".","results/results_exp_param-dist_{}_reps-{}_sigma-{}_alpha-{}".format(initialisation,num_reps,sigma,type_alpha))

    # Get mean and standard deviation for each N
    mean_1 = numpy.zeros(shape=num_tests)
    sd_1   = numpy.zeros(shape=num_tests)


    for t in range(num_tests):
        N = num_nodes_list[t]

        conf = configure.Configure(num_nodes=N,
                                   initialisation=initialisation,
                                   sigma=sigma,
                                   type_alpha=type_alpha)
        
        count_adhe_hori_1 = numpy.load(os.path.join(path_results_sigma, "perm_effe_1_N-{}.npy".format(N)))
        mean_1[t]   = numpy.mean(a=count_adhe_hori_1, axis=0)
        sd_1[t]     = numpy.std( a=count_adhe_hori_1, axis=0)

    mean_at_each_sigma = mean_1[0]
    mean_at_each_sigma_1[i_sigma] = mean_at_each_sigma
    g_bar_at_each_sigma_1[i_sigma] = conf.mean
    
# Plot scatter for distribution means
ax.scatter(numpy.log(sigma_list), numpy.log((g_bar_at_each_sigma_1-mean_at_each_sigma_1)/mean_at_each_sigma_1), label=r"$E_{\mathrm{n}}^{k}$")

# Plot guide lines
sigma_smooth = numpy.linspace(0,1,500)
#sigma_smooth = numpy.linspace(min(sigma_list),max(sigma_list),500)
ax.plot(numpy.log(sigma_smooth), 2.05*numpy.log(sigma_smooth)-0.65, color="tab:blue", ls="--")


plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$\mathrm{log}(\sigma)$",
                             y_label=r"$E_{\mathrm{n}}^{k}$",
                             x_left=-4,
                             x_right=0,
                             y_bottom=None,
                             y_top=None)



plotting.save_fig(fig=fig,fname=os.path.join(path_results,"log_k_infty_diff__vs__log_sigma.svg"), format="svg")








# Plot difference in mean at large N for each sigma: permeability
# -----------------------
plotting.thesisify_pre_ax_creation(fig_type="full_page")
fig, ax = plt.subplots(1,1)

num_nodes_list = [36]
num_tests = len(num_nodes_list)

sigma_list = [0.03,0.06,0.09,0.12,0.15,0.18,0.21,0.24,0.27,0.30]
num_sigmas = len(sigma_list)

mean_at_each_sigma_1 = numpy.zeros(shape=num_sigmas)
g_bar_at_each_sigma_1 = numpy.zeros(shape=num_sigmas)

for i_sigma,sigma in enumerate(sigma_list): 

    path_results_sigma = os.path.join(".","results/results_exp_param-dist_{}_reps-{}_sigma-{}_alpha-{}".format(initialisation,num_reps,sigma,type_alpha))

    # Get mean and standard deviation for each N
    mean_1 = numpy.zeros(shape=num_tests)
    sd_1   = numpy.zeros(shape=num_tests)


    for t in range(num_tests):
        N = num_nodes_list[t]

        conf = configure.Configure(num_nodes=N,
                                   initialisation=initialisation,
                                   sigma=sigma,
                                   type_alpha=type_alpha)
        
        count_adhe_hori_1 = numpy.load(os.path.join(path_results_sigma, "perm_effe_1_N-{}.npy".format(N)))
        mean_1[t]   = numpy.mean(a=count_adhe_hori_1, axis=0)
        sd_1[t]     = numpy.std( a=count_adhe_hori_1, axis=0)

    mean_at_each_sigma = mean_1[0]
    mean_at_each_sigma_1[i_sigma] = mean_at_each_sigma
    g_bar_at_each_sigma_1[i_sigma] = conf.mean
    
# Plot scatter for distribution means
ax.scatter(sigma_list, (g_bar_at_each_sigma_1-mean_at_each_sigma_1)/mean_at_each_sigma_1, label=r"$E_{\mathrm{n}}^{k}$")

# Plot guide lines
sigma_smooth = numpy.linspace(0,0.4,1000)
ax.plot(sigma_smooth, numpy.exp(-0.65)*sigma_smooth**(2.05), color="tab:blue", ls="-", label=r"$0.52\sigma^{2}$")
print(numpy.exp(-0.65))

colors = ["tab:orange","tab:green"]
for i,sigma in enumerate([0.03,0.3]):
    ax.vlines(x=sigma, 
              ymin=-0.002, 
              ymax=numpy.exp(-0.65)*sigma**(2.05), 
              color=colors[i], 
              linewidth=2.0, 
              linestyle="--", 
              alpha=1.0, 
              label=r"$\sigma={}$".format(sigma))
    sigma_smooth = numpy.linspace(-0.01,sigma,1000)
    ax.plot(sigma_smooth, numpy.exp(-0.65)*sigma**(2.05)*numpy.ones_like(sigma_smooth), color=colors[i],linestyle="--")

plotting.thesisify_post_plot(ax=ax,
                             fig_type="full_page",
                             x_label=r"$\sigma$",
                             y_label=r"$E_{\mathrm{n}}^{k}$",
                             x_left=-0.01,
                             x_right=0.41,
                             y_bottom=-0.002,
                             y_top=None)



plotting.save_fig(fig=fig,fname=os.path.join(path_results,"k_infty_diff__vs__sigma.svg"), format="svg")





















# Plot mean at large N for each sigma: adhesivity
# -----------------------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

num_nodes_list = [36]
num_tests = len(num_nodes_list)

sigma_list = [0.03,0.06,0.09,0.12,0.15,0.18,0.21,0.24,0.27,0.30]
num_sigmas = len(sigma_list)

mean_at_each_sigma_1 = numpy.zeros(shape=num_sigmas)
g_bar_at_each_sigma_1 = numpy.zeros(shape=num_sigmas)

for i_sigma,sigma in enumerate(sigma_list): 

    path_results_sigma = os.path.join(".","results/results_exp_param-dist_{}_reps-{}_sigma-{}_alpha-{}".format(initialisation,num_reps,sigma,type_alpha))

    # Get mean and standard deviation for each N
    mean_1 = numpy.zeros(shape=num_tests)
    sd_1   = numpy.zeros(shape=num_tests)


    for t in range(num_tests):
        N = num_nodes_list[t]

        conf = configure.Configure(num_nodes=N,
                                   initialisation=initialisation,
                                   sigma=sigma,
                                   type_alpha=type_alpha)
        
        count_adhe_hori_1 = numpy.load(os.path.join(path_results_sigma, "depo_effe_1_N-{}.npy".format(N)))
        mean_1[t]   = numpy.mean(a=count_adhe_hori_1, axis=0)
        sd_1[t]     = numpy.std( a=count_adhe_hori_1, axis=0)

    mean_at_each_sigma = mean_1[0]
    mean_at_each_sigma_1[i_sigma] = mean_at_each_sigma
    g_bar_at_each_sigma_1[i_sigma] = conf.mean*conf.get_cdf(conf.mean)
    
# Plot scatter for distribution means
ax.scatter(sigma_list, mean_at_each_sigma_1, label=r"$\bar{j}^{1}|_{N \rightarrow \infty}$")
#ax.scatter(sigma_list, g_bar_at_each_sigma_1, label=r"$\bar{G}\mathrm{cdf}(\bar{G})$")

# Plot guide lines
sigma_smooth = numpy.linspace(min(sigma_list),max(sigma_list),500)
sigma_smooth = numpy.linspace(0,max(sigma_list),500)
#ax.plot(sigma_smooth, numpy.exp(conf.mu+0.5*sigma_smooth**2)*conf.get_cdf(numpy.exp(conf.mu+0.5*sigma_smooth**2)), color="tab:orange", ls="-")
ax.plot(sigma_smooth, 0.55*sigma_smooth+0.80, color="tab:blue", ls="-",label=r"$\bar{G}\mathrm{cdf}(\bar{G})$")
ax.plot(sigma_smooth, 0.29*sigma_smooth+0.815, color="tab:blue", ls="--", label=r"$0.29\sigma+0.82$")


#conf = configure.Configure(num_nodes=N,
#                           initialisation=initialisation,
#                           sigma=0.03,
#                           type_alpha=type_alpha) 
#ax.plot(sigma_smooth, conf.mean*conf.get_cdf(conf.mean)*numpy.ones(shape=sigma_smooth.shape), color="tab:blue", ls="--", label=r"$\bar{G}_{0}\mathrm{cdf}(\bar{G}_{0})$")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$\sigma$",
                             y_label=None,
                             x_left=0.00,
                             x_right=0.33,
                             y_bottom=None,
                             y_top=None)



plotting.save_fig(fig=fig,fname=os.path.join(path_results,"j_infty__vs__sigma.svg"), format="svg")









# Plot log-log difference in mean at large N for each sigma: adhesivity
# -----------------------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

num_nodes_list = [36]
num_tests = len(num_nodes_list)

sigma_list = [0.03,0.06,0.09,0.12,0.15,0.18,0.21,0.24,0.27,0.30]
num_sigmas = len(sigma_list)

mean_at_each_sigma_1 = numpy.zeros(shape=num_sigmas)
g_bar_at_each_sigma_1 = numpy.zeros(shape=num_sigmas)

for i_sigma,sigma in enumerate(sigma_list): 

    path_results_sigma = os.path.join(".","results/results_exp_param-dist_{}_reps-{}_sigma-{}_alpha-{}".format(initialisation,num_reps,sigma,type_alpha))

    # Get mean and standard deviation for each N
    mean_1 = numpy.zeros(shape=num_tests)
    sd_1   = numpy.zeros(shape=num_tests)


    for t in range(num_tests):
        N = num_nodes_list[t]

        conf = configure.Configure(num_nodes=N,
                                   initialisation=initialisation,
                                   sigma=sigma,
                                   type_alpha=type_alpha)
        
        count_adhe_hori_1 = numpy.load(os.path.join(path_results_sigma, "depo_effe_1_N-{}.npy".format(N)))
        mean_1[t]   = numpy.mean(a=count_adhe_hori_1, axis=0)
        sd_1[t]     = numpy.std( a=count_adhe_hori_1, axis=0)

    mean_at_each_sigma = mean_1[0]
    mean_at_each_sigma_1[i_sigma] = mean_at_each_sigma
    g_bar_at_each_sigma_1[i_sigma] = conf.mean*conf.get_cdf(conf.mean)
    
# Plot scatter for distribution means
ax.scatter(numpy.log(sigma_list), numpy.log((g_bar_at_each_sigma_1-mean_at_each_sigma_1)/mean_at_each_sigma_1), label=r"log($\frac{\bar{G}\mathrm{cdf}(\bar{G})-\bar{j}^{1}_{N \rightarrow \infty}}{\bar{j}^{1}_{N \rightarrow \infty}}$)")

# Plot guide lines
sigma_smooth = numpy.linspace(min(sigma_list),max(sigma_list),500)
sigma_smooth = numpy.linspace(min(sigma_list),1,500)
ax.plot(numpy.log(sigma_smooth), 1.5*numpy.log(sigma_smooth)-0.8, color="tab:blue", ls="--")


#conf = configure.Configure(num_nodes=N,
#                           initialisation=initialisation,
#                           sigma=0.03,
#                           type_alpha=type_alpha) 
#ax.plot(sigma_smooth, conf.mean*conf.get_cdf(conf.mean)*numpy.ones(shape=sigma_smooth.shape), color="tab:blue", ls="--", label=r"$\bar{G}_{0}\mathrm{cdf}(\bar{G}_{0})$")

plotting.thesisify_post_plot(ax=ax,
                             fig_type="full_page",
                             x_label=r"log($\sigma$)",
                             y_label=r"log($\frac{\bar{G}\mathrm{cdf}(\bar{G})-\bar{j}^{1}_{N \rightarrow \infty}}{\bar{j}^{1}_{N \rightarrow \infty}}$)",
                             x_left=None,
                             x_right=None,
                             y_bottom=None,
                             y_top=None)



plotting.save_fig(fig=fig,fname=os.path.join(path_results,"log_j_infty_diff__vs__log_sigma.svg"), format="svg")






# Plot difference in mean at large N for each sigma: adhesivity
# -----------------------
plotting.thesisify_pre_ax_creation(fig_type="full_page")
fig, ax = plt.subplots(1,1)

num_nodes_list = [36]
num_tests = len(num_nodes_list)

sigma_list = [0.03,0.06,0.09,0.12,0.15,0.18,0.21,0.24,0.27,0.30]
num_sigmas = len(sigma_list)

mean_at_each_sigma_1 = numpy.zeros(shape=num_sigmas)
g_bar_at_each_sigma_1 = numpy.zeros(shape=num_sigmas)

for i_sigma,sigma in enumerate(sigma_list): 

    path_results_sigma = os.path.join(".","results/results_exp_param-dist_{}_reps-{}_sigma-{}_alpha-{}".format(initialisation,num_reps,sigma,type_alpha))

    # Get mean and standard deviation for each N
    mean_1 = numpy.zeros(shape=num_tests)
    sd_1   = numpy.zeros(shape=num_tests)


    for t in range(num_tests):
        N = num_nodes_list[t]

        conf = configure.Configure(num_nodes=N,
                                   initialisation=initialisation,
                                   sigma=sigma,
                                   type_alpha=type_alpha)
        
        count_adhe_hori_1 = numpy.load(os.path.join(path_results_sigma, "depo_effe_1_N-{}.npy".format(N)))
        mean_1[t]   = numpy.mean(a=count_adhe_hori_1, axis=0)
        sd_1[t]     = numpy.std( a=count_adhe_hori_1, axis=0)

    mean_at_each_sigma = mean_1[0]
    mean_at_each_sigma_1[i_sigma] = mean_at_each_sigma
    g_bar_at_each_sigma_1[i_sigma] = conf.mean*conf.get_cdf(conf.mean)
    
# Plot scatter for distribution means
ax.scatter(sigma_list, (g_bar_at_each_sigma_1-mean_at_each_sigma_1)/mean_at_each_sigma_1, label=r"$E_{\mathrm{n}}^{j}$")

# Plot guide lines
sigma_smooth = numpy.linspace(0,0.4,1000)
ax.plot(sigma_smooth, numpy.exp(-0.8)*sigma_smooth**(1.5), color="tab:blue", ls="-",label=r"$0.45\sigma^{\frac{3}{2}}$")
print(numpy.exp(-0.8))


#conf = configure.Configure(num_nodes=N,
#                           initialisation=initialisation,
#                           sigma=0.03,
#                           type_alpha=type_alpha) 
#ax.plot(sigma_smooth, conf.mean*conf.get_cdf(conf.mean)*numpy.ones(shape=sigma_smooth.shape), color="tab:blue", ls="--", label=r"$\bar{G}_{0}\mathrm{cdf}(\bar{G}_{0})$")


colors = ["tab:orange","tab:green"]
for i,sigma in enumerate([0.03,0.3]):
    ax.vlines(x=sigma, 
              ymin=-0.002, 
              ymax=numpy.exp(-0.8)*sigma**(1.5), 
              color=colors[i], 
              linewidth=2.0, 
              linestyle="--", 
              alpha=1.0, 
              label=r"$\sigma={}$".format(sigma))
    sigma_smooth = numpy.linspace(-0.01,sigma,1000)
    ax.plot(sigma_smooth, numpy.exp(-0.8)*sigma**(1.5)*numpy.ones_like(sigma_smooth), color=colors[i],linestyle="--")


plotting.thesisify_post_plot(ax=ax,
                             fig_type="full_page",
                             x_label=r"$\sigma$",
                             y_label=r"$E_{\mathrm{n}}^{j}$",
                             x_left=-0.01,
                             x_right=0.41,
                             y_bottom=-0.002,
                             y_top=None)



plotting.save_fig(fig=fig,fname=os.path.join(path_results,"j_infty_diff__vs__sigma.svg"), format="svg")










