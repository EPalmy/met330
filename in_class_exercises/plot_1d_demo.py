import matplotlib.pyplot as plt
import numpy as np
x = np.arange(0,4*np.pi, 0.01)
y = np.sin(x)
y2 = np.cos(x)
#y3 = 1/y
fig, ax = plt.subplots()
ax.plot(x,y,color='blue',label='sin(x)')
ax.plot(x,y2,color='red',label='cos(x)')
#ax.plot(x,y3,color='green',label='arcsin(x)')
ax.legend(loc='lower left')
plt.savefig('plot_demo.png')