import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

corelli=LoadEmptyInstrument(InstrumentName='CORELLI')
ApplyCalibration('corelli','CalibTable')


LoadDiffCal(Filename='/SNS/users/rwp/corelli/cal_2018_05/0/calB_si.h5',InstrumentName='CORELLI',WorkspaceName='cal')

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
