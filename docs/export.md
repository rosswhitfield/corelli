# Exporting Data

[SaveMD](http://docs.mantidproject.org/nightly/algorithms/SaveMD.html)
with save the file as a [NeXus](http://www.nexusformat.org) Data
Format. It can be read with any [HDF5](https://www.hdfgroup.org)
reader such as
[HDFView](https://support.hdfgroup.org/products/java/hdfview) or
[h5py](http://www.h5py.org). This is the format needed if you would
like to read the data back into Mantid, done with
[LoadMD](http://docs.mantidproject.org/nightly/algorithms/LoadMD.html).


```python
# Save
SaveMD(InputWorkspace='benzil', Filename='benzil.nxs')
# Load MD(Filename='benzil.nxs', OutputWorkspace='benzil')
```

[SaveMDWorkspaceToVTK](http://docs.mantidproject.org/nightly/algorithms/SaveMDWorkspaceToVTK.html)
with save the file into [VTK](http://www.vtk.org) format.

```python
SaveMDWorkspaceToVTK(InputWorkspace='benzil', Filename='benzil.vts')
```

Export to numpy array
```python
benzil_np=mtd['benzil'].getSignalArray()
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
