import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration/CalibTableNew.txt')

corelli = LoadEmptyInstrument(InstrumentName='CORELLI')
ApplyCalibration('corelli','CalibTable')

LoadDiffCal(Filename='combined_Si_C60.h5',
            InstrumentName='CORELLI',
            WorkspaceName='cal')

# L1

print(mtd["corelli"].getInstrument().getSource().getPos())
AlignComponents(Workspace='corelli',CalibrationTable="cal_cal",MaskWorkspace="cal_mask",FitSourcePosition=True,Zposition=True)
print(mtd["corelli"].getInstrument().getSource().getPos())

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

ExportGeometry(InputWorkspace='corelli',Filename='AlignCombined.xml',EulerConvention='YXZ',Components=componentList)
SaveNexus(InputWorkspace='corelli',Filename='AlignCombined.nxs')
