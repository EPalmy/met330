import numpy as np
a = np.array([1,2,4,8,12])
#print(a[a>4])
mask = a>4

b = np.array([35,76,0,-2,5])

print(mask,b[mask],np.sum(mask))