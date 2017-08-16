from mantid.simpleapi import Load, SetGoniometer, ConvertToMD
import numpy as np

run1='CORELLI_48505'
run2='CORELLI_48513'

ws1=Load(run1)
ws2=Load(run2)

SetGoniometer(ws1,Axis0="BL9:Mot:Sample:Axis2,0,1,0,1")
SetGoniometer(ws2,Axis0="BL9:Mot:Sample:Axis2,0,1,0,1")

md1=ConvertToMD(ws1, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', MinValues=[-10,-10,-10], MaxValues=[10,10,10])
md2=ConvertToMD(ws2, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', MinValues=[-10,-10,-10], MaxValues=[10,10,10])

bin1=BinMD(md1, AlignedDim0='Q_sample_x,-10,10,1000', AlignedDim1='Q_sample_z,-10,10,1000', AlignedDim2='Q_sample_y,-10,10,1')
bin2=BinMD(md2, AlignedDim0='Q_sample_x,-10,10,1000', AlignedDim1='Q_sample_z,-10,10,1000', AlignedDim2='Q_sample_y,-10,10,1')
bin1/=ws1.run().getProtonCharge()
bin2/=ws2.run().getProtonCharge()
diff=bin2-bin1
