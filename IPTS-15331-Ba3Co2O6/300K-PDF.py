outDir = '/SNS/users/rwp/corelli/IPTS-15331-Ba3Co2O6/'

ConvertMultipleRunsToSingleCrystalMD(Filename='CORELLI_20153:20229',SetGoniometer=True,Axis0='BL9:Mot:Sample:Axis1,0,1,0,1',OutputWorkspace='md',MinValues=[-15,-15,-15],MaxValues=[15,15,15])

FindPeaksMD(InputWorkspace='md', MaxPeaks=500, DensityThresholdFactor=100, OutputWorkspace='peaks')
FindUBUsingFFT(PeaksWorkspace='peaks', MinD=1, MaxD=15)
SaveIsawUB('peaks', outDir+'Ba3Co2O6_300K.mat')

ShowPossibleCells(PeaksWorkspace='peaks')
SelectCellOfType(PeaksWorkspace='peaks', CellType='Hexagonal', Apply=True)
SaveIsawUB('peaks', outDir+'Ba3Co2O6_300K_H.mat')


FindPeaksMD(InputWorkspace='md', MaxPeaks=1000, DensityThresholdFactor=100, OutputWorkspace='peaks')
FindUBUsingFFT(PeaksWorkspace='peaks', MinD=1, MaxD=15)
ShowPossibleCells(PeaksWorkspace='peaks', AllowPermutations=False)
SelectCellOfType(PeaksWorkspace='peaks', CellType='Hexagonal', Apply=True)
IndexPeaks(PeaksWorkspace='peaks')
OptimizeLatticeForCellType(PeaksWorkspace='peaks', CellType='Hexagonal', Apply=True)

SaveIsawUB('peaks', outDir+'Ba3Co2O6_300K.mat')

peaks=mtd['peaks']
ol=peaks.sample().getOrientedLattice()
ol.setc(ol.c()*2)
SaveIsawUB('peaks', outDir+'Ba3Co2O6_300K_2.mat')

SingleCrystalDiffuseReduction(Filename='CORELLI_20153:20229',
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
                              OutputWorkspace='output',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              UBMatrix=outDir+'Ba3Co2O6_300K_2.mat',
                              BinningDim0='-15.02,15.02,751',
                              BinningDim1='-15.02,15.02,751',
                              BinningDim2='-15.02,15.02,751')



# sym 152?
SingleCrystalDiffuseReduction(Filename='CORELLI_20153:20229',
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
                              OutputWorkspace='sym',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              UBMatrix=outDir+'Ba3Co2O6_300K_2.mat',
                              BinningDim0='-15.02,15.02,751',
                              BinningDim1='-15.02,15.02,751',
                              BinningDim2='-15.02,15.02,751',
                              SymmetryOps=152)

