import matplotlib.pyplot as plt
import numpy as np

results=np.load('CORELLI_29782-29788_results_events_b1_all_banks.npy')

y,x = results.shape
xx=np.array(range(x))*1
yy=np.array(range(y))*10
X,Y = np.meshgrid(xx,yy)
plt.pcolormesh(X, Y, results, vmin=0)

plt.colorbar()
plt.title('Benzil all banks')
plt.xlabel('total time of flight (uS)')
plt.ylabel('incident flight time (uS)')
plt.savefig('bresults_events_b1_all_bank.png')

