from mantid.simpleapi import *
from matplotlib import pyplot as plt
import numpy as np
import math

filename="CORELLI_11005" #120Hz
filename="CORELLI_11004" #60Hz
resolution=1

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

def new_monitor(A,B,C):
    out=np.zeros(len(y))
    tofs_new = scale_tof(s1.getTofs(),A,B,C)
    try:
        for tof in tofs_new:
            out[int(tof/resolution)]+=1
    except IndexError:
        pass
    return out


y_old=new_monitor(101.9,0.41,282.0)
y_new=new_monitor(105,0.1,282.0)


plt.plot(x[:-1],y,label="monitor2")
plt.plot(x2[:-1],y2,label="monitor3")
plt.plot(x2[:-1],y_old,label="arcs")
plt.plot(x2[:-1],y_new,label="new")
plt.legend()
plt.show()



e=np.array(range(10,200))
arcs=t_zero(e,101.9,0.41,282.0)
new=t_zero(e,105,0.1,282.0)

plt.plot(e,arcs,label="arcs")
plt.plot(e,new,label="new")

#plt.plot(e,101.9*e**(-0.41)*np.exp(-e/1000.0),label="something")
#for i in np.arange(0.1,0.4,0.1):
#    plt.plot(e,101.9*e**(-i),label=str(i))

plt.plot(e,198.2*(1.0+e)**(-0.84098),label="CNCS")
plt.plot(e,100*e**(-0.1),label="VISION")
plt.plot(e,4.0+(107.0/(1.0+(e/31.0)**3)),label="HYSPEC")

plt.legend()
plt.show()
