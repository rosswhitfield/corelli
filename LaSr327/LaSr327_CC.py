outputdir="/SNS/CORELLI/IPTS-13252/shared/20150218-LaSr327/"
LoadNexus(Filename=outputdir+'Spectrum.nxs', OutputWorkspace='flux')
LoadNexus(Filename=outputdir+'SolidAngle.nxs', OutputWorkspace='sa')

sa=mtd['sa']
flux=mtd['flux']
#runs=range(4938,4949)
#T=100K
#runs=range(4984,5012,2)
runs=range(5019,5020)
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
data2=ConvertUnits(data_CC,Target="Momentum",EMode="Elastic")
data4=ConvertUnits(data_CC,Target="dSpacing",EMode="Elastic")
SetGoniometer(data2,Axis0="BL9:Mot:Sample:Axis5,0,1,0,1")
SetGoniometer(data4,Axis0="BL9:Mot:Sample:Axis5,0,1,0,1")
#DeleteWorkspace(data)
data3=CropWorkspace(data2,XMin=2.5,XMax=10)
#DeleteWorkspace(data2)
mdqsampparts=ConvertToMD(data3,QDimensions="Q3D",dEAnalysisMode="Elastic",Q3DFrames="Q_sample",LorentzCorrection=1,MinValues="-15,-15,-15",MaxValues="15,15,15",Uproj='1,0,0',Vproj='0,1,0',Wproj='0,0,1')#
mdqsamp=MergeMD(mdqsampparts)

LoadIsawUB(InputWorkspace=data2,Filename=outputdir+"LaSr327-UB-150K.mat")
md_cc=ConvertToMD(InputWorkspace=data2,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
        QConversionScales='HKL',LorentzCorrection='0', MinValues='-10.1,-10.1,-0.1',MaxValues='10.1,10.1,45.1')
mdmerged_CC=MergeMD(md)

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
