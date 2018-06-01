import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

DReference = [1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353]

Load(Filename='CORELLI_59313-59320', OutputWorkspace='rawSi')
rawSi_org=CloneWorkspace('rawSi')

ApplyCalibration('rawSi','CalibTable')


tmp_group, _, _ = CreateGroupingWorkspace(InputWorkspace='rawSi')

for i in range(0,256*16*91):
    tmp_group.dataY(i)[0] = i//8

rawSi_grouped = GroupDetectors(InputWorkspace='rawSi', CopyGroupingFromWorkspace=tmp_group)

PDCalibration(InputWorkspace='rawSi_grouped',
              #TofBinning='3400,10,16660',
              TofBinning='3000,-0.001,16660',
              BackgroundType='Flat',
              PeakPositions=DReference,
              MinimumPeakHeight=5,
              OutputCalibrationTable='calG',
              DiagnosticWorkspaces='diagG')

cal = mtd['cal']
np.savetxt('/SNS/users/rwp/corelli/cal_2018_05/cal_difc.txt',cal.column(1))

SaveNexus(cal, '/SNS/users/rwp/corelli/cal_2018_05/cal.nxs')
SaveDiffCal(Filename='/SNS/users/rwp/corelli/cal_2018_05/cal.h5',
            CalibrationWorkspace="cal",
            MaskWorkspace='cal_mask')


# Check
ConvertUnits(InputWorkspace='rawSi', OutputWorkspace='rawSi_d', Target='dSpacing')
AlignDetectors(InputWorkspace='rawSi', OutputWorkspace='rawSi_d_aligned', CalibrationWorkspace='cal')
