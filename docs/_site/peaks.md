# Finding Peaks

## Convert to MD

This will convert to event workspace into a multi-dimensional (MD) workspace in Q_sample units.

[ConvertToMD](http://docs.mantidproject.org/nightly/algorithms/ConvertToMD.html)

[ConvertMultipleRunsToSingleCrystalMD](http://docs.mantidproject.org/nightly/algorithms/ConvertMultipleRunsToSingleCrystalMD.html)

```python
ConvertMultipleRunsToSingleCrystalMD(Filename='CORELLI_29782:29817:10',
                                     FilterByTofMin=1000,
                                     FilterByTofMax=16666,
                                     SetGoniometer=True,
                                     Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                                     OutputWorkspace='md')

# Plot in Slice Viewer
sv=plotSlice('md',xydim=('Q_sample_x','Q_sample_z'),colormax=1e8,limits=[-5,5,-5,5],colorscalelog=True)
sv.setRebinMode(True)
sv.setRebinNumBins(300,300)
sv.saveImage('md.png')
```

![MD](md.png)

## Finding Peaks

[FindPeaksMD](http://docs.mantidproject.org/nightly/algorithms/FindPeaksMD.html)

```python
FindPeaksMD(InputWorkspace='md',DensityThresholdFactor=50000, OutputWorkspace='peaks')

# plot in Slice Viewer
sv=plotSlice('md',xydim=('Q_sample_x','Q_sample_z'),colormax=1e8,limits=[-5,5,-5,5],colorscalelog=True)
sv.setRebinMode(True)
sv.setRebinNumBins(300,300)
slicer = sv.getSlicer()
slicer.setPeaksWorkspaces(['peaks'])
sv.saveImage('md_peaks.png')
```

![MD Peaks](md_peaks.png)
