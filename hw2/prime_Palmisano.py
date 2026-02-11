# Ethan Palmisano
# MET-330
# Dr. Christopher Phillips
# 22 September 2025
# I have neither given or received nor have I tolerated others' use of unauthorized aid.
#
# This code is for Homework 2.
# "Write a script that checks whether a number is prime. Recall that a prime number is only divisible by itself and 1. Be sure to print your result to the screen for the user."

user_num = int(input('Input your integer to check if it is prime: '))

tf = True # Starts true, goes through the checks. This also makes sure that 1 comes out as prime.
for n in range(2, user_num): # Excluding 1 and the number itself to see if it is divisible by any other number
	if (user_num % n) == 0:
		print(f'{int(user_num)} is not prime.')
		tf = False
		break
if tf == True:
	print(f'{int(user_num)} is prime!')