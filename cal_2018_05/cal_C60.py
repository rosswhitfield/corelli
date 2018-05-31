import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

DReference = [2.7251,2.8904,4.2694,5.0063,8.1753]

Load(Filename='CORELLI_59583-59590', OutputWorkspace='rawC60')
ApplyCalibration('rawC60','CalibTable')

#MaskBTP(Workspace='rawC60',Pixel="1-16,241-256")
#MaskBTP(Workspace='rawC60',Bank="1-6,29,30,62-67,91")


PDCalibration(InputWorkspace='rawC60',
              #TofBinning='3400,10,16660',
              TofBinning='3000,-0.001,16660',
              BackgroundType='Flat',
              PeakPositions=DReference,
              MinimumPeakHeight=5,
              OutputCalibrationTable='cal',
              DiagnosticWorkspaces='diag')

cal = mtd['cal']
np.savetxt('/SNS/users/rwp/corelli/cal_2018_05/C60cal_difc.txt',cal.column(1))

SaveNexus(cal, '/SNS/users/rwp/corelli/cal_2018_05/C60cal.nxs')
SaveDiffCal(Filename='/SNS/users/rwp/corelli/cal_2018_05/C60cal.h5',
            CalibrationWorkspace="cal",
            MaskWorkspace='cal_mask')


# Check
ConvertUnits(InputWorkspace='rawC60', OutputWorkspace='rawC60_d', Target='dSpacing')
AlignDetectors(InputWorkspace='rawC60', OutputWorkspace='rawC60_d_aligned', CalibrationWorkspace='cal')
