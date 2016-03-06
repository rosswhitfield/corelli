from mantid.simpleapi import *

### Silicon

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Si_20492-9_sum4_mask_lt_3.cal', WorkspaceName='Si')
MaskBTP(Workspace='Si_mask',Pixel="1-16,241-256")
MaskBTP(Workspace='Si_mask',Bank="1-29,63-91")

LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='SiA')
f = open('/SNS/users/rwp/corelli/cal_2016_02/Align_L1_Brow_Si.log','a')
for i in range(100):
    AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='SiA',FitSourcePosition=True,Zposition=True)
    f.write("Si Source i="+str(i)+" "+str(mtd['SiA'].getInstrument().getSource().getPos())+'\n')
    AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='SiA',ComponentList='B row',Xposition=True,Yposition=True,Zposition=True)
    f.write("Si Brow   i="+str(i)+" "+str(mtd['SiA'].getInstrument().getComponentByName("B row").getPos())+'\n')

f.close()

LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='SiA')
f = open('/SNS/users/rwp/corelli/cal_2016_02/Align_L1xz_Brow_Si.log','a')
for i in range(100):
    AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='SiA',FitSourcePosition=True,Xposition=True,Zposition=True)
    f.write("Si Source i="+str(i)+" "+str(mtd['SiA'].getInstrument().getSource().getPos())+'\n')
    AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='SiA',ComponentList='B row',Xposition=True,Yposition=True,Zposition=True)
    f.write("Si Brow   i="+str(i)+" "+str(mtd['SiA'].getInstrument().getComponentByName("B row").getPos())+'\n')


f.close()

LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='SiA')
RotateInstrumentComponent(Workspace='SiA',ComponentName='B row',Y=1,Angle=0.01) # Kick
f = open('/SNS/users/rwp/corelli/cal_2016_02/Align_L1_Brow_xyza_Si.log','a')
for i in range(100):
    AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='SiA',FitSourcePosition=True,Zposition=True)
    f.write("Si Source i="+str(i)+" "+str(mtd['SiA'].getInstrument().getSource().getPos())+'\n')
    AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='SiA',ComponentList='B row',Xposition=True,Yposition=True,Zposition=True,EulerConvention="YXZ",AlphaRotation=True)
    f.write("Si Brow   i="+str(i)+" "+str(mtd['SiA'].getInstrument().getComponentByName("B row").getPos())+
            str(mtd['SiA'].getInstrument().getComponentByName("B row").getRotation().getEulerAngles("YXZ"))+'\n')

f.close()

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Si_20492-9_sum4_mask_lt_3.cal', WorkspaceName='Si')
MaskBTP(Workspace='Si_mask',Pixel="1-16,241-256")

LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='SiA')
RotateInstrumentComponent(Workspace='SiA',ComponentName='A row',Y=1,Angle=0.01) # Kick
RotateInstrumentComponent(Workspace='SiA',ComponentName='B row',Y=1,Angle=0.01) # Kick
RotateInstrumentComponent(Workspace='SiA',ComponentName='C row',Y=1,Angle=0.01) # Kick
f = open('/SNS/users/rwp/corelli/cal_2016_02/Align_L1_rows_xyza_Si.log','a')
for i in range(100):
    AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='SiA',FitSourcePosition=True,Zposition=True)
    f.write("Si Source i="+str(i)+" "+str(mtd['SiA'].getInstrument().getSource().getPos())+'\n')
    AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='SiA',ComponentList='A row,B row,C row',Xposition=True,Yposition=True,Zposition=True,EulerConvention="YXZ",AlphaRotation=True)
    f.write("Si Arow   i="+str(i)+" "+str(mtd['SiA'].getInstrument().getComponentByName("A row").getPos())+
            str(mtd['SiA'].getInstrument().getComponentByName("A row").getRotation().getEulerAngles("YXZ"))+'\n')
    f.write("Si Brow   i="+str(i)+" "+str(mtd['SiA'].getInstrument().getComponentByName("B row").getPos())+
            str(mtd['SiA'].getInstrument().getComponentByName("B row").getRotation().getEulerAngles("YXZ"))+'\n')
    f.write("Si Crow   i="+str(i)+" "+str(mtd['SiA'].getInstrument().getComponentByName("C row").getPos())+
            str(mtd['SiA'].getInstrument().getComponentByName("C row").getRotation().getEulerAngles("YXZ"))+'\n')

