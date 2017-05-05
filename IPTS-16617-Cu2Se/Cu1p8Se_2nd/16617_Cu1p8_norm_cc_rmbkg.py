import sys,os
sys.path.append(os.path.join("/opt/mantidnightly/bin"))
from mantid.simpleapi import *
from mantid.geometry import SymmetryOperationFactory
from mantid import logger
import numpy as np
import time
# Either subtract proton charge normalized background prioir to convert to MD, or just reduced the background seperatly but in the
# exact same way as the data, and subtract the MDE's 

def load_Sum(r, ub_list, bkg):
        print 'Loading run number:'+ str(r)
        filename='/SNS/CORELLI/IPTS-16617/shared/autoreduce/CORELLI_'+str(r)+'_elastic.nxs'
        dataR=LoadNexus(Filename=filename)        
        LoadInstrument(Workspace= dataR, Filename='/SNS/CORELLI/shared/Calibration/CORELLI_Definition_cal_20160310.xml',RewriteSpectraMap=False)
        MaskDetectors(Workspace=dataR,MaskedWorkspace='sa')
        pc=sum(dataR.getRun()['proton_charge'].value)/1e12
        temp= dataR.getRun().getLogData('BL9:SE:LakeShore:KRDG3').value.mean()
        Omega = dataR.getRun().getLogData('BL9:Mot:Sample:Axis1').value.mean()+ 0
        print 'proton charge: %5.2f C; temperature = %5.2f K; Omega = %5.2f deg.' %(pc, temp, Omega)
        dataR=ConvertUnits(dataR,Target="Momentum",EMode="Elastic")
        dataR=CropWorkspace(dataR,XMin=2.5,XMax=10)
        SetGoniometer(dataR,Axis0="BL9:Mot:Sample:Axis1,0,1,0,1") 
        #bkg.run().getGoniometer().setR(dataR.run().getGoniometer().getR()) # Set background Goniometer to be the same as data
        #bkg = mtd[background]
        
        # Subtract background run, scaled by proton charge 
        bkg_pc=sum(bkg.getRun()['proton_charge'].value)
        mon_scale = pc/bkg_pc
        dataR = Minus(dataR, bkg*mon_scale*1e12*0.95)

        for ub in ub_list:
            print "using UB:"
            print ub
            SetUB(dataR, UB=ub)
            
            md=ConvertToMD(InputWorkspace=dataR,
                           QDimensions='Q3D',
                           dEAnalysisMode='Elastic',
                           Q3DFrames='HKL',
                           QConversionScales='HKL',
                           LorentzCorrection='0',
                           Uproj='1,0,0', Vproj='0,1,0',Wproj='0,0,1',
                           MinValues='-10.1,-10.1,-10.1',MaxValues='10.1,10.1,10.1')
            
            
            a1,b1=MDNormSCD(InputWorkspace='md',
                            FluxWorkspace='flux',
                            SolidAngleWorkspace='sa',
                            AlignedDim0="[H,0,0],-10.025,10.025,401",
                            AlignedDim1="[0,K,0],-10.025,10.025,401",
                            AlignedDim2="[0,0,L],-10.025,10.025,401")
        
                        
            if mtd.doesExist('dataMD'):
                mtd['dataMD']+=a1
            else :
                CloneMDWorkspace(a1, OutputWorkspace = 'dataMD')
            
            if mtd.doesExist('normMD'):
                mtd['normMD']+=b1
            else :
                CloneMDWorkspace(b1, OutputWorkspace = 'normMD')


###############################  scans, UB matrix and in/out dirs here #############################


outputdir = '/SNS/CORELLI/IPTS-16617/shared/'



outputname = 'Cu1p8_300K_HK0'
runs = range(38740, 38770,1) # Cu1.8Se, 250K
UBname = "Cu1p8Se_2nd/Cu1p8Se_UB_rough.mat"
 
LoadNexus(Filename='/SNS/CORELLI/shared/Vanadium/Spectrum20161123_cc.nxs', OutputWorkspace='flux')
LoadNexus(Filename='/SNS/CORELLI/shared/Vanadium/SolidAngle20161123_cc.nxs', OutputWorkspace='sa')

# Get UBs
LoadEmptyInstrument(Filename='/SNS/CORELLI/shared/Calibration/CORELLI_Definition_cal_20160310.xml', OutputWorkspace='ub')
LoadIsawUB(InputWorkspace='ub', Filename=outputdir+UBname)
ub=mtd['ub'].sample().getOrientedLattice().getUB()
print "Starting UB :"
print ub

