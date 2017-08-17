#!/opt/Mantid/bin/mantidpython
from __future__ import print_function
from mantid.simpleapi import Load, SetGoniometer, ConvertToMD, BinMD
import numpy as np
import sys

run1='CORELLI_'+sys.argv[1]
run2='CORELLI_'+sys.argv[2]
filename=sys.argv[3]

ws1=Load(run1)
ws2=Load(run2)

SetGoniometer(ws1,Axis0="BL9:Mot:Sample:Axis2,0,1,0,1")
SetGoniometer(ws2,Axis0="BL9:Mot:Sample:Axis2,0,1,0,1")

md1=ConvertToMD(ws1, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', MinValues=[-10,-10,-10], MaxValues=[10,10,10])

bin1=BinMD(md1, AlignedDim0='Q_sample_x,-10,10,1000', AlignedDim1='Q_sample_z,-10,10,1000', AlignedDim2='Q_sample_y,-10,10,1')
bin1/=ws1.run().getProtonCharge()

s1=bin1.getSignalArray().copy()

x=np.linspace(-1,1,1000)
X,Y=np.meshgrid(x,x)
mask = (X**2 + Y**2 >1) + (X**2 + Y**2 < 0.25)

s1[mask] = 0

s1_mask = s1 < np.percentile(s1,99.9)

mask[s1_mask[:,:,0]] = True

s1[mask]=np.nan

start=ws2.getRun().getLogData('BL9:Mot:Sample:Axis2.RBV').value.mean()

max_corr=0
max_angle=0

for angle in np.arange(-0.1,0.1,0.01):
    SetGoniometer(ws2,Axis0=str(start+angle)+',0,1,0,1')
    md2=ConvertToMD(ws2, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', MinValues=[-10,-10,-10], MaxValues=[10,10,10])
    bin2=BinMD(md2, AlignedDim0='Q_sample_x,-10,10,1000', AlignedDim1='Q_sample_z,-10,10,1000', AlignedDim2='Q_sample_y,-10,10,1')
    bin2/=ws2.run().getProtonCharge()
    s2=bin2.getSignalArray().copy()
    s2[mask]=np.nan
    corr=np.nansum(s1*s2)
    if corr>max_corr:
        max_corr = corr
        max_angle=angle

print("Actual = ",start+max_angle, "Diff = ", max_angle)
with open(filename,'a') as f:
    f.write(run1+' '+run2+' '+'Actual = '+str(start+max_angle)+' Diff = '+str(max_angle)+'\n')
