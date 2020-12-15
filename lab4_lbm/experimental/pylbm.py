#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 14:23:47 2020

@author: grzegorz

based on
"A concise Python implementation of the Lattice Boltzmann Method on HPC
for geo-fluid flow", Gabriele Morra, Geophysical Journal International · September 2019
"""

import os
import numpy as np
import matplotlib.pyplot as plt

c = np.array([
    [0,0],
    [1,0],
    [-1,0],
    [0,1],
    [0,-1],
    [1,1],
    [-1,-1],
    [1,-1],
    [-1,1],
    ])

ai = np.array([0,2,1,4,3,6,5,8,7])

na = 9 # number of lattice valocities
D = 2

w0 = 4./9
w1 = 1./9
w2 = 1./36

w = np.array([w0,w1,w1,w1,w1,w2,w2,w2,w2])

dt = 1
dx =1 
S =dx/dt

c1 =1.
c2 =3./(S**2)
c3 =9./(2.0*S**4)
c4 =-3./(2.0*S**2)

nu_f = 0.1 # viscosity
tau_f = nu_f * 3./(S*dt) + 0.5

nt = 200
nx = 101
nz = 101

# initialize arrays
f = np.zeros((na,nz,nx),dtype=float)
f_stream = np.zeros((na,nz,nx),dtype=float)
f_eq = np.zeros((na,nz,nx),dtype=float)
Delta_f = np.zeros((na,nz,nx),dtype=float)

rho = np.ones((nz,nx),dtype=float)
u = np.zeros((D,nz,nx),dtype=float)
Pi = np.zeros((D,nz,nx),dtype=float)
u2 = np.zeros((nz,nx),dtype=float)
cu = np.zeros((nz,nx),dtype=float)

# mark solid nodes

solid = np.zeros((na,nz,nx),dtype=int)
solid[:, 0, :] = 1
solid[:, -1, :] = 1

solid[:, nz//2: 5+nz//2, nx//4:5+nx//4] = 1
# initialize density

rho_0 = 1.0
rho*= rho_0
rho[nz//2,3*nx//4] = 2*rho_0

for a in np.arange(na):
    f[a] = rho * w[a]
    
    
indexes = np.zeros((na, nx*nz), dtype=int)

for a in range(na):
    xArr = (np.arange(nx) - c[a][0] + nx) % nx
    zArr = (np.arange(nz) - c[a][1] + nz) % nz
    xInd,zInd = np.meshgrid(xArr,zArr)
    indTotal = zInd*nx + xInd
    indexes[a] = indTotal.reshape(nx*nz)
    



def make_plot(data):
    T_num = data
    ny, nx = T_num.shape
        
    print("---------- PLOTTING -------------")
    x_grid = np.linspace(start=0, stop=nx, num=nx, endpoint=False)
    y_grid = np.linspace(start=0, stop=ny, num=ny, endpoint=False)
  
    xx, yy = np.meshgrid(x_grid, y_grid)
    T_num_slice = T_num[:, :]
    
    fig = plt.figure(figsize=(12, 8))
    ax = fig.gca()

    cntr = ax.pcolormesh(xx, yy, T_num_slice, cmap='coolwarm', label='T_num', shading='auto',
                         # norm=colors.LogNorm(vmin=9.975, vmax=11.025)
                         # vmin=9.98,
                         # vmax=11.02
                          )  # this one has smooth colors
    
    # cntr = ax.contourf(xx, yy, T_num_slice, cmap='coolwarm', antialiased=True)  # this one is has step colors
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_aspect('equal')

    # Add a color bar which maps values to colors.
    fig.colorbar(cntr, shrink=0.5, aspect=5)

    # plt.title(f'Field \n ')
    # plt.grid(True)  # or use default grid
    
    plotdir = os.path.join('plots')
    if not os.path.exists(plotdir):
        os.makedirs(plotdir)
    fig_name = f'{plotdir}/py_lbm.png'
    
    fig.savefig(fig_name, bbox_inches='tight')
    plt.show()
    plt.close(fig)  # close the figure
    

for t in np.arange(nt +1):
    print(f"iteration {t}")
    # periodic BC
    f[0:na,0:nz, 0] = f[0:na,0:nz, -2] 
    f[0:na,0:nz, -1] = f[0:na,0:nz, 1]
    
    # streaming term
    for a in range(na):
        f_new = f[a].reshape(nx*nz)[indexes[a]]
        # f_stream[a] = f_new.reshape(nz,nx)
        f_bounce  = f[ai[a]]
        f_stream[a] = solid[a]*f_bounce + (1-solid[a])*f_new.reshape(nz,nx)
        
    f = f_stream.copy()
    
    # macroscopic properties: rho and u
    rho = np.sum(f,axis=0)
    Pi = np.einsum('azx,ad->dzx',f,c)
    u[0:D]=Pi[0:D]/rho_0
    
    # Equilibrium distribution
    u2= u[0]*u[0] + u[1]*u[1]
    for a in np.arange(na):
        cu = c[a][0]*u[0]+c[a][1]*u[1]
        f_eq[a] = rho * w[a]*(c1+c2*cu+c3*cu**2+ c4*u2)
    
    # Collision
    Delta_f = (f_eq -f)/tau_f
    f += Delta_f
    
    
    

    if t % 10 == 0:
        print(np.sum(rho))
        make_plot(rho)