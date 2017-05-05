outputdir="/SNS/CORELLI/IPTS-16617/shared/"
LoadNexus(Filename='/SNS/CORELLI/shared/Vanadium/SolidAngle20161123_cc.nxs', OutputWorkspace='sa')
LoadNexus(Filename='/SNS/CORELLI/shared/Vanadium/Spectrum20161123_cc.nxs', OutputWorkspace='flux')
sa=mtd['sa']
flux=mtd['flux']
#MaskBTP(Workspace='sa',Pixel="1-15,242-256")
#MaskBTP(Workspace='sa',Bank="45",Tube="16")
#MaskBTP(Workspace='sa',Bank="70",Tube="3")
#MaskBTP(Workspace='sa',Bank="73",Tube="13")
#MaskBTP(Workspace='sa',Bank="74",Tube="2")
#MaskBTP(Workspace='sa',Bank="58",Tube="13-16",Pixel="80-130")
#MaskBTP(Workspace='sa',Bank="59",Tube="1-4",Pixel="80-130")
#MaskBTP(Workspace='sa',Bank="1-4,25,29,30,62-65,87,88,91")

#LoadEmptyInstrument(Filename='/SNS/CORELLI/shared/Calibration/CORELLI_Definition_cal_20160310.xml', OutputWorkspace='ub')


#Cu1.8Se, T=300 K
runs = range(38291,38295)

for r in runs:
        print 'Processing run : %s' %r
        filename='/SNS/CORELLI/IPTS-16617/nexus/CORELLI_'+str(r)+'.nxs.h5'
        dataR=LoadEventNexus(Filename=filename)
        LoadInstrument(Workspace= dataR, Filename='/SNS/CORELLI/shared/Calibration/CORELLI_Definition_cal_20160310.xml',RewriteSpectraMap=False)
        dataR=CorelliCrossCorrelate(dataR, TimingOffset=56000)
        #MaskBTP(Workspace='dataR',Pixel="1-15,242-256")
        #MaskBTP(Workspace='dataR',Bank="45",Tube="16")
        #MaskBTP(Workspace='dataR',Bank="70",Tube="3")
        #MaskBTP(Workspace='dataR',Bank="73",Tube="13")
        #MaskBTP(Workspace='dataR',Bank="74",Tube="2")
        #MaskBTP(Workspace='dataR',Bank="58",Tube="13-16",Pixel="80-130")
        #MaskBTP(Workspace='dataR',Bank="59",Tube="1-4",Pixel="80-130")
        #MaskBTP(Workspace='dataR',Bank="1-4,25,29,30,62-65,87,88,91")
        dataR=ConvertUnits(dataR,Target="Momentum",EMode="Elastic")
        dataR=CropWorkspace(dataR,XMin=2.5,XMax=10)
        SetGoniometer(dataR,Axis0="BL9:Mot:Sample:Axis1,0,1,0,1") 
        #LoadEmptyInstrument(Filename='/SNS/CORELLI/shared/Calibration/CORELLI_Definition_cal_20160310.xml', OutputWorkspace='ub')
        LoadIsawUB(InputWorkspace=dataR,Filename=outputdir+"Cu1p8Se/300K/Cu1p8Se_quickUB_300K.mat")
        md=ConvertToMD(InputWorkspace=dataR,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
                       QConversionScales='HKL',LorentzCorrection='0',Uproj='1,0,0',Vproj='0,1,0',Wproj='0,0,1',MinValues='-10.6,-10.6,-10.6',MaxValues='10.6,10.6,10.6')
        a,b=MDNormSCD(InputWorkspace='md',FluxWorkspace='flux',SolidAngleWorkspace='sa',
                      AlignedDim0="[H,0,0],-2.525,2.525,101",
                      AlignedDim1="[0,K,0],-2.525,2.525,101",
                      AlignedDim2="[0,0,L],-2.525,2.525,101")
        if mtd.doesExist('dataMD'):
                dataMD=dataMD+a
        else:
                dataMD=CloneMDWorkspace(a)
        if mtd.doesExist('normMD'):
                normMD=normMD+b
        else:
                normMD=CloneMDWorkspace(b)

