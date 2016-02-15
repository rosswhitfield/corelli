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

def min_monitor(x):
    new=new_monitor(x[0],x[1],x[2])
    return sum(y2*new)

x0=[101.9,0.41,282.0]
bounds = [(0,10000),(0,10),(10,3000)]

res=[]

for A in range(10,220,100):
    for B in np.arange(0.1,1.2,0.5):
        for C in range(100,400,100):
            result=min_monitor([A,B,C])
            print A,B,C,result
            res.append((A,B,C,result))

print res



resB=[]
A=101.9
C=282.0
#for B in np.arange(0.00,0.25,0.01):
for B in np.arange(0.25,1.00,0.01):
    result=min_monitor([A,B,C])
    print B,result
    resB.append((A,B,C,result))


resA=[]
A=101.9
B=0.1
C=282.0
for A in range(50,150,5):
    result=min_monitor([A,B,C])
    print A,result
    resA.append((A,B,C,result))

resC=[]
A=105
B=0.1
C=282.0
for C in range(10,1000,20):
    result=min_monitor([A,B,C])
    print C,result
    resC.append((A,B,C,result))

for C in range(1000,100000,100):
    result=min_monitor([A,B,C])
    print C,result
    resC.append((A,B,C,result))

for C in range(100000,10000000,100000):
    result=min_monitor([A,B,C])
    print C,result
    resC.append((A,B,C,result))




#plot results
x=[]
y=[]
for i in range(len(resC)):
    x.append(resC[i][2])
    y.append(resC[i][3])

outx=np.array(x)
outy=np.array(y)
np.savetxt(filename+"resC.txt",np.transpose(np.array((outx,outy))),fmt="%f")

#plot results
x=[]
y=[]
for i in range(len(resA)):
    x.append(resA[i][0])
    y.append(resA[i][3])

outx=np.array(x)
outy=np.array(y)
np.savetxt(filename+"resA.txt",np.transpose(np.array((outx,outy))),fmt="%f")

#plot results
x=[]
y=[]
for i in range(len(resB)):
    x.append(resB[i][1])
    y.append(resB[i][3])

outx=np.array(x)
outy=np.array(y)
#np.savetxt(filename+"resB.txt",np.transpose(np.array((outx,outy))),fmt="%f")
np.savetxt(filename+"resB.txt2",np.transpose(np.array((outx,outy))),fmt="%f")
