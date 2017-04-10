from mantid.simpleapi import *
from mantid.geometry import SymmetryOperationFactory
import numpy as np

# Get UBs
LoadEmptyInstrument(Filename='/SNS/CORELLI/shared/Calibration/CORELLI_Definition_cal_20160310.xml', OutputWorkspace='ub')
LoadIsawUB(InputWorkspace='ub', Filename="/SNS/users/rwp/benzil/benzil_Hexagonal.mat")
ub=mtd['ub'].sample().getOrientedLattice().getUB()
print "Starting UB :"
print ub

symOps = SymmetryOperationFactory.createSymOps("x,y,z; -y,x-y,z+1/3; -x+y,-x,z+2/3; y,x,-z; x-y,-y,-z+2/3; -x,-x+y,-z+1/3")
ub_list=[]
for sym in symOps:
    UBtrans = np.zeros((3,3))
    UBtrans[0] = sym.transformHKL([1,0,0])
    UBtrans[1] = sym.transformHKL([0,1,0])
    UBtrans[2] = sym.transformHKL([0,0,1])
    UBtrans=np.matrix(UBtrans.T)
    new_ub = ub*UBtrans
    print "Symmetry transform for "+sym.getIdentifier()
    print UBtrans
    print "New UB:"
    print new_ub
    ub_list.append(new_ub)

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
bkg=ConvertUnits(bkg,Target="Momentum",EMode="Elastic")
bkg=CropWorkspace(bkg,XMin=2.5,XMax=10)

#mesh scan at 100K, 20 mins/angle, combined both 5mins and 20 mins at 100K, additional 30 mins.
#runs = range(29715,29755)+range(29589,29625)+range(29533,29536)+range(29556,29589)

#runs = range(29533,29536)+range(29556,29589)
#runs = [29588]

#mesh scan at 300K, 70 mins/angle
runs=range(29782,29818)

if mtd.doesExist('normMD'):
    DeleteWorkspace('normMD')
if mtd.doesExist('dataMD'):
    DeleteWorkspace('dataMD')
if mtd.doesExist('bkgMD'):
    DeleteWorkspace('bkgMD')
if mtd.doesExist('bkg_normMD'):
    DeleteWorkspace('bkg_normMD')

for r in runs:
        filename='/SNS/CORELLI/IPTS-15526/nexus/CORELLI_'+str(r)+'.nxs.h5'
        print 'Loading run number:'+ str(r)
        dataR=LoadEventNexus(Filename=filename)
        LoadInstrument(Workspace= dataR, Filename='/SNS/CORELLI/shared/Calibration/CORELLI_Definition_cal_20160310.xml',RewriteSpectraMap=False)
        MaskDetectors(Workspace=dataR,MaskedWorkspace='sa')
        pc_data=sum(dataR.getRun()['proton_charge'].value)
        print 'pc_data=:'+str(pc_data)
        #dataR=dataR - bkg*pc_data/pc_bkg
        dataR=ConvertUnits(dataR,Target="Momentum",EMode="Elastic")
        dataR=CropWorkspace(dataR,XMin=2.5,XMax=10)
        SetGoniometer(dataR,Axis0="BL9:Mot:Sample:Axis1,0,1,0,1") 
        bkg.run().getGoniometer().setR(dataR.run().getGoniometer().getR()) # Set background Goniometer to be the same as data
        for ub in ub_list:
            print "using UB:"
            print ub
            SetUB(dataR, UB=ub)
            SetUB(bkg, UB=ub)
            md=ConvertToMD(InputWorkspace=dataR,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
                           QConversionScales='HKL',LorentzCorrection='0',MinValues='-10.1,-10.1,-10.1',MaxValues='10.1,10.1,10.1')
            bkg_md=ConvertToMD(InputWorkspace=bkg,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
                           QConversionScales='HKL',LorentzCorrection='0',MinValues='-10.1,-10.1,-10.1',MaxValues='10.1,10.1,10.1')
            a1,b1=MDNormSCD(InputWorkspace='md',FluxWorkspace='flux',SolidAngleWorkspace='sa',
                            AlignedDim0="[H,0,0],-10.02,10.02,501",
                            AlignedDim1="[0,K,0],-10.02,10.02,501",
                            AlignedDim2="[0,0,L],-10.02,10.02,501")
            c1=BinMD(InputWorkspace='bkg_md',
                     AlignedDim0="[H,0,0],-10.02,10.02,501",
                     AlignedDim1="[0,K,0],-10.02,10.02,501",
                     AlignedDim2="[0,0,L],-10.02,10.02,501")
            if mtd.doesExist('dataMD'):
                dataMD=dataMD+a1
            else:
                dataMD=CloneMDWorkspace(a1)
            if mtd.doesExist('normMD'):
                normMD=normMD+b1
            else:
                normMD=CloneMDWorkspace(b1)
            if mtd.doesExist('bkgMD'):
                bkgMD=bkgMD+c1
            else:
                bkgMD=CloneMDWorkspace(c1)
            if mtd.doesExist('bkg_normMD'):
                bkg_normMD=bkg_normMD+b1*pc_bkg/pc_data
            else:
                bkg_normMD=CloneMDWorkspace(b1*pc_bkg/pc_data)
normData=dataMD/normMD
bkgNormData=bkgMD/bkg_normMD
bkg_subtract = normData-bkgNormData
outputdir="/SNS/users/rwp/benzil/"
SaveMD(Inputworkspace='dataMD',Filename=outputdir+'benzil_300K_data_sym_All_noCC_flat2.nxs')
SaveMD(Inputworkspace='normMD',Filename=outputdir+'benzil_300K_norm_sym_All_noCC_flat2.nxs')
SaveMD(Inputworkspace='normData',Filename=outputdir+'benzil_300K_normData_sym_All_noCC_flat2.nxs')
SaveMD(Inputworkspace='bkgMD',Filename=outputdir+'benzil_300K_bkg_sym_All_noCC_flat2.nxs')
SaveMD(Inputworkspace='bkg_normMD',Filename=outputdir+'benzil_300K_bkg_norm_sym_All_noCC_flat2.nxs')
SaveMD(Inputworkspace='bkgNormData',Filename=outputdir+'benzil_300K_bkgNormData_sym_All_noCC_flat2.nxs')
SaveMD(Inputworkspace='bkg_subtract',Filename=outputdir+'benzil_300K_bkg_subtract_sym_All_noCC_flat2.nxs')
