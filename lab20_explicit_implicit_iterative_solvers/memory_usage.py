import numpy as np
from numpy.linalg import inv
import psutil
# arr = np.ones((170_000,), dtype=np.uint8)

n = 5000
M = np.random.rand(n,n)
Minv = inv(M)

np.allclose(np.dot(M, Minv), np.eye(n))

# mem = psutil.virtual_memory()
# print(mem)

# https://en.wikipedia.org/wiki/Resident_set_size
# In computing, resident set size (RSS) is the portion of memory occupied by a process 
# that is held in main memory (RAM). 
# The rest of the occupied memory exists in the swap space or file system, 
# either because some parts of the occupied memory were paged out, 
# or because some parts of the executable were never loaded.

# psutil.Process().memory_info().rss  # in bytes 
print(f"Memory used by process: {psutil.Process().memory_info().rss/(1024*1024)} [MB]")
