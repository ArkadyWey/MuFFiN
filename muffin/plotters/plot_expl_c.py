from matplotlib import pyplot as plt
import os 
import numpy 
from scipy import integrate


import sys
sys.path.append("/home/user/utils_python")
import plotting

# Parameters 
# -----
path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/mono/sweep-alph/")


# Plot concentration
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

posi_1 = numpy.linspace(0,1,101)

#alph=1.0
alph_1 = numpy.arange(start=0,stop=11,step=1)
for alph in alph_1:
#ax.plot(posi_1,numpy.exp(-alph*posi_1),c="black",ls="--")
    ax.plot(posi_1,numpy.exp(-alph*posi_1),c="tab:blue",ls="-")

#ax.plot(posi_1,numpy.exp(-alph)*numpy.ones_like(posi_1), c="black", ls="--")

#ax.legend()
plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$c$",
                             x_left=0,
                             x_right=1,
                             y_bottom=0,
                             y_top=1.01)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"conc_2__v__posi_1.svg"), format="svg")




# Plot concentration
# -----
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

posi_1 = numpy.linspace(0,1,101)

alph=1.0
ax.plot(posi_1,numpy.exp(-alph*posi_1),c="tab:blue",ls="-")

epsi_1 = [1/3,1/4,1/5,1/10,1/20]#,1/30,1/40,1/80
c_1=["tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown"]
for e,epsi in enumerate(epsi_1):
    posi_1 = numpy.linspace(0,1,int(1/epsi),endpoint=True)
    #ax.plot(posi_1, (1-alph*epsi)**(posi_1/epsi), c="tab:orange", ls="--")
    ax.plot(posi_1, (1-alph*posi_1*epsi)**(1/epsi), c=c_1[e], ls="--")




path_results = os.path.join("/home/user/home_temp/projects/papers/2023_homogenisation/figures/mono/comp")
plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$x$",
                             y_label=r"$c$",
                             x_left=0,
                             x_right=1,
                             y_bottom=0.3,
                             y_top=1.01)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"conc_2__v__posi_1.svg"), format="svg")



# Find erro_concr
# -----------
epsi_1 = [1/3,1/4,1/5,1/10,1/20,1/30,1/40,1/80]

posi_1  = numpy.linspace(0,1,101,endpoint=True)
macr_1 = numpy.exp(-alph*posi_1)


erro_conc_1 = []
erro_eta_1 = []
for epsi in epsi_1:
    micr_1 = (1-alph*posi_1*epsi)**(1/epsi)

    inte_macr_1 = integrate.trapezoid(macr_1,dx=posi_1[1]-posi_1[0])
    inte_micr_1 = integrate.trapezoid(micr_1,dx=posi_1[1]-posi_1[0])

    erro_conc = inte_macr_1-inte_micr_1
    erro_conc_1.append(erro_conc)

    erro_eta = macr_1[-1]-micr_1[-1]
    erro_eta_1.append(erro_eta)


# Plot log-log of error to find fit
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

epsi_smth_1 = numpy.linspace(0,0.5,101,endpoint=True)

x_1 = numpy.log(epsi_1)
y_1 = numpy.log(erro_conc_1)

m_conc = 1.05
c_conc = -2.35

x_smth_1 = numpy.log(epsi_smth_1)
fit_conc_1 = m_conc*x_smth_1+c_conc

ax.scatter(x_1,y_1, c="tab:blue")
ax.plot(x_smth_1,fit_conc_1, c="tab:blue")



y_1 = numpy.log(erro_eta_1)

m_eta = 1.05
c_eta = -1.50

x_smth_1 = numpy.log(epsi_smth_1)
fit_eta_1 = m_eta*x_smth_1+c_eta

ax.scatter(x_1,y_1, c="tab:orange")
ax.plot(x_smth_1,fit_eta_1, c="tab:orange")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$\mathrm{log}(\varepsilon)$",
                             y_label=r"$\mathrm{log}(E)$",
                             x_left=None,
                             x_right=0,
                             y_bottom=None,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"log-erro_1__v__log-epsi_1.svg"), format="svg")






plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

ax.scatter(epsi_1,erro_conc_1, c="tab:blue", label=r"$E_c$")
fit_1       = numpy.exp(c_conc)*epsi_smth_1**m_conc
ax.plot(epsi_smth_1,fit_1, c="tab:blue")
print(r"$c_conc={:.3f},m_conc={}$".format(numpy.exp(c_conc), m_conc))


ax.scatter(epsi_1,erro_eta_1, c="tab:orange", label=r"$E_\eta$")
fit_1       = numpy.exp(c_eta)*epsi_smth_1**m_eta
ax.plot(epsi_smth_1,fit_1,c="tab:orange")#, label=r"${:.3f}\varepsilon^{}$".format(numpy.exp(c_eta), m_eta))
print(r"$c_eta={:.3f},m_eta={}$".format(numpy.exp(c_eta), m_eta))


plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$\varepsilon$",
                             y_label=r"$\mathrm{Error}$",
                             x_left=0,
                             x_right=None,
                             y_bottom=0,
                             y_top=None)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"erro_1__v__epsi_1.svg"), format="svg")
