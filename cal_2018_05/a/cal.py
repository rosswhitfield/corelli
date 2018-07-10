from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

Load(Filename='CORELLI_59583-59590', OutputWorkspace='rawC60')
ApplyCalibration('rawC60','CalibTable')

DReference = [2.7251,2.8904,4.2694,5.0063,8.1753]

d = -0.01
TofBinning='3000,{},16660'.format(d)
PDCalibration(InputWorkspace='rawC60',
              TofBinning=TofBinning,
              #PreviousCalibrationTable='si_cal',
              BackgroundType='Flat',
              PeakPositions=DReference,
              MinimumPeakHeight=50,
              PeakWidthPercent=0.03,
              PeakWindow=0.5,
              OutputCalibrationTable='C60_cal',
              DiagnosticWorkspaces='C60_diag')

DReference = [0.9179, 0.9600, 1.0451, 1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353]

Load(Filename='CORELLI_59313-59320', OutputWorkspace='rawSi')

ApplyCalibration('rawSi','CalibTable')

d = -0.002
TofBinning='3000,{},16660'.format(d)
PDCalibration(InputWorkspace='rawSi',
              TofBinning=TofBinning,
              PeakPositions=DReference,
              MinimumPeakHeight=5,
              PeakWidthPercent=0.01,
              OutputCalibrationTable='Si_cal',
              DiagnosticWorkspaces='Si_diag')
