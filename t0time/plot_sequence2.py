from mantid.simpleapi import *
import numpy as np
import matplotlib.pyplot as plt

filename="CORELLI_11004"
LoadNexusMonitors(Filename='/SNS/CORELLI/IPTS-12310/nexus/'+filename+'.nxs.h5',OutputWorkspace=filename)
w = mtd[filename]

bin_size=1

Rebin(InputWorkspace=filename,OutputWorkspace=filename,Params=str(bin_size))
x0,x1,x2=w.extractX()
y0,y1,y2=w.extractY()

plt.plot(x1[:-1],y1)
plt.plot(x2[:-1],y2)
plt.show()

m2=[
    3005,
    3200,
    3692,
    3916,
    4046,
    4176,
    4636,
    4834,
    5056,
    5383,
    5581,
    5747,
    6096,
    6469,
    6623,
    6862,
    7444,
    7648,
    7779,
    7978,
    8108,
    8269,
    8589,
    9121,
    9684,
    9814,
    9946,
    10170,
    10437,
    10634,
    10959,
    11320,
    11618,
    11913,
    12176,
    12436,
    12695
]

plt.plot(x1[:-1],y1)
plt.plot(m2,y1[m2],linestyle='None',marker=u'v',markersize=10)
plt.show()

m3=[
    4061,
    4328,
    4993,
    5300,
    5475,
    5654,
    6275,
    6546,
    6858,
    7303,
    7570,
    7792,
    8280,
    8773,
    8993,
    9306,
    10109,
    10376,
    10555,
    10821,
    11001,
    11221,
    11671,
    12382,
    13140,
    13320,
    13498,
    13812,
    14170,
    14436,
    14877,
    15372,
    15774,
    16174,
    16530,
    224+16667,
    574+16667,
]

plt.plot(x2[:-1],y2)
plt.plot(m3,y2[m3],linestyle='None',marker=u'v',markersize=10)
plt.show()

NeutronMass = 1.674927211e-27
meV = 1.602176487e-22

d=6.502
distanceMtoM3=24.554
distanceMtoM2=18.052


e_2=np.zeros(len(m2))
t0_2=np.zeros(len(m2))
for i in range(len(m2)):
    v=d/(m3[i]-m2[i])
    e_2[i]=v**2*0.5e+12*NeutronMass/meV
    t0_2[i]=m2[i]-(m3[i]-m2[i])/d*distanceMtoM2

plt.plot(e_2,t0_2,marker='.',markersize=20)
plt.show()

ex=np.array(range(10,200))
A=101.9
B=0.41
C=282.0
plt.plot(ex,A*ex**(-B)*np.exp(-ex/C))
plt.plot(e,t0,marker='.',markersize=20)
plt.plot(e_2,t0_2,marker='.',markersize=20)
plt.show()

from scipy.optimize import curve_fit

def t_zero(x,A,B,C):
    return A*x**(-B)

popt, pcov = curve_fit(t_zero,e,t0)
plt.plot(e,t0,marker='.',markersize=20)
plt.plot(ex,t_zero(ex,popt[0],popt[1],popt[2]))
plt.plot(ex,t_zero(ex,86,0.098,1))
plt.show()

popt2, pcov2 = curve_fit(t_zero,e_2,t0_2)
plt.plot(e_2,t0_2,marker='.',markersize=20)
plt.plot(ex,t_zero(ex,popt2[0],popt2[1],popt2[2]))
plt.show()


# t0 = 86.0 e_i**(-0.098)
