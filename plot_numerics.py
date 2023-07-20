from matplotlib import pyplot as plt
import os 
import numpy 
from scipy import integrate


import sys
sys.path.append("/home/user/utils_python")
import plotting

# Parameters 
# -----
path_results = os.path.join("/home/user/projects/papers/2023_homogenisation/figures/numerics")

import sys
sys.path.append("/home/user/utils_python")
import plotting

def get_wpc(T,X,L,N,S):
    return T*X**L + S*N**L

def get_npc(T,X,L,N):
    return T*X**L + T*X*N**L

def get_mm(T,A,B,L,N):
    return T*(A*B*N)**L

# def get_wpc_repeat(T,X,L,N,S,R):
#     return R*T*X**L + S*N**L

# def get_npc_repeat(T,X,L,N,R):
#     return R*(T*X**L + T*X*N**L)

# def get_mm_repeat(T,A,B,L,N,R):
#     return R*(T*(A*B*N)**L)

T = 500
X = 100
S = 100
A = 100
B = 1

#L = 3
L_1 = numpy.linspace(2,3,5,endpoint=True)
N_1 = numpy.linspace(1,1000,1001,dtype=int)

# Plot npc over wpc
# ----------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

# N_1 = numpy.linspace(1,10,10,dtype=int)**2
# wpc_2 = numpy.zeros(shape=(len(L_1),len(N_1)))
# npc_2 = numpy.zeros(shape=(len(L_1),len(N_1)))
# mm_2  = numpy.zeros(shape=(len(L_1),len(N_1)))
# for l,L in enumerate(L_1):
#     for n,N in enumerate(N_1):
#         wpc = get_wpc(T,X,L,N,S)
#         npc = get_npc(T,X,L,N)
#         mm  = get_mm(T,A,B,L,N)
#         wpc_2[l,n] = wpc
#         npc_2[l,n] = npc
#         mm_2[l,n]  = mm

#         #plt.scatter(N,npc/wpc, color="tab:blue")



wpc_2 = numpy.zeros(shape=(len(L_1),len(N_1)))
npc_2 = numpy.zeros(shape=(len(L_1),len(N_1)))
mm_2  = numpy.zeros(shape=(len(L_1),len(N_1)))
for l,L in enumerate(L_1):
    for n,N in enumerate(N_1):
        wpc = get_wpc(T,X,L,N,S)
        npc = get_npc(T,X,L,N)
        mm  = get_mm(T,A,B,L,N)
        if N==30 and L==2.0:
            print(npc/wpc)
        wpc_2[l,n] = wpc
        npc_2[l,n] = npc
        mm_2[l,n]  = mm

for l,L in enumerate(L_1):
    plt.plot(N_1,npc_2[l,:]/wpc_2[l,:], color="tab:blue")
    #plt.plot(N_1,numpy.ones_like(N_1), ls="--",color="tab:orange")

plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$N$",
                             y_label=r"$C_{\mathrm{NPC}}/C_{\mathrm{WPC}}$",
                             x_left=0,
                             x_right=1000,
                             y_bottom=0.0,
                             y_top=500)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"npc_over_wpc__v__N.svg"), format="svg")


# Plot mm over wpc
# ----------
plotting.thesisify_pre_ax_creation()
fig, ax = plt.subplots(1,1)

N_1 = numpy.linspace(1,100,101,dtype=int)
wpc_2 = numpy.zeros(shape=(len(L_1),len(N_1)))
npc_2 = numpy.zeros(shape=(len(L_1),len(N_1)))
mm_2  = numpy.zeros(shape=(len(L_1),len(N_1)))
for l,L in enumerate(L_1):
    for n,N in enumerate(N_1):
        wpc = get_wpc(T,X,L,N,S)
        npc = get_npc(T,X,L,N)
        mm  = get_mm(T,A,B,L,N)
        if N==32 and L==2.0:
            print(mm/wpc)
        wpc_2[l,n] = wpc
        npc_2[l,n] = npc
        mm_2[l,n]  = mm

