# Ethan Palmisano
# MET-330
# Dr. Christopher Phillips
# 22 September 2025
# I have neither given or received nor have I tolerated others' use of unauthorized aid.
#
# This code is for question 3 in homework two.
# "Write a short script that stores the numbers divisible by 3 or 7 from 1 to 100 in a list. Then print that list."

my_list = []
for n in range(1, 101):
	if (n % 3) == 0 or (n % 7) == 0:
		my_list.append(n)
print(my_list)