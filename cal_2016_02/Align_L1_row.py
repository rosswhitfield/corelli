from mantid.simpleapi import *

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Si_20492-9_sum4_mask_lt_3.cal', WorkspaceName='Si')
MaskBTP(Workspace='Si_mask',Pixel="1-16,241-256")
MaskBTP(Workspace='Si_mask',Bank="1-29,63-91")

LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='SiA')

f = open('/SNS/users/rwp/corelli/cal_2016_02/Align_L1_Brow_Si.log','a')

for i in range(10):
    AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='SiA',FitSourcePosition=True,Zposition=True)
    f.write("Si Source i="+str(i)+" "+str(mtd['SiA'].getInstrument().getSource().getPos())+'\n')
    AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='SiA',ComponentList='B row',Xposition=True,Yposition=True,Zposition=True)
    f.write("Si Brow   i="+str(i)+" "+str(mtd['SiA'].getInstrument().getComponentByName("B row").getPos())+'\n')

f.close()

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_20501-8_sum4_mask_lt_3.cal', WorkspaceName='C60')
MaskBTP(Workspace='C60_mask',Pixel="1-16,241-256")
MaskBTP(Workspace='C60_mask',Bank="1-29,63-91")

LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='C60A')

f = open('/SNS/users/rwp/corelli/cal_2016_02/Align_L1_Brow_C60.log','a')

for i in range(10):
    AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='C60A',FitSourcePosition=True,Zposition=True)
    f.write("C60 Source i="+str(i)+" "+str(mtd['C60A'].getInstrument().getSource().getPos())+'\n')
    AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='C60A',ComponentList='B row',Xposition=True,Yposition=True,Zposition=True)
    f.write("C60 Brow   i="+str(i)+" "+str(mtd['C60A'].getInstrument().getComponentByName("B row").getPos())+'\n')

f.close()