#symOps = SymmetryOperationFactory.createSymOps(" x, y, z;  -x ,-y, z;  -x,y,-z;  x,-y,-z;-x,-y,-z;  x,y,-z; x,-y,z; -x,y,z")
#symOps = SymmetryOperationFactory.createSymOps("x, y, z;x,-y,-z; x,y,-z; x,-y,z")
symOps = SymmetryOperationFactory.createSymOps("x, y, z")#;-x,-y,-z")
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

if mtd.doesExist('normMD'):
    DeleteWorkspace('normMD')
if mtd.doesExist('dataMD'):
    DeleteWorkspace('dataMD')
if mtd.doesExist('bkgMD'):
    DeleteWorkspace('bkgMD')
if mtd.doesExist('bkg_normMD'):
    DeleteWorkspace('bkg_normMD')

#load in background
bkg = LoadNexus(Filename = '/SNS/CORELLI/IPTS-16617/shared/CCR_StickA_Almount_Bkgcc.nxs')

MaskDetectors(Workspace=bkg,MaskedWorkspace='sa')
pc_bkg=sum(bkg.getRun()['proton_charge'].value)
print 'pc_bkg=:'+str(pc_bkg)
bkg=ConvertUnits(bkg,Target="Momentum",EMode="Elastic")
bkg=CropWorkspace(bkg,XMin=2.5,XMax=10)



# run continuously, waiting for next run to come in
idx = 0
while idx < np.size(runs):
   test_file='/SNS/CORELLI/IPTS-16617/shared/autoreduce/CORELLI_'+str(runs[idx])+'_elastic.nxs'
   filethere = os.path.isfile(test_file)
   if filethere:
      load_Sum(runs[idx],ub_list, bkg)
      idx+=1
      dataMD = mtd['dataMD']
      normMD= mtd['normMD']
      normData=dataMD/normMD
   else :
      print "file: " + test_file + " not found.   Waiting for it to appear... "
      time.sleep(1500)
dataMD = mtd['dataMD']
normMD= mtd['normMD']
normData_250K=dataMD/normMD

SaveMD(Inputworkspace='normData',Filename='/SNS/users/krogstad/Desktop/Cu1p8Se_250K_2ndrun.nxs')

data=dataMD.getSignalArray()
error=dataMD.getErrorSquaredArray()
norm=normMD.getSignalArray()

normData=dataMD/normMD



SaveMD(Inputworkspace='dataMD',Filename=outputdir+'data_CC_rmbkg_'+outputname+'.nxs')
SaveMD(Inputworkspace='normMD',Filename=outputdir+'V_CC_rmbkg_'+outputname+'.nxs')
SaveMD(Inputworkspace='normData',Filename=outputdir+'norm_CC_rmbkg_'+outputname+'.nxs')



#data2=data+data[::1,::-1,::1]+data[::1,::-1,::-1]+data[::1,::1,::-1]+data[::-1,::-1,::1]+data[::-1,::-1,::-1]+data[::-1,::1,::-1]+data[::-1,::1,::1]
#error2=error+error[::1,::-1,::1]+error[::1,::-1,::-1]+error[::1,::1,::-1]+error[::-1,::-1,::1]+error[::-1,::-1,::-1]+error[::-1,::1,::-1]+error[::-1,::1,::1]
#norm2=norm+norm[::1,::-1,::1]+norm[::1,::-1,::-1]+norm[::1,::1,::-1]+norm[::-1,::-1,::1]+norm[::-1,::-1,::-1]+norm[::-1,::1,::-1]+norm[::-1,::1,::1]


#dataMD.setSignalArray(data2)
#dataMD.setErrorSquaredArray(error2)
#normMD.setSignalArray(norm2)

#normData_sym=dataMD/normMD

#SaveMD(Inputworkspace='dataMD',Filename=outputdir+'data_sym_CC_nobkg_'+outputname+'.nxs')
#SaveMD(Inputworkspace='normMD',Filename=outputdir+'V_sym_CC_nobkg_'+outputname+'.nxs')
#SaveMD(Inputworkspace='normData_sym',Filename=outputdir+'norm_sym_CC_nobkg_'+outputname+'.nxs')


