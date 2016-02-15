from mantid.simpleapi import *
from matplotlib import pyplot as plt
from scipy.optimize import minimize
import numpy as np

filename="CORELLI_11005" #120Hz
filename="CORELLI_11004" #60Hz
resolution=0.5

w=LoadNexusMonitors(Filename='/SNS/CORELLI/IPTS-12310/nexus/'+filename+'.nxs.h5',OutputWorkspace=filename)
SortEvents(w)
#new=ModeratorTzero(w)

source = w.getInstrument().getSource()
distanceMtoM3 = source.getDistance(w.getInstrument().getComponentByName("monitor3"))
distanceMtoM2 = source.getDistance(w.getInstrument().getComponentByName("monitor2"))
scale=distanceMtoM3/distanceMtoM2

def min_func(x):
    SetInstrumentParameter(w,ParameterName="t0_formula",Value=str(x[0]))
    new=ModeratorTzero(w)
    SortEvents(new)
    new_scaled=ScaleX(new,Factor=scale)
    new=Rebin(new,Params='3700,'+str(resolution)+',16600')
    new_scaled=Rebin(new_scaled,Params='3700,'+str(resolution)+',16600')
    y0_new,y1_new,y2_new=new.extractY()
    y0_new_scaled,y1_new_scaled,y2_new_scaled=new_scaled.extractY()
    results = 1/np.sum(np.sqrt(y2_new*y1_new_scaled))
    print x,results
    return results


x0=[70]
bounds=[(60,80)]
res = minimize(min_func,x0,bounds=bounds,options={'disp': True})
res = minimize(min_func,x0,options={'disp': True})

x0=[60]
res = minimize(min_func,x0,method='L-BFGS-B',bounds=bounds,options={'disp': True, 'eps':1})
res = minimize(min_func,x0,method='SLSQP',bounds=bounds,options={'disp': True, 'eps':1})


plt.plot(y2_new)
plt.plot(y1_new_scaled)
plt.show()

r=[]
for i in range(0,200,10):
    r.append([i,min_func([i])])
    print r

r=np.array(r)
plt.plot(r[:,0],r[:,1])
#plt.show()


r2=[]
for i in range(60,80,1):
    r2.append([i,min_func([i])])
    print r2

r2=np.array(r2)
plt.plot(r2[:,0],r2[:,1])
#plt.show()

r3=[]
for i in np.arange(71,72.5,0.1):
    r3.append([i,min_func([i])])
    print r3

r3=np.array(r3)
plt.plot(r3[:,0],r3[:,1])
plt.show()


#min at 72us
