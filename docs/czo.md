# 15%Ca doped ZrO2

This is an example for the data reduction done for 15%Ca doped ZrO2 (Zr0.85Ca0.15O2)

### Convert first 2 minutes of each run to MDEventWorkspace in Q Sample
```python
ConvertMultipleRunsToSingleCrystalMD(Filename='CORELLI_34682:34773',
                                     SetGoniometer=True,
				     FilterByTimeStop=120,
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
FindPeaksMD-[Notice] Number of peaks found: 806
```

### Determine the UB matrix from the peaks
```python
FindUBUsingFFT(PeaksWorkspace='peaks', MinD=5, MaxD=15)
```
Ouput:
```
UB = Matrix(3,3)-0.194222,-0.0124187,-0.00345943,-0.00139888,-0.0144863,0.189499,-0.0125676,0.193659,0.0142593
New UB will index 806 Peaks out of 806 with tolerance of  0.15
Lattice Parameters:    5.137969    5.138837    5.261445   90.091818   90.352532   89.997039   138.916099
Parameter Errors  :    0.000925    0.000885    0.002787    0.031913    0.032060    0.014280    0.081328
```

### Show possible cell of UB
```python
ShowPossibleCells(PeaksWorkspace='peaks')
```
Output
```
Num Cells : 8
Form # 3  Error: 0.1226  Cubic         P   Lat Par:   5.1388   5.2614   5.1380    90.353   89.997   90.092     138.92
Form # 2  Error: 0.1226  Rhombohedral  R   Lat Par:   7.3487   7.2666   8.9951    90.100   88.752  119.789     416.75
Form #21  Error: 0.0220  Tetragonal    P   Lat Par:   5.1388   5.1380   5.2614    90.353   90.092   89.997     138.92
Form #23  Error: 0.0220  Orthorhombic  C   Lat Par:   7.2670   7.2666   5.2614    90.184   90.314   90.010     277.83
Form #32  Error: 0.0226  Orthorhombic  P   Lat Par:   5.1380   5.1388   5.2614    90.092   90.353   89.997     138.92
Form #14  Error: 0.0167  Monoclinic    C   Lat Par:   7.2670   7.2666   5.2614    90.184   90.314   90.010     277.83
Form #33  Error: 0.0059  Monoclinic    P   Lat Par:   5.1380   5.1388   5.2614    90.092   90.353   89.997     138.92
Form #31  Error: 0.0000  Triclinic     P   Lat Par:   5.2614   5.1388   5.1380    89.997   89.647   89.908     138.92
```

### Select desired cell
```python
SelectCellOfType(PeaksWorkspace='peaks',CellType='Cubic',Apply=True)
```
Output
```
Form # 3  Error: 0.1226  Cubic         P   Lat Par:   5.1388   5.2614   5.1380    90.353   89.997   90.092     138.92
Transformation Matrix =  0.0770225 -1.01682 -0.088986 0.0121867 -0.0803965 0.973284 -0.99671 -0.08477 0.00337399
```

### Save the UB matix
```python
SaveIsawUB(InputWorkspace='peaks', Filename='CZO.mat')
```

### Reduced data to a correctly normalised MDHistoWorkspace with P23 symmetry
```python
SingleCrystalDiffuseReduction(Filename='CORELLI_34682:34773',
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
                              UBMatrix="CZO.mat",
                              OutputWorkspace='CZO',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              BinningDim0='-10.04,10.04,251',
                              BinningDim1='-10.04,10.04,251',
                              BinningDim2='-10.04,10.04,251',
                              SymmetryOps='195')
```

### Save the reduced workspace
```python
SaveMD(InputWorkspace='CZO', Filename='CZO.nxs')
SaveMDWorkspaceToVTK(InputWorkspace='CZO', Filename='CZO.vts')
```

### Same but using the elastic signal
```python
SingleCrystalDiffuseReduction(Filename=','.join('/SNS/CORELLI/IPTS-17467/shared/autoreduce/CORELLI_'+str(run)+'_elastic.nxs' for run in range(34682,34774)),
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
                              UBMatrix="CZO.mat",
                              OutputWorkspace='CZO_elastic',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              BinningDim0='-10.04,10.04,251',
                              BinningDim1='-10.04,10.04,251',
                              BinningDim2='-10.04,10.04,251',
                              SymmetryOps='195')
```

### Save the reduced workspace
```python
SaveMD(InputWorkspace='CZO_elastic', Filename='CZO_elastic.nxs')
SaveMDWorkspaceToVTK(InputWorkspace='CZO_elastic', Filename='CZO_elastic.vts')
```

* * *
#### Previous: [Benzil](benzil)  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Next: [Mn2O3](mn2o3)
#### Up: [Index](index)
