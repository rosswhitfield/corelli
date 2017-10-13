from paraview.simple import *

# create a new 'XML Structured Grid Reader'
#CZOvts = XMLStructuredGridReader(FileName=['CZO.vts'])
CZOvts = XMLImageDataReader(FileName=['CZO.vti'])

# get active view
renderView = GetActiveViewOrCreate('RenderView')

# uncomment following to set a specific view size
renderView.ViewSize = [1280, 720]

# Properties modified on renderView
renderView.OrientationAxesVisibility = 0
renderView.Background = [0.0, 0.0, 0.0]

# create a new 'Extract Subset'
extractSubset1 = ExtractSubset(Input=CZOvts)
extractSubset1.VOI = [25, 226, 25, 226, 25, 226]
extractSubset1Display = Show(extractSubset1, renderView)

# change representation type
extractSubset1Display.SetRepresentationType('Volume')
extractSubset1Display.Opacity = 0.0

# create a new 'Slice'
slice1 = Slice(Input=extractSubset1)
slice1.SliceType.Normal = [1.0, 0.0, 0.0]
slice1.SliceType.Origin = [1.0, 0.0, 0.0]

# create a new 'Slice'
slice2 = Slice(Input=extractSubset1)
slice2.SliceType.Normal = [0.0, 1.0, 0.0]
slice2.SliceType.Origin = [0.0, 2.0, 0.0]

# create a new 'Slice'
slice3 = Slice(Input=extractSubset1)
slice3.SliceType.Normal = [0.0, 0.0, 1.0]
slice3.SliceType.Origin = [0.0, 0.0, 0.0]

# get color transfer function/color map for 'Scalars_'
scalars_LUT = GetColorTransferFunction('Scalars_')

# show data in view
slice1Display = Show(slice1, renderView)
slice2Display = Show(slice2, renderView)
slice3Display = Show(slice3, renderView)

# Rescale transfer function
#scalars_LUT.RescaleTransferFunction(0.0, 8e-05)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
scalars_LUT.ApplyPreset('Viridis (matplotlib)', True)

# get opacity transfer function/opacity map for 'Scalars_'
scalars_PWF = GetOpacityTransferFunction('Scalars_')
scalars_PWF.Points = [0, 0, 0, 0,
                      0, 0.0, 0.5, 0.0,
                      1e-04, 0.0, 0.5, 0.0]

renderView.CameraPosition = [-20, -20, -20]

scene = GetAnimationScene()
scene.NumberOfFrames = 1000

cameraAnimationCue1 = GetCameraTrack(view=renderView)

PythonAnimationCue1 = PythonAnimationCue()
PythonAnimationCue1.Script = """
def start_cue(self): pass
def tick(self):
    time = scene.TimeKeeper.Time
    if time <=0.1:
        time *= 10
        scalars_LUT.RescaleTransferFunction(0.0, 1e-02*100**-time)
def end_cue(self): pass
"""

scene.Cues.append(PythonAnimationCue1)

# get animation track
track = GetAnimationTrack('Origin', index=2, proxy=slice3.SliceType)

# create keyframes for this animation track

# create a key frame
frame0 = CompositeKeyFrame(KeyTime = 0.0, KeyValues = [0.0])
frame1 = CompositeKeyFrame(KeyTime = 0.1, KeyValues = [0.0])
frame2 = CompositeKeyFrame(KeyTime = 0.15, KeyValues = [4.0])
frame3 = CompositeKeyFrame(KeyTime = 0.2, KeyValues = [0.0])

# initialize the animation track
track.KeyFrames = [frame0, frame1, frame2, frame3]

extractSubset1VOITrack0 = GetAnimationTrack('VOI', index=0, proxy=extractSubset1)
extractSubset1VOITrack1 = GetAnimationTrack('VOI', index=1, proxy=extractSubset1)
extractSubset1VOITrack2 = GetAnimationTrack('VOI', index=2, proxy=extractSubset1)
extractSubset1VOITrack3 = GetAnimationTrack('VOI', index=3, proxy=extractSubset1)
extractSubset1VOITrack4 = GetAnimationTrack('VOI', index=4, proxy=extractSubset1)
extractSubset1VOITrack5 = GetAnimationTrack('VOI', index=5, proxy=extractSubset1)


