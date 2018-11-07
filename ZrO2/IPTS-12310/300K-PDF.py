outDir = '/SNS/users/rwp/corelli/ZrO2/IPTS-12310/'

ConvertMultipleRunsToSingleCrystalMD(Filename='CORELLI_8569:8601',
                                     SetGoniometer=True,
                                     Axis0='BL9:Mot:Sample:Axis1,0,1,0,1',
                                     OutputWorkspace='md',
                                     MinValues=[-15,-15,-15],
                                     MaxValues=[15,15,15])

FindPeaksMD(InputWorkspace='md', DensityThresholdFactor=100, OutputWorkspace='peaks')
FindUBUsingFFT(PeaksWorkspace='peaks', MinD=4, MaxD=6)
ShowPossibleCells(PeaksWorkspace='peaks')
SelectCellOfType(PeaksWorkspace='peaks', CellType='Orthorhombic', Centering='F', Apply=True)
IndexPeaks(PeaksWorkspace='peaks')
OptimizeLatticeForCellType(PeaksWorkspace='peaks', Apply=True)

SaveIsawUB('peaks', outDir+'ZrO2_300K.mat')

SingleCrystalDiffuseReduction(Filename='CORELLI_8569:8601',
                              SolidAngle=outDir+'SA.nxs',
                              Flux=outDir+'Flux.nxs',
                              MaskFile=outDir+'mask.xml',
                              OutputWorkspace='output',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              UBMatrix=outDir+'ZrO2_300K.mat',
                              BinningDim0='-10.02,10.02,501',
                              BinningDim1='-10.02,10.02,501',
                              BinningDim2='-10.02,10.02,501')



SingleCrystalDiffuseReduction(Filename='CORELLI_8569:8601',
                              SolidAngle=outDir+'SA.nxs',
                              Flux=outDir+'Flux.nxs',
                              MaskFile=outDir+'mask.xml',
                              OutputWorkspace='sym',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              UBMatrix=outDir+'ZrO2_300K.mat',
                              BinningDim0='-10.02,10.02,501',
                              BinningDim1='-10.02,10.02,501',
                              BinningDim2='-10.02,10.02,501',
                              SymmetryOps='221') # Really 225

SaveMD('sym', outDir+'ZrO2_300K_sym.nxs')
