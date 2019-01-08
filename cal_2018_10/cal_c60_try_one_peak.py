import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

LoadDiffCal(Filename='/SNS/users/rwp/corelli/cal_2018_05/1/calB_si.h5',InstrumentName='CORELLI',WorkspaceName='si')

#DReference = [2.7251,2.8904,4.2694,5.0063,8.1753]
DReference = [4.2694,5.0063,8.1753]

Load(Filename='CORELLI_59583-59590', OutputWorkspace='rawC60')

ApplyCalibration('rawC60','CalibTable')

LoadIsawDetCal('rawC60','/SNS/users/rwp/corelli/cal_2018_05/a/Aligned3.nxs.detcal')

TofBinning='3000,-0.01,16660'

PDCalibration(InputWorkspace='rawC60',
              TofBinning=TofBinning,
              PreviousCalibrationTable='si_cal',
              BackgroundType='Flat',
              PeakPositions=DReference,
              MinimumPeakHeight=50,
              PeakWidthPercent=0.03,
              PeakWindow=0.5,
              OutputCalibrationTable='c60_cal',
              DiagnosticWorkspaces='c60_diag')


PDCalibration(InputWorkspace='rawC60',
              TofBinning=TofBinning,
              PreviousCalibrationTable='si_cal',
              BackgroundType='Flat',
              PeakPositions=DReference,
              MinimumPeakHeight=50,
              PeakWidthPercent=0.03,
              AllowSinglePeakCalibration=True,
              PeakWindow=0.5,
              OutputCalibrationTable='c60_cal_1',
              DiagnosticWorkspaces='c60_diag_1')


