import numpy as np
import psutil

import scipy.sparse.linalg
from scipy.sparse import csc_matrix

np.random.seed(0)  

n = 3000
rhs = np.array(np.random.rand(n), dtype=np.float64)

# mtx = np.random.rand(n,n) 
mtx = scipy.sparse.random(n, n, density=0.01, dtype = np.float64).toarray()

# Direct method of solving system of linear equations
# https://developer.apple.com/documentation/accelerate/solving_systems_of_linear_equations_with_lapack
# https://stackoverflow.com/questions/31256252/why-does-numpy-linalg-solve-offer-more-precise-matrix-inversions-than-numpy-li
# mtx_inv = scipy.linalg.inv(mtx)
# np.allclose(np.dot(mtx, mtx_inv), np.eye(n))
# x = np.dot(mtx, rhs)

x = scipy.linalg.solve(mtx, rhs)
# np.allclose(np.dot(mtx, x), rhs)

# Now an iterative method
# https://scipy-lectures.org/advanced/scipy_sparse/solvers.html#iterative-solvers
# https://stackoverflow.com/questions/15755270/scipy-sparse-matrices-purpose-and-usage-of-different-implementations
# csc_matrix - converts the matrix to Compressed Sparse Column (CSC) format
# x = scipy.sparse.linalg.bicg(csc_matrix(mtx), rhs) # check the performance loss without converting to csc matrix
# x = scipy.sparse.linalg.bicg(mtx, rhs)
# x = scipy.sparse.linalg.gmres(csc_matrix(mtx), rhs)




# https://en.wikipedia.org/wiki/Resident_set_size
# In computing, resident set size (RSS) is the portion of memory occupied by a process 
# that is held in main memory (RAM). 
# The rest of the occupied memory exists in the swap space or file system, 
# either because some parts of the occupied memory were paged out, 
# or because some parts of the executable were never loaded.

print(f"Memory used by process: {psutil.Process().memory_info().rss/(1024*1024)} [MB]")  # convert from bytes to MB 

# print(psutil.virtual_memory())

#$ time python3 memory_usage.py