import tube
from tube_spec import TubeSpec
import numpy as np
run=39611 # 57
ws = Load('CORELLI_'+str(run))
ws = LoadInstrument(ws, Filename='/SNS/users/rwp/CORELLI_Definition_91.07cm.xml', RewriteSpectraMap='False')
ws = Integration(ws)
CloneWorkspace(InputWorkspace='ws', OutputWorkspace='ws2')

tubeSet = TubeSpec(ws)
tubeSet.setTubeSpecByString("bank57")

a=(2*25.4+2)/1000
knownPositions=np.arange(-7.5*a,8.5*a,a)
funcForm = [1]*16

calibTable = tube.calibrate(ws, tubeSet, knownPositions, funcForm,margin=6)

ApplyCalibration(Workspace='ws2', PositionTable='CalibTable')
