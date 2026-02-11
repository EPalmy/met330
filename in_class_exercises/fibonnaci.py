# Ethan Palmisano
# MET-330
# Code for running the Fibonnaci Sequence Until 55

num_1 = 0
num_2 = 1
fib = num_1+num_2

while fib <= 55:
    print(fib)
    fib = num_1+num_2
    num_1 = num_2
    num_2 = fib