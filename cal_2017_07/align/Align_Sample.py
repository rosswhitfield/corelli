import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration/CalibTableNew.txt')

corelli = LoadEmptyInstrument(InstrumentName='CORELLI')
ApplyCalibration('corelli','CalibTable')

# Start with Si

LoadDiffCal(Filename='../cal_Si_C60/cal_Si2_47327-47334_TubeCal_sum16_mask_lt_3.h5',
            InstrumentName='CORELLI',
            WorkspaceName='SiCal')


print(mtd["corelli"].getInstrument().getSample().getPos())
AlignComponents(Workspace='corelli',CalibrationTable="SiCal_cal",MaskWorkspace="SiCal_mask",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print(mtd["corelli"].getInstrument().getSample().getPos())


corelli2 = LoadEmptyInstrument(InstrumentName='CORELLI')
ApplyCalibration('corelli2','CalibTable')

# Start with Si

LoadDiffCal(Filename='../cal_Si_C60/cal_C60_2_47367-47382_TubeCal_sum16_mask_lt_3.h5',
            InstrumentName='CORELLI',
            WorkspaceName='C60Cal')


print(mtd["corelli2"].getInstrument().getSample().getPos())
AlignComponents(Workspace='corelli2',CalibrationTable="C60Cal_cal",MaskWorkspace="C60Cal_mask",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print(mtd["corelli2"].getInstrument().getSample().getPos())
