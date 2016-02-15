outputdir="/SNS/CORELLI/IPTS-13252/shared/"
LoadNexus(Filename=outputdir+'Spectrum.nxs', OutputWorkspace='flux')
LoadNexus(Filename=outputdir+'SolidAngle.nxs', OutputWorkspace='sa')

sa=mtd['sa']
flux=mtd['flux']
#runs=range(4938,4949)
#T=100K
#runs=range(4953,4960)
runs=range(4959,4960)+range(4975,497)
#T=6K
#runs=range(4960,4967)
#T=150K
#runs=range(4967,4974)
toMerge=[]
for r in runs:
	filename='/SNS/CORELLI/IPTS-13252/nexus/CORELLI_'+str(r)+'.nxs.h5'
	ows='COR_'+str(r)
	toMerge.append(ows)
	LoadEventNexus(Filename=filename,outputWorkspace=ows)
data=GroupWorkspaces(toMerge)

data=mtd['data']
MaskBTP(data,Pixel="1-10,247-256")
MaskBTP(data,Bank="45",Tube="15")
MaskBTP(data,Bank="49",Tube="1")
# mask all banks that there is no module installed 
MaskBTP(data,Bank="1-6,14-30,62-73,77-91")
#data2=ConvertUnits(data,Target="Momentum",EMode="Elastic")
data4=ConvertUnits(data,Target="dSpacing",EMode="Elastic")
SetGoniometer(data4,Axis0="BL9:Mot:Sample:Axis5,0,1,0,1")
#DeleteWorkspace(data)
#data3=CropWorkspace(data2,XMin=2.5,XMax=10)
#DeleteWorkspace(data2)
SetGoniometer(data4,Axis0="BL9:Mot:Sample:Axis5,0,1,0,1")
#mdqsampparts=ConvertToMD(data3,QDimensions="Q3D",dEAnalysisMode="Elastic",Q3DFrames="Q_sample",LorentzCorrection=1,MinValues="-15,-15,-15",MaxValues="15,15,15",Uproj='1,0,0',Vproj='0,1,0',Wproj='0,0,1')#
#mdqsamp=MergeMD(mdqsampparts)

LoadIsawUB(InputWorkspace=data4,Filename=outputdir+"BaFe2As2-UB.mat")
md=ConvertToMD(InputWorkspace=data4,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
        QConversionScales='HKL',LorentzCorrection='0', MinValues='-10.1,-10.1,-0.1',MaxValues='10.1,10.1,45.1')
mdmerged=MergeMD(md)

a,b=MDNormSCD(InputWorkspace='md',FluxWorkspace='flux',SolidAngleWorkspace='sa',
	AlignedDim0="[H,,0],-10.1,10.1,401",
        AlignedDim1="[0,K,0],-5.1,5.1,401",
        AlignedDim2="[0,0,L],-10.1,10.1,401")
	
if type(a)	==mantid.api._api.WorkspaceGroup:
	dataMD=CloneMDWorkspace(a[0])
	normMD=CloneMDWorkspace(b[0])
	for i in range(1,a.getNumberOfEntries()):
		dataMD+=a[i]
		normMD+=b[i]

from numpy import *
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
normalized=dataMD/normMD
