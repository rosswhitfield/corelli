runs = range(29818,29829)
print len(runs)
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
                       QConversionScales='HKL',LorentzCorrection='0',Uproj='1,1,0',Vproj='1,-1,0',Wproj='0,0,1',MinValues='-1.1,-10.1,-5.1,80',MaxValues='5.1,0,5.1,260',
                       OverwriteExisting=0)

BinMD(InputWorkspace='results',
            OutputWorkspace='binned',
            AlignedDim0="[H,H,0],-1.01,5.01,301",
            AlignedDim1="[H,-H,0],-10.01,0.01,501",
            AlignedDim2="[0,0,L],-5.1,5.1,51",
            AlignedDim3="BL9:SE:Lakeshore:SETP2,80,260,60")
SaveMD(InputWorkspace='binned',Filename='/SNS/users/rwp/benzil/temp_deps.nxs')

SliceMDHisto(InputWorkspace='binned',OutputWorkspace='hk0',Start=[0,0,25,0],End=[301,501,26,60])
SaveMD(InputWorkspace='hk0',Filename='/SNS/users/rwp/benzil/temp_deps_hk0.nxs')


# fake temperature number
for n, r in enumerate(runs):
        filename='/SNS/CORELLI/IPTS-15526/nexus/CORELLI_'+str(r)+'.nxs.h5'
        name='COR_'+str(r)
        print 'Loading run number:'+ str(r)
        dataR=LoadEventNexus(Filename=filename)
        AddSampleLog(dataR,LogName='number',LogText=str(n),LogType='Number',NumberType='Double')
        LoadInstrument(Workspace= dataR, Filename='/SNS/CORELLI/shared/Calibration/CORELLI_Definition_cal_20160310.xml',RewriteSpectraMap=False)
        MaskBTP(workspace=dataR,Bank='69-72')
        dataR=ConvertUnits(dataR,Target="Momentum",EMode="Elastic")
        dataR=CropWorkspace(dataR,XMin=2.5,XMax=10)
        SetGoniometer(dataR,Axis0="BL9:Mot:Sample:Axis1,0,1,0,1") 
        LoadIsawUB(InputWorkspace=dataR,Filename="/SNS/users/rwp/benzil/benzil_Hexagonal.mat")
        ConvertToMD(InputWorkspace=dataR,OutputWorkspace='results2',QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',OtherDimensions='number',
                       QConversionScales='HKL',LorentzCorrection='0',Uproj='1,1,0',Vproj='1,-1,0',Wproj='0,0,1',MinValues='-1.1,-10.1,-5.1,0',MaxValues='5.1,0,5.1,11',
                       OverwriteExisting=0)

BinMD(InputWorkspace='results2',
            OutputWorkspace='binned2',
            AlignedDim0="[H,H,0],-1.01,5.01,301",
            AlignedDim1="[H,-H,0],-10.01,0.01,501",
            AlignedDim2="[0,0,L],-5.1,5.1,51",
            AlignedDim3="number,0,11,11")

SaveMD(InputWorkspace='binned2',Filename='/SNS/users/rwp/benzil/temp_deps2.nxs')

SliceMDHisto(InputWorkspace='binned2',OutputWorkspace='hk0',Start=[0,0,25,0],End=[301,501,26,11])
SaveMD(InputWorkspace='hk0',Filename='/SNS/users/rwp/benzil/temp_deps2_hk0.nxs')





# #######################################
#Change axis

# fake temperature number
DeleteWorkspace('results3')
for n, r in enumerate(runs):
        filename='/SNS/CORELLI/IPTS-15526/nexus/CORELLI_'+str(r)+'.nxs.h5'
        name='COR_'+str(r)
        print 'Loading run number:'+ str(r)
        dataR=LoadEventNexus(Filename=filename)
        AddSampleLog(dataR,LogName='number',LogText=str(n),LogType='Number',NumberType='Double')
        LoadInstrument(Workspace= dataR, Filename='/SNS/CORELLI/shared/Calibration/CORELLI_Definition_cal_20160310.xml',RewriteSpectraMap=False)
        MaskBTP(workspace=dataR,Bank='69-72')
        dataR=ConvertUnits(dataR,Target="Momentum",EMode="Elastic")
        dataR=CropWorkspace(dataR,XMin=2.5,XMax=10)
        SetGoniometer(dataR,Axis0="BL9:Mot:Sample:Axis1,0,1,0,1") 
        LoadIsawUB(InputWorkspace=dataR,Filename="/SNS/users/rwp/benzil/benzil_Hexagonal.mat")
        ConvertToMD(InputWorkspace=dataR,OutputWorkspace='results3',QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',OtherDimensions='number',
                       QConversionScales='HKL',LorentzCorrection='0',MinValues='-8.1,2.1,-5.1,0',MaxValues='-2.1,10.1,5.1,11',
                       OverwriteExisting=0)


BinMD(InputWorkspace='results3',
            OutputWorkspace='binned3',
            AlignedDim0="[H,0,0],-8.01,-2.01,301",
            AlignedDim1="[0,K,0],1.99,10.01,401",
            AlignedDim2="[0,0,L],-5.1,5.1,51",
            AlignedDim3="number,0,11,11")

SaveMD(InputWorkspace='binned2',Filename='/SNS/users/rwp/benzil/temp_deps_flat.nxs')

SliceMDHisto(InputWorkspace='binned2',OutputWorkspace='hk0',Start=[0,0,25,0],End=[301,501,26,11])
SaveMD(InputWorkspace='hk0',Filename='/SNS/users/rwp/benzil/temp_deps_flat_hk0.nxs')
