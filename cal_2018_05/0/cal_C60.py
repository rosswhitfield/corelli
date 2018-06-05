import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

DReference = [2.7251,2.8904,4.2694,5.0063,8.1753]

Load(Filename='CORELLI_59583-59590', OutputWorkspace='rawC60')

ApplyCalibration('rawC60','CalibTable')

TofBinning='3000,-0.001,16660'

PDCalibration(InputWorkspace='rawC60',
              TofBinning=TofBinning,
              PeakPositions=DReference,
              MinimumPeakHeight=5,
              PeakWidthPercent=0.01,
              OutputCalibrationTable='cal',
              DiagnosticWorkspaces='diag')

rawC60_binned = Rebin('rawC60',Params=TofBinning,PreserveEvents=False)

Y = rawC60_binned.extractY()
Y_sum = Y[::8]+Y[1::8]+Y[2::8]+Y[3::8]+Y[4::8]+Y[5::8]+Y[6::8]+Y[7::8]

for n in range(rawC60_binned.getNumberHistograms()):
    rawC60_binned.setY(n, Y_sum[n//8])

PDCalibration(InputWorkspace='rawC60_binned',
              TofBinning=TofBinning,
              PeakPositions=DReference,
              MinimumPeakHeight=5,
              PeakWidthPercent=0.01,
              OutputCalibrationTable='calB',
              DiagnosticWorkspaces='diagB')

SaveDiffCal('calB',MaskWorkspace='calB_mask', Filename='/SNS/users/rwp/corelli/cal_2018_05/0/calB_c60.h5')

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
