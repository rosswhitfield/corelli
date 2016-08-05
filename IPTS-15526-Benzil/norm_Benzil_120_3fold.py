outputdir="/SNS/CORELLI/IPTS-15526/shared/"
LoadNexus(Filename='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs', OutputWorkspace='sa')
LoadNexus(Filename='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs', OutputWorkspace='flux')

#MaskBTP(workspace='sa',Pixel='1-16,241-256')
MaskBTP(workspace='sa',Bank='69-72')


#load in background
bkg=LoadEventNexus('/SNS/CORELLI/IPTS-15796/nexus/CORELLI_28124.nxs.h5')
MaskDetectors(Workspace=bkg,MaskedWorkspace='sa')
pc_bkg=sum(bkg.getRun()['proton_charge'].value)
print 'pc_bkg=:'+str(pc_bkg)

# get differeant UBs
LoadEmptyInstrument(Filename='/SNS/CORELLI/shared/Calibration/CORELLI_Definition_cal_20160310.xml', OutputWorkspace='ub')
LoadIsawUB(InputWorkspace='ub', Filename='/SNS/users/rwp/benzil/benzil_Hexagonal.mat')
ub=mtd['ub'].sample().getOrientedLattice().getUB()
ub_list=[]
print "Starting UB :"
print ub
for angle in range(0,360,120):
     rad = angle* np.pi/180.
     rot = np.matrix([[np.cos(rad), -np.sin(rad), 0],
                      [np.sin(rad), np.cos(rad), 0],
                      [0, 0, 1]])
     new_ub = ub * rot
     print "New UB for angle = "+str(angle)
     print new_ub
     ub_list.append(new_ub)
print ub_list

#mesh scan at 100K, 20 mins/angle, combined both 5mins and 20 mins at 100K
runs = range(29533,29536)+range(29556,29589)+range(29589,29625)

#runs = range(29533,29536)+range(29556,29589)
#runs = [29625]
if mtd.doesExist('normMD'):
    DeleteWorkspace('normMD')
if mtd.doesExist('dataMD'):
    DeleteWorkspace('dataMD')

for r in runs:
        filename='/SNS/CORELLI/IPTS-15526/nexus/CORELLI_'+str(r)+'.nxs.h5'
        print 'Loading run number:'+ str(r)
        dataR=LoadEventNexus(Filename=filename)
        LoadInstrument(Workspace= dataR, Filename='/SNS/CORELLI/shared/Calibration/CORELLI_Definition_cal_20160310.xml',RewriteSpectraMap=False)
        MaskDetectors(Workspace=dataR,MaskedWorkspace='sa')
        pc_data=sum(dataR.getRun()['proton_charge'].value)
        print 'pc_data=:'+str(pc_data)
        dataR=dataR - bkg*pc_data/pc_bkg
        dataR=ConvertUnits(dataR,Target="Momentum",EMode="Elastic")
        dataR=CropWorkspace(dataR,XMin=2.5,XMax=10)
        SetGoniometer(dataR,Axis0="BL9:Mot:Sample:Axis1,0,1,0,1") 
        for ub in ub_list:
            SetUB(dataR, UB=ub)
            md=ConvertToMD(InputWorkspace=dataR,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
                       QConversionScales='HKL',LorentzCorrection='0',Uproj='1,1,0',Vproj='1,-1,0',Wproj='0,0,1',MinValues='-10.1,-7.1,-3.1',MaxValues='10.1,7.1,3.1')
            a1,b1=MDNormSCD(InputWorkspace='md',FluxWorkspace='flux',SolidAngleWorkspace='sa',
                      AlignedDim0="[H,H,0],-10.1,10.1,400",
                      AlignedDim1="[H,-H,0],-7.1,7.1,400",
                      AlignedDim2="[0,0,L],-3.1,3.1,30")
            if mtd.doesExist('dataMD'):
                dataMD=dataMD+a1
            else:
                dataMD=CloneMDWorkspace(a1)
            if mtd.doesExist('normMD'):
                normMD=normMD+b1
            else:
                normMD=CloneMDWorkspace(b1)
normData_100K=dataMD/normMD                
SaveMD(Inputworkspace=dataMD,Filename='/SNS/users/rwp/benzil/benzil_100K_data_hex_3.nxs')
SaveMD(Inputworkspace=normMD,Filename='/SNS/users/rwp/benzil/benzil_100K_norm_hex_3.nxs')
SaveMD(Inputworkspace=normData_100K,Filename='/SNS/users/rwp/benzil/benzil_100K_normData_hex_3.nxs')