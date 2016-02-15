from mantid.simpleapi import *
from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import argrelextrema

LoadNexusMonitors(Filename='/SNS/CORELLI/IPTS-12310/nexus/CORELLI_13115.nxs.h5', OutputWorkspace='CORELLI_13115')
Rebin(InputWorkspace='CORELLI_13115', OutputWorkspace='CORELLI_13115', Params='-0.01,0.1,16666.5')
COR_13115=mtd['CORELLI_13115']
m1,m2,m3=COR_13115.extractY()
x1,x2,x3=COR_13115.extractX()

x=np.arange(0.05,16666.55,0.1)

plt.plot(x,m2)
plt.show()



#1

Rebin(InputWorkspace='CORELLI_13115', OutputWorkspace='CORELLI_13115', Params='9.99,1,16666.5')
COR_13115=mtd['CORELLI_13115']
m1,m2,m3=COR_13115.extractY()
x1,x2,x3=COR_13115.extractX()
x=np.arange(10.5,16666.55,1)

plt.plot(x,m2)
plt.show()

# Derivative
d=m2[1:]-m2[:-1]
minima=argrelextrema(d,np.less_equal,order=22)[0]
maxima=argrelextrema(d,np.greater_equal,order=25)[0]

plt.scatter(minima,d[minima])
plt.scatter(maxima,d[maxima])

plt.plot(m2/16)
plt.plot(d)
plt.show()

minima_mask=np.ma.masked_where(d[minima]>-100,minima)
minima_mask_points=[3385,4270,5669,9682,6109,6944,7742,9727,10372,10955,11714,12303,12654,12855,13020]
for point in minima_mask_points:
    a = np.argwhere(minima==point)
    minima_mask.mask[a]=True

maxima_mask=np.ma.masked_where(d[maxima]<100,maxima)
maxima_mask_points=[3434,3985,4283,4549,4684,6620,7781,8027,10416,11766,12649,12905]
for point in maxima_mask_points:
    a = np.argwhere(maxima==point)
    maxima_mask.mask[a]=True

plt.scatter(minima_mask,d[minima_mask])
plt.scatter(maxima_mask,d[maxima_mask])

plt.plot(m2/16)
plt.plot(d)
plt.show()

right=np.extract(np.invert(minima_mask.mask),minima_mask)
left=np.extract(np.invert(maxima_mask.mask),maxima_mask)
centre=(x[right]+x[left])/2
plt.plot(m2)
plt.plot()




# M3

d=m3[1:]-m3[:-1]
minima=argrelextrema(d,np.less_equal,order=40)[0]
maxima=argrelextrema(d,np.greater_equal,order=49)[0]

plt.scatter(minima,d[minima])
plt.scatter(maxima,d[maxima])

plt.plot(m3/10)
plt.plot(d)
plt.show()

minima_mask=np.ma.masked_where(d[minima]>-50,minima)
minima_mask_points=[]
for point in minima_mask_points:
    a = np.argwhere(minima==point)
    minima_mask.mask[a]=True

maxima_mask=np.ma.masked_where(d[maxima]<50,maxima)
maxima_mask_points=[]
for point in maxima_mask_points:
    a = np.argwhere(maxima==point)
    maxima_mask.mask[a]=True

plt.scatter(minima_mask,d[minima_mask])
plt.scatter(maxima_mask,d[maxima_mask])

plt.plot(m3/10)
plt.plot(d)
plt.show()

right=np.extract(np.invert(minima_mask.mask),minima_mask)
left=np.extract(np.invert(maxima_mask.mask),maxima_mask)
centre=(x[right]+x[left])/2
plt.plot(m3)
plt.plot()


                        
# Smooth
Rebin(InputWorkspace='CORELLI_13115', OutputWorkspace='CORELLI_13115', Params='9.99,0.1,16666.59')
SmoothData(InputWorkspace='CORELLI_13115', OutputWorkspace='CORELLI_13115s',NPoints=100)
COR_13115=mtd['CORELLI_13115s']
m1,m2,m3=COR_13115.extractY()
x1,x2,x3=COR_13115.extractX()
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


d2ave=average(d2,100)
plt.plot(d2)
plt.plot(d2ave)
plt.show()

minima=argrelextrema(d2ave,np.less_equal,order=500)[0]
maxima=argrelextrema(d2ave,np.greater_equal,order=500)[0]

minima_mask=np.ma.masked_where(d2ave[minima]>-0.8,minima)
maxima_mask=np.ma.masked_where(d2ave[maxima]<0.8,maxima)


plt.scatter(minima_mask,d2ave[minima_mask])
plt.scatter(maxima_mask,d2ave[maxima_mask])

plt.plot(m2/100)
plt.plot(d2ave)
plt.show()





d3ave=average(d3,100)
plt.plot(d3)
plt.plot(d3ave)
plt.show()

minima3=argrelextrema(d3ave,np.less_equal,order=500)[0]
maxima3=argrelextrema(d3ave,np.greater_equal,order=500)[0]

minima3_mask=np.ma.masked_where(d3ave[minima3]>-0.06,minima3)
maxima3_mask=np.ma.masked_where(d3ave[maxima3]<0.06,maxima3)


plt.scatter(minima3_mask,d3ave[minima3_mask])
plt.scatter(maxima3_mask,d3ave[maxima3_mask])

plt.plot(m3/200)
plt.plot(d3ave)
plt.show()





right2=np.extract(np.invert(minima_mask.mask),minima_mask)
left2=np.extract(np.invert(maxima_mask.mask),maxima_mask)
right3=np.extract(np.invert(minima3_mask.mask),minima3_mask)
left3=np.extract(np.invert(maxima3_mask.mask),maxima3_mask)

#left3=np.roll(left3,-6)
#right3=np.roll(right3,-6)


NeutronMass = 1.674927211e-27
meV = 1.602176487e-22

d=6.502
distanceMtoM3=24.554
distanceMtoM2=18.052

e=[]
t0=[]
for i in range(76):
    r3=x[right3[np.mod(i+5,77)]]
    if r3<1000:
        r3+=16666.6
    v=d/(r3-x[right2[i]])
    e.append(v**2*0.5e+12*NeutronMass/meV)
    t0.append(x[right2[i]]-distanceMtoM2/v)
    print i,r3,v,e[-1],t0[-1]

#plt.plot(e,t0,'o')
#plt.show()

e=[]
t0=[]
for i in range(78):
    l3=x[left3[np.mod(i+6,78)]]
    if l3<1000:
        l3+=16666.6
    v=d/(l3-x[left2[i]])
    e.append(v**2*0.5e+12*NeutronMass/meV)
    t0.append(x[left2[i]]-distanceMtoM2/v)
    print i,l3,v,e[-1],t0[-1]

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

# Use centre

centre2=(x[left2]+x[right2])/2

ec=[]
t0c=[]
for i in range(77):
    centre3=(x[left3[np.mod(i+6,78)]]+x[right3[np.mod(i+5,77)]])/2
    if centre3<1000:
        centre3+=16666.6
    v=d/(centre3-centre2[i])
    ec.append(v**2*0.5e+12*NeutronMass/meV)
    t0c.append(centre2[i]-distanceMtoM2/v)
    print i,centre3,v,ec[-1],t0c[-1]

plt.plot(ec,t0c,'o')
plt.show()
