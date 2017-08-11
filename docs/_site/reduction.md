# Single Crystal Diffuse Scattering Reduction

## Normalisation

The SolidAngle and Flux should be provided by the instrument scientist
but the example used here is shown
[below](#create-solid-angle-and-flux-workspace-for-normalization)

[SingleCrystalDiffuseReduction](http://docs.mantidproject.org/nightly/algorithms/SingleCrystalDiffuseReduction.html)
makes use of
[MDNormSCD](http://docs.mantidproject.org/nightly/algorithms/MDNormSCD.html)

* [SingleCrystalDiffuseReduction](http://docs.mantidproject.org/nightly/algorithms/SingleCrystalDiffuseReduction.html)
* [SaveMD](http://docs.mantidproject.org/nightly/algorithms/SaveMD.html)

## Create solid angle and flux workspace for normalization

There is an example of creating the SolidAngle and Flux workspaces in
the
[MDNormSCD](http://docs.mantidproject.org/nightly/algorithms/MDNormSCD.html)
usage examples
[here](http://docs.mantidproject.org/nightly/algorithms/MDNormSCD-v1.html#usage)

For the example [above](#normalisation) the SolidAngle and Flux were
made as below.

```python
# Vanadium for normalisation
Load(Filename='CORELLI_28119-28123', OutputWorkspace='van')
ConvertUnits(InputWorkspace='van', OutputWorkspace='van', Target='Momentum')
CropWorkspace(InputWorkspace='van', OutputWorkspace='van', XMin='2.5', XMax='10')
# Get Solid Angle
Rebin(InputWorkspace='van', OutputWorkspace='sa', Params='2.5,10,10', PreserveEvents='0')
SaveNexus(InputWorkspace='sa', Filename='SolidAngle.nxs')
# Get Flux
SumSpectra(InputWorkspace='van', OutputWorkspace='flux')
CompressEvents(InputWorkspace='flux', OutputWorkspace='flux')
Rebin(InputWorkspace='flux', OutputWorkspace='flux', Params='2.5,10,10')
flux=mtd['flux']
for i in range(flux.getNumberHistograms()):
    el=flux.getSpectrum(i)
    el.divide(flux.readY(i)[0],0)
Rebin(InputWorkspace='flux', OutputWorkspace='flux', Params='2.5,10,10')
IntegrateFlux(InputWorkspace='flux', OutputWorkspace='flux')
SaveNexus(InputWorkspace='flux', Filename='Spectrum.nxs')
```

```
sv=plotSlice('md',xydim=('Q_sample_x','Q_sample_z'),colormax=1e6,limits=[-5,5,-5,5])
sv.saveImage('plot.png')
```
