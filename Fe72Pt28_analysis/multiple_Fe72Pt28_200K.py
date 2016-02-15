from mantid.simpleapi import *

outputdir="/SNS/users/rwp/Fe72Pt28_analysis/"
van=Load("CORELLI_1946")
MaskBTP(van,Pixel="1-10,247-256")
MaskBTP(van,Bank="12",Tube="5-8") 
MaskBTP(van,Bank="45",Tube="16") 
MaskBTP(van,Bank="59",Tube="8") 
data1=ChangeBinOffset(van,Offset=500,IndexMin=237568,IndexMax=249855)
DeleteWorkspace(van)
van=ChangeBinOffset(data1,Offset=500,IndexMin=36864,IndexMax=53247)
van=ConvertUnits(van,Target="Momentum",EMode="Elastic")
van=CropWorkspace(van,XMin=2.5,XMax=10)

data=Load("CORELLI_2168:2199")
MaskBTP(data,Pixel="1-10,247-256")
MaskBTP(data,Bank="12",Tube="5-8") 
MaskBTP(data,Bank="45",Tube="16") 
MaskBTP(data,Bank="59",Tube="8") 
data1=ChangeBinOffset(data,Offset=500,IndexMin=36864,IndexMax=40959)
DeleteWorkspace(data)
data2=ChangeBinOffset(data1,Offset=500,IndexMin=45056,IndexMax=53247)
DeleteWorkspace(data1)
data3=ChangeBinOffset(data2,Offset=500,IndexMin=163840,IndexMax=167935)
DeleteWorkspace(data2)
data4=ChangeBinOffset(data3,Offset=500,IndexMin=237568,IndexMax=249855)
DeleteWorkspace(data3)
data2=ConvertUnits(data4,Target="Momentum",EMode="Elastic")
DeleteWorkspace(data4)
data3=CropWorkspace(data2,XMin=2.5,XMax=10)
DeleteWorkspace(data2)
SetGoniometer(data3,Axis0="BL9:SampleRotation:phi,0,1,0,1")
mdqsampparts=ConvertToMD(data3,QDimensions="Q3D",dEAnalysisMode="Elastic",Q3DFrames="Q_sample",LorentzCorrection=1,MinValues="-10,-10,-10",MaxValues="10,10,10")
mdqsamp=MergeMD(mdqsampparts)

#van=mtd['van']
#data3=mtd['data3']
SetGoniometer(data3,Axis0="BL9:SampleRotation:phi,0,1,0,1")
LoadIsawUB(InputWorkspace=van,Filename=outputdir+"Fe72Pt28UB_100K.mat")
CopySample(InputWorkspace=van,OutputWorkspace=data3,CopyName=0,CopyMaterial=0,CopyEnvironment=0,CopyShape=0,CopyLattice=1)

for di in data3:
    d3di=ConvertToMD(InputWorkspace=di,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
        QConversionScales='HKL',LorentzCorrection='0', MinValues='-5.05,-10.1,-2.525',MaxValues='5.05,0,2.525')
    dataRebinned=BinMD(InputWorkspace=d3di,AxisAligned='0',
        BasisVector0='[H,0,0],(r.l.u.),1,0,0',BasisVector1='[0,K,0],(r.l.u.),0,1,0',
        BasisVector2='[0,0,L],(r.l.u.),0,0,1',OutputExtents='-5.05,5.05,-10.1,0,-2.025,2.025',
        OutputBins='601,601,301',Parallel='1')   
    if mtd.doesExist('dataHisto'):
        dataHisto=dataHisto+dataRebinned
    else:
        dataHisto=CloneMDWorkspace(dataRebinned)
    runObj=di.run()
    vani=van*runObj.getProtonCharge()
    ang=runObj['BL9:SampleRotation:phi'].getStatistics().mean
    SetGoniometer(Workspace=vani,Axis0=str(ang)+",0,1,0,1")
    van3di=ConvertToMD(InputWorkspace=vani,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
        QConversionScales='HKL',LorentzCorrection='0', MinValues='-5.05,-10.1,-2.525',MaxValues='5.05,0,2.525')
    van3drebinned=BinMD(InputWorkspace=van3di,AxisAligned='0',
        BasisVector0='[H,0,0],(r.l.u.),1,0,0',BasisVector1='[0,K,0],(r.l.u.),0,1,0',
        BasisVector2='[0,0,L],(r.l.u.),0,0,1',OutputExtents='-5.05,5.05,-10.1,0,-2.025,2.025',
        OutputBins='601,601,301',Parallel='1')   
    if mtd.doesExist('vanHisto'):
        vanHisto=vanHisto+van3drebinned
    else:
        vanHisto=CloneMDWorkspace(van3drebinned)
        
SaveMD(vanHisto,outputdir+"VanHisto_200K.nxs")
SaveMD(dataHisto,outputdir+"DataHisto_200K.nxs")         
norm=dataHisto/vanHisto
SaveMD(norm,outputdir+"NormlizedHisto_200K.nxs")         
