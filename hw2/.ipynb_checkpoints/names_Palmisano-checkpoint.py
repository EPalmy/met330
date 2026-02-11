# Ethan Palmisano
# MET-330
# Dr. Christopher Phillips
# 22 September 2025
# I have neither given or received nor have I tolerated others' use of unauthorized aid.
#
# This code is for Homework 2.
# "Write a script that prints the first name of people whose last name starts with “O”."

first_names = ['Betty Ann','John','Roan','Jane']
last_names = ['Johnson','Smith','Oak','Oston']

for f, l in zip(first_names, last_names):
	if l[0].lower() == 'o':
		print(f,l)