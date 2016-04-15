#!/usr/bin/env python2
from mantid.simpleapi import *
import numpy as np

md = LoadMD(Filename = "/SNS/CORELLI/IPTS-15796/shared/20160401-FeS/normData_LT_No2_6K_Large_V2.nxs")
s = md.getSignalArray().copy()

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

xd=3.71
yd=5.08
zd=3.71

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

def get_peak(h,k,l,dq,da):
    """
    (h k l) of target peak
    dq is ±% in q
    da is range in degrees from peak
    """
    s1 = 1-dq
    s2 = 1+dq
    q_mask = np.logical_or(q < get_q(h*s1, k*s1, l*s1), q > get_q(h*s2, k*s2, l*s2))
    length=np.sqrt(h**2+k**2+l**2)
    angle = np.arccos((qx*h + qy*l + qz*k)/(q*length))
    angle_mask = np.logical_or(q_mask, angle > da*np.pi/180)
    new=np.ma.array(s,mask=angle_mask)
    return new

# 200
peak_200 = get_peak(2,0,0,0.035,20)
print peak_200.count(),peak_200.min(),peak_200.max(),peak_200.sum()
print peak_200[:,:,7].count(),peak_200[:,:,7].min(),peak_200[:,:,7].max(),peak_200[:,:,7].sum()
md.setSignalArray(np.ma.filled(peak_200,np.nan)) # Apply to workspace

# 00-2
peak_00n2 = get_peak(0,0,-2,0.035,15)
print peak_00n2.count(),peak_00n2.min(),peak_00n2.max(),peak_00n2.sum()
md.setSignalArray(np.ma.filled(peak_00n2,np.nan)) # Apply to workspace

# back to origonal
md.setSignalArray(s)
