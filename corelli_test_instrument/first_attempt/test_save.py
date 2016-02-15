import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

x=np.linspace(0, 50000, 5000)
y=np.linspace(0, 8120, 812)
X,Y = np.meshgrid(x,y)
out=np.load('out_374_4960-5024.npy')
fig, ax = plt.subplots()
p = ax.pcolormesh(X, Y, out)
cb = fig.colorbar(p, ax=ax)
fig.savefig('test.png')
