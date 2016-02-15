from numpy import *
outputdir="/SNS/users/rwp/ZrO2-Ca-Xtal/"
van=Load("CORELLI_562")
MaskBTP(van,Pixel="1-10,247-256")
MaskBTP(van,Bank="63-91") 
MaskBTP(van,Bank="45",Tube="15") 
van=ChangeBinOffset(van,Offset=500,IndexMin=237568,IndexMax=249855)
van=ConvertUnits(van,Target="Momentum",EMode="Elastic")
van=CropWorkspace(van,XMin=2.5,XMax=10)

#van=mtd['van']
van=Rebin(InputWorkspace=van,Params='2.5,10,10')
sa=Rebin(InputWorkspace=van,Params='2.5,10,10',PreserveEvents='0')
flux=SumSpectra(van)
flux=Rebin(InputWorkspace=flux,Params='2.5,10,10')
flux=CompressEvents(flux,1e-5)
flux/=flux.readY(0)[0]
flux=IntegrateFlux(flux)

data=Load("CORELLI_637")
MaskBTP(data,Pixel="1-10,247-256")
MaskBTP(data,Bank="63-91") 
MaskBTP(data,Bank="45",Tube="15") 
data1=ChangeBinOffset(data,Offset=500,IndexMin=237568,IndexMax=249855)
DeleteWorkspace(data)
data2=ConvertUnits(data1,Target="Momentum",EMode="Elastic")
DeleteWorkspace(data1)
data3=CropWorkspace(data2,XMin=2.5,XMax=10)
DeleteWorkspace(data2)
SetGoniometer(data3,Axis0="0,0,1,0,1")
mdqsampparts=ConvertToMD(data3,QDimensions="Q3D",dEAnalysisMode="Elastic",Q3DFrames="Q_sample",LorentzCorrection=1,MinValues="-10,-10,-10",MaxValues="10,10,10",Uproj='1,0,0',Vproj='0,1,0',Wproj='0,0,1')

#van=mtd['van']
#data3=mtd['data3']
SetGoniometer(data3,Axis0="0,0,1,0,1")
LoadIsawUB(InputWorkspace=data3,Filename=outputdir+"ZrO2-Xtal-UB-run637.mat")

md=ConvertToMD(InputWorkspace=data3,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
        QConversionScales='HKL',LorentzCorrection='0', MinValues='-10.1,-10.1,-10.1',MaxValues='10.1,10.1,10.1')

a,b=MDNormSXD(InputWorkspace='md',FluxWorkspace='flux',SolidAngleWorkspace='sa',
	#AlignedDim0="[0,K,0],-1.5,6,401",
	#AlignedDim1="[0,0,L],-3.0,0.,301",
	#AlignedDim2="[H,0,0],2.9,3.1,1")
	AlignedDim0="[H,0,0],0,10,201",
        AlignedDim1="[0,K,0],-1,9,201",
        AlignedDim2="[0,0,L],-10,0,201")
	
#if type(a)	==mantid.api._api.WorkspaceGroup:
#	dataMD=CloneMDWorkspace(a[0])
#	normMD=CloneMDWorkspace(b[0])
#	for i in range(1,a.getNumberOfEntries()):
#		dataMD+=a[i]
#		normMD+=b[i]
#normalized=DivideMD(dataMD,normMD)

aa=a.getSignalArray()
bb=b.getSignalArray()
aashape=aa.shape
aa=reshape(aa,(-1))
bb=reshape(bb,(-1))
xaa=aa*0
idx1=(aa==0)
idx2=(bb!=0)
xaa[logical_and(idx1,idx2)]=1
aa=xaa+aa
aa=reshape(aa,aashape)
a.setSignalArray(aa)

normalized_hk0_all=a/b
#range=[1e-6,1]
