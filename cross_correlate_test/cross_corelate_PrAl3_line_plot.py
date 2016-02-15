import numpy as np
import matplotlib.pyplot as plt
import math

Lmc=17.999347
Lcs=20-Lmc
#Lsd=ws.getInstrument().getDetector(168064).getDistance(i.getSample())
Lsd=2.586
L=Lmc+Lcs+Lsd


results_664=np.load('CORELLI_664_results.npy')
results_666=np.load('CORELLI_666_results.npy')

bin_size=10
xx=range(0,len(results_664[0])*bin_size,bin_size)


plt.plot(np.sum(results_664[10:15],axis=0))
plt.plot(np.sum(results_666[178:183],axis=0))
plt.show()

plt.plot(np.sum(results_664,axis=0))
plt.plot(np.sum(results_666,axis=0))
plt.show()



chopper_per_664=4245.9343705281253
chopper_per_666=3408.2893842061367

x=12000

y_664=((x*Lmc/L)-50)%chopper_per_664/10
y_666=((x*Lmc/L)-50)%chopper_per_666/10

yy_664=np.sum(results_664[y_664:y_664+5],axis=0)[x/10-15:x/10+15]
yy_666=np.sum(results_666[y_666:y_666+5],axis=0)[x/10-15:x/10+15]

plt.plot(xx,np.sum(results_664[y_664:y_664+5],axis=0))
plt.plot(xx,np.sum(results_666[y_666:y_666+5],axis=0))
plt.show()



from scipy.optimize import curve_fit

xxx=range(0,len(yy_664)*bin_size,bin_size)

def gauss(x, *p):
    A, mu, sigma = p
    return A*np.exp(-(x-mu)**2/(2.*sigma**2))

p0=[yy_664.max(), 15., 1.]

coeff, var_matrix = curve_fit(gauss, xxx, yy_664, p0=p0)
