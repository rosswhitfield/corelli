```python
# Convert first 5 minutes of each run to MDEventWorkspace in Q Sample
ConvertMultipleRunsToSingleCrystalMD(Filename='CORELLI_29782:29817',
                                     SetGoniometer=True,
				     FilterByTimeStop=300,
                                     Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                                     MinValues='-10,-10,-10',
                                     MaxValues='10,10,10',
                                     OutputWorkspace='md')

# Find the peaks in the MD Workspace
FindPeaksMD(InputWorkspace='md',
            DensityThresholdFactor=1000,
            PeakDistanceThreshold=0.5,
            OutputWorkspace='peaks')

# Determine the UB matrix from the peaks
FindUBUsingFFT(PeaksWorkspace='peaks', MinD=5, MaxD=15)

# Show possible cell of UB
ShowPossibleCells(PeaksWorkspace='peaks')

# Select desired cell
SelectCellOfType(PeaksWorkspace='peaks',CellType='Hexagonal',Apply=True)

# Save the UB matix
SaveIsawUB(InputWorkspace='peaks', Filename='benzil.mat')

# Reduced data to a correctly normalised MDHistoWorkspace with P 31 2 1 symmetry
SingleCrystalDiffuseReduction(Filename='CORELLI_29782:29817',
                              Background='CORELLI_28124',
                              BackgroundScale=0.95,
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
                              UBMatrix="benzil.mat",
                              OutputWorkspace='output',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              BinningDim0='-10.05,10.05,201',
                              BinningDim1='-10.05,10.05,201',
                              BinningDim2='-0.1,0.1,1',
                              SymmetryOps="P 31 2 1")

# Save the reduced workspace
SaveMD(InputWorkspace='output', Filename='benzil.nxs')
```
