# Ethan Palmisano
# MET-330
# This code takes three inputs from the user and prints each number's square at the end.

import math
try:

	list = [int(input('Please input your first number: ')),int(input('Please input your second number: ')),int(input('Please input your third number: '))]
	for number in list:
		print(f'Number is {number}, Square Root is {math.sqrt(number)}')
except:
	print('Please input numbers.')
