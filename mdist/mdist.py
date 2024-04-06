import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import manhattan_distances

A = csr_matrix(np.array([[1,2,3],[8,9,0]],dtype=np.float64))
B = csr_matrix(np.array([[1,2,4],[3,4,5]],dtype=np.float64))

C = manhattan_distances(A, B)
print(A)
print(B)
print(C)