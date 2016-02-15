from mantid.simpleapi import *
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

filename="CORELLI_11005" #120Hz
filename="CORELLI_11004" #60Hz
resolution=0.1

w=LoadNexusMonitors(Filename='/SNS/CORELLI/IPTS-12310/nexus/'+filename+'.nxs.h5',OutputWorkspace=filename)

source = w.getInstrument().getSource()
cc = w.getInstrument().getComponentByName("correlation-chopper")
distanceMtoM3 = source.getDistance(w.getInstrument().getComponentByName("monitor3"))
distanceMtoM2 = source.getDistance(w.getInstrument().getComponentByName("monitor2"))
distanceM2toM3 = w.getInstrument().getComponentByName("monitor2").getDistance(w.getInstrument().getComponentByName("monitor3"))

scale=distanceMtoM3/distanceMtoM2


Rebin(InputWorkspace=filename,OutputWorkspace=filename,Params='0,'+str(resolution)+',16666')
x=w.extractX()[1]
y=w.extractY()[1]
x2=w.extractX()[2]
y2=w.extractY()[2]

#plt.plot(x[:-1],y)
#plt.plot(x2[:-1],y2)
#plt.show()

NeutronMass = 1.674927211e-27
meV = 1.602176487e-22
factor = 0.5e+12*NeutronMass/meV

# t0 = (101.9 * incidentEnergy^(-0.41) * exp(-incidentEnergy/282.0))
# t0 = A*x^(-B)*exp(-x/C)

def t_zero(x,A=101.9,B=0.41,C=282.0):
    return A*x**(-B)*np.exp(-x/C)

# for event in monitor 2
# calculate energy and then t0
# (tof-t0)
# (tof-t0)*scale

def scale_tof(tof,A=101.9,B=0.41,C=282.0):
    t0 = t_zero( (distanceMtoM2/tof)**2*factor ,A,B,C)
    return (tof - t0)*scale + t0
    

s1=w.getEventList(1)
tofs_new = scale_tof(s1.getTofs())

yyy=np.zeros(len(y))
for tof in tofs_new:
    yyy[int(tof/resolution)]+=1

#tofs_new_int = map(int,tofs_new)
#yyy=np.zeros(len(y))
#for tof in tofs_new_int:
#    yyy[tof]+=1

plt.plot(x[:-1],y)
plt.plot(x2[:-1],y2)
plt.plot(x2[:-1],yyy)
plt.show()

# compare scaled spectra to monitor 3
# minimise 1/correlation for A, B and C.


def new_monitor(A,B,C):
    out=np.zeros(len(y))
    tofs_new = scale_tof(s1.getTofs())
    for tof in s1.getTofs():
        out[int(tof/resolution)]+=1
    return out