trackKeyFrame0_0 = CompositeKeyFrame(KeyTime = 0.2, KeyValues = [25.0])
trackKeyFrame0_1 = CompositeKeyFrame(KeyTime = 0.3, KeyValues = [100.0])
trackKeyFrame1_0 = CompositeKeyFrame(KeyTime = 0.2, KeyValues = [226.0])
trackKeyFrame1_1 = CompositeKeyFrame(KeyTime = 0.3, KeyValues = [151.0])
trackKeyFrame2_0 = CompositeKeyFrame(KeyTime = 0.2, KeyValues = [25.0])
trackKeyFrame2_1 = CompositeKeyFrame(KeyTime = 0.3, KeyValues = [100.0])
trackKeyFrame3_0 = CompositeKeyFrame(KeyTime = 0.2, KeyValues = [226.0])
trackKeyFrame3_1 = CompositeKeyFrame(KeyTime = 0.3, KeyValues = [151.0])
trackKeyFrame4_0 = CompositeKeyFrame(KeyTime = 0.2, KeyValues = [25.0])
trackKeyFrame4_1 = CompositeKeyFrame(KeyTime = 0.3, KeyValues = [100.0])
trackKeyFrame5_0 = CompositeKeyFrame(KeyTime = 0.2, KeyValues = [226.0])
trackKeyFrame5_1 = CompositeKeyFrame(KeyTime = 0.3, KeyValues = [151.0])

extractSubset1VOITrack0.KeyFrames = [trackKeyFrame0_0, trackKeyFrame0_1]
extractSubset1VOITrack1.KeyFrames = [trackKeyFrame1_0, trackKeyFrame1_1]
extractSubset1VOITrack2.KeyFrames = [trackKeyFrame2_0, trackKeyFrame2_1]
extractSubset1VOITrack3.KeyFrames = [trackKeyFrame3_0, trackKeyFrame3_1]
extractSubset1VOITrack4.KeyFrames = [trackKeyFrame4_0, trackKeyFrame4_1]
extractSubset1VOITrack5.KeyFrames = [trackKeyFrame5_0, trackKeyFrame5_1]


# get camera animation track for the view
#cameraAnimationCue1 = GetCameraTrack(view=renderView)

# Zoom to volume
keyFrame4863 = CameraKeyFrame()
keyFrame4863.KeyTime = 0.3
keyFrame4863.Position = [-20.0, -20.0, -20.0]
keyFrame4863.PositionPathPoints = [-20.0, -20.0, -20.0,
                                   -10.0, -5.0, -5.0]
keyFrame4863.FocalPathPoints = [0.0, 0.0, 0.0,
                                0.0, 0.0, 0.0]

# create a key frame
keyFrame4864 = CameraKeyFrame()
keyFrame4864.KeyTime = 0.4
keyFrame4864.Position = [-10.0, -5.0, -5.0]

# initialize the animation track
cameraAnimationCue1.Mode = 'Path-based'
cameraAnimationCue1.KeyFrames = [keyFrame4863, keyFrame4864]


# Change to volume

slice1track = GetAnimationTrack('Opacity', proxy=slice1)
slice1track.KeyFrames = [CompositeKeyFrame(KeyTime = 0, KeyValues = 1, Interpolation = 'Boolean'),
                         CompositeKeyFrame(KeyTime = 0.5, KeyValues = 0, Interpolation = 'Boolean')]

slice2track = GetAnimationTrack('Opacity', proxy=slice2)
slice2track.KeyFrames = [CompositeKeyFrame(KeyTime = 0, KeyValues = 1, Interpolation = 'Boolean'),
                         CompositeKeyFrame(KeyTime = 0.5, KeyValues = 0, Interpolation = 'Boolean')]

slice3track = GetAnimationTrack('Opacity', proxy=slice3)
slice3track.KeyFrames = [CompositeKeyFrame(KeyTime = 0, KeyValues = 1, Interpolation = 'Boolean'),
                         CompositeKeyFrame(KeyTime = 0.5, KeyValues = 0, Interpolation = 'Boolean')]

# Change PWF

PythonAnimationCue2 = PythonAnimationCue()
PythonAnimationCue2.Script = """
def start_cue(self): pass
def tick(self):
    time = scene.TimeKeeper.Time
    if time > 0.4 and time <=0.5:
        time = (time - 0.4) * 10
        scalars_PWF.Points = [0.0, 0.0, 0.5, 0.0,
                             0.0, 0.0, 0.5, 0.0,
                             2e-04, time, 0.5, 0.0]
    elif time > 0.5 and time <=0.6:
        time = (time - 0.5) * 50
        scalars_PWF.Points = [0.0, 0.0, 0.5, 0.0,
                             2e-04*10**-time, 0.0, 0.5, 0.0,
                             2e-04, 1.0, 0.5, 0.0]
def end_cue(self): pass
"""

scene.Cues.append(PythonAnimationCue2)


# Rotate


# ORNL logo

SaveAnimation('/tmp/CZO.png', renderView)
