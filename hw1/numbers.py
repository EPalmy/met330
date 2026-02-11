# Ethan Palmisano
# 10 September 2025
# MET-330
#
# This code is built to do some basic math for HW #1.

# Import Modules
import math

# Do the calculations, use try/except in case user inputs something that is not a number.
try:
	num1 = float(input('Please input your first number: '))
	num2 = float(input('Please input your second number: '))
	main_num = str((math.sqrt(num1*num2))+4) # Calculate the square root of the input numbers and add 4.
	print(f'Your new number is {main_num}')
except:
	print('Please only input numbers.')
