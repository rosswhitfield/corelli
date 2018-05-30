import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

DReference = [1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353]

Load(Filename='CORELLI_59313-59320', OutputWorkspace='rawSi')
rawSi_org=CloneWorkspace('rawSi')

ApplyCalibration('rawSi','CalibTable')


#MaskBTP(Workspace='rawSi',Pixel="1-16,241-256")
#MaskBTP(Workspace='rawSi',Bank="1-6,29,30,62-67,91")


PDCalibration(InputWorkspace='rawSi',
              #TofBinning='3400,10,16660',
              TofBinning='3000,-0.001,16660',
              BackgroundType='Flat',
              PeakPositions=DReference,
              MinimumPeakHeight=2,
              OutputCalibrationTable='cal',
              DiagnosticWorkspaces='diag')
