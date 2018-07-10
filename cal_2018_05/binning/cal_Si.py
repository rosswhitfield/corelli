import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

DReference = [0.9179, 0.9600, 1.0451, 1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353]

Load(Filename='CORELLI_59313-59320', OutputWorkspace='rawSi')

ApplyCalibration('rawSi','CalibTable')


for d in [-0.02, -0.01, -0.005, -0.002, -0.001]:
    TofBinning='3000,{},16660'.format(d)
    Rebin(InputWorkspace='rawSi', OutputWorkspace='rawSi_{}'.format(d),Params=TofBinning)
            

for d in [-0.02, -0.01, -0.005, -0.002, -0.001]:
    TofBinning='3000,{},16660'.format(d)
    try:
        PDCalibration(InputWorkspace='rawSi',
                      TofBinning=TofBinning,
                      PeakPositions=DReference,
                      MinimumPeakHeight=5,
                      PeakWidthPercent=0.01,
                      OutputCalibrationTable='cal_{}'.format(d),
                      DiagnosticWorkspaces='diag_{}'.format(d))
    except:
        pass

