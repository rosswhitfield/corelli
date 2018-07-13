import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

corelli=LoadEmptyInstrument(InstrumentName='CORELLI')
ApplyCalibration('corelli','CalibTable')
LoadIsawDetCal('corelli','/SNS/users/rwp/corelli/cal_2018_05/a/Aligned.nxs.detcal')

difc_old=CalculateDIFC('corelli')

LoadDiffCal(Filename='/SNS/users/rwp/corelli/cal_2018_05/a/cal.h5',InstrumentName='CORELLI',WorkspaceName='cal')

MaskBTP('cal_mask',Bank='26',Tube='1-8')
MaskBTP('cal_mask',Bank='74',Tube='13')
MaskBTP('cal_mask',Pixel='1-16,241-256')


componentList =  ','.join("bank"+str(i)+"/sixteenpack" for i in range(1,92))

#AlignComponents(Workspace='corelli',CalibrationTable="cal_cal",MaskWorkspace="cal_mask",ComponentList=componentList,GammaRotation=True)
AlignComponents(Workspace='corelli',CalibrationTable="cal_cal",MaskWorkspace="cal_mask",ComponentList=componentList,GammaRotation=True,Xposition=True,Zposition=True)

SaveNexus('corelli','/SNS/users/rwp/corelli/cal_2018_05/a/Aligned2.nxs')

difc_new=CalculateDIFC('corelli')
difc_diff = difc_new/difc_old
