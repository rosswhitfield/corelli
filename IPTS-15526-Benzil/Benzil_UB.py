from mantid.simpleapi import *
outputdir="/SNS/CORELLI/IPTS-15526/shared/"

#Quick mesh scan, 5 mins/angle
runs = range(29533,29536)+range(29556,29589)

#mesh scan at 100K, 20 mins/angle
#runs = range(29589,29614)
toMerge1=[]
toMerge2=[]
BinParm='1.,0.1,15'
UBfile="Benzil_100K_UB.mat"

for r in runs:
    print 'Processing run : %s' %r
    filename='/SNS/CORELLI/IPTS-15526/nexus/CORELLI_'+str(r)+'.nxs.h5'
    ows='COR_'+str(r)
    omd=ows+'_md'
    toMerge1.append(ows)
    toMerge2.append(omd)
    LoadEventNexus(Filename=filename, OutputWorkspace=ows)
    MaskBTP(workspace=ows,Pixel='1-16,241-256')
    LoadInstrument(Workspace= ows, Filename='/SNS/CORELLI/shared/Calibration/CORELLI_Definition_cal_20160310.xml',RewriteSpectraMap=False)
    #ConvertUnits(InputWorkspace=ows, OutputWorkspace=ows, Target='dSpacing')
    #Rebin(InputWorkspace=ows, OutputWorkspace=ows, Params=BinParm)
    SetGoniometer(ows,Axis0="BL9:Mot:Sample:Axis1,0,1,0,1")
    #LoadIsawUB(InputWorkspace=ows,Filename=outputdir+UBfile)
    ConvertToMD(InputWorkspace=ows,OutputWorkspace=omd,QDimensions='Q3D',dEAnalysisMode='Elastic', 
       QConversionScales='Q in A^-1',LorentzCorrection='0', MinValues='-15.1,-25.1,-15.1',MaxValues='15.1,25.1,15.1')
data=GroupWorkspaces(toMerge1)
md=GroupWorkspaces(toMerge2)
merged100K=MergeMD(toMerge2)
FindPeaksMD(InputWorkspace='merged100K',DensityThresholdFactor=50000, OutputWorkspace='peaks')
FindUBUsingFFT(PeaksWorkspace='peaks', MinD=5, MaxD=15)
ShowPossibleCells(PeaksWorkspace='peaks')
SelectCellOfType(PeaksWorkspace='peaks',CellType='Hexagonal',Apply=True)
SaveIsawUB(InputWorkspace='peaks', Filename='/SNS/users/rwp/benzil/benzil_Hexagonal.mat')
