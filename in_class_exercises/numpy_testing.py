# For Testing with Numpy

# Import Modules
import numpy as np


#print(new_array)
#print(type(new_array))
#print(len(new_array))

arr_size = 25
exponent = 2
#arr = np.zeros(arr_size)
#for i in range(0,arr_size):
#    arr[i] = i

ones_2d = np.ones((25,25),dtype='float')

my_array = np.arange(1,arr_size+1,dtype='float')
#my_array_2d = 
new_array = my_array*(my_array)**(exponent-1)

# For 2D
arr2d = new_array.reshape((5,5))
#print(arr2d)
#print(arr2d[2,1:3]) # slicing: [rows, columns]

# In class exercies here:

ic_arr = np.arange(200,401,5,dtype='int')

#print((ic_arr))

arr2D = np.array([[1,2,3],[4,5,6]])
print(arr2D)
print('Shape',arr2D.shape)
arr2DT = arr2D.transpose()
print('------------------')
print(arr2DT)
print('Shape',arr2DT.shape)
print('------------------')
arr2DR = arr2D.reshape(1,6)
print(arr2DR)
print('Shape',arr2DR.shape)