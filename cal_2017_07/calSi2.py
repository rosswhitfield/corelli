import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration/CalibTableNew.txt')

#DReference = [0.9179, 0.9600, 1.0451, 1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353]
DReference = [1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353]

Load(Filename='CORELLI_47327-47334', OutputWorkspace='rawSi')
SetInstrumentParameter(Workspace="rawSi",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
ModeratorTzero(InputWorkspace="rawSi",OutputWorkspace="rawSi",EMode="Elastic")
    
MaskBTP(Workspace='rawSi',Pixel="1-16,241-256")
ConvertUnits(InputWorkspace='rawSi',OutputWorkspace='siliconD',Target='dSpacing')
SumNeighbours(InputWorkspace="siliconD", OutputWorkspace="siliconD", SumX=1, SumY=16)
Rebin(InputWorkspace='siliconD',OutputWorkspace='siliconD',Params='0.5,-0.004,3.5')

GetDetOffsetsMultiPeaks(
    InputWorkspace = 'siliconD',
    DReference = DReference,
    FitWindowMaxWidth=0.1,
    BackgroundType = "Flat",
    OutputWorkspace = 'offset')

SaveCalFile(Filename='cal_Si2_47327-47334_sum16.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='mask')
ConvertDiffCal(OffsetsWorkspace="offset",
               OutputWorkspace="cal")
SaveDiffCal(CalibrationWorkspace="cal",
            MaskWorkspace="mask",
            Filename='cal_Si2_47327-47334_sum16.h5')
maskNumberPeaksFitted = np.where(mtd['NumberPeaksFitted'].extractY() <3)
MaskDetectors('mask',DetectorList=maskNumberPeaksFitted[0])
SaveCalFile(Filename='cal_Si2_47327-47334_sum16_mask_lt_3.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='mask')
ConvertDiffCal(OffsetsWorkspace="offset",
               OutputWorkspace="cal")
SaveDiffCal(CalibrationWorkspace="cal",
            MaskWorkspace="mask",
            Filename='cal_Si2_47327-47334_sum16_mask_lt_3.h5')

# With tube cal

Load(Filename='CORELLI_47327-47334', OutputWorkspace='rawSi')
ApplyCalibration('rawSi','CalibTable')
SetInstrumentParameter(Workspace="rawSi",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
ModeratorTzero(InputWorkspace="rawSi",OutputWorkspace="rawSi",EMode="Elastic")
    
MaskBTP(Workspace='rawSi',Pixel="1-16,241-256")
ConvertUnits(InputWorkspace='rawSi',OutputWorkspace='siliconD',Target='dSpacing')
SumNeighbours(InputWorkspace="siliconD", OutputWorkspace="siliconD", SumX=1, SumY=16)
Rebin(InputWorkspace='siliconD',OutputWorkspace='siliconD',Params='0.5,-0.004,3.5')


GetDetOffsetsMultiPeaks(
    InputWorkspace = 'siliconD',
    DReference = DReference,
    FitWindowMaxWidth=0.1,
    BackgroundType = "Flat",
    OutputWorkspace = 'offset',
    MaskWorkspace='mask')


SaveCalFile(Filename='cal_Si2_47327-47334_sum16.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='mask')
ConvertDiffCal(OffsetsWorkspace="offset",
               OutputWorkspace="cal")
SaveDiffCal(CalibrationWorkspace="cal",
            GroupingWorkspace="group",
            MaskWorkspace="mask",
            Filename='cal_Si2_47327-47334_sum16.h5')


maskNumberPeaksFitted = np.where(mtd['NumberPeaksFitted'].extractY() <3)
MaskDetectors('mask',DetectorList=maskNumberPeaksFitted[0])
SaveCalFile(Filename='cal_Si2_47327-47334_sum16_mask_lt_3.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='mask')




