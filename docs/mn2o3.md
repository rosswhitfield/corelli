This is an example for the data reduction done for Mn2O3

### Convert first 5 minutes of each run to MDEventWorkspace in Q Sample
```python
ConvertMultipleRunsToSingleCrystalMD(Filename='CORELLI_36964:36993',
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
            DensityThresholdFactor=25000,
            PeakDistanceThreshold=0.5,
            OutputWorkspace='peaks')
```

Output:
```
Number of peaks found: 1080
```

### Determine the UB matrix from the peaks
```python
FindUBUsingFFT(PeaksWorkspace='peaks', MinD=5, MaxD=15)
```
Ouput:
```
UB = Matrix(3,3)-0.0304945,-0.135679,-0.0949406,-0.0992292,-0.00159089,-0.110837,0.107315,0.0648093,-0.0280319
New UB will index 1080 Peaks out of 1080 with tolerance of  0.15
Lattice Parameters:    8.165650    8.174817    8.214825  109.942734  108.596272  109.735616   422.801161
Parameter Errors  :    0.002488    0.002751    0.002806    0.023199    0.028995    0.022224    0.328352
```

### Show possible cell of UB
```python
ShowPossibleCells(PeaksWorkspace='peaks')
```
Output
```
Form # 5  Error: 0.0715  Cubic         I   Lat Par:   9.4034   9.4075   9.5592    89.589   90.102   90.007     845.60
Form #24  Error: 0.0696  Rhombohedral  R   Lat Par:  13.3005  13.4209   8.1656    89.399   89.892  119.510    1268.40
Form # 6  Error: 0.0400  Tetragonal    I   Lat Par:   9.4034   9.4075   9.5592    89.589   90.102   90.007     845.60
Form #16  Error: 0.0863  Orthorhombic  F   Lat Par:   9.4075  13.4209  13.3971    90.942   90.289   89.702    1691.20
Form # 8  Error: 0.0400  Orthorhombic  I   Lat Par:   9.4075   9.4034   9.5592    90.102   89.589   90.007     845.60
Form #43  Error: 0.0105  Monoclinic    I   Lat Par:   8.2148  13.3005   8.1656    89.892  108.596   89.852     845.60
Form #44  Error: 0.0000  Triclinic     P   Lat Par:   8.1656   8.1748   8.2148   109.943  108.596  109.736     422.80
```

### Select desired cell
```python
SelectCellWithForm(PeaksWorkspace='peaks',FormNumber=5,Apply=True)
```
Output
```
Form # 5  Error: 0.0715  Cubic         I   Lat Par:   9.4034   9.4075   9.5592    89.589   90.102   90.007     845.60
Transformation Matrix =  0.498497 -0.34453 -0.508802 0.332157 0.502706 0.605884 0.505526 -0.624468 0.498797
Re-indexed the peaks with the new UB.
Now, 1060 are indexed with average error 0.0178275
```

### Save the UB matix
```python
SaveIsawUB(InputWorkspace='peaks', Filename='Mn2O3.mat')
```

### Reduced data to a correctly normalised MDHistoWorkspace with P23 symmetry
```python
SingleCrystalDiffuseReduction(Filename='CORELLI_36964:36993',
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
                              UBMatrix="Mn2O3.mat",
                              OutputWorkspace='Mn2O3',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              BinningDim0='-5.02,5.02,251',
                              BinningDim1='-5.02,5.02,251',
                              BinningDim2='-5.02,5.02,251',
			      SymmetryOps='195')
```

### Save the reduced workspace
```python
SaveMD(InputWorkspace='Mn2O3', Filename='Mn2O3.nxs')
SaveMDWorkspaceToVTK(InputWorkspace='Mn2O3', Filename='Mn2O3.vts')
```

### Do the same but just for the elastic signal
```python
SingleCrystalDiffuseReduction(Filename=','.join('/SNS/CORELLI/IPTS-16344/shared/autoreduce/CORELLI_'+str(run)+'_elastic.nxs' for run in range(36964,36994)),
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
                              UBMatrix="Mn2O3.mat",
                              OutputWorkspace='Mn2O3_elastic',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              BinningDim0='-5.02,5.02,251',
                              BinningDim1='-5.02,5.02,251',
                              BinningDim2='-5.02,5.02,251',
			      SymmetryOps='195')
```

### Save the reduced workspace
```python
SaveMD(InputWorkspace='Mn2O3_elastic', Filename='Mn2O3_elastic.nxs')
SaveMDWorkspaceToVTK(InputWorkspace='Mn2O3_elastic', Filename='Mn2O3_elastic.vts')
```

### Same again but for a smaller range at higher resolution
```python
SingleCrystalDiffuseReduction(Filename=','.join('/SNS/CORELLI/IPTS-16344/shared/autoreduce/CORELLI_'+str(run)+'_elastic.nxs' for run in range(36964,36994)),
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
                              UBMatrix="Mn2O3.mat",
                              OutputWorkspace='Mn2O3_elastic_3.5',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              BinningDim0='-3.52,3.52,351',
                              BinningDim1='-3.52,3.52,351',
                              BinningDim2='-3.52,3.52,351',
			      SymmetryOps='195')
```

### Save the reduced workspace
```python
SaveMD(InputWorkspace='Mn2O3_elastic_3.5', Filename='Mn2O3_elastic_3.5.nxs')
SaveMDWorkspaceToVTK(InputWorkspace='Mn2O3_elastic_3.5', Filename='Mn2O3_elastic_3.5.vts')
```

* * *
#### Previous: [15%Ca doped ZrO2](czo)
#### Up: [Index](index)
