outputdir="/SNS/CORELLI/IPTS-12310/shared/2015-0309-Ni-Xtal/"
LoadEventNexus(Filename='/SNS/CORELLI/IPTS-13300/nexus/CORELLI_7080.nxs.h5',outputWorkspace='van')
LoadInstrument(Workspace='van', InstrumentName='CORELLI')
MaskBTP(Workspace='van',Pixel="1-10,247-256")
MaskBTP(Workspace='van',Bank="49",Tube="1")
MaskBTP(Workspace='van',Bank="54",Tube="1")
MaskBTP(Workspace='van',Bank="72",Tube="13")
MaskBTP(Workspace='van',Bank="74",Tube="2")
#MaskBTP(Workspace='van',Bank="1-6,14-30,62-71,73,81-91")
MaskBTP(Workspace='van',Bank="1-6,14-30,62-91")

# T=280K
runs=range(6140,6145)
toMerge=[]
for r in runs:
	filename='/SNS/CORELLI/IPTS-12310/nexus/CORELLI_'+str(r)+'.nxs.h5'
	ows='COR_'+str(r)
	toMerge.append(ows)
	LoadEventNexus(Filename=filename, OutputWorkspace=ows)

data=GroupWorkspaces(toMerge)

van=mtd['van']

LoadInstrument(Workspace=data, InstrumentName='CORELLI')
data=CorelliCrossCorrelate(data, TimingOffset=56000)

MaskDetectors(data,MaskedWorkspace=van)

data2=ConvertUnits(data,Target="Momentum",EMode="Elastic")
#DeleteWorkspace(data)
data3=CropWorkspace(data2,XMin=2.5,XMax=10)
DeleteWorkspace(data2)
#data4=ConvertUnits(data,Target="dSpacing",EMode="Elastic")
#RebinParams='0.5,0.01,6'
#data4=rebin(data4,Params='0.5,0.01,6')

van=ConvertUnits(van,Target="Momentum",EMode="Elastic")
van=CropWorkspace(van,XMin=2.5,XMax=10)
van=Rebin(InputWorkspace=van,Params='2.5,10,10')
sa=Rebin(InputWorkspace=van,Params='2.5,10,10',PreserveEvents='0')
flux=SumSpectra(van)
flux=Rebin(InputWorkspace=flux,Params='2.5,10,10')
flux=CompressEvents(flux,1e-5)
flux/=flux.readY(0)[0]
flux=IntegrateFlux(flux)
#SaveNexus(flux,outputdir+'Spectrum.nxs')
#SaveNexus(sa,outputdir+'SolidAngle.nxs')
	
SetGoniometer(data3,Axis0="BL9:Mot:Sample:Axis5,0,1,0,1")
#mdqsampparts=ConvertToMD(data,QDimensions="Q3D",dEAnalysisMode="Elastic",Q3DFrames="Q_sample",LorentzCorrection=1,MinValues="-15,-15,-15",MaxValues="15,15,15",Uproj='1,0,0',Vproj='0,1,0',Wproj='0,0,1')
#mdqsamp=MergeMD(mdqsampparts)

LoadIsawUB(InputWorkspace=data3,Filename=outputdir+"Ni-Xtal-150309-UB.mat")
#md=ConvertToMD(InputWorkspace=data,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
#        QConversionScales='HKL',LorentzCorrection='0', MinValues='-10.1,-10.1,-10.1',MaxValues='10.1,10.1,10.1')
#mdmerged=MergeMD(md)

mdrun=ConvertToMD(InputWorkspace=data3,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
        QConversionScales='HKL',LorentzCorrection='1',Uproj='1,0,0',Vproj='0,1,0',Wproj='0,0,1',MinValues='-12.5,-12.5,-12.5',MaxValues='12.5,12.5,12.5')
#mdrunmerged=MergeMD(mdrun)

mdrun=mtd['mdrun']
a,b=MDNormSCD(InputWorkspace='mdrun',FluxWorkspace='flux',SolidAngleWorkspace='sa',
	AlignedDim0="[H,0,0],-1.5,8.5,501",
	AlignedDim1="[0,K,0],-2.5,2.5,101",
	AlignedDim2="[0,0,L],-0.5,9.5,501")

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
normalized006K=dataMD/normMD
