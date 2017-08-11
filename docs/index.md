# Corelli Single Crystal Diffuse Scattering Reduction

* [Elastic scattering using cross-correlation](cc.md)
* [Diffuse reduction](reduction.md)

## Convert to MD

[ConvertToMD](http://docs.mantidproject.org/nightly/algorithms/ConvertToMD.html)

## Finding Peaks

[FindPeaksMD](http://docs.mantidproject.org/nightly/algorithms/FindPeaksMD.html)

## Finding UB matrix

Using the peaks workspace from [Finding Peaks](#finding-peaks) using either
* [FindUBUsingFFT](http://docs.mantidproject.org/nightly/algorithms/FindUBUsingFFT.html)
* [FindUBUsingLatticeParameters](http://docs.mantidproject.org/nightly/algorithms/FindUBUsingLatticeParameters.html)

Show possible cells
* [ShowPossibleCells](http://docs.mantidproject.org/nightly/algorithms/ShowPossibleCells.html)

Select the cell using either
* [SelectCellOfType](http://docs.mantidproject.org/nightly/algorithms/SelectCellOfType.html)
* [SelectCellWithForm](http://docs.mantidproject.org/nightly/algorithms/SelectCellWithForm.html)

Once you have the desired UB and cell save it with
* [SaveIsawUB](http://docs.mantidproject.org/nightly/algorithms/SaveIsawUB.html)


