outDir = '/SNS/users/rwp/corelli/IPTS-15331-Ba3Co2O6/'

"""
ConvertMultipleRunsToSingleCrystalMD(Filename='CORELLI_20153:20229',SetGoniometer=True,Axis0='BL9:Mot:Sample:Axis1,0,1,0,1',OutputWorkspace='md',MinValues=[-15,-15,-15],MaxValues=[15,15,15])
FindPeaksMD(InputWorkspace='md', PeakDistanceThreshold=0.25, DensityThresholdFactor=500000, OutputWorkspace='peaks')
FindUBUsingFFT(PeaksWorkspace='peaks', MinD=4, MaxD=12)
ShowPossibleCells(PeaksWorkspace='peaks')
SelectCellOfType(PeaksWorkspace='peaks', CellType='Orthorhombic', Centering='F', Apply=True)
IndexPeaks(PeaksWorkspace='peaks')

SaveIsawUB('peaks', outDir+'ZrO2_300K.mat')
"""


SingleCrystalDiffuseReduction(Filename='CORELLI_20153:20229',
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
                              OutputWorkspace='output',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              UBMatrix=outDir+'Ba3Co2O6_UB_300K.mat',
                              BinningDim0='-10.02,10.02,501',
                              BinningDim1='-10.02,10.02,501',
                              BinningDim2='-10.02,10.02,501')
