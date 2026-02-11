# Ethan Palmisano
# This code asks a user for wind speed and direction and outputs the wind vector.

# Import Modules
import math

try:
    # Ask for wind speed and direction
    wspd = float(input('Please give the wind speed in kts: '))
    wdir = float(input('Please give the wind direction in degrees: '))
    wdir = 270.0-wdir # Fix wind angle for trig

    # Compute the vector components
    uwind = wspd*math.cos(wdir*3.14159/180.0)
    vwind = wspd*math.sin(wdir*3.14159/180.0)

    # Output the result
    print(f'The wind vector is: <{uwind:.2f}i,{vwind:.2f}j>')
except:
    print('Please input units in correct format.')