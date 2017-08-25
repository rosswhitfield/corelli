# Paraview

> [ParaView](https://www.paraview.org) is an open-source, multi-platform
> data analysis and visualization application. ParaView users can
> quickly build visualizations to analyze their data using qualitative
> and quantitative techniques. The data exploration can be done
> interactively in 3D or programmatically using ParaView’s batch
> processing capabilities.
>
> ParaView was developed to analyze extremely large datasets using
> distributed memory computing resources. It can be run on
> supercomputers to analyze datasets of petascale size as well as on
> laptops for smaller data, has become an integral tool in many national
> laboratories, universities and industry, and has won several awards
> related to high performance computation.

To use paraview first save the data as a VTK file, see
[here](export#vtk). The following scripts can be run from ParaView
(_Tools->Python Shell->Run Script_) or by running in `pvpython`.

## Converting to Image Data

By converting the data to Image data performace, particularly for
volume rendering, can be greatly improved.

```python
#### import the simple module from the paraview
from paraview.simple import *

# create a new 'XML Structured Grid Reader'
mn2O3_elastic_35vts = XMLStructuredGridReader(FileName=['Mn2O3_elastic_3.5.vts'])

# create a new 'Resample To Image'
resampleToImage1 = ResampleToImage(Input=mn2O3_elastic_35vts)
resampleToImage1.SamplingDimensions = [351, 351, 351]

SaveData('Mn2O3_elastic_3.5.vti', proxy=resampleToImage1)
```

## Slices

```python
#### import the simple module from the paraview
from paraview.simple import *

# create a new 'XML Structured Grid Reader'
benzilvts = XMLStructuredGridReader(FileName=['benzil.vts'])

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# uncomment following to set a specific view size
renderView1.ViewSize = [400, 400]

#change interaction mode for render view
renderView1.InteractionMode = '2D'

# Properties modified on renderView1
renderView1.OrientationAxesVisibility = 0

# create a new 'Slice'
slice1 = Slice(Input=benzilvts)
slice1.SliceType.Normal = [0.0, 0.0, 1.0]

# get color transfer function/color map for 'Scalars_'
scalars_LUT = GetColorTransferFunction('Scalars_')

# show data in view
slice1Display = Show(slice1, renderView1)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# Rescale transfer function
scalars_LUT.RescaleTransferFunction(0.0, 1e-05)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
scalars_LUT.ApplyPreset('Viridis (matplotlib)', True)

# current camera placement for renderView1
renderView1.CameraParallelScale = 10

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).

SaveScreenshot('benzil_hk0.png', quality=100, view=renderView1)
```

![Benzil_HK0](benzil_hk0.png)

### HK1

```python
slice1.SliceType.Origin = [0.0, 0.0, 1.0]
SaveScreenshot('benzil_hk1.png', quality=100, view=renderView1)
```

![Benzil_HK1](benzil_hk1.png)

### HK4

```python
slice1.SliceType.Origin = [0.0, 0.0, 4.0]
SaveScreenshot('benzil_hk4.png', quality=100, view=renderView1)
```

![Benzil_HK4](benzil_hk4.png)

### Animation

```python
# hide color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, False)

# get animation scene
animationScene1 = GetAnimationScene()

# Properties modified on animationScene1
animationScene1.NumberOfFrames = 100

# get animation track
track = GetAnimationTrack('Origin', index=2, proxy=slice1.SliceType)

# create keyframes for this animation track

# create a key frame
startKeyFrame = CompositeKeyFrame()
startKeyFrame.KeyValues = [-4]

# create a key frame
endKeyFrame = CompositeKeyFrame()
endKeyFrame.KeyTime = 1.0
endKeyFrame.KeyValues = [4]

# initialize the animation track
track.KeyFrames = [startKeyFrame, endKeyFrame]

# save animation
SaveAnimation('/tmp/benzil.png', renderView1, ImageResolution=[200, 200],
    TransparentBackground=1,
    FrameWindow=[0, 99])
```

A series of images are created that you can them convert to an animated gif, _e.g._ using `ffmpeg`:
```shell
$ ffmpeg -i /tmp/benzil.%04d.png benzil.gif
```

![Benzil Animation](benzil.gif)

## Multiple slices

### Mn2O3 showing 0KL, H1L and HK2

```python
#### import the simple module from the paraview
from paraview.simple import *

# create a new 'XML Structured Grid Reader'
mn2O3_elasticvts = XMLStructuredGridReader(FileName=['Mn2O3_elastic.vts'])

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# uncomment following to set a specific view size
renderView1.ViewSize = [400, 400]

# Properties modified on renderView1
renderView1.OrientationAxesVisibility = 0

# create a new 'Slice'
slice1 = Slice(Input=mn2O3_elasticvts)
slice1.SliceType.Normal = [1.0, 0.0, 0.0]

# create a new 'Slice'
slice2 = Slice(Input=mn2O3_elasticvts)
slice2.SliceType.Normal	= [0.0, 1.0, 0.0]
slice2.SliceType.Origin = [0.0, 1.0, 0.0]

# create a new 'Slice'
slice3 = Slice(Input=mn2O3_elasticvts)
slice3.SliceType.Normal = [0.0, 0.0, 1.0]
slice3.SliceType.Origin = [0.0, 0.0, 2.0]

# get color transfer function/color map for 'Scalars_'
scalars_LUT = GetColorTransferFunction('Scalars_')

# show data in view
slice1Display = Show(slice1, renderView1)
slice2Display = Show(slice2, renderView1)
slice3Display = Show(slice3, renderView1)

# Rescale transfer function
scalars_LUT.RescaleTransferFunction(0.0, 3e-05)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
scalars_LUT.ApplyPreset('Viridis (matplotlib)', True)

renderView1.CameraPosition = [-14, -14, -14]

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).

SaveScreenshot('Mn2O3_multiSlice.png', quality=100, view=renderView1)
```

![Mn2O3 multiSlice](Mn2O3_multiSlice.png)

### CZO showing 0KL, H1L and HK2

```python
#### import the simple module from the paraview
from paraview.simple import *

# create a new 'XML Structured Grid Reader'
CZOvts = XMLStructuredGridReader(FileName=['CZO.vts'])

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# uncomment following to set a specific view size
renderView1.ViewSize = [400, 400]

# Properties modified on renderView1
renderView1.OrientationAxesVisibility = 0

# create a new 'Slice'
slice1 = Slice(Input=CZOvts)
slice1.SliceType.Normal = [1.0, 0.0, 0.0]

# create a new 'Slice'
slice2 = Slice(Input=CZOvts)
slice2.SliceType.Normal	= [0.0, 1.0, 0.0]
slice2.SliceType.Origin = [0.0, 1.0, 0.0]

# create a new 'Slice'
slice3 = Slice(Input=CZOvts)
slice3.SliceType.Normal = [0.0, 0.0, 1.0]
slice3.SliceType.Origin = [0.0, 0.0, 2.0]

# get color transfer function/color map for 'Scalars_'
scalars_LUT = GetColorTransferFunction('Scalars_')

# show data in view
slice1Display = Show(slice1, renderView1)
slice2Display = Show(slice2, renderView1)
slice3Display = Show(slice3, renderView1)

# Rescale transfer function
scalars_LUT.RescaleTransferFunction(0.0, 8e-05)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
scalars_LUT.ApplyPreset('Viridis (matplotlib)', True)

renderView1.CameraPosition = [-14, -14, -14]

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).

SaveScreenshot('CZO_multiSlice.png', quality=100, view=renderView1)
```

![CZO multiSlice](CZO_multiSlice.png)

### Sphere

#### Changing radius while rotating

```python
#### import the simple module from the paraview
from paraview.simple import *

# create a new 'XML Structured Grid Reader'
CZOvts = XMLStructuredGridReader(FileName=['CZO.vts'])

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# uncomment following to set a specific view size
renderView1.ViewSize = [400, 400]

# Properties modified on renderView1
renderView1.OrientationAxesVisibility = 0

# create a new 'Slice'
slice1 = Slice(Input=CZOvts)
slice1.SliceType = 'Sphere'
slice1.SliceType.Radius = 7.0

# get color transfer function/color map for 'Scalars_'
scalars_LUT = GetColorTransferFunction('Scalars_')

# show data in view
slice1Display = Show(slice1, renderView1)

# Rescale transfer function
scalars_LUT.RescaleTransferFunction(0.0, 8e-05)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
scalars_LUT.ApplyPreset('Viridis (matplotlib)', True)

# get animation scene
animationScene1 = GetAnimationScene()

# Properties modified on animationScene1
animationScene1.NumberOfFrames = 200

# get animation track
slice1SliceTypeRadiusTrack = GetAnimationTrack('Radius', index=0, proxy=slice1.SliceType)

# create a key frame
startKeyFrame = CompositeKeyFrame()
startKeyFrame.KeyTime = 0.0
startKeyFrame.KeyValues = 7.0

# create a key frame
midKeyFrame = CompositeKeyFrame()
midKeyFrame.KeyTime = 0.5
midKeyFrame.KeyValues = 3.0

# create a key frame
endKeyFrame = CompositeKeyFrame()
endKeyFrame.KeyTime = 1.0
endKeyFrame.KeyValues = 7.0

# initialize the animation track
slice1SliceTypeRadiusTrack.KeyFrames = [startKeyFrame, midKeyFrame, endKeyFrame]

cameraAnimationCue1 = GetCameraTrack(view=renderView1)

# create keyframes for this animation track

# create a key frame
keyFrame0 = CameraKeyFrame()
keyFrame0.Position = [0.0, 0.0, 30.74036927872979]
keyFrame0.ParallelScale = 1.73
keyFrame0.PositionPathPoints = [0.0, 0.0, 30.0, 23.31437884370913, 0.0, 18.879611731495125, 29.34442802201417, 0.0, -6.23735072453278, 13.619714992186408, 0.0, -26.730195725651036, -12.202099292274005, 0.0, -27.40636372927803, -28.97777478867205, 0.0, -7.7645713530756275, -24.27050983124843, 0.0, 17.633557568774194]
keyFrame0.FocalPathPoints = [0.0, 0.0, 0.0]
keyFrame0.ClosedPositionPath = 1

# create a key frame
keyFrame1 = CameraKeyFrame()
keyFrame1.KeyTime = 1.0
keyFrame1.Position = [0.0, 0.0, 30.74036927872979]
keyFrame1.ParallelScale = 1.73

# initialize the animation track
cameraAnimationCue1.Mode = 'Path-based'
cameraAnimationCue1.KeyFrames = [keyFrame0, keyFrame1]

# save animation
SaveAnimation('/tmp/CZO.png', renderView1, ImageResolution=[200, 200], FrameWindow=[0, 198])
```

A series of images are created that you can them convert to an animated gif, _e.g._ using `ffmpeg`:
```shell
$ ffmpeg -i /tmp/CZO.%04d.png CZO_sphere.gif
```

![Mn2O3 sphere](CZO_sphere.gif)

## Clipping

```python
#### import the simple module from the paraview
from paraview.simple import *

# create a new 'XML Structured Grid Reader'
mn2O3vts = XMLStructuredGridReader(FileName=['Mn2O3.vts'])

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# uncomment following to set a specific view size
renderView1.ViewSize = [400, 400]

# Properties modified on renderView1
renderView1.OrientationAxesVisibility = 0

# create a new 'Clip'
clip1 = Clip(Input=mn2O3vts)
clip1.ClipType = 'Sphere'
clip1.InsideOut = 1
clip1.ClipType.Radius = 5.0

# create a new 'Clip'
clip2 = Clip(Input=clip1)
clip2.ClipType = 'Box'
clip2.ClipType.Position = [0, 0, 0]
clip2.ClipType.Scale = [5, 5, 5]

# get color transfer function/color map for 'Scalars_'
scalars_LUT = GetColorTransferFunction('Scalars_')

# show data in view
clipDisplay = Show(clip2, renderView1)

# Rescale transfer function
scalars_LUT.RescaleTransferFunction(0.0, 5e-05)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
scalars_LUT.ApplyPreset('Viridis (matplotlib)', True)

renderView1.CameraPosition = [12, 12, 12]

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).

SaveScreenshot('Mn2O3_clipping.png', quality=100, view=renderView1)
```

![Mn2O3 clipping](Mn2O3_clipping.png)

## Surface

```python
#### import the simple module from the paraview
from paraview.simple import *

# create a new 'XML Structured Grid Reader'
cZOvts = XMLStructuredGridReader(FileName=['CZO.vts'])

# update the view to ensure updated data information
renderView1 = GetActiveViewOrCreate('RenderView')

# uncomment following to set a specific view size
renderView1.ViewSize = [400, 400]

# create a new 'Clip'
clip1 = Clip(Input=cZOvts)
clip1.ClipType = 'Sphere'
clip1.InsideOut = 1
clip1.ClipType.Radius = 5.5

# get color transfer function/color map for 'Scalars_'
scalars_LUT = GetColorTransferFunction('Scalars_')

# create a new 'Threshold'
threshold1 = Threshold(Input=clip1)
threshold1.Scalars = ['CELLS', 'Scalars_']
threshold1.ThresholdRange = [0.0001, 0.00015]

# show data in view
threshold1Display = Show(threshold1, renderView1)

# Rescale transfer function
scalars_LUT.RescaleTransferFunction(0.0001, 0.00013)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
scalars_LUT.ApplyPreset('Viridis (matplotlib)', True)

renderView1.CameraPosition = [12,12,12]

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).

SaveScreenshot('CZO_surface.png', quality=100, view=renderView1)
```

![CZS surface](CZO_surface.png)

### Animation

```python
# get animation scene
animationScene1 = GetAnimationScene()

# Properties modified on animationScene1
animationScene1.NumberOfFrames = 100

cameraAnimationCue1 = GetCameraTrack(view=renderView1)

# create keyframes for this animation track

# create a key frame
keyFrame0 = CameraKeyFrame()
keyFrame0.Position = [13.62154428344417, 13.623338860089067, 13.623338860089067]
keyFrame0.ParallelScale = 8.941515994338047
keyFrame0.PositionPathPoints = [12.0, 12.0, 12.0, 16.8775962300817, 12.0, -1.7739068448856008, 9.242830918992556, 12.0, -14.23271149861878, -5.2441922933858525, 12.0, -16.139964287134976, -15.843385208620813, 12.0, -6.081705774801609, -14.696938456699069, 12.0, 8.485281374238571, -2.654780904989691, 12.0, 16.761626960009046]
keyFrame0.FocalPathPoints = [0.0, 0.0, 0.0]
keyFrame0.ClosedPositionPath = 1

# create a key frame
keyFrame1 = CameraKeyFrame()
keyFrame1.KeyTime = 1.0
keyFrame1.Position = [13.62154428344417, 13.623338860089067, 13.623338860089067]
keyFrame1.ParallelScale = 8.941515994338047

# initialize the animation track
cameraAnimationCue1.Mode = 'Path-based'
cameraAnimationCue1.KeyFrames = [keyFrame0, keyFrame1]

# save animation
SaveAnimation('/tmp/CZO.png', renderView1, ImageResolution=[200, 200], FrameWindow=[0, 99])
```

A series of images are created that you can them convert to an animated gif, _e.g._ using `ffmpeg`:
```shell
$ ffmpeg -i /tmp/CZO.%04d.png CZO_surface.gif
```

![CZO surface](CZO_surface.gif)

## Volume

I suggest first [converting the data to Image Data](#converting-to-image-data).

```python
#### import the simple module from the paraview
from paraview.simple import *

# create a new 'XML Image Data Reader'
mn2O3_elastic_35vti = XMLImageDataReader(FileName=['Mn2O3_elastic_3.5.vti'])

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
renderView1.ViewSize = [400, 400]

mn2O3_elastic_35vtiDisplay = Show(mn2O3_elastic_35vti, renderView1)

# change representation type
mn2O3_elastic_35vtiDisplay.SetRepresentationType('Volume')

# get color transfer function/color map for 'Scalars_'
scalars_LUT = GetColorTransferFunction('Scalars_')
#scalars_LUT.RGBPoints = [-7.929198181955144e-05, 0.231373, 0.298039, 0.752941, 0.03102709207814769, 0.865003, 0.865003, 0.865003, 0.06213347613811493, 0.705882, 0.0156863, 0.14902]
#scalars_LUT.ScalarRangeInitialized = 1.0

# Rescale transfer function
scalars_LUT.RescaleTransferFunction(0.0, 5e-05)

# get opacity transfer function/opacity map for 'Scalars_'
scalars_PWF = GetOpacityTransferFunction('Scalars_')
# Rescale transfer function
scalars_PWF.RescaleTransferFunction(0.0, 5e-05)

scalars_PWF.Points = [0.0, 0.0, 0.5, 0.0, 5e-05, 1.0, 0.5, 0.0]

# current camera placement for renderView1
renderView1.CameraPosition = [15, 8, 15]

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).


```


* * *
#### Previous: [Matplotlib](matplotlib) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Next: [Benzil](benzil)
#### Up: [Index](index)
