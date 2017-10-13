from paraview.simple import *

# create a new 'XML Structured Grid Reader'
CZOvts = XMLStructuredGridReader(FileName=['CZO.vts'])

# get active view
renderView = GetActiveViewOrCreate('RenderView')

# uncomment following to set a specific view size
renderView.ViewSize = [1280, 720]

# Properties modified on renderView
renderView.OrientationAxesVisibility = 0

# create a new 'Slice'
slice1 = Slice(Input=CZOvts)
slice1.SliceType.Normal = [1.0, 0.0, 0.0]

# create a new 'Slice'
slice2 = Slice(Input=CZOvts)
slice2.SliceType.Normal= [0.0, 1.0, 0.0]
slice2.SliceType.Origin = [0.0, 2.0, 0.0]

# create a new 'Slice'
slice3 = Slice(Input=CZOvts)
slice3.SliceType.Normal = [0.0, 0.0, 1.0]
slice3.SliceType.Origin = [0.0, 0.0, 2.0]

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

renderView.CameraPosition = [-25, -25, -25]

scene = GetAnimationScene()
scene.EndTime = 2.0
scene.NumberOfFrames = 200



PythonAnimationCue = PythonAnimationCue()
PythonAnimationCue.Script = """
def start_cue(self): pass
def tick(self):
    time = scene.TimeKeeper.Time
    if time <=1:
        scalars_LUT.RescaleTransferFunction(0.0, 1e-02*100**-time)
def end_cue(self): pass
"""

scene.Cues.append(PythonAnimationCue)



# get animation track
track = GetAnimationTrack('Origin', index=2, proxy=slice3.SliceType)

# create keyframes for this animation track

# create a key frame
frame0 = CompositeKeyFrame()
frame0.KeyTime = 0.0
frame0.KeyValues = 1

frame1 = CompositeKeyFrame()
frame1.KeyTime = 1.0
frame1.KeyValues = 1

# create a key frame
frame2 = CompositeKeyFrame()
frame2.KeyTime = 1.5
frame2.KeyValues = 3

# create a key frame
frame3 = CompositeKeyFrame()
frame3.KeyTime = 2.0
frame3.KeyValues = 1

# initialize the animation track
track.KeyFrames = [frame0, frame1, frame2, frame3]

SaveAnimation('/tmp/CZO.png', renderView)
