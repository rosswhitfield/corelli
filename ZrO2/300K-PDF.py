outDir = '/SNS/users/rwp/corelli/ZrO2/'

ConvertMultipleRunsToSingleCrystalMD(Filename='CORELLI_82204:82232', SetGoniometer=True, Axis0='BL9:Mot:Sample:Axis1,0,1,0,1', OutputWorkspace='md')
FindPeaksMD(InputWorkspace='md', PeakDistanceThreshold=0.25, DensityThresholdFactor=10000000, OutputWorkspace='peaks')
FindUBUsingFFT(PeaksWorkspace='peaks', MinD=1, MaxD=10)
SaveIsawUB('peaks', outDir+'ZrO2_300K.mat')

