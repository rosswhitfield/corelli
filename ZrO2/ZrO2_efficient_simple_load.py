outputdir="/SNS/CORELLI/IPTS-12008/shared/2015-0411-ZrO2/"
LoadNexus(Filename=outputdir+'SolidAngle.nxs', OutputWorkspace='sa')
LoadNexus(Filename=outputdir+'Spectrum.nxs', OutputWorkspace='flux')

runs=range(8193,8235)
for r in runs:
        filename='/SNS/CORELLI/IPTS-12008/nexus/CORELLI_'+str(r)+'.nxs.h5'
        ows='COR_'+str(r)
        dataR=LoadEventNexus(Filename=filename)
        LoadInstrument(Workspace=dataR, MonitorList='-1,-2,-3', InstrumentName='CORELLI')
        dataR=CorelliCrossCorrelate(dataR, TimingOffset=56000)
        MaskDetectors(Workspace=dataR,MaskedWorkspace=van)
        dataR=ConvertUnits(dataR,Target="Momentum",EMode="Elastic")
        dataR=CropWorkspace(dataR,XMin=2.5,XMax=10)
        SetGoniometer(dataR,Axis0="BL9:Mot:Sample:Axis1,0,1,0,1") 
        LoadIsawUB(InputWorkspace=dataR,Filename=outputdir+"ZrO2-UB.mat")
        md=ConvertToMD(InputWorkspace=dataR,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
                       QConversionScales='HKL',LorentzCorrection='1',Uproj='1,0,0',Vproj='0,1,0',Wproj='0,0,1',MinValues='-10.5,-10.5,-10.5',MaxValues='10.5,10.5,10.5')
        a,b=MDNormSCD(InputWorkspace='md',FluxWorkspace='flux',SolidAngleWorkspace='sa',
                      AlignedDim0="[H,0,0], -10.5,10.5,700",
                      AlignedDim1="[0,K,0],-10.5,10.5,700",
                      AlignedDim2="[0,0,L],-10.5,10.5,700")
        if mtd.doesExist('dataMD'):
                dataMD=dataMD+a
        else:
                dataMD=CloneMDWorkspace(a)
        if mtd.doesExist('normMD'):
                normMD=normMD+b
        else:
                normMD=CloneMDWorkspace(b)
                
normData_CC_300K=dataMD/normMD

#SaveMD(dataMD,Filename=outputdir+'ZrO2_CC_Data_300K.h5')
#SaveMD(normMD,Filename=outputdir+'ZrO2_CC_Norm_300K.h5')
#SaveMD(normData_CC_300K,Filename=outputdir+'ZrO2_CC_Normalized_300K.h5')
