# Exporting Data

* [SaveMD](http://docs.mantidproject.org/nightly/algorithms/SaveMD.html)

```python
SaveMD(InputWorkspace='benzil', Filename='benzil.nxs')
```

* [SaveMDWorkspaceToVTK](http://docs.mantidproject.org/nightly/algorithms/SaveMDWorkspaceToVTK.html)

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
