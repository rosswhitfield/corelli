import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

DReference = [0.9179, 0.9600, 1.0451, 1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353]

Load(Filename='CORELLI_59313-59320', OutputWorkspace='rawSi')

ApplyCalibration('rawSi','CalibTable')

TofBinning='3000,-0.001,16660'

PDCalibration(InputWorkspace='rawSi',
              TofBinning=TofBinning,
              PeakPositions=DReference,
              MinimumPeakHeight=5,
              PeakWidthPercent=0.01,
              OutputCalibrationTable='cal',
              DiagnosticWorkspaces='diag')

rawSi_binned = Rebin('rawSi',Params=TofBinning,PreserveEvents=False)

Y = rawSi_binned.extractY()
Y_sum = Y[::8]+Y[1::8]+Y[2::8]+Y[3::8]+Y[4::8]+Y[5::8]+Y[6::8]+Y[7::8]

for n in range(rawSi_binned.getNumberHistograms()):
    rawSi_binned.setY(n, Y_sum[n//8])

PDCalibration(InputWorkspace='rawSi_binned',
              TofBinning=TofBinning,
              PeakPositions=DReference,
              MinimumPeakHeight=5,
              PeakWidthPercent=0.01,
              OutputCalibrationTable='calB',
              DiagnosticWorkspaces='diagB')

PDCalibration(InputWorkspace='rawSi_binned',
              TofBinning=TofBinning,
              PeakPositions=DReference,
              MinimumPeakHeight=5,
              PeakWidthPercent=0.01,
              PeakFunction='Lorentzian',
              OutputCalibrationTable='calBL',
              DiagnosticWorkspaces='diagBL')


# Compare in d

CreateGroupingWorkspace(InputWorkspace='rawSi', GroupDetectorsBy='All', OutputWorkspace='group')


ConvertUnits(InputWorkspace='rawSi', OutputWorkspace='rawSid', Target='dSpacing')
DiffractionFocussing('rawSid', OutputWorkspace='rawSid', GroupingWorkspace='group')

AlignDetectors('rawSi', OutputWorkspace='rawSi_d_2', CalibrationWorkspace='cal2')
DiffractionFocussing('rawSi_d_2', OutputWorkspace='rawSi_d_2', GroupingWorkspace='group')
AlignDetectors('rawSi', OutputWorkspace='rawSi_d_2B', CalibrationWorkspace='cal2B')
DiffractionFocussing('rawSi_d_2B', OutputWorkspace='rawSi_d_2B', GroupingWorkspace='group')
AlignDetectors('rawSi', OutputWorkspace='rawSi_d_2BL', CalibrationWorkspace='cal2BL')
DiffractionFocussing('rawSi_d_2BL', OutputWorkspace='rawSi_d_2BL', GroupingWorkspace='group')


import matplotlib.pyplot as plt
from mantid import plots
fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
ax.plot(mtd['rawSid'])
ax.plot(mtd['rawSi_d_2'])
ax.plot(mtd['rawSi_d_2B'])
ax.plot(mtd['rawSi_d_2BL'])
for d in DReference:
    ax.axvline(d,linewidth=1)
plt.show()
