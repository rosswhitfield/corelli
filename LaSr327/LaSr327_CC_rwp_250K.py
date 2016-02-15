outputdir="/SNS/CORELLI/IPTS-13252/shared/20150218-LaSr327/"
runs=range(5021,5022)
toMerge=[]
for r in runs:
	filename='/SNS/CORELLI/IPTS-13252/nexus/CORELLI_'+str(r)+'.nxs.h5'
	ows='COR_'+str(r)
	toMerge.append(ows)
	LoadEventNexus(Filename=filename,outputWorkspace=ows)
data=GroupWorkspaces(toMerge)

LoadInstrument(Workspace=data, MonitorList='-1,-2,-3', InstrumentName='CORELLI')
CorelliCrossCorrelate(InputWorkspace='data', OutputWorkspace='data_CC', TimingOffset=56000)

data_CC=mtd['data_CC']
MaskBTP(data_CC,Pixel="1-10,247-256")
MaskBTP(data_CC,Bank="45",Tube="15")
MaskBTP(data_CC,Bank="49",Tube="1")
# mask all banks that there is no module installed 
MaskBTP(data_CC,Bank="1-9,14-30,62-71,75-91")

# mask all banks that there is no module installed 
data2_CC=ConvertUnits(data_CC,Target="Momentum",EMode="Elastic")
SetGoniometer(data2_CC,Axis0="BL9:Mot:Sample:Axis5,0,1,0,1")
#DeleteWorkspace(data)
#data3=CropWorkspace(data2,XMin=2.5,XMax=10)
#DeleteWorkspace(data2)
LoadIsawUB(InputWorkspace=data2_CC,Filename=outputdir+"LaSr327-UB-150K.mat")
md_cc=ConvertToMD(InputWorkspace=data2_CC,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
        QConversionScales='HKL',LorentzCorrection='0', MinValues='-5.1,-5.1,-0.1',MaxValues='5.1,5.1,45.1')
#mdmerged_CC=MergeMD(md_cc)



data=mtd['data']
MaskBTP(data,Pixel="1-10,247-256")
MaskBTP(data,Bank="45",Tube="15")
MaskBTP(data,Bank="49",Tube="1")
MaskBTP(data,Bank="1-6,14-30,62-73,77-91")

# mask all banks that there is no module installed 
data2=ConvertUnits(data,Target="Momentum",EMode="Elastic")
SetGoniometer(data2,Axis0="BL9:Mot:Sample:Axis5,0,1,0,1")
#DeleteWorkspace(data)
#data3=CropWorkspace(data2,XMin=2.5,XMax=10)
#DeleteWorkspace(data2)
LoadIsawUB(InputWorkspace=data2,Filename=outputdir+"LaSr327-UB-150K.mat")
md=ConvertToMD(InputWorkspace=data2,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
        QConversionScales='HKL',LorentzCorrection='0', MinValues='-5.1,-5.1,-0.1',MaxValues='5.1,5.1,45.1')
#mdmerged_CC=MergeMD(md_cc)


