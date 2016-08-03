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

for r in runs:
        filename='/SNS/CORELLI/IPTS-15526/nexus/CORELLI_'+str(r)+'.nxs.h5'
        print 'Loading run number:'+ str(r)
        dataR=LoadEventNexus(Filename=filename)
        LoadInstrument(Workspace= dataR, Filename='/SNS/CORELLI/shared/Calibration/CORELLI_Definition_cal_20160310.xml',RewriteSpectraMap=False)
        MaskDetectors(Workspace=dataR,MaskedWorkspace='sa')
        #pc_data=sum(dataR.getRun()['proton_charge'].value)
        #print 'pc_data=:'+str(pc_data)
        #dataR=dataR - bkg*pc_data/pc_bkg
        dataR=ConvertUnits(dataR,Target="Momentum",EMode="Elastic")
        dataR=CropWorkspace(dataR,XMin=2.5,XMax=10)
        SetGoniometer(dataR,Axis0="BL9:Mot:Sample:Axis1,0,1,0,1") 
        #LoadIsawUB(InputWorkspace=dataR,Filename="/SNS/users/rwp/benzil/benzil_Hexagonal.mat")
        for sym in range(6):
            ub=ub_list[sym]
            print "using UB:"
            print ub
            SetUB(dataR, UB=ub)
            md=ConvertToMD(InputWorkspace=dataR,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
                           QConversionScales='HKL',LorentzCorrection='0',Uproj='1,1,0',Vproj='1,-1,0',Wproj='0,0,1',MinValues='-10.1,-17.6,-5.1',MaxValues='10.1,17.6,5.1')
            a1,b1=MDNormSCD(InputWorkspace='md',FluxWorkspace='flux',SolidAngleWorkspace='sa',
                            AlignedDim0="[H,H,0],-10.1,10.1,401",
                            AlignedDim1="[H,-H,0],-17.6,17.6,401",
                            AlignedDim2="[0,0,L],-5.1,5.1,51")
            if mtd.doesExist('dataMD'+str(sym)):
                PlusMD(LHSWorkspace='dataMD'+str(sym),RHSWorkspace=a1,OutputWorkspace='dataMD'+str(sym))
            else:
                CloneMDWorkspace(InputWorkspace=a1,OutputWorkspace='dataMD'+str(sym))
            if mtd.doesExist('normMD'+str(sym)):
                PlusMD(LHSWorkspace='normMD'+str(sym),RHSWorkspace=b1,OutputWorkspace='normMD'+str(sym))
            else:
                CloneMDWorkspace(InputWorkspace=b1,OutputWorkspace='normMD'+str(sym))

for sym in range(6):
    DivideMD(LHSWorkspace='dataMD'+str(sym),RHSWorkspace='normMD'+str(sym),OutputWorkspace='normData'+str(sym))
    SaveMD(Inputworkspace='dataMD'+str(sym),Filename='/SNS/users/rwp/benzil/benzil_300K_data_sym_part'+str(sym)+'_All_noCC.nxs')
    SaveMD(Inputworkspace='normMD'+str(sym),Filename='/SNS/users/rwp/benzil/benzil_300K_norm_sym_part'+str(sym)+'_All_noCC.nxs')
    SaveMD(Inputworkspace='normData'+str(sym),Filename='/SNS/users/rwp/benzil/benzil_300K_normData_sym_part'+str(sym)+'_All_noCC.nxs')
