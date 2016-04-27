#!/usr/bin/env python2
from mantid.simpleapi import *
import numpy as np
from distutils.version import LooseVersion

md = LoadMD(Filename = "/SNS/CORELLI/IPTS-15796/shared/20160401-FeS/normData_LT_No2_6K_Large_V2.nxs")
s = md.getSignalArray().copy()

lattice = md.getExperimentInfo(0).sample().getOrientedLattice()

#create q array
x=md.getXDimension()
x_step = (x.getMaximum() - x.getMinimum())/(x.getNBins())
qx = np.arange(x.getMinimum()+x_step/2, x.getMaximum()+x_step/2, x_step).reshape([x.getNBins(), 1, 1])
y=md.getYDimension()
y_step = (y.getMaximum() - y.getMinimum())/(y.getNBins())
qy = np.arange(y.getMinimum()+y_step/2, y.getMaximum()+y_step/2, y_step).reshape([1, y.getNBins(), 1])
z=md.getZDimension()
z_step = (z.getMaximum() - z.getMinimum())/(z.getNBins())
qz = np.arange(z.getMinimum()+z_step/2, z.getMaximum()+z_step/2, z_step).reshape([1, 1, z.getNBins()])

qx *= lattice.astar()*2*np.pi
qy *= lattice.cstar()*2*np.pi
qz *= lattice.bstar()*2*np.pi

q = np.sqrt(qx**2 + qy**2 + qz**2)

def get_q(h,k,l):
    return lattice.dstar(h,k,l)*2*np.pi

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
peak_200 = get_peak(2,0,0,0.05,25)
print np.min(peak_200),np.max(peak_200),np.sum(peak_200)
print np.min(peak_200[:,:,7]),np.max(peak_200[:,:,7]),np.sum(peak_200[:,:,7])
md.setSignalArray(np.ma.filled(peak_200,np.nan)) # Apply to workspace

# 00-2
peak_00n2 = get_peak(0,0,-2,0.05,20)
print np.min(peak_00n2),np.max(peak_00n2),np.sum(peak_00n2)
md.setSignalArray(np.ma.filled(peak_00n2)) # Apply to workspace

# 00-1
peak_00n1 = get_peak(0,0,-1,0.15,25)
print np.min(peak_00n1),np.max(peak_00n1),np.sum(peak_00n1)
md.setSignalArray(np.ma.filled(peak_00n1)) # Apply to workspace

# 00-3
peak_00n3 = get_peak(0,0,-3,0.05,20)
print np.min(peak_00n3),np.max(peak_00n3),np.sum(peak_00n3)
md.setSignalArray(np.ma.filled(peak_00n3)) # Apply to workspace

# 201
peak_201 = get_peak(2,0,1,0.03,20)
print np.min(peak_201),np.max(peak_201),np.sum(peak_201)
md.setSignalArray(np.ma.filled(peak_201)) # Apply to workspace

# 20n1
peak_20n1 = get_peak(2,0,-1,0.03,20)
print np.min(peak_20n1),np.max(peak_20n1),np.sum(peak_20n1)
md.setSignalArray(np.ma.filled(peak_20n1)) # Apply to workspace

# back to original
md.setSignalArray(s)

def get_bg(array, percent=10):
    if LooseVersion(np.__version__)<LooseVersion("1.9.0"):
        from scipy.stats import scoreatpercentile
        flat = array.flatten()
        return scoreatpercentile(np.delete(flat, np.where(np.isnan(np.ma.filled(flat,np.nan)))),percent)
    else:
        return np.nanpercentile(np.ma.filled(array,np.nan),percent)



p200 = np.sum(peak_200-get_bg(peak_200))
p00n2 = np.sum(peak_00n2-get_bg(peak_00n2))
p00n1 = np.sum(peak_00n1-get_bg(peak_00n1))
p00n3 = np.sum(peak_00n3-get_bg(peak_00n3))
p201 = np.sum(peak_201-get_bg(peak_201))
p20n1 = np.sum(peak_20n1-get_bg(peak_20n1))

print p00n1, p200, p00n2, p00n3, p201, p20n1
