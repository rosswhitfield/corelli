from mantid.simpleapi import *
from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import argrelextrema

LoadNexusMonitors(Filename='/SNS/CORELLI/IPTS-12310/nexus/CORELLI_13977.nxs.h5', OutputWorkspace='CORELLI_13977')
LoadNexusMonitors(Filename='/SNS/CORELLI/IPTS-12310/nexus/CORELLI_13978.nxs.h5', OutputWorkspace='CORELLI_13978')
#LoadNexusMonitors(Filename='/SNS/CORELLI/IPTS-12310/nexus/CORELLI_13979.nxs.h5', OutputWorkspace='CORELLI_13979')

MergeRuns(InputWorkspaces='CORELLI_13977,CORELLI_13978',OutputWorkspace='CORELLI_180')

# Smooth
Rebin(InputWorkspace='CORELLI_180', OutputWorkspace='CORELLI_180', Params='9.99,0.1,16666.59')
SmoothData(InputWorkspace='CORELLI_180', OutputWorkspace='CORELLI_180s',NPoints=100)
COR_180=mtd['CORELLI_180s']
m1,m2,m3=COR_180.extractY()
x1,x2,x3=COR_180.extractX()
x=np.arange(10.05,16666.65,0.1)
d2=m2[1:]-m2[:-1]
d3=m3[1:]-m3[:-1]
plt.plot(m2/10)
plt.plot(d2)
plt.show()
plt.plot(m3/10)
plt.plot(d3)
plt.show()


def average(x,n=3):
    out = np.zeros(len(x))
    for i in range(n,len(x)-n-1):
        out[i]=x[i]
        for j in range(n):
            out[i]+=x[i-j]
            out[i]+=x[i+j]
    out/=n*2+1
    return out


def cleanDoubles(x,lookup):
    out = np.zeros(len(x))
    out[0]=x[0]
    count=0
    for i in range(1,len(x)):
        if x[i]-x[i-1]<100 and lookup[x[i]]==lookup[x[i-1]]:
            continue
        count+=1
        out[count]=x[i]
    out=out[:count]
    return out

d2ave=average(d2,100)
plt.plot(d2)
plt.plot(d2ave)
plt.show()

minima=argrelextrema(d2ave,np.less_equal,order=400)[0]
maxima=argrelextrema(d2ave,np.greater_equal,order=400)[0]

minima_mask=np.ma.masked_where(d2ave[minima]>-0.45,minima)
maxima_mask=np.ma.masked_where(d2ave[maxima]<0.45,maxima)


plt.scatter(minima_mask,d2ave[minima_mask])
plt.scatter(maxima_mask,d2ave[maxima_mask])

plt.plot(m2/100)
plt.plot(d2ave)
plt.show()





d3ave=average(d3,101)
plt.plot(d3)
plt.plot(d3ave)
plt.show()

minima3=argrelextrema(d3ave,np.less_equal,order=400)[0]
maxima3=argrelextrema(d3ave,np.greater_equal,order=400)[0]

minima3_mask=np.ma.masked_where(d3ave[minima3]>-0.030,minima3)
maxima3_mask=np.ma.masked_where(d3ave[maxima3]<0.030,maxima3)


plt.scatter(minima3_mask,d3ave[minima3_mask])
plt.scatter(maxima3_mask,d3ave[maxima3_mask])

plt.plot(m3/200)
plt.plot(d3ave)
plt.show()





right2=np.extract(np.invert(minima_mask.mask),minima_mask)
left2=np.extract(np.invert(maxima_mask.mask),maxima_mask)
right3=np.extract(np.invert(minima3_mask.mask),minima3_mask)
left3=np.extract(np.invert(maxima3_mask.mask),maxima3_mask)

left2=cleanDoubles(left2,d2ave)
right2=cleanDoubles(right2,d2ave)
left3=cleanDoubles(left3,d3ave)
right3=cleanDoubles(right3,d3ave)


#left3=np.roll(left3,-6)
#right3=np.roll(right3,-6)


NeutronMass = 1.674927211e-27
meV = 1.602176487e-22

d=6.502
distanceMtoM3=24.554
distanceMtoM2=18.052

e=[]
t0=[]
for i in range(4,107):
    r3=x[right3[np.mod(i+2,1000)]]
    if r3<1000:
        r3+=16666.6
    v=d/(r3-x[right2[i]])
    e.append(v**2*0.5e+12*NeutronMass/meV)
    t0.append(x[right2[i]]-distanceMtoM2/v)
    print i,x[right2[i]],r3,v,e[-1],t0[-1]

plt.plot(e,t0,'o')
plt.show()

e=[]
t0=[]
for i in range(4,107):
    l3=x[left3[np.mod(i+1,1000)]]
    if l3<1000:
        l3+=16666.6
    v=d/(l3-x[left2[i]])
    e.append(v**2*0.5e+12*NeutronMass/meV)
    t0.append(x[left2[i]]-distanceMtoM2/v)
    print i,x[left2[i]],l3,v,e[-1],t0[-1]

plt.plot(e,t0,'o')
plt.show()

# Fit

from scipy.optimize import curve_fit

def t_zero(x,A,B,C):
    return A*x**(-B)*np.exp(x/-C)

popt, pcov = curve_fit(t_zero,e,t0)
ex=np.array(range(5,220))
A=101.9
B=0.41
C=282.0
plt.plot(ex,A*ex**(-B)*np.exp(-ex/C))
plt.plot(e,t0,'o',markersize=5)
plt.plot(ex,t_zero(ex,popt[0],popt[1],popt[2]))
plt.show()

