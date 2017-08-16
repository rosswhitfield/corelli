# Normalisation and symmetry

Once you have an UB matrix for your series of runs you can perform a
correctly normalised reduction of your data.

The only other thing requires is the SolidAngle and Flux workspaces
which should be provided by the instrument scientist but the example
used here is shown [here](van)

[SingleCrystalDiffuseReduction](http://docs.mantidproject.org/nightly/algorithms/SingleCrystalDiffuseReduction.html)
makes use of
[MDNormSCD](http://docs.mantidproject.org/nightly/algorithms/MDNormSCD.html)

* [SingleCrystalDiffuseReduction](http://docs.mantidproject.org/nightly/algorithms/SingleCrystalDiffuseReduction.html)
* [SaveMD](http://docs.mantidproject.org/nightly/algorithms/SaveMD.html)

```python
SingleCrystalDiffuseReduction(Filename='CORELLI_29782:29817:10',
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
                              UBMatrix="/SNS/CORELLI/IPTS-15526/shared/benzil_Hexagonal.mat",
			      KeepTemporaryWorkspaces=True,
                              OutputWorkspace='output',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              BinningDim0='-10.05,10.05,201',
                              BinningDim1='-10.05,10.05,201',
                              BinningDim2='-0.1,0.1,1',
                              SymmetryOps="P 31 2 1")
```

If you have a look at the un-normalized data you will see the
overlapping of the data.

```python
sv=plotSlice('output_data',colormax=5e2,limits=[-10,10,-10,10])
sv.saveImage('output_data.png')
```

![output_data](output_data.png)

If you have a look at the normalization workspace you will see how the
is correctly normalized for the overlapping data.

```python
sv=plotSlice('output_normalization',colormax=1e8,limits=[-10,10,-10,10])
sv.saveImage('output_normalization.png')
```

![output_normalization](output_normalization.png)

The correctly normalized output is the data divided by the
normalization.

```
sv=plotSlice('output',colormax=1e-5,limits=[-10,10,-10,10])
sv.saveImage('output.png')
```

![output](output.png)

* * *
#### Previous: [Finding the UB Matrix](ub) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Next: [Creating Solid Angle and Flux workpace](van)
#### Up: [Index](index)
