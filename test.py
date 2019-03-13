import numpy as np
array1 = np.array([[1,2,3],[3,4,5]])
print(array1.ndim)
print(array1.shape)
print(array1.size)
a = np.random.random((3,4))
print(a)
max = np.max(a,axis=0)
min = np.min(a,axis=1)
sum = np.sum(a,axis=1)
print(max)
print(min)
print(sum)

