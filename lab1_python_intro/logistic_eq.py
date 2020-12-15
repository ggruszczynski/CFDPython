#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 11:15:26 2020

@author: grzegorz
"""


import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


N = 1000

r = np.linspace(0, 4, N)
y0 = 0.3
y = y0


fig, ax = plt.subplots()

steps = 1000
for i in range(steps):
    y = r*y*(1-y)
    if i > 100:
        ax.plot(r, y, color="red", marker="x", linestyle="", markersize=0.005)
        # ax.plot(r, y, color="red", marker="x", markevery=1, markersize=0.01, linestyle="")


plt.grid(True)
plt.legend()
plt.xlabel("r")
plt.ylabel("y")
plt.title("Logistic Eq")

fig.tight_layout()
fig.savefig('logistic_eq.png', bbox_inches='tight', dpi=500)
plt.show()
plt.close(fig)  # close the figure

print("Done.")
