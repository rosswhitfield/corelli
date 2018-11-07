outDir = '/SNS/users/rwp/corelli/ZrO2/'

ConvertMultipleRunsToSingleCrystalMD(Filename='CORELLI_2340:2360',
                                     SetGoniometer=True,
                                     Axis0='BL9:Mot:Sample:Axis1,0,1,0,1', # Something is wrong with the goniometer
                                     OutputWorkspace='md',
                                     MinValues=[-15,-15,-15],
                                     MaxValues=[15,15,15])
FindPeaksMD(InputWorkspace='md', PeakDistanceThreshold=0.25, DensityThresholdFactor=10000, OutputWorkspace='peaks')
FindUBUsingFFT(PeaksWorkspace='peaks', MinD=4, MaxD=6)
ShowPossibleCells(PeaksWorkspace='peaks')
SelectCellOfType(PeaksWorkspace='peaks', CellType='Cubic', Centering='F', Apply=True)
IndexPeaks(PeaksWorkspace='peaks')
OptimizeLatticeForCellType(PeaksWorkspace='peaks', Apply=True)

SaveIsawUB('peaks', outDir+'CaZrO2_300K.mat')

SingleCrystalDiffuseReduction(Filename='CORELLI_2274:2318',
                              SolidAngle=outDir+'IPTS-12310/SA.nxs',
                              Flux=outDir+'IPTS-12310/Flux.nxs',
                              OutputWorkspace='output',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              UBMatrix=outDir+'CaZrO2_300K.mat',
                              BinningDim0='-10.02,10.02,501',
                              BinningDim1='-10.02,10.02,501',
                              BinningDim2='-10.02,10.02,501')

SingleCrystalDiffuseReduction(Filename='CORELLI_2274:2318',
                              SolidAngle=outDir+'IPTS-12310/SA.nxs',
                              Flux=outDir+'IPTS-12310/Flux.nxs',
                              OutputWorkspace='sym',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              UBMatrix=outDir+'CaZrO2_300K.mat',
                              BinningDim0='-10.02,10.02,501',
                              BinningDim1='-10.02,10.02,501',
                              BinningDim2='-10.02,10.02,501',
                              SymmetryOps='221') # Really 225

SaveMD('sym', outDir+'CaZrO2_300K_sym.nxs')
