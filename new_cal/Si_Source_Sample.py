#!/usr/bin/env python2
from mantid.simpleapi import *

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/new_cal/cal_run14324_sn.dat', WorkspaceName='Si')
MaskBTP(Workspace='Si_mask',Bank="1-30,56-60,62-91")
MaskBTP(Workspace='Si_mask',Pixel="1-15,242-256")

# Source
AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSourcePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSource().getPos()

# Sample
AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos()

# B row - Y
AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",ComponentList="B row",Yposition=True)
print mtd['alignedWorkspace'].getInstrument().getComponentByName('B row').getPos()


compon