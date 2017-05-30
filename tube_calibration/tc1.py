import tube
from tube_spec import TubeSpec
import numpy as np
run=47301
ws = Load('CORELLI_'+str(run))
LoadInstrument(ws, Filename='/SNS/users/rwp/CORELLI_Definition_91.07cm.xml', RewriteSpectraMap='False')
ws = Integration(ws)
CloneWorkspace(InputWorkspace='ws', OutputWorkspace='ws2')
CloneWorkspace(InputWorkspace='ws', OutputWorkspace='ws1')

tubeSet = TubeSpec(ws)
tubeSet.setTubeSpecByStringArray(["bank33","bank45","bank57"])

a=(2*25.4+2)/1000
knownPositions=np.arange(-7.5*a,8.5*a,a)
funcForm = [1]*16

calibTable = tube.calibrate(ws, tubeSet, knownPositions, funcForm,margin=6, plotTube=True, outputPeak=True)

ApplyCalibration(Workspace='ws2', PositionTable='CalibTable')

calibTable1 = tube.calibrate(ws, tubeSet, knownPositions, funcForm,margin=6, fitPolyn=1)

ApplyCalibration(Workspace='ws1', PositionTable='CalibTable')
