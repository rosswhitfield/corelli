outDir = '/SNS/users/rwp/corelli/ZrO2/'

ConvertMultipleRunsToSingleCrystalMD(Filename='CORELLI_7647:7709',
                                     SetGoniometer=True,
                                     Axis0='BL9:Mot:Sample:Axis1,0,1,0,1',
                                     OutputWorkspace='md',
                                     MinValues=[-15,-15,-15],
                                     MaxValues=[15,15,15])
FindPeaksMD(InputWorkspace='md', PeakDistanceThreshold=0.25, DensityThresholdFactor=10000, OutputWorkspace='peaks')
FindUBUsingFFT(PeaksWorkspace='peaks', MinD=4, MaxD=6)
ShowPossibleCells(PeaksWorkspace='peaks')
SelectCellOfType(PeaksWorkspace='peaks', CellType='Cubic', Centering='F', Apply=True)
IndexPeaks(PeaksWorkspace='peaks')
OptimizeLatticeForCellType(PeaksWorkspace='peaks', Apply=True)

SaveIsawUB('peaks', outDir+'ZrO2_480K.mat')

SingleCrystalDiffuseReduction(Filename='CORELLI_7647:7709',
                              SolidAngle=outDir+'IPTS-12310/SA.nxs',
                              Flux=outDir+'IPTS-12310/Flux.nxs',
                              OutputWorkspace='output',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              UBMatrix=outDir+'ZrO2_480K.mat',
                              BinningDim0='-10.02,10.02,501',
                              BinningDim1='-10.02,10.02,501',
                              BinningDim2='-10.02,10.02,501')

SingleCrystalDiffuseReduction(Filename='CORELLI_7647:7709',
                              SolidAngle=outDir+'IPTS-12310/SA.nxs',
                              Flux=outDir+'IPTS-12310/Flux.nxs',
                              OutputWorkspace='sym',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              UBMatrix=outDir+'ZrO2_480K.mat',
                              BinningDim0='-10.02,10.02,501',
                              BinningDim1='-10.02,10.02,501',
                              BinningDim2='-10.02,10.02,501',
                              SymmetryOps='221') # Really 225

SaveMD('sym', outDir+'ZrO2_480K_sym.nxs')
