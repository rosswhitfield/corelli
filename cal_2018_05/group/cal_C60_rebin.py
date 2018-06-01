import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

DReference = [2.7251,2.8904,4.2694,5.0063,8.1753]

Load(Filename='CORELLI_59583-59590', OutputWorkspace='rawC60')
ApplyCalibration('rawC60','CalibTable')

#MaskBTP(Workspace='rawC60',Pixel="1-16,241-256")
#MaskBTP(Workspace='rawC60',Bank="1-6,29,30,62-67,91")

TofBinning='3000,-0.001,16660'

rawC60_binned = Rebin('rawC60',Params=TofBinning,PreserveEvents=False)

Y = rawC60_binned.extractY()
Y_sum = Y[::16]+Y[1::16]+Y[2::16]+Y[3::16]+Y[4::16]+Y[5::16]+Y[6::16]+Y[7::16]+Y[8::16]+Y[9::16]+Y[10::16]+Y[11::16]+Y[12::16]+Y[13::16]+Y[14::16]+Y[15::16]

for n in range(rawC60_binned.getNumberHistograms()):
        rawC60_binned.setY(n, Y_sum[n//16])

PDCalibration(InputWorkspace='rawC60_binned',
              TofBinning=TofBinning,
              PeakPositions=DReference,
              MinimumPeakHeight=100,
              PeakWindow=0.5,
              OutputCalibrationTable='calG',
              DiagnosticWorkspaces='diagG')



calG = mtd['calG']
np.savetxt('/SNS/users/rwp/corelli/cal_2018_05/C60calG_difc.txt',calG.column(1))

SaveNexus(calG, '/SNS/users/rwp/corelli/cal_2018_05/C60calG.nxs')
SaveDiffCal(Filename='/SNS/users/rwp/corelli/cal_2018_05/C60calG.h5',
            CalibrationWorkspace="calG",
            MaskWorkspace='calG_mask')


# Check
ConvertUnits(InputWorkspace='rawC60', OutputWorkspace='rawC60_d', Target='dSpacing')
AlignDetectors(InputWorkspace='rawC60', OutputWorkspace='rawC60_d_aligned', CalibrationWorkspace='cal')