f.close()


### C60

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_20501-8_sum4_mask_lt_3.cal', WorkspaceName='C60')
MaskBTP(Workspace='C60_mask',Pixel="1-16,241-256")
MaskBTP(Workspace='C60_mask',Bank="1-29,63-91")

LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='C60A')
f = open('/SNS/users/rwp/corelli/cal_2016_02/Align_L1_Brow_C60.log','a')
for i in range(100):
    AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='C60A',FitSourcePosition=True,Zposition=True)
    f.write("C60 Source i="+str(i)+" "+str(mtd['C60A'].getInstrument().getSource().getPos())+'\n')
    AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='C60A',ComponentList='B row',Xposition=True,Yposition=True,Zposition=True)
    f.write("C60 Brow   i="+str(i)+" "+str(mtd['C60A'].getInstrument().getComponentByName("B row").getPos())+'\n')

f.close()

LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='C60A')
f = open('/SNS/users/rwp/corelli/cal_2016_02/Align_L1xz_Brow_C60.log','a')
for i in range(100):
    AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='C60A',FitSourcePosition=True,Xposition=True,Zposition=True)
    f.write("C60 Source i="+str(i)+" "+str(mtd['C60A'].getInstrument().getSource().getPos())+'\n')
    AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='C60A',ComponentList='B row',Xposition=True,Yposition=True,Zposition=True)
    f.write("C60 Brow   i="+str(i)+" "+str(mtd['C60A'].getInstrument().getComponentByName("B row").getPos())+'\n')

f.close()

LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='C60A')
RotateInstrumentComponent(Workspace='C60A',ComponentName='B row',Y=1,Angle=0.01) # Kick
f = open('/SNS/users/rwp/corelli/cal_2016_02/Align_L1_Brow_xyza_C60.log','a')
for i in range(100):
    AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='C60A',FitSourcePosition=True,Zposition=True)
    f.write("C60 Source i="+str(i)+" "+str(mtd['C60A'].getInstrument().getSource().getPos())+'\n')
    AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='C60A',ComponentList='B row',Xposition=True,Yposition=True,Zposition=True,EulerConvention="YXZ",AlphaRotation=True)
    f.write("C60 Brow   i="+str(i)+" "+str(mtd['C60A'].getInstrument().getComponentByName("B row").getPos())+
            str(mtd['C60A'].getInstrument().getComponentByName("B row").getRotation().getEulerAngles("YXZ"))+'\n')

f.close()

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_20501-8_sum4_mask_lt_3.cal', WorkspaceName='C60')
MaskBTP(Workspace='C60_mask',Pixel="1-16,241-256")

LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='C60A')
RotateInstrumentComponent(Workspace='C60A',ComponentName='A row',Y=1,Angle=0.01) # Kick
RotateInstrumentComponent(Workspace='C60A',ComponentName='B row',Y=1,Angle=0.01) # Kick
RotateInstrumentComponent(Workspace='C60A',ComponentName='C row',Y=1,Angle=0.01) # Kick
f = open('/SNS/users/rwp/corelli/cal_2016_02/Align_L1_rows_xyza_C60.log','a')
for i in range(100):
    AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='C60A',FitSourcePosition=True,Zposition=True)
    f.write("C60 Source i="+str(i)+" "+str(mtd['C60A'].getInstrument().getSource().getPos())+'\n')
    AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='C60A',ComponentList='A row,B row,C row',Xposition=True,Yposition=True,Zposition=True,EulerConvention="YXZ",AlphaRotation=True)
    f.write("C60 Brow   i="+str(i)+" "+str(mtd['C60A'].getInstrument().getComponentByName("A row").getPos())+
            str(mtd['C60A'].getInstrument().getComponentByName("A row").getRotation().getEulerAngles("YXZ"))+'\n')
    f.write("C60 Brow   i="+str(i)+" "+str(mtd['C60A'].getInstrument().getComponentByName("B row").getPos())+
            str(mtd['C60A'].getInstrument().getComponentByName("B row").getRotation().getEulerAngles("YXZ"))+'\n')
    f.write("C60 Brow   i="+str(i)+" "+str(mtd['C60A'].getInstrument().getComponentByName("C row").getPos())+
            str(mtd['C60A'].getInstrument().getComponentByName("C row").getRotation().getEulerAngles("YXZ"))+'\n')

f.close()
