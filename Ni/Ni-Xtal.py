outputdir="/SNS/CORELLI/IPTS-12008/shared/Ni-Xtal-feng/"
van=Load(Filename='/SNS/CORELLI/IPTS-12008/nexus/CORELLI_2434.nxs.h5')
van=mtd['van']
MaskBTP(van,Pixel="1-10,247-256")
MaskBTP(van,Bank="49",Tube="1")
MaskBTP(van,Bank="1-9,14-30,62-71,75-91")
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

sa=mtd['sa']
flux=mtd['flux']
runs=range(2977,2983)
runs=range(2977,2983)
toMerge=[]
for r in runs:
	filename='/SNS/CORELLI/IPTS-12008/nexus/CORELLI_'+str(r)+'.nxs.h5'
	ows='COR_'+str(r)
	toMerge.append(ows)
	LoadEventNexus(Filename=filename,outputWorkspace=ows)
data=GroupWorkspaces(toMerge)

MaskBTP(data,Pixel="1-10,247-256")
MaskBTP(data,Bank="49",Tube="1")
# mask all banks that there is no module installed 
MaskBTP(data,Bank="1-9,14-30,62-71,75-91")
data2=ConvertUnits(data,Target="Momentum",EMode="Elastic")
#DeleteWorkspace(data)
data3=CropWorkspace(data2,XMin=2.5,XMax=10)
#DeleteWorkspace(data2)
#SetGoniometer(data3,Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",Axis1="BL9:Mot:Sample:Axis3,0,0,1,-1",Axis2="BL9:Mot:Sample:Axis2,0,1,0,1")
SetGoniometer(data3,Axis0="omega,0,1,0,1",Axis1="chi,0,0,1,1",Axis2="phi,0,1,0,1")
MaskBTP(data3,Bank="1-9,14-30,62-71,75-91")
mdqsampparts=ConvertToMD(data3,QDimensions="Q3D",dEAnalysisMode="Elastic",Q3DFrames="Q_sample",LorentzCorrection=1,MinValues="-15,-15,-15",MaxValues="15,15,15",Uproj='1,0,0',Vproj='0,1,0',Wproj='0,0,1')
mdqsamp=MergeMD(mdqsampparts)

data3=mtd['data3']
LoadIsawUB(InputWorkspace=data3,Filename="/SNS/users/rwp/Ni-Xtal_2axis.mat")
md=ConvertToMD(InputWorkspace=data3,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
        QConversionScales='HKL',LorentzCorrection='0', MinValues='-10.1,-5.1,-10.1',MaxValues='10.1,5.1,10.1')
mdmerged=MergeMD(md)

