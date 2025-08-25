import numpy as np
import os

os.system('cls')

arr1 = np.arange(10)
print(arr1, end = '\n\n-----------\n\n')

arr2 = np.random.rand(3,3)
print(arr2, end = '\n\n-----------\n\n')

arr3 = np.arange(2, 21, 2)
print(arr3, end = '\n\n-----------\n\n')

arr4 = np.arange(10)
odd_indices = arr4[1::2]
print(odd_indices, end = '\n\n-----------\n\n')

arr5 = np.arange(1,10).reshape(3,3)
second_column = arr5[:, 1]
print(arr5, end = '\n\n')
print(second_column, end = '\n\n-----------\n\n')

arr6 =  np.arange(1,10).reshape(3,3)
inverted_array = np.flip(arr6)
print(arr6)
print(inverted_array, end = '\n\n-----------\n\n')


arr7 = np.arange(16).reshape(2,8)
print(arr7, end = '\n\n-----------\n\n')


arr8h = np.hstack((arr7,arr7))
arr8v = np.vstack((arr7,arr7))
print(arr8h,'\n\n-----------\n\n', arr8v, end = '\n\n-----------\n\n')