import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

DReference = [1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353]

Load(Filename='CORELLI_59313-59320', OutputWorkspace='rawSi', BankName='bank50')

ApplyCalibration('rawSi','CalibTable')

TofBinning='3000,-0.001,16660'

PDCalibration(InputWorkspace='rawSi',
              TofBinning=TofBinning,
              PeakPositions=DReference,
              MinimumPeakHeight=5,
              PeakWidthPercent=0.01,
              OutputCalibrationTable='cal2',
              DiagnosticWorkspaces='diag2')

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
                            OutputCalibrationTable='cal2B',
                            DiagnosticWorkspaces='diag2B')

