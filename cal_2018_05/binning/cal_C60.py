from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

Load(Filename='CORELLI_59583-59590', OutputWorkspace='rawC60')
ApplyCalibration('rawC60','CalibTable')


for d in [-0.02, -0.01, -0.005, -0.002, -0.001]:
    TofBinning='3000,{},16660'.format(d)
    Rebin(InputWorkspace='rawC60', OutputWorkspace='rawC60_{}'.format(d),Params=TofBinning)


DReference = [4.2694,5.0063,8.1753]

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
              OutputCalibrationTable='cal_3_{}'.format(d),
              DiagnosticWorkspaces='diag_3_{}'.format(d))

d = -0.005
TofBinning='3000,{},16660'.format(d)
PDCalibration(InputWorkspace='rawC60',
              TofBinning=TofBinning,
              #PreviousCalibrationTable='si_cal',
              BackgroundType='Flat',
              PeakPositions=DReference,
              MinimumPeakHeight=50,
              PeakWidthPercent=0.03,
              PeakWindow=0.5,
              OutputCalibrationTable='cal_3_{}'.format(d),
              DiagnosticWorkspaces='diag_3_{}'.format(d))

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
              OutputCalibrationTable='cal_5_{}'.format(d),
              DiagnosticWorkspaces='diag_5_{}'.format(d))

d = -0.005
TofBinning='3000,{},16660'.format(d)
PDCalibration(InputWorkspace='rawC60',
              TofBinning=TofBinning,
              #PreviousCalibrationTable='si_cal',
              BackgroundType='Flat',
              PeakPositions=DReference,
              MinimumPeakHeight=50,
              PeakWidthPercent=0.03,
              PeakWindow=0.5,
              OutputCalibrationTable='cal_5_{}'.format(d),
              DiagnosticWorkspaces='diag_5_{}'.format(d))

