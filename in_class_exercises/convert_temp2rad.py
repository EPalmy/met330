# Code for messing with converting temperature to radians
# Does nothing meaninful
# Ethan Palmisano

str_temp = input("What's the temperature in Kelvin?")
try:
    flt_temp = float(str_temp)
    flt_tempF = (flt_temp-273.15)*9.0/5.0+32.0
    rad_temp = flt_tempF/(2*3.14159265358979323846264338327950288419917)
    print(f'The temperature in radians F is {rad_temp:02f}')
except:
    print('Please input a real number.')