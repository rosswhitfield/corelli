from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

Load(Filename='CORELLI_59583-59590', OutputWorkspace='rawC60')
ApplyCalibration('rawC60','CalibTable')
LoadIsawDetCal('rawC60','/SNS/users/rwp/corelli/cal_2018_05/a/Aligned4.nxs.detcal')

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

Load(Filename='CORELLI_59313-59320', OutputWorkspace='rawSi')
ApplyCalibration('rawSi','CalibTable')
LoadIsawDetCal('rawSi','/SNS/users/rwp/corelli/cal_2018_05/a/Aligned4.nxs.detcal')

DReference = [0.9179, 0.9600, 1.0451, 1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353]

d = -0.002
TofBinning='3000,{},16660'.format(d)
PDCalibration(InputWorkspace='rawSi',
              TofBinning=TofBinning,
              PeakPositions=DReference,
              MinimumPeakHeight=5,
              PeakWidthPercent=0.01,
              OutputCalibrationTable='Si_cal',
              DiagnosticWorkspaces='Si_diag')

difc=CalculateDIFC('rawSi')


si_difc = CalculateDIFC('rawSi', CalibrationWorkspace='Si_cal')
c60_difc = CalculateDIFC('rawSi', CalibrationWorkspace='C60_cal')
si_diff = si_difc/difc
c60_diff = c60_difc/difc


combined_cal = CloneWorkspace('Si_cal')
combined_mask = CloneWorkspace('Si_cal_mask')

for bank in [22,23,24,25,26,27,28, 53,54,55,56,57,58,59,60,61, 84,85,86,87,88,89,90]:
    for detID in range((bank-1)*4096,bank*4096):
        combined_mask.setY(detID, mtd['C60_cal_mask'].readY(detID))
        combined_cal.setCell(detID, 1, mtd['C60_cal'].cell(detID, 1))

combined_difc = CalculateDIFC('rawSi', CalibrationWorkspace='combined_cal')
combined_diff = combined_difc/difc

SaveDiffCal(CalibrationWorkspace='combined_cal', MaskWorkspace='combined_mask', Filename='/SNS/users/rwp/corelli/cal_2018_05/a/cal5.h5')
