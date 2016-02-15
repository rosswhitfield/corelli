outputdir="/SNS/CORELLI/IPTS-12008/shared/ZrO2-Ca-Xtal-2014-1020/"
van=Load("CORELLI_1946")
MaskBTP(van,Pixel="1-10,247-256")
MaskBTP(van,Bank="12",Tube="5-8")
MaskBTP(van,Bank="45",Tube="16")
MaskBTP(van,Bank="59",Tube="8")
van=ChangeBinOffset(van,Offset=500,IndexMin=237568,IndexMax=249855)
van=ConvertUnits(van,Target="Momentum",EMode="Elastic")
van=CropWorkspace(van,XMin=2.5,XMax=10)

van=Rebin(InputWorkspace=van,Params='2.5,10,10')
sa=Rebin(InputWorkspace=van,Params='2.5,10,10',PreserveEvents='0')
flux=SumSpectra(van)
flux=Rebin(InputWorkspace=flux,Params='2.5,10,10')
flux=CompressEvents(flux,1e-5)
flux/=flux.readY(0)[0]

data=Load("CORELLI_2319:2339")
MaskBTP(data,Pixel="1-10,247-256")
MaskBTP(data,Bank="12",Tube="5-8")
MaskBTP(data,Bank="45",Tube="16")
MaskBTP(data,Bank="59",Tube="8")
data2=ConvertUnits(data,Target="Momentum",EMode="Elastic")
DeleteWorkspace(data)
data3=CropWorkspace(data2,XMin=2.5,XMax=10)
DeleteWorkspace(data2)
SetGoniometer(data3,Axis0="BL9:SampleRotation:phi,0,-1,0,1") 
mdqsampparts=ConvertToMD(data3,QDimensions="Q3D",dEAnalysisMode="Elastic",Q3DFrames="Q_sample",LorentzCorrection=1,MinValues="-10,-10,-10",MaxValues="10,10,10",Uproj='1,0,0',Vproj='0,1,0',Wproj='0,0,1')
mdqsamp=MergeMD(mdqsampparts)

LoadIsawUB(InputWorkspace=data3,Filename=outputdir+"ZrO2-Xtal-UB.mat")

md=ConvertToMD(InputWorkspace=data3,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
        QConversionScales='HKL',LorentzCorrection='0', MinValues='-10.1,-10.1,-10.1',MaxValues='10.1,10.1,10.1')

a,b=SXDMDNorm(InputWorkspace='md',FluxWorkspace='flux',SolidAngleWorkspace='sa',
	AlignedDim0="[H,0,0],-2,10,301",
        AlignedDim1="[0,K,0],-2,10,301",
        AlignedDim2="[0,0,L],-10,10,501")

if type(a)	==mantid.api._api.WorkspaceGroup:
	dataMD=CloneMDWorkspace(a[0])
	normMD=CloneMDWorkspace(b[0])
	for i in range(1,a.getNumberOfEntries()):
		dataMD+=a[i]
		normMD+=b[i]
normalized=DivideMD(dataMD,normMD)

aa=dataMD.getSignalArray()
bb=normMD.getSignalArray()
aashape=aa.shape
aa=reshape(aa,(-1))
bb=reshape(bb,(-1))
xaa=aa*0
idx1=(aa==0)
idx2=(bb!=0)
xaa[logical_and(idx1,idx2)]=1
aa=xaa+aa
aa=reshape(aa,aashape)
dataMD.setSignalArray(aa)
normalized_hk0_all=dataMD/normMD
