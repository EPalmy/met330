# Ethan Palmisano
# MET-330
# Dr. Christopher Phillips
# 9 September 2025
#
# This code is designed for the Practical 1 assignment, being to build the 3x+1 idea called the Collatz Conjecture.
# Note there is no try/except loop because Dr. Phillips said no :(

starting = float(input('Input your number: ')) # Take an input, make it a mathable number
if starting > 0 and (starting % 1 == 0): # Check to see if it is BOTH positive and an integer, just in case
    c = 0 # Counter
    n = starting
    # Main Function
    while n > 1:
        print(int(n)) # Used for debugging, can be toggled on just to see the fun of the code! (I think it's more fun)
        if (n % 2 == 0):
            n = n/2
        elif (n % 2 == 1):
            n = 3*n+1
        c += 1
    if n == 1: # End of cycle
        print(f'Your number, {int(starting)}, took {c} iterations to reach {int(n)}.')