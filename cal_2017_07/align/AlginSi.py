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

# rows - Y
AlignComponents(Workspace='corelli',CalibrationTable="cal_cal",MaskWorkspace="cal_mask",ComponentList="A row,B row,C row",Yposition=True)
print(mtd['corelli'].getInstrument().getComponentByName('A row').getPos())
print(mtd['corelli'].getInstrument().getComponentByName('B row').getPos())
print(mtd['corelli'].getInstrument().getComponentByName('C row').getPos())


# Banks, X, Z, and rotate Y

componentList =  ','.join("bank"+str(i)+"/sixteenpack" for i in range(1,92))
print(componentList)

AlignComponents(CalibrationTable="cal_cal",MaskWorkspace="cal_mask",Workspace='corelli',
                EulerConvention='YXZ',ComponentList=componentList,Xposition=True,Zposition=True,AlphaRotation=True)

ExportGeometry(InputWorkspace='corelli',Filename='AlignSi.xml',EulerConvention='YXZ',Components=componentList)
SaveNexus(InputWorkspace='corelli',Filename='AlignSi.nxs')
