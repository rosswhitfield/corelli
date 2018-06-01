import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

DReference = [1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353]

Load(Filename='CORELLI_59313-59320', OutputWorkspace='rawSi')
rawSi_org=CloneWorkspace('rawSi')

ApplyCalibration('rawSi','CalibTable')


TofBinning='3000,-0.001,16660'

rawSi_binned = Rebin('rawSi',Params=TofBinning,PreserveEvents=False)

Y = rawSi_binned.extractY()
Y_sum = Y[::16]+Y[1::16]+Y[2::16]+Y[3::16]+Y[4::16]+Y[5::16]+Y[6::16]+Y[7::16]+Y[8::16]+Y[9::16]+Y[10::16]+Y[11::16]+Y[12::16]+Y[13::16]+Y[14::16]+Y[15::16]

for n in range(rawSi_binned.getNumberHistograms()):
    rawSi_binned.setY(n, Y_sum[n//16])

PDCalibration(InputWorkspace='rawSi_binned',
              #TofBinning='3400,10,16660',
              TofBinning=TofBinning,
              BackgroundType='Flat',
              PeakPositions=DReference,
              MinimumPeakHeight=50,
              OutputCalibrationTable='calG',
              DiagnosticWorkspaces='diagG')

calG = mtd['calG']
np.savetxt('/SNS/users/rwp/corelli/cal_2018_05/calG_difc.txt',calG.column(1))

SaveNexus(calG, '/SNS/users/rwp/corelli/cal_2018_05/calG.nxs')
SaveDiffCal(Filename='/SNS/users/rwp/corelli/cal_2018_05/calG.h5',
            CalibrationWorkspace="calG",
            MaskWorkspace='calG_mask')


# Check
ConvertUnits(InputWorkspace='rawSi', OutputWorkspace='rawSi_d', Target='dSpacing')
AlignDetectors(InputWorkspace='rawSi', OutputWorkspace='rawSi_d_aligned', CalibrationWorkspace='calG')
