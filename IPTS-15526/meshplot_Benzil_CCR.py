outputdir="/SNS/CORELLI/IPTS-15526/shared/"

#Quick mesh scan, 5 mins/angle
runs = range(29533,29536)+range(29556,29589)

#mesh scan at 100K, 20 mins/angle
runs = range(29589,29614)

runs = [29589]

toMerge1=[]
toMerge2=[]
BinParm='1.,0.1,15'
UBfile="Benzil_100K_UB.mat"

for r in runs:
    print 'Processing run : %s' %r
    filename='/SNS/CORELLI/IPTS-15526/nexus/CORELLI_'+str(r)+'.nxs.h5'
    ows='COR_'+str(r)
    omd=ows+'_md'
    toMerge1.append(ows)
    toMerge2.append(omd)
    LoadEventNexus(Filename=filename, OutputWorkspace=ows)
    MaskBTP(workspace=ows,Pixel='1-16,241-256')
    #MaskBTP(workspace=ows,Bank='1-17,30-49,63-79')
    #MaskBTP(Workspace=ows,Bank="1-11,17-91")
    owshandle=mtd[ows]
    lrun=owshandle.getRun()
    pclog=lrun.getLogData('proton_charge')
    pc=sum(pclog.value)/1e11
    owshandle /= pc
    print 'the current proton charge :'+ str(pc)
    
    LoadInstrument(Workspace= ows, Filename='/SNS/CORELLI/shared/Calibration/CORELLI_Definition_cal_20160310.xml',RewriteSpectraMap=False)
    ConvertUnits(InputWorkspace=ows, OutputWorkspace=ows, Target='dSpacing')
    Rebin(InputWorkspace=ows, OutputWorkspace=ows, Params=BinParm)
    SetGoniometer(ows,Axis0="BL9:Mot:Sample:Axis1,0,1,0,1")
    LoadIsawUB(InputWorkspace=ows,Filename=outputdir+UBfile)
    ConvertToMD(InputWorkspace=ows,OutputWorkspace=omd,QDimensions='Q3D',dEAnalysisMode='Elastic', 
       Q3DFrames='HKL',Uproj='1,0,0',Vproj='0,0,1',Wproj='0,1,0',
       QConversionScales='HKL',LorentzCorrection='0', MinValues='-15.1,-25.1,-15.1',MaxValues='15.1,25.1,15.1')
data=GroupWorkspaces(toMerge1)
#dataold=GroupWorkspaces(['dataold','data'])
md=GroupWorkspaces(toMerge2)
merged100K=MergeMD(toMerge2)

md6Kold=GroupWorkspaces(['md6K','md6Kold'])
merged6K=MergeMD('md6Kold')
#merged6K=MergeMD(['merged6Kold','merged6K'])

LoadIsawUB(InputWorkspace='data',Filename=outputdir+"Benzil_100K_UB.mat")
ConvertToMD(InputWorkspace='data',OutputWorkspace='md',QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',Uproj='1,1,0',Vproj='1,-1,0',Wproj='0,0,1',
   QConversionScales='HKL',LorentzCorrection='0', MinValues='-15.1,-15.1,-25.1',MaxValues='15.1,15.1,25.1')
merged100K=MergeMD('md')

#data=mtd['data']
mdqsampparts=ConvertToMD(data,QDimensions="Q3D",dEAnalysisMode="Elastic",
Q3DFrames="Q_sample",LorentzCorrection=1,MinValues="-15,-15,-15",MaxValues="15,15,15",Uproj='1,0,0',Vproj='0,1,0',Wproj='0,0,1')
mdqsamp=MergeMD(mdqsampparts)