normData_Cu1p8Se_300K=dataMD/normMD
SaveMD('normData_','/SNS/users/krogstad/Desktop/newnamehere.nxs')

DeleteWorkspace(dataMD)
DeleteWorkspace(normMD)
DeleteWorkspace(a)
DeleteWorkspace(b)

#T=300 K, applied electric field
runs = range(19558,19559)

for r in runs:
        print 'Processing run : %s' %r
        filename='/SNS/CORELLI/IPTS-16617/nexus/CORELLI_'+str(r)+'.nxs.h5'
        dataR=LoadEventNexus(Filename=filename)
        LoadInstrument(Workspace=dataR , RewriteSpectraMap=False,InstrumentName='CORELLI')
        dataR=CorelliCrossCorrelate(dataR, TimingOffset=56000)
        #MaskBTP(Workspace='dataR',Pixel="1-15,242-256")
        #MaskBTP(Workspace='dataR',Bank="45",Tube="16")
        #MaskBTP(Workspace='dataR',Bank="70",Tube="3")
        #MaskBTP(Workspace='dataR',Bank="73",Tube="13")
        #MaskBTP(Workspace='dataR',Bank="74",Tube="2")
        #MaskBTP(Workspace='dataR',Bank="58",Tube="13-16",Pixel="80-130")
        #MaskBTP(Workspace='dataR',Bank="59",Tube="1-4",Pixel="80-130")
        #MaskBTP(Workspace='dataR',Bank="1-4,25,29,30,62-65,87,88,91")
        dataR=ConvertUnits(dataR,Target="Momentum",EMode="Elastic")
        dataR=CropWorkspace(dataR,XMin=2.5,XMax=10)
        SetGoniometer(dataR,Axis0="BL9:Mot:Sample:Axis1,0,1,0,1") 
        LoadIsawUB(InputWorkspace=dataR,Filename=outputdir+"Cu1p8Se/300K/Cu1p8Se_quickUB_300K.mat")
        md=ConvertToMD(InputWorkspace=dataR,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
                       QConversionScales='HKL',LorentzCorrection='0',Uproj='1,0,0',Vproj='0,1,0',Wproj='0,0,1',MinValues='-3.6,-2.6,-4.6',MaxValues='8.6,8.6,2.6')
        a,b=MDNormSCD(InputWorkspace='md',FluxWorkspace='flux',SolidAngleWorkspace='sa',
                      AlignedDim0="[H,0,0],-3.51,8.51,601",
                      AlignedDim1="[0,K,0],-2.51,8.51,551",
                      AlignedDim2="[0,0,L],-4.51,2.51,351")
        if mtd.doesExist('dataMD'):
                dataMD=dataMD+a
        else:
                dataMD=CloneMDWorkspace(a)
        if mtd.doesExist('normMD'):
                normMD=normMD+b
        else:
                normMD=CloneMDWorkspace(b)
        normData_PMN30PT_Efield=dataMD/normMD

SaveMD('normData_','/SNS/users/krogstad/Desktop/newnamehere.nxs')

DeleteWorkspace(dataMD)
DeleteWorkspace(normMD)
DeleteWorkspace(a)
DeleteWorkspace(b)

#LoadEventNexus(Filename='/SNS/CORELLI/shared/Vanadium/SolidAngle20150825New9.nxs',outputWorkspace='van')
#van=mtd['van']
#MaskBTP(Workspace=van,Pixel="1-10,247-256")
#MaskBTP(Workspace=van,Bank="16",Tube="4")
#MaskBTP(Workspace=van,Bank="54",Tube="1")
#MaskBTP(Workspace=van,Bank="73",Tube="13")
#MaskBTP(Workspace=van,Bank="74",Tube="2")
#MaskBTP(Workspace=van,Bank="87-88")

# cooling from RT
#runs=range(6901,6921)
runs=range(38626,38636)
toMerge=[]
for r in runs:
	filename='/SNS/CORELLI/IPTS-16617/nexus/CORELLI_'+str(r)+'.nxs.h5'
	ows='COR_'+str(r)
	toMerge.append(ows)
	LoadEventNexus(Filename=filename, OutputWorkspace=ows)
    
