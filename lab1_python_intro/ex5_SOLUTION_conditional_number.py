#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 19:05:22 2020

@author: grzegorz
"""

import numpy as np
from numpy import linalg as LA

def dot_product(u,v):
    return u @ v

def calc_condition_number_naive(f, u, v, delta):
    cond_number = LA.norm(f(u+delta, v) - f(u,v)) / LA.norm(f(u,v))
    cond_number /= LA.norm(u+delta)/LA.norm(u)
    return cond_number


x0 = np.array([1, 2, 3])
x1 = np.array([2, 6, -5])

dx = 0.02 * x0
# dx = np.array([0.02, 0.04, -0.04])
c = calc_condition_number_naive(dot_product, x0, x1, dx)
print(c)

# calculate the difference explicitly
print(
      abs(1 - ((x0 + dx) @ x1 / (x0 @ x1) ))
      )