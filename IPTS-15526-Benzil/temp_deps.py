runs = range(29818,29829)

for r in runs:
        filename='/SNS/CORELLI/IPTS-15526/nexus/CORELLI_'+str(r)+'.nxs.h5'
        name='COR_'+str(r)
        print 'Loading run number:'+ str(r)
        dataR=LoadEventNexus(Filename=filename)
        LoadInstrument(Workspace= dataR, Filename='/SNS/CORELLI/shared/Calibration/CORELLI_Definition_cal_20160310.xml',RewriteSpectraMap=False)
        MaskBTP(workspace=dataR,Bank='69-72')
        dataR=ConvertUnits(dataR,Target="Momentum",EMode="Elastic")
        dataR=CropWorkspace(dataR,XMin=2.5,XMax=10)
        SetGoniometer(dataR,Axis0="BL9:Mot:Sample:Axis1,0,1,0,1") 
        LoadIsawUB(InputWorkspace=dataR,Filename="/SNS/users/rwp/benzil/benzil_Hexagonal.mat")
        ConvertToMD(InputWorkspace=dataR,OutputWorkspace='results',QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',OtherDimensions='BL9:SE:Lakeshore:SETP2',
                       QConversionScales='HKL',LorentzCorrection='0',Uproj='1,1,0',Vproj='1,-1,0',Wproj='0,0,1',MinValues='-1.1,-10.1,-5.1,50',MaxValues='5.1,0,5.1,300',
                       OverwriteExisting=0)

