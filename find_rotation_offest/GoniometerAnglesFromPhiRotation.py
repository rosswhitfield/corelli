run1='CORELLI_48505'
run2='CORELLI_48513'

ws1=Load(run1)
ws2=Load(run2)

SetGoniometer(ws1,Axis0="BL9:Mot:Sample:Axis2,0,1,0,1")
SetGoniometer(ws2,Axis0="BL9:Mot:Sample:Axis2,0,1,0,1")

md1=ConvertToMD(ws1, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', MinValues=[-10,-10,-10], MaxValues=[10,10,10])
md2=ConvertToMD(ws2, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', MinValues=[-10,-10,-10], MaxValues=[10,10,10])

peaks1=FindPeaksMD(md1,PeakDistanceThreshold=0.25,DensityThresholdFactor=10000)
peaks2=FindPeaksMD(md2,PeakDistanceThreshold=0.25,DensityThresholdFactor=10000)


GoniometerAnglesFromPhiRotation(peaks1,peaks2,MIND=0.5,MAXD=5)
