from mantid.simpleapi import *
import numpy as np

# Generate fit window workspace
DReference = [1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353]

for run in range(20492,20500):
        LoadEventNexus(Filename='/SNS/CORELLI/IPTS-15796/nexus/CORELLI_'+str(run)+'.nxs.h5', OutputWorkspace='rawSi')
        LoadInstrument(Workspace="rawSi",Filename="/SNS/users/rwp/CORELLI_Definition_91.07cm.xml",RewriteSpectraMap=False)
        SetInstrumentParameter(Workspace="rawSi",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
        ModeratorTzero(InputWorkspace="rawSi",OutputWorkspace="rawSi",EMode="Elastic")
        MaskBTP(Workspace='rawSi',Pixel="1-16,241-256")
        #SumNeighbours(InputWorkspace="rawSi", OutputWorkspace="rawSi", SumX=1, SumY=16)
        PDCalibration(UncalibratedWorkspace='rawSi',
                      TofBinning=[300,-.001,16666.7],
                      PeakPositions=DReference,
                      OutputCalibrationTable='cal')
        SaveDiffCal(Filename='/SNS/users/rwp/corelli/PDCalibration/cal_Si_'+str(run)+'.h5',
                    CalibrationWorkspace="cal",
                    MaskWorkspace='cal_mask')
# Average
LoadEventNexus(Filename='/SNS/CORELLI/IPTS-15796/nexus/CORELLI_20492.nxs.h5', OutputWorkspace='rawSi')
LoadInstrument(Workspace="rawSi",Filename="/SNS/users/rwp/CORELLI_Definition_91.07cm.xml",RewriteSpectraMap=False)
SetInstrumentParameter(Workspace="rawSi",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
ModeratorTzero(InputWorkspace="rawSi",OutputWorkspace="rawSi",EMode="Elastic")
for run in range(20493,20500):
        LoadEventNexus(Filename='/SNS/CORELLI/IPTS-15796/nexus/CORELLI_'+str(run)+'.nxs.h5', OutputWorkspace='rawSi2')
        LoadInstrument(Workspace="rawSi2",Filename="/SNS/users/rwp/CORELLI_Definition_91.07cm.xml",RewriteSpectraMap=False)
        SetInstrumentParameter(Workspace="rawSi2",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
        ModeratorTzero(InputWorkspace="rawSi2",OutputWorkspace="rawSi2",EMode="Elastic")
        Plus(LHSWorkspace="rawSi",RHSWorkspace="rawSi2",OutputWorkspace="rawSi",ClearRHSWorkspace=True)

#MaskBTP(Workspace='rawSi',Pixel="1-16,241-256")
#SumNeighbours(InputWorkspace="rawSi", OutputWorkspace="rawSi", SumX=1, SumY=16)
SortEvents(InputWorkspace='rawSi')
CompressEvents(InputWorkspace='rawSi',OutputWorkspace='rawSi')
PDCalibration(UncalibratedWorkspace='rawSi',
              TofBinning=[300,-.001,16666.7],
              PeakPositions=DReference,
              OutputCalibrationTable='cal')
SaveDiffFile(Filename='/SNS/users/rwp/corelli/PDCalibration/cal_Si_20492-9.h5',
            CalibrationWorkspace="cal_cal",
            MaskWorkspace='cal_mask')
