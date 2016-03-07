from mantid.simpleapi import *

### C60

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_20501-8_sum4_mask_lt_3.cal', WorkspaceName='C60')
MaskBTP(Workspace='C60_mask',Pixel="1-16,241-256")
MaskBTP(Workspace='C60_mask',Bank="1-54,62-91")

LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='C60A')
f = open('/SNS/users/rwp/corelli/cal_2016_02/Align_L1_banks_55_61_C60.log','a')
for i in range(10):
    AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='C60A',FitSourcePosition=True,Zposition=True)
    f.write("C60 Source i="+str(i)+" "+str(mtd['C60A'].getInstrument().getSource().getPos())+'\n')
    AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='C60A',ComponentList='bank55/sixteenpack,bank56/sixteenpack,bank57/sixteenpack,bank58/sixteenpack,bank59/sixteenpack,bank60/sixteenpack,bank61/sixteenpack',Xposition=True,Yposition=True,Zposition=True,EulerConvention="YXZ",AlphaRotation=True)
    for b in range(55,62):
        f.write("C60 Brow   i="+str(i)+" "+str(mtd['C60A'].getInstrument().getComponentByName("bank"+str(b)+"/sixteenpack").getPos())+
                str(mtd['C60A'].getInstrument().getComponentByName("bank"+str(b)+"/sixteenpack").getRotation().getEulerAngles("YXZ"))+'\n')

f.close()
