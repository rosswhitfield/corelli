outDir = '/SNS/users/rwp/corelli/ZrO2/'

ConvertMultipleRunsToSingleCrystalMD(Filename='CORELLI_8192:8246',SetGoniometer=True,Axis0='BL9:Mot:Sample:Axis1,0,1,0,1',OutputWorkspace='md',MinValues=[-15,-15,-15],MaxValues=[15,15,15])
FindPeaksMD(InputWorkspace='md', PeakDistanceThreshold=0.25, DensityThresholdFactor=1000000, OutputWorkspace='peaks')
FindUBUsingFFT(PeaksWorkspace='peaks', MinD=4, MaxD=6)
SaveIsawUB('peaks', outDir+'ZrO2_300K.mat')

