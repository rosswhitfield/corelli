from mantid.simpleapi import *
import numpy as np
import math

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

def t_zero(x,A):
    return A*x

def scale_tof(tof,A):
    #t0 = t_zero( (distanceMtoM2/tof)**2*factor ,A)
    t0=A
    return (tof - t0)*scale + t0

s1=w.getEventList(1)

def new_monitor(A):
    out=np.zeros(len(y))
    t=s1.getTofs()
    cut=t.searchsorted(1000)
    t=t[cut:]
    tofs_new = scale_tof(t,A)
    try:
        for tof in tofs_new:
            out[int(tof/resolution)]+=1
    except IndexError:
        pass
    return out

def min_monitor(x):
    new=new_monitor(x)
    return sum(y2*new)

resA=[]
for A in np.arange(10,200,5.0):
    result=min_monitor(A)
    print A,result
    resA.append((A,result))


#plot results
xx=[]
yy=[]
for i in range(len(resA)):
    xx.append(resA[i][0])
    yy.append(resA[i][1])

outx=np.array(xx)
outy=np.array(yy)
np.savetxt(filename+"_constant_A.txt",np.transpose(np.array((outx,outy))),fmt="%f")
