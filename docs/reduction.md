# Normalisation and symmetry

Once you have an UB matrix for your series of runs you can perform a
correctly normalised reduction of your data.

The only other thing requires is the SolidAngle and Flux workspaces
which should be provided by the instrument scientist but the example
used here is shown [here](van.md)

[SingleCrystalDiffuseReduction](http://docs.mantidproject.org/nightly/algorithms/SingleCrystalDiffuseReduction.html)
makes use of
[MDNormSCD](http://docs.mantidproject.org/nightly/algorithms/MDNormSCD.html)

* [SingleCrystalDiffuseReduction](http://docs.mantidproject.org/nightly/algorithms/SingleCrystalDiffuseReduction.html)
* [SaveMD](http://docs.mantidproject.org/nightly/algorithms/SaveMD.html)
