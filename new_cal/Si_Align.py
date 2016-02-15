#!/usr/bin/env python2
from mantid.simpleapi import *
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/new_cal/cal_run14324_sn.dat', WorkspaceName='Si')
cList="bank55/sixteenpack"
AlignComponents(CalibrationTable="Si_cal",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",ComponentList=cList,Xposition=True)
print mtd['alignedWorkspace'].getInstrument().getComponentByName("bank55/sixteenpack").getPos()
ExportGeometry(InputWorkspace='alignedWorkspace',Components=cList,Filename="/SNS/users/rwp/nil.xml")
