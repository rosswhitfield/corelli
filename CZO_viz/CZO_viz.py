from paraview.simple import *

# create a new 'XML Structured Grid Reader'
CZOvts = XMLStructuredGridReader(FileName=['CZO.vts'])

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

renderView.CameraPosition = [-20, -20, -20]

scene = GetAnimationScene()
scene.NumberOfFrames = 1000

PythonAnimationCue = PythonAnimationCue()
PythonAnimationCue.Script = """
def start_cue(self): pass
def tick(self):
    time = scene.TimeKeeper.Time
    if time <=0.1:
        time *= 10
        scalars_LUT.RescaleTransferFunction(0.0, 1e-02*100**-time)
def end_cue(self): pass
"""

scene.Cues.append(PythonAnimationCue)

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


trackKeyFrame0 = CompositeKeyFrame(KeyTime = 0.2, KeyValues = [25.0])
trackKeyFrame1 = CompositeKeyFrame(KeyTime = 0.3, KeyValues = [100.0])

trackKeyFrame2 = CompositeKeyFrame(KeyTime = 0.2, KeyValues = [226.0])
trackKeyFrame3 = CompositeKeyFrame(KeyTime = 0.3, KeyValues = [151.0])

extractSubset1VOITrack0.KeyFrames = [trackKeyFrame0, trackKeyFrame1]
extractSubset1VOITrack1.KeyFrames = [trackKeyFrame2, trackKeyFrame3]
extractSubset1VOITrack2.KeyFrames = [trackKeyFrame0, trackKeyFrame1]
extractSubset1VOITrack3.KeyFrames = [trackKeyFrame2, trackKeyFrame3]
extractSubset1VOITrack4.KeyFrames = [trackKeyFrame0, trackKeyFrame1]
extractSubset1VOITrack5.KeyFrames = [trackKeyFrame2, trackKeyFrame3]


# Zoom to volume


# Change to volume


# Change PWF


# Rotate


# ORNL logo

SaveAnimation('/tmp/CZO.png', renderView)
