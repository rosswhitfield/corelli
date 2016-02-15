#!//usr/bin/env python2
from mantid.simpleapi import *
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/new_cal/cal_run14324_sn.dat', WorkspaceName='Si')
cList="bank55/sixteenpack"
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
AlignComponents(CalibrationTable="Si_cal",InputWorkspace='ws',ComponentList=cList,Xposition=True)
print mtd['ws'].getInstrument().getComponentByName("bank55/sixteenpack").getPos()
ExportGeometry(InputWorkspace='ws',Components=cList,Filename="/SNS/users/rwp/nil2.xml")
