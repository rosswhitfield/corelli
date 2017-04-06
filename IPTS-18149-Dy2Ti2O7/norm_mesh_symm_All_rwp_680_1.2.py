from mantid.simpleapi import *
from mantid.geometry import SymmetryOperationFactory
import numpy as np

# about information on where the data are and where to save
iptsfolder= "/SNS/CORELLI/IPTS-18149/"
outputdir="/SNS/users/rwp/corelli/IPTS-18149-Dy2Ti2O7/"
nxfiledir=iptsfolder + "nexus/"
ccfiledir = iptsfolder +"shared/autoreduce/"

UBfile = iptsfolder+"shared/DTO_UB.mat"
reducedfile_prefix = "DTO_cc"

LoadNexus(Filename='/SNS/CORELLI/shared/Vanadium/2017A/SolidAngle_SlimSam_20170307_Central.nxs', OutputWorkspace='sa')
LoadNexus(Filename='/SNS/CORELLI/shared/Vanadium/2017A/Spectrum_SlimSam_20170307_Central.nxs', OutputWorkspace='flux')

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
#pc_bkg=sum(bkg.getRun()['proton_charge'].value)/1e12
#print 'pc_bkg=:'+str(pc_bkg)

H=0.0

T=100 #mK
runs =  range(40689,40731,1)
T=100 #mK, part2
runs =  range(40733,40751,1)
T=100 #mK, total
runs=range(40689,40731,1)+range(40733,40751,1)

T=680 #mK
runs =  range(40754,40785,1)

T=680 #mK
H=0.2 #Tesla
runs =  range(40786,40823,1)

#T=680 mK, H=0.4 Tesla
#runs =  range(40824,40861,1)

#T=680 mK, H=0.6 Tesla
#runs =  range(40862,40899,1)

T=680 #mK
H=0.8 #Tesla
runs =  range(40900,40937,1)

T=680 #mK
H=1.0 #Tesla
runs =  range(40938,40946,1)+range(40947,40976,1)

T=680 #mK
H=1.2 #Tesla
runs =  range(40977,41014,1)

"""
T=680 #mK, quick check at
H=0 #Tesla
runs =  range(41015,41034,1)

T=680 #mK, quick check at
H=0.1 #Tesla
runs =  range(41035,41072,1)

T=680 #mK, quick check at
H=0.3 #Tesla
runs =  range(41073,41110,1)

T=680 #mK, quick check at
H=0.5 #Tesla
runs =  range(41111,41148,1)

T=680 #mK, quick check at
H=1.5 #Tesla
runs =  range(41111,41148,1)
"""

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
        filename='/SNS/CORELLI/IPTS-18149/nexus/CORELLI_'+str(r)+'.nxs.h5'
        dataR=LoadEventNexus(Filename=filename)
        #filename=ccfiledir+'CORELLI_'+str(r)+'_elastic.nxs'
        #dataR=LoadNexus(Filename=filename)
        LoadInstrument(Workspace= dataR, Filename='/SNS/CORELLI/shared/Calibration/CORELLI_Definition_cal_20160310.xml',RewriteSpectraMap=False)
        MaskDetectors(Workspace=dataR,MaskedWorkspace='sa')
        pc_data=sum(dataR.getRun()['proton_charge'].value)/1e12
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
                           QConversionScales='HKL',LorentzCorrection='0',MinValues='-10.1,-10.1,-10.1',MaxValues='10.1,10.1,10.1')
            a1,b1=MDNormSCD(InputWorkspace='md',FluxWorkspace='flux',SolidAngleWorkspace='sa',
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
normData=dataMD/normMD

SaveMD('normData',Filename=outputdir+'DTO_normdata_48sym_'+str(T)+'mK_H'+str(H)+'T.nxs')

# group the data
#data6K=GroupWorkspaces(datatoMerge)
#md6K=GroupWorkspaces(mdtoMerge)
