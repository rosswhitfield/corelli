from mantid.simpleapi import *
import numpy as np
import matplotlib.pyplot as plt

filename="CORELLI_11005"
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
    3023,
    3163,
    3292,
    3486,
    3549,
    3615,
    3700,
    3797,
    3944,
    4140,
    4302,
    4414,
    4563,
    4755,
    4905,
    5021,
    5102,
    5246,
    5380,
    5446,
    5590,
    5707,
    5773,
    5873,
    5968,
    6186,
    6265,
    6441,
    6640,
    6790,
    6889,
    7019,
    7133,
    7248,
    7314,
    7379,
    7610,
    7709,
    7823,
    7988,
    8084,
    8166,
    8346,
    8528,
    8609,
    8724,
    9020,
    9116,
    9182,
    9283,
    9347,
    9430,
    9592,
    9860,
    10136,
    10200,
    10265,
    10380,
    10512,
    10612,
    10776,
    10957,
    11104,
    11250,
    11379,
    11514,
    11644,
    11842,
    11905,
    11970,
    12054,
    12153
]

plt.plot(x1[:-1],y1)
plt.plot(m2,y1[m2],linestyle='None',marker=u'v',markersize=10)
plt.show()

m3=[
    4098,
    4275,
    4455,
    4717,
    4807,
    4896,
    5008,
    5143,
    5340,
    5607,
    5831,
    5983,
    6184,
    6456,
    6652,
    6808,
    6920,
    7123,
    7299,
    7388,
    7590,
    7744,
    7833,
    7967,
    8100,
    8390,
    8501,
    8750,
    9014,
    9215,
    9348,
    9526,
    9682,
    9838,
    9927,
    10016,
    10327,
    10462,
    10618,
    10842,
    10976,
    11086,
    11333,
    11576,
    11686,
    11844,
    12246,
    12380,
    12468,
    12603,
    12692,
    12804,
    13027,
    13383,
    13760,
    13850,
    13939,
    14095,
    14274,
    14408,
    14628,
    14876,
    15076,
    15279,
    15455,
    15634,
    15813,
    16080,
    16169,
    16258,
    16370,
    16503
]

plt.plot(x2[:-1],y2)
plt.plot(m3,y2[m3],linestyle='None',marker=u'v',markersize=10)
plt.show()

NeutronMass = 1.674927211e-27
meV = 1.602176487e-22

d=6.502
distanceMtoM3=24.554
distanceMtoM2=18.052


e=np.zeros(len(m2))
t0=np.zeros(len(m2))
for i in range(len(m2)):
    v=d/(m3[i]-m2[i])
    e[i]=v**2*0.5e+12*NeutronMass/meV
    t0[i]=m2[i]-(m3[i]-m2[i])/d*distanceMtoM2

plt.plot(e,t0,marker='.',markersize=20)
plt.show()
