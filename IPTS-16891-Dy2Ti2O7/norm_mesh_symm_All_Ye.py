from mantid.simpleapi import *
from mantid.geometry import SymmetryOperationFactory
import numpy as np

# about information on where the data are and where to save
iptsfolder= "/SNS/CORELLI/IPTS-16891/"
outputdir=iptsfolder+"shared/"
nxfiledir=iptsfolder + "nexus/"
ccfiledir = iptsfolder +"shared/autoreduce/"

UBfile = iptsfolder+"shared/DTO_UB_111Vertical.mat"
reducedfile_prefix = "DTO_cc"

LoadNexus(Filename='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs', OutputWorkspace='sa')
LoadNexus(Filename='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs', OutputWorkspace='flux')
MaskBTP(Workspace='sa',Bank="1-30,62-91")
MaskBTP(workspace='sa',Pixel='1-16,200-256') #Mask the magnet
MaskBTP(Workspace='sa',Bank="49",Tube="1")
MaskBTP(Workspace='sa',Bank="54",Tube="1")
MaskBTP(Workspace='sa',Bank="58",Tube="13-16",Pixel="80-130")
MaskBTP(Workspace='sa',Bank="59",Tube="1-4",Pixel="80-130")

# Get UBs
LoadEmptyInstrument(Filename='/SNS/CORELLI/shared/Calibration/CORELLI_Definition_cal_20160310.xml', OutputWorkspace='ub')
LoadIsawUB(InputWorkspace='ub', Filename=UBfile)
ub=mtd['ub'].sample().getOrientedLattice().getUB()
print "Starting UB :"
print ub

#DTO   Fd-3m (227)  general position has 192 symmety operations.
symOps = SymmetryOperationFactory.createSymOps(\
     "x,y,z; -x,-y,z; -x,y,-z; x,-y,-z;\
    z,x,y; z,-x,-y; -z,-x,y; -z,x,-y;\
    y,z,x; -y,z,-x; y,-z,-x; -y,-z,x;\
    y,x,-z; -y,-x,-z; y,-x,z; -y,x,z;\
    x,z,-y; -x,z,y; -x,-z,-y; x,-z,y;\
    z,y,-x; z,-y,x; -z,y,x; -z,-y,-x;\
    -x,-y,-z; x,y,-z; x,-y,z; -x,y,z;\
    -z,-x,-y; -z,x,y; z,x,-y; z,-x,y;\
    -y,-z,-x; y,-z,x; -y,z,x; y,z,-x;\
    -y,-x,z; y,x,z; -y,x,-z; y,-x,-z;\
    -x,-z,y; x,-z,-y; x,z,y; -x,z,-y;\
    -z,-y,x; -z,y,-x; z,-y,-x; z,y,x")


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


#load in background
#bkg=LoadEventNexus('/SNS/CORELLI/IPTS-15796/nexus/CORELLI_28124.nxs.h5')
#bkg=LoadNexus('/SNS/CORELLI/IPTS-15796/shared/autoreduce/CORELLI_28124_elastic.nxs')
#MaskDetectors(Workspace=bkg,MaskedWorkspace='sa')
#pc_bkg=sum(bkg.getRun()['proton_charge'].value)
#print 'pc_bkg=:'+str(pc_bkg)

#T=1.8 K
runs =  range(34599,34635,1)

#T=100 mK
runs =  range(34635,34653,1) 
totalrun = len(runs)
print "Total number of runs %d" %totalrun

if mtd.doesExist('normMD'):
    DeleteWorkspace('normMD')
if mtd.doesExist('dataMD'):
    DeleteWorkspace('dataMD')

#for r in runs:
for index, r in enumerate(runs):
        print index, '      Processing run : %s' %r
        num=0
        print 'Loading run number:'+ str(r)
        #filename='/SNS/CORELLI/IPTS-15526/nexus/CORELLI_'+str(r)+'.nxs.h5'
        #dataR=LoadEventNexus(Filename=filename)
        filename=ccfiledir+'CORELLI_'+str(r)+'_elastic.nxs'
        dataR=LoadNexus(Filename=filename)        
        LoadInstrument(Workspace= dataR, Filename='/SNS/CORELLI/shared/Calibration/CORELLI_Definition_cal_20160310.xml',RewriteSpectraMap=False)
        MaskDetectors(Workspace=dataR,MaskedWorkspace='sa')
        pc_data=sum(dataR.getRun()['proton_charge'].value)
        print 'pc_data=:'+str(pc_data)
        #dataR=dataR - bkg*pc_data/pc_bkg
        # subtract the background if a background file was provided. Please make sure that the data were treated in the same way in terms of proton charge.
        if mtd.doesExist('Bkg'):
            bkg = mtd['Bkg']
            ratio =  pc_data/pc_bkg
            bkg_c = bkg*ratio
            Minus(LHSWorkspace=dataR, RHSWorkspace=bkg_c, OutputWorkspace=dataR)
            
        dataR=ConvertUnits(dataR,Target="Momentum",EMode="Elastic")
        dataR=CropWorkspace(dataR,XMin=2.5,XMax=10)
        SetGoniometer(dataR,Axis0="BL9:Mot:Sample:Axis2,0,1,0,1") 
        LoadIsawUB(InputWorkspace=dataR,Filename=UBfile)
        for ub in ub_list:
        #for index, ub in enumerate(ub_list):
            #print "index, using UB ", (index+1), ":"
            num += 1
            print "Run number"+str(r)+" Using UB:"+str(num)
            print ub
            SetUB(dataR, UB=ub)
            md=ConvertToMD(InputWorkspace=dataR,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
                           QConversionScales='HKL',LorentzCorrection='0',Uproj='1,-1,0',Vproj='1,1,-2',Wproj='1,1,1',MinValues='-8.4,-5.1,-3.1',MaxValues='8.4,5.1,3.1')
            a1,b1=MDNormSCD(InputWorkspace='md',FluxWorkspace='flux',SolidAngleWorkspace='sa',
                            AlignedDim0="[H,-H,0],-8.4,8.4,501",
                            AlignedDim1="[L,L,-2L],-5.1,5.1,501",
                            AlignedDim2="[H,H,H],-3.1,3.1,61")
            if mtd.doesExist('dataMD'):
                dataMD=dataMD+a1
            else:
                dataMD=CloneMDWorkspace(a1)
            if mtd.doesExist('normMD'):
                normMD=normMD+b1
            else:
                normMD=CloneMDWorkspace(b1)
normData_CC=dataMD/normMD

#SaveMD('dataMD',Filename=outputdir+'6K/FeGeTe_6K_datacc_sym.nxs')
#SaveMD('normMD',Filename=outputdir+'6K/FeGeTe_6K_normfactorcc_sym.nxs')
SaveMD('normData_CC',Filename=outputdir+'DTO_normdatacc_48sym_AllTemp.nxs')

# group the data
#data6K=GroupWorkspaces(datatoMerge) 
#md6K=GroupWorkspaces(mdtoMerge)