#MaskBTP(Workspace='COR_'+str(runs[0]),Pixel="1-10,247-256")
#MaskBTP(Workspace='COR_'+str(runs[0]),Bank="49",Tube="1")
#MaskBTP(Workspace='COR_'+str(runs[0]),Bank="54",Tube="1")
#MaskBTP(Workspace='COR_'+str(runs[0]),Bank="72",Tube="13")
#MaskBTP(Workspace='COR_'+str(runs[0]),Bank="74",Tube="2")
#MaskBTP(Workspace='COR_'+str(runs[0]),Bank="1-6,14-30,62-71,73,81-91")
#for r in runs[:-1]:
    #MaskDetectors(Workspace='COR_'+str(r),MaskedWorkspace='COR_'+str(runs[0]))
    #MaskDetectors(Workspace='COR_'+str(r),MaskedWorkspace=van)
data=GroupWorkspaces(toMerge)

#van=ConvertUnits(van,Target="Momentum",EMode="Elastic")
#van=CropWorkspace(van,XMin=2.5,XMax=10)

#van=Rebin(InputWorkspace=van,Params='2.5,10,10')
#sa=Rebin(InputWorkspace=van,Params='2.5,10,10',PreserveEvents='0')
#flux=SumSpectra(van)
#flux=Rebin(InputWorkspace=flux,Params='2.5,10,10')
#flux=CompressEvents(flux,1e-5)
#flux/=flux.readY(0)[0]
#flux=IntegrateFlux(flux)
#SaveNexus(flux,outputdir+'Spectrum.nxs')
#SaveNexus(sa,outputdir+'SolidAngle.nxs')

LoadInstrument(Workspace=data , RewriteSpectraMap=False,InstrumentName='CORELLI')
#data=CorelliCrossCorrelate(data, TimingOffset=56000)
	
SetGoniometer(data,Axis0="BL9:Mot:Sample:Axis1,0,1,0,1")
#mdqsampparts=ConvertToMD(data,QDimensions="Q3D",dEAnalysisMode="Elastic",Q3DFrames="Q_sample",LorentzCorrection=1,MinValues="-15,-15,-15",MaxValues="15,15,15",Uproj='1,0,0',Vproj='0,1,0',Wproj='0,0,1')
#mdqsamp=MergeMD(mdqsampparts)
#data=ConvertUnits(data,Target="dSpacing",EMode="Elastic")
#RebinParams='0.5,0.01,6'
#data=rebin(data,Params='0.5,0.01,6')

LoadIsawUB(InputWorkspace=data,Filename=outputdir+"Cu1p8Se_2nd/Cu1p8Se_UB_rough.mat")
md=ConvertToMD(InputWorkspace=data,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
        QConversionScales='HKL',LorentzCorrection='0', MinValues='-10.1,-10.1,-10.1',MaxValues='10.1,10.1,10.1')
mdmerged=MergeMD(md)

data2=ConvertUnits(data,Target="Momentum",EMode="Elastic")
DeleteWorkspace(data)
data3=CropWorkspace(data2,XMin=2.5,XMax=10)
DeleteWorkspace(data2)

data=ConvertUnits(data,Target="dSpacing",EMode="Elastic")
RebinParams='0.5,0.01,6'
data=rebin(data,Params='0.5,0.01,6')

mdrun=ConvertToMD(InputWorkspace=data2,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
        QConversionScales='HKL',LorentzCorrection='1',Uproj='1,0,0',Vproj='0,1,0',Wproj='0,0,1',MinValues='-3.5,-2.5,-5.5',MaxValues='6.5,7.5,5.5')
mdrunmerged=MergeMD(mdrun)

mdrun=mtd['mdrun']
a,b=MDNormSCD(InputWorkspace='mdrun',FluxWorkspace='flux',SolidAngleWorkspace='sa',
	AlignedDim0="[H,0,0],-8.5,0.5,501",
	AlignedDim1="[0,K,0],-5.0,1.5,401",
	AlignedDim2="[0,0,L],-3.5,3.5,501")

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

SaveMD(Inputworkspace='normData',Filename='/SNS/users/krogstad/Desktop/Cu1p8Se_250K.nxs')