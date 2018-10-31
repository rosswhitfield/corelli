ConvertMultipleRunsToSingleCrystalMD(Filename='CORELLI_82204:82232', SetGoniometer=True, Axis0='BL9:Mot:Sample:Axis3,0,1,0,1', OutputWorkspace='md')
FindPeaksMD(InputWorkspace='md', PeakDistanceThreshold=0.25, DensityThresholdFactor=10000000, OutputWorkspace='peaks')
FindUBUsingFFT(PeaksWorkspace='peaks', MinD=1, MaxD=10)
SaveIsawUB('peaks', '/SNS/users/rwp/corelli/IPTS-20534/PMN/PMN_5K.mat')

SingleCrystalDiffuseReduction(Filename='CORELLI_82204:82232',
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2018B_1019_CCR/SolidAngle_CCR_20181019tot.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2018B_1019_CCR/Spectrum_CCR_20181019tot.nxs',
                              OutputWorkspace='output',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis3,0,1,0,1",
                              UBMatrix="/SNS/users/rwp/corelli/IPTS-20534/PMN/PMN_5K.mat",
                              BinningDim0='-10.01,10.01,501',
                              BinningDim1='-10.01,10.01,501',
                              BinningDim2='-10.01,10.01,501')


