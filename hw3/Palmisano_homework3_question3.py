# Ethan Palmisano
# MET-330
# Dr. Christopher Phillips
# 3 October 2025
# I have neither given or receieved nor have I tolerated others' use of unauthorized aid.

# Instructions: Create a numpy array of numbers 212 through 237 and print that array.
# Reshape that array into one with 2 rows and 13 columns. Print the array and its shape.

# Import Modules
import numpy as np

arr = np.arange(212, 238, 1) # Create Main Array
print(arr)

arr = np.reshape(arr,(2,13)) # Reshape Array
print(arr, arr.shape)