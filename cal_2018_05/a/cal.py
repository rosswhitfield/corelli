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

difc=CalculateDIFC('rawSi')

import matplotlib.pyplot as plt
import numpy as np

si = np.array(mtd['Si_cal'].column(1))
c60 = np.array(mtd['C60_cal'].column(1))
difcc = difc.extractY().flatten()

plt.plot(difcc,label='difc')
plt.plot(si,label='si')
plt.plot(c60,label='c60')
plt.legend()
plt.show()


plt.plot(si/difcc,label='si')
plt.plot(c60/difcc,label='c60')
plt.legend()
plt.show()



si_difc = CalculateDIFC('rawSi', CalibrationWorkspace='Si_cal')
c60_difc = CalculateDIFC('rawSi', CalibrationWorkspace='C60_cal')
si_diff = si_difc/difc
c60_diff = c60_difc/difc


combined_cal = CloneWorkspace('Si_cal')
combined_mask = CloneWorkspace('Si_cal_mask')
