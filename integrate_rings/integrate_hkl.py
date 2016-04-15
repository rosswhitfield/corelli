#!/usr/bin/env python2
from mantid.simpleapi import *
from matplotlib import pyplot as plt
import numpy as np

LoadMD(Filename = "/SNS/CORELLI/IPTS-15796/shared/20160401-FeS/normData_LT_No2_6K_Large_V2.nxs", OutputWorkspace = 'md')

md=mtd['md']

s = md.getSignalArray()

# x.getX(397) = 1.9873332977294922
# x.getX(398) = 2.002666473388672
# y.getX(300) = -4.76837158203125e-07
# z.getX(7) = -0.10000002384185791
# z.getX(7) = 0.10000002384185791

s[398,300,7]


plt.imshow(s[:,:,7],clim=[0,0.002])
plt.ion()
plt.show()

#create q array
x=md.getXDimension()
x_step = (x.getMaximum() - x.getMinimum())/(x.getNBins())
qx = np.arange(x.getMinimum()+x_step/2, x.getMaximum()+x_step/2, x_step)
y=md.getYDimension()
y_step = (y.getMaximum() - y.getMinimum())/(y.getNBins())
qy = np.arange(y.getMinimum()+y_step/2, y.getMaximum()+y_step/2, y_step)
z=md.getZDimension()
z_step = (z.getMaximum() - z.getMinimum())/(z.getNBins())
qz = np.arange(z.getMinimum()+z_step/2, z.getMaximum()+z_step/2, z_step)

xd=3.7
yd=5.08
zd=3.7

qx *= 2*np.pi/xd
qy *= 2*np.pi/yd
qz *= 2*np.pi/zd

qx.shape = [x.getNBins(), 1, 1]
qy.shape = [1, y.getNBins(), 1]
qz.shape = [1, 1, z.getNBins()]

q = np.sqrt(qx**2 + qy**2 + qz**2)

def get_q(h,k,l):
    return np.sqrt((h*2*np.pi/xd)**2
                   + (l*2*np.pi/yd)**2
                   + (k*2*np.pi/zd)**2)

a = np.logical_or(q < get_q(1.95,0,0), q > get_q(2.08,0,0))
new=np.ma.array(s,mask=a)
plt.imshow(new[:,:,7],clim=[0,0.002])
plt.show()


# get angle array

h=2
k=0
l=0

a = np.logical_or(q < get_q(1.95,0,0), q > get_q(2.08,0,0))
length=np.sqrt(h**2+k**2+l**2)
angle = np.arccos((qx*h + qy*l + qz*k)/(q*length))
b = np.logical_or(a, angle > 20*np.pi/180)
new=np.ma.array(s,mask=b)
plt.clf()
plt.imshow(new[:,:,7],clim=[0,0.002])



# 00-2

h=0
k=0
l=-2
a = np.logical_or(q < get_q(0,0,-1.96), q > get_q(0,0,-2.08))
length=np.sqrt(h**2+k**2+l**2)
angle = np.arccos((qx*h + qy*l + qz*k)/(q*length))
b = np.logical_or(a, angle > 20*np.pi/180)
new=np.ma.array(s,mask=b)
(new-new.min()).sum()
new.count()
