from mantid.simpleapi import *
from mantid.geometry import SymmetryOperationFactory, SpaceGroupFactory
import numpy as np

# about information on where the data are and where to save
iptsfolder= "/SNS/CORELLI/IPTS-16617/"
outputdir="/SNS/users/rwp/corelli/IPTS-16617-PMN/"
nxfiledir=iptsfolder + "nexus/"
ccfiledir = iptsfolder +"shared/autoreduce/"

UBfile = iptsfolder+"shared/PMN_UB_300K.mat"

LoadNexus(Filename='/SNS/CORELLI/shared/Vanadium/Spectrum20161123_cc.nxs', OutputWorkspace='flux')
LoadNexus(Filename='/SNS/CORELLI/shared/Vanadium/SolidAngle20161123_cc.nxs', OutputWorkspace='sa')

# Get UBs
LoadEmptyInstrument(Filename='/SNS/CORELLI/shared/Calibration/CORELLI_Definition_cal_20160310.xml', OutputWorkspace='ub')
LoadIsawUB(InputWorkspace='ub', Filename=UBfile)
ub=mtd['ub'].sample().getOrientedLattice().getUB()
print "Starting UB :"
print ub

#PMN   pm-3m (227)  general position has 48 symmety operations.
sg=SpaceGroupFactory.createSpaceGroup("P m -3 m")
symOps = sg.getSymmetryOperations()

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

# T=300K
runs =  range(39008,39019,1)

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
        filename=iptsfolder+'/nexus/CORELLI_'+str(r)+'.nxs.h5'
        dataR=LoadEventNexus(Filename=filename)
        #filename=ccfiledir+'CORELLI_'+str(r)+'_elastic.nxs'
        #dataR=LoadNexus(Filename=filename)
        LoadInstrument(Workspace= dataR, Filename='/SNS/CORELLI/shared/Calibration/CORELLI_Definition_cal_20160310.xml',RewriteSpectraMap=False)
        MaskDetectors(Workspace=dataR,MaskedWorkspace='sa')
        pc_data=sum(dataR.getRun()['proton_charge'].value)/1e12
        print 'pc_data=:'+str(pc_data)

        dataR=ConvertUnits(dataR,Target="Momentum",EMode="Elastic")
        dataR=CropWorkspace(dataR,XMin=2.5,XMax=10)
        SetGoniometer(dataR,Axis0="BL9:Mot:Sample:Axis2,0,1,0,1")
        LoadIsawUB(InputWorkspace=dataR,Filename=UBfile)
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
        SaveMD('normData',Filename=outputdir+'PMN_normdata_300K.nxs')
