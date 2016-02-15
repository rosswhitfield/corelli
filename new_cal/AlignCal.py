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

# B row - XYZ
AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",ComponentList="B row",Yposition=True, Xposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getComponentByName('B row').getPos()



componentList1=""
for i in range(31,56):
    componentList1+="bank"+str(i)+"/sixteenpack,"

componentList1+="bank61/sixteenpack"
print componentList1

# CL1
AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",ComponentList=componentList1,Xposition=True,Yposition=True,Zposition=True)
for i in componentList1.split(','):
    print i,mtd['alignedWorkspace'].getInstrument().getComponentByName(i).getPos()


AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='alignedWorkspace',ComponentList="B row",Yposition=True, Xposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getComponentByName('B row').getPos()
AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='alignedWorkspace',FitSourcePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSource().getPos()





LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/new_cal/cal_run14324_sn.dat', WorkspaceName='Si2')
MaskBTP(Workspace='Si2_mask',Bank="1-6,18-30,56-60,62-70,87,91")
MaskBTP(Workspace='Si2_mask',Pixel="1-15,242-256")

# rows - Y
AlignComponents(CalibrationTable="Si2_cal",MaskWorkspace="Si2_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",ComponentList="A row,B row,C row",Yposition=True)
print mtd['alignedWorkspace'].getInstrument().getComponentByName('A row').getPos()
print mtd['alignedWorkspace'].getInstrument().getComponentByName('B row').getPos()
print mtd['alignedWorkspace'].getInstrument().getComponentByName('C row').getPos()

AlignComponents(CalibrationTable="Si2_cal",MaskWorkspace="Si2_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",ComponentList="A row,B row,C row",Yposition=True, Xposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getComponentByName('A row').getPos()
print mtd['alignedWorkspace'].getInstrument().getComponentByName('B row').getPos()
print mtd['alignedWorkspace'].getInstrument().getComponentByName('C row').getPos()



AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",ComponentList="B row",Yposition=True)
ExportGeometry(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/new_cal/si_Brow_y.xml',EulerConvention='YZX',Components=componentList1)
AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='alignedWorkspace',ComponentList=componentList1,Xposition=True,Zposition=True,AlphaRotation=True,BetaRotation=True,GammaRotation=True)
ExportGeometry(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/new_cal/si_Brow+banks_xzabg.xml',EulerConvention='YXZ',Components=componentList1)
SaveNexus(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/new_cal/si_Brow+banks_xzabg.nxs')


LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='alignedWorkspace')
# Give the rotation a kick otherwise they won't move
RotateInstrumentComponent(Workspace='alignedWorkspace',ComponentName='A row',X=1,Y=1,Z=1,Angle=0.01)
RotateInstrumentComponent(Workspace='alignedWorkspace',ComponentName='B row',X=1,Y=1,Z=1,Angle=0.01)
RotateInstrumentComponent(Workspace='alignedWorkspace',ComponentName='C row',X=1,Y=1,Z=1,Angle=0.01)
AlignComponents(CalibrationTable="Si2_cal",MaskWorkspace="Si2_mask",Workspace='alignedWorkspace',ComponentList="A row,B row,C row",EulerConvention='YXZ',AlphaRotation=True,BetaRotation=True,GammaRotation=True)
print mtd['alignedWorkspace'].getInstrument().getComponentByName('A row').getPos()
print mtd['alignedWorkspace'].getInstrument().getComponentByName('B row').getPos()
print mtd['alignedWorkspace'].getInstrument().getComponentByName('C row').getPos()
print mtd['alignedWorkspace'].getInstrument().getComponentByName('A row').getRotation().getEulerAngles("YXZ")
print mtd['alignedWorkspace'].getInstrument().getComponentByName('B row').getRotation().getEulerAngles("YXZ")
print mtd['alignedWorkspace'].getInstrument().getComponentByName('C row').getRotation().getEulerAngles("YXZ")
ExportGeometry(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/new_cal/si_row_abg.xml',EulerConvention='YXZ',Components=componentList1)


LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='alignedWorkspace')
# Give the rotation a kick otherwise they won't move
RotateInstrumentComponent(Workspace='alignedWorkspace',ComponentName='A row',X=0,Y=1,Z=0,Angle=0.01)
RotateInstrumentComponent(Workspace='alignedWorkspace',ComponentName='B row',X=0,Y=1,Z=0,Angle=0.01)
RotateInstrumentComponent(Workspace='alignedWorkspace',ComponentName='C row',X=0,Y=1,Z=0,Angle=0.01)
AlignComponents(CalibrationTable="Si2_cal",MaskWorkspace="Si2_mask",Workspace='alignedWorkspace',ComponentList="A row,B row,C row",EulerConvention='YXZ',AlphaRotation=True,BetaRotation=False,GammaRotation=False,Yposition=True, Xposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getComponentByName('A row').getPos()
print mtd['alignedWorkspace'].getInstrument().getComponentByName('B row').getPos()
print mtd['alignedWorkspace'].getInstrument().getComponentByName('C row').getPos()
print mtd['alignedWorkspace'].getInstrument().getComponentByName('A row').getRotation().getEulerAngles("YXZ")
print mtd['alignedWorkspace'].getInstrument().getComponentByName('B row').getRotation().getEulerAngles("YXZ")
print mtd['alignedWorkspace'].getInstrument().getComponentByName('C row').getRotation().getEulerAngles("YXZ")




AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",ComponentList="B row",Yposition=True)
ExportGeometry(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/new_cal/si_Brow_y.xml',EulerConvention='YZX',Components=componentList1)

AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='alignedWorkspace',ComponentList=componentList1,Xposition=True,Zposition=True,AlphaRotation=True,BetaRotation=True,GammaRotation=True,MinAlphaRotation=-20,MaxAlphaRotation=20)
ExportGeometry(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/new_cal/si_Brow+banks_xzabg.xml',EulerConvention='YXZ',Components=componentList1)
SaveNexus(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/new_cal/si_Brow+banks_xzabg.nxs')


# Source first
AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSourcePosition=True)
AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='alignedWorkspace',ComponentList="B row",Yposition=True)
ExportGeometry(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/new_cal/si_source_Brow_y.xml',EulerConvention='YZX',Components=componentList1)

AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='alignedWorkspace',ComponentList=componentList1,Xposition=True,Zposition=True,AlphaRotation=True,BetaRotation=True,GammaRotation=True,MinAlphaRotation=-20,MaxAlphaRotation=20)
ExportGeometry(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/new_cal/si_Brow+banks_xzabg.xml',EulerConvention='YXZ',Components=componentList1)
SaveNexus(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/new_cal/si_source_Brow+banks_xzabg.nxs')



