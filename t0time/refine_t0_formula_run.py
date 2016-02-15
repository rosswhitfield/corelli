import matplotlib.pyplot as plt
from mantid.simpleapi import *
import numpy as np
import math
from scipy.optimize import minimize

filename="CORELLI_11005" #120Hz
filename="CORELLI_11004" #60Hz
resolution=0.1

w=LoadNexusMonitors(Filename='/SNS/CORELLI/IPTS-12310/nexus/'+filename+'.nxs.h5',OutputWorkspace=filename)

source = w.getInstrument().getSource()
cc = w.getInstrument().getComponentByName("correlation-chopper")
distanceMtoM3 = source.getDistance(w.getInstrument().getComponentByName("monitor3"))
distanceMtoM2 = source.getDistance(w.getInstrument().getComponentByName("monitor2"))

scale=distanceMtoM3/distanceMtoM2

Rebin(InputWorkspace=filename,OutputWorkspace=filename,Params='0,'+str(resolution)+',16666')
x=w.extractX()[1]
y=w.extractY()[1]
x2=w.extractX()[2]
y2=w.extractY()[2]

NeutronMass = 1.674927211e-27
meV = 1.602176487e-22
factor = 0.5e+12*NeutronMass/meV

def t_zero(x,A,B,C):
    return A*x**(-B)*np.exp(-x/C)

def scale_tof(tof,A,B,C):
    t0 = t_zero( (distanceMtoM2/tof)**2*factor ,A,B,C)
    return (tof - t0)*scale + t0

s1=w.getEventList(1)
#tofs_new = scale_tof(s1.getTofs())

#yyy=np.zeros(len(y))
#for tof in tofs_new:
#    yyy[int(tof/resolution)]+=1

def new_monitor(A,B,C):
    out=np.zeros(len(y))
    tofs_new = scale_tof(s1.getTofs(),A,B,C)
    try:
        for tof in tofs_new:
            out[int(tof/resolution)]+=1
    except IndexError:
        pass
    return out

#yyy=new_monitor(101.9,0.41,282.0)
#plt.plot(x[:-1],y)
#plt.plot(x2[:-1],y2)
#plt.plot(x2[:-1],yyy)
#plt.show()


def min_monitor(x):
    new=new_monitor(x[0],x[1],x[2])
    #return 10000000000-sum(y2*new)
    return sum(y2*new)/1000000000

x0=[101.9,0.41,282.0]
bounds = [(0,10000),(0,10),(10,3000)]
res = minimize(min_monitor,x0,method='SLSQP',bounds=bounds,options={'disp':True})
print res
