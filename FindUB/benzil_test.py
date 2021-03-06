from mantid.simpleapi import *
outputdir="/SNS/CORELLI/IPTS-15526/shared/"

#Quick mesh scan, 5 mins/angle
runs = range(29533,29536)#+range(29556,29589)
runs = range(29556,29589,20)

#mesh scan at 100K, 20 mins/angle
#runs = range(29589,29614)
toMerge=[]

for r in runs:
    print 'Processing run : %s' %r
    filename='/SNS/CORELLI/IPTS-15526/nexus/CORELLI_'+str(r)+'.nxs.h5'
    ows='COR_'+str(r)
    omd=ows+'_md'
    toMerge.append(omd)
    data=LoadEventNexus(Filename=filename)
    MaskBTP(data,Pixel='1-16,241-256')
    LoadInstrument(data, Filename='/SNS/CORELLI/shared/Calibration/CORELLI_Definition_cal_20160310.xml',RewriteSpectraMap=False)
    SetGoniometer(data,Axis0="BL9:Mot:Sample:Axis1,0,1,0,1")
    ConvertToMD(data,OutputWorkspace=omd,QDimensions='Q3D',dEAnalysisMode='Elastic',
                QConversionScales='Q in A^-1',LorentzCorrection='0', MinValues='-15.1,-25.1,-15.1',MaxValues='15.1,25.1,15.1')

md=GroupWorkspaces(toMerge)
merged=MergeMD(md)
FindPeaksMD(InputWorkspace='merged',DensityThresholdFactor=50000, OutputWorkspace='peaks')
FindUBUsingFFT(PeaksWorkspace='peaks', MinD=5, MaxD=15)
ShowPossibleCells(PeaksWorkspace='peaks')
SelectCellOfType(PeaksWorkspace='peaks',CellType='Hexagonal',Apply=True)
SaveIsawUB(InputWorkspace='peaks', Filename='benzil.mat')
