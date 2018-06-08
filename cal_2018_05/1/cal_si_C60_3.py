import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

LoadDiffCal(Filename='/SNS/users/rwp/corelli/cal_2018_05/1/calB_si.h5',InstrumentName='CORELLI',WorkspaceName='si')

DReference = [2.7251,2.8904,4.2694,5.0063,8.1753]
DReference = [4.2694,5.0063,8.1753]

Load(Filename='CORELLI_59583-59590', OutputWorkspace='rawC60')

ApplyCalibration('rawC60','CalibTable')

LoadIsawDetCal('rawC60','/SNS/users/rwp/corelli/cal_2018_05/0a/Aligned_row_si_c60.nxs.detcal')

TofBinning='3000,-0.01,16660'

PDCalibration(InputWorkspace='rawC60',
              TofBinning=TofBinning,
              PreviousCalibrationTable='si_cal',
              BackgroundType='Flat',
              PeakPositions=DReference,
              MinimumPeakHeight=20,
              PeakWidthPercent=0.03,
              PeakWindow=0.5,
              OutputCalibrationTable='cal',
              DiagnosticWorkspaces='diag')

SaveDiffCal('cal',MaskWorkspace='cal_mask', Filename='/SNS/users/rwp/corelli/cal_2018_05/1/cal_si_c60_3.h5')

rawC60_binned = Rebin('rawC60',Params=TofBinning,PreserveEvents=False)

Y = rawC60_binned.extractY()
Y_sum = Y[::4]+Y[1::4]+Y[2::4]+Y[3::4]

for n in range(rawC60_binned.getNumberHistograms()):
    rawC60_binned.setY(n, Y_sum[n//4])

PDCalibration(InputWorkspace='rawC60_binned',
              TofBinning=TofBinning,
              PreviousCalibrationTable='si_cal',
              BackgroundType='Flat',
              PeakPositions=DReference,
              MinimumPeakHeight=50,
              PeakWindow=0.5,
              PeakWidthPercent=0.01,
              OutputCalibrationTable='calB',
              DiagnosticWorkspaces='diagB')

SaveDiffCal('calB',MaskWorkspace='calB_mask', Filename='/SNS/users/rwp/corelli/cal_2018_05/1/calB_si_c60_3.h5')

# Compare in d


CreateGroupingWorkspace(InputWorkspace='rawC60', GroupDetectorsBy='All', OutputWorkspace='group')


ConvertUnits(InputWorkspace='rawC60', OutputWorkspace='rawC60d', Target='dSpacing')
DiffractionFocussing('rawC60d', OutputWorkspace='rawC60d', GroupingWorkspace='group')

AlignDetectors('rawC60', OutputWorkspace='rawC60_d', CalibrationWorkspace='cal')
DiffractionFocussing('rawC60_d', OutputWorkspace='rawC60_d', GroupingWorkspace='group')
AlignDetectors('rawC60', OutputWorkspace='rawC60_dB', CalibrationWorkspace='cal2B')
DiffractionFocussing('rawC60_dB', OutputWorkspace='rawC60_dB', GroupingWorkspace='group')


import matplotlib.pyplot as plt
from mantid import plots
fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
ax.plot(mtd['rawC60d'])
ax.plot(mtd['rawC60_d'])
ax.plot(mtd['rawC60_dB'])
for d in DReference:
    ax.axvline(d,linewidth=1)
plt.show()
