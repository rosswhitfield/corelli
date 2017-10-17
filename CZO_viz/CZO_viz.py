from paraview.simple import *

#CZO = XMLStructuredGridReader(FileName=['CZO.vts'])
CZO = XMLImageDataReader(FileName=['CZO.vti'])

renderView = GetActiveViewOrCreate('RenderView')
renderView.ViewSize = [1920, 1080]
renderView.OrientationAxesVisibility = 0
renderView.Background = [0.0, 0.0, 0.0]

# ORNL logo
txt = servermanager.rendering.ImageTexture()
txt.FileName = "SNS_white_1080.jpg"
renderView.BackgroundTexture = txt
renderView.UseTexturedBackground = 1

# Extract Subset
extractSubset1 = ExtractSubset(Input=CZO)
extractSubset1.VOI = [25, 225, 25, 225, 25, 225]
extractSubset1Display = Show(extractSubset1, renderView)

# change representation to volume
extractSubset1Display.SetRepresentationType('Volume')
extractSubset1Display.Opacity = 0.0

slice1 = Slice(Input=extractSubset1)
slice1.SliceType.Normal = [1.0, 0.0, 0.0]
slice1.SliceType.Origin = [-1.0, 0.0, 0.0]

slice2 = Slice(Input=extractSubset1)
slice2.SliceType.Normal = [0.0, 1.0, 0.0]
slice2.SliceType.Origin = [0.0, -2.0, 0.0]

slice3 = Slice(Input=extractSubset1)
slice3.SliceType.Normal = [0.0, 0.0, 1.0]
slice3.SliceType.Origin = [0.0, 0.0, 0.0]

slice1Display = Show(slice1, renderView)
slice2Display = Show(slice2, renderView)
slice3Display = Show(slice3, renderView)


scalars_LUT = GetColorTransferFunction('Scalars_')
scalars_LUT.ApplyPreset('Viridis (matplotlib)', True)

# get opacity transfer function/opacity map for 'Scalars_'
scalars_PWF = GetOpacityTransferFunction('Scalars_')
scalars_PWF.Points = [0, 0, 0, 0,
                      0, 0.0, 0.5, 0.0,
                      1e-04, 0.0, 0.5, 0.0]

renderView.CameraPosition = [20, 20, 20]

scene = GetAnimationScene()
scene.NumberOfFrames = 1000

cameraAnimationCue1 = GetCameraTrack(view=renderView)

# Change LUT
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

# Change slice origin
track = GetAnimationTrack('Origin', index=2, proxy=slice3.SliceType)

frame0 = CompositeKeyFrame(KeyTime = 0.0, KeyValues = [0.0])
frame1 = CompositeKeyFrame(KeyTime = 0.1, KeyValues = [0.0])
frame2 = CompositeKeyFrame(KeyTime = 0.15, KeyValues = [-4.0])
frame3 = CompositeKeyFrame(KeyTime = 0.2, KeyValues = [0.0])

track.KeyFrames = [frame0, frame1, frame2, frame3]

# Change Subset VOI
extractSubset1VOITrack0 = GetAnimationTrack('VOI', index=0, proxy=extractSubset1)
extractSubset1VOITrack1 = GetAnimationTrack('VOI', index=1, proxy=extractSubset1)
extractSubset1VOITrack2 = GetAnimationTrack('VOI', index=2, proxy=extractSubset1)
extractSubset1VOITrack3 = GetAnimationTrack('VOI', index=3, proxy=extractSubset1)
extractSubset1VOITrack4 = GetAnimationTrack('VOI', index=4, proxy=extractSubset1)
extractSubset1VOITrack5 = GetAnimationTrack('VOI', index=5, proxy=extractSubset1)

trackKeyFrame0_0 = CompositeKeyFrame(KeyTime = 0.2, KeyValues = [25.0])
trackKeyFrame0_1 = CompositeKeyFrame(KeyTime = 0.3, KeyValues = [100.0])
trackKeyFrame1_0 = CompositeKeyFrame(KeyTime = 0.2, KeyValues = [225.0])
trackKeyFrame1_1 = CompositeKeyFrame(KeyTime = 0.3, KeyValues = [150.0])

extractSubset1VOITrack0.KeyFrames = [trackKeyFrame0_0, trackKeyFrame0_1]
extractSubset1VOITrack1.KeyFrames = [trackKeyFrame1_0, trackKeyFrame1_1]
extractSubset1VOITrack2.KeyFrames = [trackKeyFrame0_0, trackKeyFrame0_1]
extractSubset1VOITrack3.KeyFrames = [trackKeyFrame1_0, trackKeyFrame1_1]
extractSubset1VOITrack4.KeyFrames = [trackKeyFrame0_0, trackKeyFrame0_1]
extractSubset1VOITrack5.KeyFrames = [trackKeyFrame1_0, trackKeyFrame1_1]