for l,L in enumerate(L_1):
    plt.plot(N_1,mm_2[l,:]/wpc_2[l,:], color="tab:blue")
    plt.plot(N_1,(5/6)*N_1**L, ls="--",color="tab:orange")


plotting.thesisify_post_plot(ax=ax,
                             x_label=r"$N$",
                             y_label=r"$C_{\mathrm{MM}}/C_{\mathrm{WPC}}$",
                             x_left=0,
                             x_right=100,
                             y_bottom=0.0,
                             y_top=10000)

plotting.save_fig(fig=fig,fname=os.path.join(path_results,"mm_over_wpc__v__N.svg"), format="svg")








# T = 500
# X = 100
# S = 100
# L = 3
# A = 100
# B = 1
# L = 2.5


# #R_1 = [1,10,100,1000,10000]
# R_1 = numpy.linspace(1,10,5)

# # Plot npc over wpc repeat
# # ----------
# plotting.thesisify_pre_ax_creation()
# fig, ax = plt.subplots(1,1)

# N_1 = numpy.linspace(1,100,101,dtype=int)
# wpc_2 = numpy.zeros(shape=(len(R_1),len(N_1)))
# npc_2 = numpy.zeros(shape=(len(R_1),len(N_1)))
# mm_2  = numpy.zeros(shape=(len(R_1),len(N_1)))
# for r,R in enumerate(R_1):
#     for n,N in enumerate(N_1):
#         wpc = get_wpc_repeat(T,X,L,N,S,R)
#         npc = get_npc_repeat(T,X,L,N,R)
#         mm  = get_mm_repeat(T,A,B,L,N,R)
#         wpc_2[r,n] = wpc
#         npc_2[r,n] = npc
#         mm_2[r,n]  = mm

# for r,R in enumerate(R_1):
#     plt.plot(N_1,npc_2[r,:]/wpc_2[r,:], color="tab:blue")

# plotting.thesisify_post_plot(ax=ax,
#                              x_label=r"$N$",
#                              y_label=r"$C_{\mathrm{NPC-R}}/C_{\mathrm{WPC-R}}$",
#                              x_left=0,
#                              x_right=100,
#                              y_bottom=0.0,
#                              y_top=None)

# plotting.save_fig(fig=fig,fname=os.path.join(path_results,"npc_over_wpc_repeat__v__N.svg"), format="svg")


# # Plot mm over wpc
# # ----------
# plotting.thesisify_pre_ax_creation()
# fig, ax = plt.subplots(1,1)

# N_1 = numpy.linspace(1,100,101,dtype=int)
# wpc_2 = numpy.zeros(shape=(len(R_1),len(N_1)))
# npc_2 = numpy.zeros(shape=(len(R_1),len(N_1)))
# mm_2  = numpy.zeros(shape=(len(R_1),len(N_1)))
# for r,R in enumerate(R_1):
#     for n,N in enumerate(N_1):
#         wpc = get_wpc_repeat(T,X,L,N,S,R)
#         npc = get_npc_repeat(T,X,L,N,R)
#         mm  = get_mm_repeat(T,A,B,L,N,R)
#         wpc_2[r,n] = wpc
#         npc_2[r,n] = npc
#         mm_2[r,n]  = mm

# for r,R in enumerate(R_1):
#     plt.plot(N_1,mm_2[r,:]/wpc_2[r,:], color="tab:blue")

# plotting.thesisify_post_plot(ax=ax,
#                              x_label=r"$N$",
#                              y_label=r"$C_{\mathrm{MM-R}}/C_{\mathrm{WPC-R}}$",
#                              x_left=0,
#                              x_right=100,
#                              y_bottom=0.0,
#                              y_top=100)

# plotting.save_fig(fig=fig,fname=os.path.join(path_results,"mm_over_wpc_repeat__v__N.svg"), format="svg")
