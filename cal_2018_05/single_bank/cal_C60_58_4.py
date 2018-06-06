import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

DReference = [4.2694,5.0063,8.1753]

Load(Filename='CORELLI_59583-59590', OutputWorkspace='rawC60',BankName='bank58')
ApplyCalibration('rawC60','CalibTable')

TofBinning='3000,-0.001,16660'

PDCalibration(InputWorkspace='rawC60',
              TofBinning=TofBinning,
              PeakPositions=DReference,
              PeakWindow=0.5,
              MinimumPeakHeight=5,
              PeakWidthPercent=0.01,
              OutputCalibrationTable='cal2',
              DiagnosticWorkspaces='diag2')

rawC60_binned = Rebin('rawC60',Params=TofBinning,PreserveEvents=False)

Y = rawC60_binned.extractY()
Y_sum = Y[::4]+Y[1::4]+Y[2::4]+Y[3::4]

for n in range(rawC60_binned.getNumberHistograms()):
    rawC60_binned.setY(n, Y_sum[n//4])

PDCalibration(InputWorkspace='rawC60_binned',
              TofBinning=TofBinning,
              PeakPositions=DReference,
              MinimumPeakHeight=5,
              PeakWidthPercent=0.01,
              PeakWindow=0.5,
              OutputCalibrationTable='cal2B',
              DiagnosticWorkspaces='diag2B')

PDCalibration(InputWorkspace='rawC60_binned',
              TofBinning=TofBinning,
              PreviousCalibrationTable='cal2B',
              PeakPositions=DReference,
              MinimumPeakHeight=5,
              PeakWidthPercent=0.01,
              PeakWindow=0.5,
              OutputCalibrationTable='cal2B_s2',
              DiagnosticWorkspaces='diag2B_s2')


# Compare in d

CreateGroupingWorkspace(InputWorkspace='rawC60', GroupDetectorsBy='All', OutputWorkspace='group')


ConvertUnits(InputWorkspace='rawC60', OutputWorkspace='rawC60d', Target='dSpacing')
DiffractionFocussing('rawC60d', OutputWorkspace='rawC60d', GroupingWorkspace='group')

AlignDetectors('rawC60', OutputWorkspace='rawC60_d_2', CalibrationWorkspace='cal2')
DiffractionFocussing('rawC60_d_2', OutputWorkspace='rawC60_d_2', GroupingWorkspace='group')
AlignDetectors('rawC60', OutputWorkspace='rawC60_d_2B', CalibrationWorkspace='cal2B')
DiffractionFocussing('rawC60_d_2B', OutputWorkspace='rawC60_d_2B', GroupingWorkspace='group')
AlignDetectors('rawC60', OutputWorkspace='rawC60_d_2B_s2', CalibrationWorkspace='cal2B_s2')
DiffractionFocussing('rawC60_d_2B_s2', OutputWorkspace='rawC60_d_2B_s2', GroupingWorkspace='group')


import matplotlib.pyplot as plt
from mantid import plots
fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
ax.plot(mtd['rawC60d'],label='rawC60d')
ax.plot(mtd['rawC60_d_2'],label='rawC60_d_2')
ax.plot(mtd['rawC60_d_2B'],label='rawC60_d_2B')
ax.plot(mtd['rawC60_d_2B_s2'],label='rawC60_d_2B_s2')
for d in DReference:
    ax.axvline(d,linewidth=1)
ax.legend()
plt.show()
