import matplotlib.pyplot as plt
import numpy as np
import math

rpm=7393


x=np.linspace(0, 50000, 5000)
y=np.linspace(0, 8120, 812)
X,Y = np.meshgrid(x,y)

results = np.load('results_373_4960-5024.npy')


fig, ax = plt.subplots()
p = ax.pcolormesh(X, Y, results, vmin=0, vmax=math.sqrt(results.max()))
cb = fig.colorbar(p, ax=ax)
fig.suptitle('DAS_373 pixelID:4960-5024')
ax.set_xlabel('total time of flight (uS)')
ax.set_ylabel('incident flight time (uS)')

r=23.2868/26.05091 #26.20091

f=(x*r)%8112
plt.plot(x,f,color='red')
fig.show()
