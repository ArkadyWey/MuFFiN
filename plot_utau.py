from matplotlib import pyplot as plt
import os 
import numpy 


import sys
sys.path.append("/home/user/utils_python")
import plotting


# Plot velocity 
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

beta_str_1 = ["0.01","0.02","0.03","0.04","0.05","0.06","0.07","0.08","0.09","0.10"]
tau_1     = []
# find t where u hits 10%.


for b, beta_str in enumerate(beta_str_1):
    # Parameters 
    # -----
    path_results = os.path.join("/home/user/home_temp/projects/papers/2023_homogenisation/figures/mono/beta-{}/flow".format(beta_str))

    time_1 = numpy.load(os.path.join(path_results, "time_1.npy"))
    velo_1 = numpy.load(os.path.join(path_results, "velo_1.npy"))

    indx_crit_1 = [i for i in range(len(velo_1)) if velo_1[i] <0.1]
    indx_crit = indx_crit_1[0]
    tau_1.append(indx_crit)
    
    ax.plot(time_1[0:indx_crit+1],velo_1[0:indx_crit+1], c="tab:blue")

ax.plot(time_1,0.1*numpy.ones_like(velo_1), c="k", ls="--")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$t$",
                             y_label=r"$u$",
                             x_left=0,
                             x_right=500,
                             y_bottom=0,
                             y_top=1.01)

path_results = os.path.join("/home/user/home_temp/projects/papers/2023_homogenisation/figures/mono/")


plotting.save_fig(fig=fig,fname=os.path.join(path_results,"velo_1__v__time_1.svg"), format="svg")




# Plot log-log 
# ------------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

beta_1 = []
for beta_str in beta_str_1:
    beta = float(beta_str)
    beta_1.append(beta)

x_1 = numpy.log(beta_1)
y_1 = numpy.log(tau_1)
 
ax.scatter(x_1,y_1)

m = -1.00
c = 1.555

fit_1 = m*x_1+c

ax.plot(x_1,fit_1)

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$\mathrm{log}(\beta)$",
                             y_label=r"$\mathrm{log}(\tau)$",
                             x_left=None,
                             x_right=0,
                             y_bottom=0,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"log-tau_1__v__log-beta_1.svg"), format="svg")




# Plot terminal time 
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)


ax.scatter(beta_1, tau_1, c="tab:blue")

beta_smth_1 = numpy.linspace(0.0049,0.1,101)
fit_1 = numpy.exp(c)*beta_smth_1**m
ax.plot(beta_smth_1,fit_1)

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$\beta$",
                             y_label=r"$\tau$",
                             x_left=0,
                             x_right=0.105,
                             y_bottom=0,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"tau_1__v__beta_1.svg"), format="svg")








