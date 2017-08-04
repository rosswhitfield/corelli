from mantid.simpleapi import *

runs = range(29533,29536)#+range(29556,29589)
#runs = range(29556,29589,20)

for r in runs:
    print 'Processing run : %s' %r
    filename='/SNS/CORELLI/IPTS-15526/nexus/CORELLI_'+str(r)+'.nxs.h5'
    data=LoadEventNexus(Filename=filename)
    MaskBTP(data,Pixel='1-16,241-256')
    LoadInstrument(data, Filename='/SNS/CORELLI/shared/Calibration/CORELLI_Definition_cal_20160310.xml',RewriteSpectraMap=False)
    SetGoniometer(data,Axis0="BL9:Mot:Sample:Axis1,0,1,0,1")
    ConvertToMD(InputWorkspace=data,OutputWorkspace='md2l',QDimensions='Q3D',dEAnalysisMode='Elastic',
                QConversionScales='Q in A^-1',LorentzCorrection='0', MinValues='-15.1,-25.1,-15.1',MaxValues='15.1,25.1,15.1',OverwriteExisting=False,Q3DFrames='Q_lab')
FindPeaksMD(InputWorkspace='md2l',DensityThresholdFactor=50000, OutputWorkspace='peaks2l')
FindUBUsingFFT(PeaksWorkspace='peaks2l', MinD=5, MaxD=15)
ShowPossibleCells(PeaksWorkspace='peaks2l')
SelectCellOfType(PeaksWorkspace='peaks2l',CellType='Hexagonal',Apply=True)
SaveIsawUB(InputWorkspace='peaks2l', Filename='benzil2l.mat')
