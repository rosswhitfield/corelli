# Exporting Data

## NeXus

[SaveMD] with save the file as a [NeXus](http://www.nexusformat.org)
Data Format. It can be read with any [HDF5](https://www.hdfgroup.org)
reader such as
[HDFView](https://support.hdfgroup.org/products/java/hdfview) or
[h5py](http://www.h5py.org). This is the format needed if you would
like to read the data back into Mantid, done with [LoadMD].


```python
# Save
SaveMD(InputWorkspace='benzil', Filename='benzil.nxs')
# Load
LoadMD(Filename='benzil.nxs', OutputWorkspace='benzil')
```

The algorithm history of a workspace can take a long time to parse
when loading so you can load it without history by
```python
LoadMD(Filename='benzil.nxs', OutputWorkspace='benzil', LoadHistory=False)
```

## VTK

[SaveMDWorkspaceToVTK] will save the file into
[VTK](http://www.vtk.org) format. This allows the workspace to be read
into visualization applications such as
[ParaView](https://www.paraview.org) or
[VisIt](https://visit.llnl.gov). See [Paraview](paraview).

```python
SaveMDWorkspaceToVTK(InputWorkspace='benzil', Filename='benzil.vts')
```

## NumPy

Export to a [NumPy
array](https://docs.scipy.org/doc/numpy/reference/arrays.ndarray.html)

```python
benzil=mtd['benzil']

benzil_np=benzil.getSignalArray()
print(benzil_np.shape)
print(benzil_np.dtype)
print(type(benzil_np))
```

Output:
```
(501, 501, 501)
float64
<type 'numpy.ndarray'>
```

From here you can save and load the array using NumPy [Input and
output](https://docs.scipy.org/doc/numpy/reference/routines.io.html).


You can get the dimension information with
`.get[X,Y,Z]Dimension()`. For examples the name of each is:

```python
print(benzil.getXDimension().name)
print(benzil.getYDimension().name)
print(benzil.getZDimension().name)
```

Output
```
[H,0,0]
[0,K,0]
[0,0,L]
```

The bins for the X dimensions by:

```python
print(benzil.getXDimension().getNBins())
print(benzil.getXDimension().getMinimum())
print(benzil.getXDimension().getMaximum())
print(benzil.getXDimension().getBinWidth())
```

Output
```
501
-10.020000457763672
10.020000457763672
0.04000000283122063
```

#### Previous: [Normalisation and symmetry](reduction) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Next: [3D-ΔPDF](pdf)
#### Up: [Index](index)

[SaveMD]: http://docs.mantidproject.org/nightly/algorithms/SaveMD.html
[LoadMD]: http://docs.mantidproject.org/nightly/algorithms/LoadMD.html
[SaveMDWorkspaceToVTK]: http://docs.mantidproject.org/nightly/algorithms/SaveMDWorkspaceToVTK.html
