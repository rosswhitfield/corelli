outputdir="/SNS/users/rwp/Fe72Pt28_analysis/"

input_string=""
for i in range(2096,2136):
    filename = "CORELLI_"+str(i)
    input_string+=outputdir+filename+".nxs,"

input_string=input_string[:-1]

data=Load(input_string)

MaskBTP(data,Pixel="1-10,247-256")
MaskBTP(data,Bank="12",Tube="5-8") 
MaskBTP(data,Bank="45",Tube="16") 
MaskBTP(data,Bank="59",Tube="8") 
data2=ConvertUnits(data,Target="Momentum",EMode="Elastic")
DeleteWorkspace(data)
data3=CropWorkspace(data2,XMin=2.5,XMax=10)
DeleteWorkspace(data2)
SetGoniometer(data3,Axis0="BL9:SampleRotation:phi,0,1,0,1")
mdqsampparts=ConvertToMD(data3,QDimensions="Q3D",dEAnalysisMode="Elastic",Q3DFrames="Q_sample",LorentzCorrection=1,MinValues="-10,-10,-10",MaxValues="10,10,10")
mdqsamp=MergeMD(mdqsampparts)

SetGoniometer(data3,Axis0="BL9:SampleRotation:phi,0,1,0,1")
#LoadIsawUB(InputWorkspace=van,Filename=outputdir+"Fe72Pt28UB_100K.mat")
#CopySample(InputWorkspace=van,OutputWorkspace=data3,CopyName=0,CopyMaterial=0,CopyEnvironment=0,CopyShape=0,CopyLattice=1)
LoadIsawUB(InputWorkspace=data3,Filename=outputdir+"Fe72Pt28UB_005K.mat")

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

SaveMD(dataHisto,outputdir+"DataHisto_005K_cc.nxs")
vanHisto=LoadMD(outputdir+"VanHisto_005K.nxs")
norm=dataHisto/vanHisto
SaveMD(norm,outputdir+"NormlizedHisto_005K_cc.nxs")         
