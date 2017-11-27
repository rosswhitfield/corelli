import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration/CalibTableNew.txt')

corelli = LoadEmptyInstrument(InstrumentName='CORELLI')
ApplyCalibration('corelli','CalibTable')

# Start with Si

LoadDiffCal(Filename='../cal_Si_C60/cal_Si2_47327-47334_TubeCal_sum16_mask_lt_3.cal',
            InstrumentName='CORELLI',
            WorkspaceName='cal')


print(mtd["corelli"].getInstrument().getSource().getPos())
AlignComponents(Workspace='corelli',CalibrationTable="cal_cal",MaskWorkspace="cal_mask",FitSourcePosition=True,Zposition=True)
print(mtd["corelli"].getInstrument().getSource().getPos())