# Camera

cameraKeyFrame0 = CameraKeyFrame()
cameraKeyFrame0.KeyTime = 0.3
cameraKeyFrame0.Position = [20.0, 20.0, 20.0]
cameraKeyFrame0.PositionPathPoints = [20.0, 20.0, 20.0,
                                   10.0, 5.0, 5.0]
cameraKeyFrame0.FocalPathPoints = [0.0, 0.0, 0.0,
                                0.0, 0.0, 0.0]

cameraKeyFrame1 = CameraKeyFrame()
cameraKeyFrame1.KeyTime = 0.4
cameraKeyFrame1.Position = [10.0, 5.0, 5.0]
cameraKeyFrame1.PositionPathPoints = [10.0, 5.0, 5.0]
cameraKeyFrame1.FocalPathPoints = [0.0, 0.0, 0.0]

cameraKeyFrame2 = CameraKeyFrame()
cameraKeyFrame2.KeyTime = 0.7
cameraKeyFrame2.Position = [10.0, 5.0, 5.0]
cameraKeyFrame2.PositionPathPoints = [10.0, 5.0, 5.0]
cameraKeyFrame2.FocalPathPoints = [0.0, 0.0, 0.0]

cameraKeyFrame3 = CameraKeyFrame()
cameraKeyFrame3.KeyTime = 0.7
cameraKeyFrame3.Position = [10.0, 5.0, 5.0]
cameraKeyFrame3.PositionPathPoints = [10.0, 5.0, 5.0,
                                   10.17893371778323, 5.0, -4.624857659320521,
                                   2.8116210954914362, 5.0, -10.821034461426855,
                                   -6.640112743185945, 5.0, -8.99493761833731,
                                   -11.169137791805014, 5.0, -0.5003608574550045,
                                   -7.417819582470554, 5.0, 8.36516303737808,
                                   1.832767551049991, 5.0, 11.029096205211845]
cameraKeyFrame3.FocalPathPoints = [0.0, 0.0, 0.0]
cameraKeyFrame3.ClosedPositionPath = 1

cameraKeyFrame4 = CameraKeyFrame()
cameraKeyFrame4.KeyTime = 1.0
cameraKeyFrame4.Position = [10.0, 5.0, 5.0]
cameraKeyFrame4.ParallelScale = 5.1151572410577275

# initialize the animation track
cameraAnimationCue1.Mode = 'Path-based'
cameraAnimationCue1.KeyFrames = [cameraKeyFrame0, cameraKeyFrame1, cameraKeyFrame2, cameraKeyFrame3, cameraKeyFrame4]

# Change to volume

sliceOKeyFrame0=CompositeKeyFrame(KeyTime = 0, KeyValues = 1)
sliceOKeyFrame1=CompositeKeyFrame(KeyTime = 0.4, KeyValues = 1)
sliceOKeyFrame2=CompositeKeyFrame(KeyTime = 0.5, KeyValues = 0)

slice1track = GetAnimationTrack('Opacity', proxy=slice1)
slice1track.KeyFrames = [sliceOKeyFrame0, sliceOKeyFrame1, sliceOKeyFrame2]

slice2track = GetAnimationTrack('Opacity', proxy=slice2)
slice2track.KeyFrames = [sliceOKeyFrame0, sliceOKeyFrame1, sliceOKeyFrame2]

slice3track = GetAnimationTrack('Opacity', proxy=slice3)
slice3track.KeyFrames = [sliceOKeyFrame0, sliceOKeyFrame1, sliceOKeyFrame2]

# Change PWF

PythonAnimationCue2 = PythonAnimationCue()
PythonAnimationCue2.Script = """
def start_cue(self): pass
def tick(self):
    time = scene.TimeKeeper.Time
    if time > 0.4 and time <=0.5:
        time = (time - 0.4) * 10
        scalars_PWF.Points = [0.0, 0.0, 0.5, 0.0,
                             2e-06, 0.0, 0.5, 0.0,
                             2e-04, time, 0.5, 0.0]
    elif time > 0.5 and time <=0.6:
        time = (time - 0.5) * 10
        scalars_PWF.Points = [0.0, 0.0, 0.5, 0.0,
                             2e-06*100**time, 0.0, 0.5, 0.0,
                             2e-04, 1.0, 0.5, 0.0]
    elif time > 0.6 and time <=0.7:
        time = (time - 0.6) * 10
        scalars_PWF.Points = [0.0, 0.0, 0.5, 0.0,
                             2e-04*10**-time, 0.0, 0.5, 0.0,
                             2e-04, 1.0, 0.5, 0.0]
def end_cue(self): pass
"""

scene.Cues.append(PythonAnimationCue2)

SaveAnimation('/tmp/CZO.png', renderView)
