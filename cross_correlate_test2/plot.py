import matplotlib.pyplot as plt
import numpy as np

results=np.load('CORELLI_30338_results.npy')
out=np.load('CORELLI_30338_out.npy')
events=np.load('CORELLI_30338_results_events.npy')
plt.imshow(out)
plt.show()
plt.imshow(results)
plt.show()
plt.imshow(events)
plt.show()

y,x = results.shape

xx=np.array(range(x))*10
yy=np.array(range(y))*10
X,Y = np.meshgrid(xx,yy)
plt.pcolormesh(X, Y, results, vmin=0, vmax=100)
plt.show()
plt.pcolormesh(X, Y, events, vmin=0, vmax=100)
plt.show()
