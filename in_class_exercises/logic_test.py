# Ethan Palmisano
# MET-330
# In-class logic tests.

# Even Number Detector
'''
num = float(input('Number: '))
if (num % 2 == 0):
    print(f'{num} is even.')
else:
    print(f'{num} is odd.')
'''

# Ask for Relative Humidity
try:
    rh = float(input('Please give the relative humidity: '))
    if rh < 1:
        real_rh = rh*100
    elif rh > 100:
        i = 1 # Does nothing, which doesn't define real_rh, which causes an error, which runs the except function, which makes us need the real value.
    else:
        real_rh = rh
    if (real_rh % 1) == 0:
        real_rh = int(real_rh)
    print(f'The relative humidity is {real_rh}%')
except:
    print('Please input a possible value for relative humidity.')