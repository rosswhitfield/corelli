from mantid.simpleapi import Load, SetGoniometer, ConvertToMD
import numpy as np

run1='CORELLI_48505'
run2='CORELLI_48513'

ws1=Load(run1)
ws2=Load(run2)

SetGoniometer(ws1,Axis0="BL9:Mot:Sample:Axis2.RBV,0,1,0,1")
SetGoniometer(ws2,Axis0="BL9:Mot:Sample:Axis2.RBV,0,1,0,1")

md1=ConvertToMD(ws1, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', MinValues=[-10,-10,-10], MaxValues=[10,10,10])
md2=ConvertToMD(ws2, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', MinValues=[-10,-10,-10], MaxValues=[10,10,10])

bin1=BinMD(md1, AlignedDim0='Q_sample_x,-10,10,1000', AlignedDim1='Q_sample_z,-10,10,1000', AlignedDim2='Q_sample_y,-10,10,1')
bin2=BinMD(md2, AlignedDim0='Q_sample_x,-10,10,1000', AlignedDim1='Q_sample_z,-10,10,1000', AlignedDim2='Q_sample_y,-10,10,1')
bin1/=ws1.run().getProtonCharge()
bin2/=ws2.run().getProtonCharge()
diff=bin2-bin1


s1=bin1.getSignalArray().copy()
s2=bin2.getSignalArray().copy()

x=np.linspace(-1,1,1000)
X,Y=np.meshgrid(x,x)
mask = X**2 + Y**2 >1

s1_mask = s1 < 100

mask[s1_mask[:,:,0]] = True
#mask[s2[:,:,0]==0] = True



s1[mask]=np.nan

start=ws1.getRun().getLogData('BL9:Mot:Sample:Axis2.RBV').value.mean()

for angle in np.arange(-0.03,-0.01,0.001):
    SetGoniometer(ws2,Axis0=str(start+angle)+',0,1,0,1')
    md2=ConvertToMD(ws2, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', MinValues=[-10,-10,-10], MaxValues=[10,10,10])
    bin2=BinMD(md2, AlignedDim0='Q_sample_x,-10,10,1000', AlignedDim1='Q_sample_z,-10,10,1000', AlignedDim2='Q_sample_y,-10,10,1')
    bin2/=ws2.run().getProtonCharge()
    s2=bin2.getSignalArray().copy()
    s2[mask]=np.nan
    corr=np.nansum(s1*s2)
    print(angle,corr)

