This is an example 


### Convert first 5 minutes of each run to MDEventWorkspace in Q Sample
```python
ConvertMultipleRunsToSingleCrystalMD(Filename='CORELLI_29782:29817',
                                     SetGoniometer=True,
				     FilterByTimeStop=300,
                                     Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                                     MinValues='-10,-10,-10',
                                     MaxValues='10,10,10',
                                     OutputWorkspace='md')
```

### Find the peaks in the MD Workspace
```python
FindPeaksMD(InputWorkspace='md',
            DensityThresholdFactor=1000,
            PeakDistanceThreshold=0.5,
            OutputWorkspace='peaks')
```

Output:
```
FindPeaksMD-[Notice] Number of peaks found: 1392
```

### Determine the UB matrix from the peaks
```python
FindUBUsingFFT(PeaksWorkspace='peaks', MinD=5, MaxD=15)
```
Ouput:
```
FindUBUsingFFT-[Notice] UB = Matrix(3,3)-0.116063,-0.00491169,-0.00104935,0.00473709,-0.00415399,-0.0717701,0.0726847,-0.136834,0.0027504
FindUBUsingFFT-[Notice] New UB will index 1242 Peaks out of 1392 with tolerance of  0.15
FindUBUsingFFT-[Notice] Lattice Parameters:    8.430130    8.432962   13.933214   89.424205   89.608702   59.962020   857.446643
FindUBUsingFFT-[Notice] Parameter Errors  :    0.001625    0.001520    0.006167    0.027374    0.027659    0.013290    0.456602
```

### Show possible cell of UB
```python
ShowPossibleCells(PeaksWorkspace='peaks')
```
Output
```
ShowPossibleCells-[Notice] Num Cells : 5
ShowPossibleCells-[Notice] Form #12  Error: 0.0712  Hexagonal     P   Lat Par:   8.4301   8.4330  13.9332    89.424   90.391  120.038     857.45
ShowPossibleCells-[Notice] Form #13  Error: 0.0712  Orthorhombic  C   Lat Par:   8.4267  14.6067  13.9332    89.442   89.815   89.978    1714.89
ShowPossibleCells-[Notice] Form #29  Error: 0.0130  Monoclinic    C   Lat Par:   8.4330  14.5958  13.9332    89.881   90.576   90.027    1714.89
ShowPossibleCells-[Notice] Form #34  Error: 0.0723  Monoclinic    P   Lat Par:   8.4330  13.9332   8.4301    89.609  120.038   90.576     857.45
ShowPossibleCells-[Notice] Form #31  Error: 0.0000  Triclinic     P   Lat Par:   8.4301   8.4330  13.9332    89.424   89.609   59.962     857.45
```

### Select desired cell
```python
SelectCellOfType(PeaksWorkspace='peaks',CellType='Hexagonal',Apply=True)
```
Output
```
SelectCellOfType-[Notice] Form #12  Error: 0.0712  Hexagonal     P   Lat Par:   8.4301   8.4330  13.9332    89.424   90.391  120.038     857.45
SelectCellOfType-[Notice] Transformation Matrix =  0.955394 -0.0304891 -0.0692404 -0.0798105 -0.998756 0.00282608 -1.22455 0.0190936 -0.956639
SelectCellOfType-[Notice] Re-indexed the peaks with the new UB.
SelectCellOfType-[Notice] Now, 1173 are indexed with average error 0.0207209
```

### Save the UB matix
```python
SaveIsawUB(InputWorkspace='peaks', Filename='benzil.mat')
```

### Reduced data to a correctly normalised MDHistoWorkspace with P 31 2 1 symmetry
```python
SingleCrystalDiffuseReduction(Filename='CORELLI_29782:29817',
                              Background='CORELLI_28124',
                              BackgroundScale=0.95,
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
                              UBMatrix="benzil.mat",
                              OutputWorkspace='benzil',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              BinningDim0='-10.05,10.05,201',
                              BinningDim1='-10.05,10.05,201',
                              BinningDim2='-0.1,0.1,1',
                              SymmetryOps="P 31 2 1")
```

### Save the reduced workspace
```python
SaveMD(InputWorkspace='benzil', Filename='benzil.nxs')
```

* * *
#### Previous: [Creating Solid Angle and Flux workpace](van)
#### Up: [Index](index)
