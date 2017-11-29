import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration/CalibTableNew.txt')

# DReference = [0.9179, 0.9600, 1.0451, 1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353] # Si
# DReference = [1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353] # Si
# runs = '47327-47334' # Si

# 73661
DReference = [2.7251,2.8904,4.2694,5.0063,8.1753]  # C60

runs='47367-47374' # long
#runs='47375-47382' # long
#runs='47367-47382' # all

binning = '2,-0.004,10'

Load(Filename='CORELLI_'+runs, OutputWorkspace='data')
SetInstrumentParameter(Workspace="data",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
ModeratorTzero(InputWorkspace="data",OutputWorkspace="data",EMode="Elastic")

MaskBTP(Workspace='data',Pixel="1-16,241-256")
ConvertUnits(InputWorkspace='data',OutputWorkspace='data',Target='dSpacing')
SumNeighbours(InputWorkspace="data", OutputWorkspace="data", SumX=1, SumY=16)
Rebin(InputWorkspace='data',OutputWorkspace='data',Params=binning)

GetDetOffsetsMultiPeaks(
    InputWorkspace = 'data',
    DReference = DReference,
    FitWindowMaxWidth=0.1,
    BackgroundType = "Flat",
    OutputWorkspace = 'offset')

SaveCalFile(Filename='cal_C60_2_'+runs+'_sum16_long.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='Mask')
ConvertDiffCal(OffsetsWorkspace="offset",
               OutputWorkspace="cal")
SaveDiffCal(CalibrationWorkspace="cal",
            MaskWorkspace="Mask",
            Filename='cal_C60_2_'+runs+'_sum16_long.h5')

maskNumberPeaksFitted = np.where(mtd['NumberPeaksFitted'].extractY() <2)
MaskDetectors('Mask',DetectorList=maskNumberPeaksFitted[0])
SaveCalFile(Filename='cal_C60_2_'+runs+'_sum16_mask_lt_2_long.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='Mask')
ConvertDiffCal(OffsetsWorkspace="offset",
               OutputWorkspace="cal")
SaveDiffCal(CalibrationWorkspace="cal",
            MaskWorkspace="Mask",
            Filename='cal_C60_2_'+runs+'_sum16_mask_lt_2_long.h5')

maskNumberPeaksFitted = np.where(mtd['NumberPeaksFitted'].extractY() <3)
MaskDetectors('Mask',DetectorList=maskNumberPeaksFitted[0])
SaveCalFile(Filename='cal_C60_2_'+runs+'_sum16_mask_lt_3_long.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='Mask')
ConvertDiffCal(OffsetsWorkspace="offset",
               OutputWorkspace="cal")
SaveDiffCal(CalibrationWorkspace="cal",
            MaskWorkspace="Mask",
            Filename='cal_C60_2_'+runs+'_sum16_mask_lt_3_long.h5')

# With tube cal

Load(Filename='CORELLI_'+runs, OutputWorkspace='data')
ApplyCalibration('data','CalibTable')
SetInstrumentParameter(Workspace="data",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
ModeratorTzero(InputWorkspace="data",OutputWorkspace="data",EMode="Elastic")

MaskBTP(Workspace='data',Pixel="1-16,241-256")
ConvertUnits(InputWorkspace='data',OutputWorkspace='data',Target='dSpacing')
SumNeighbours(InputWorkspace="data", OutputWorkspace="data", SumX=1, SumY=16)
Rebin(InputWorkspace='data',OutputWorkspace='data',Params=binning)

GetDetOffsetsMultiPeaks(
    InputWorkspace = 'data',
    DReference = DReference,
    FitWindowMaxWidth=0.1,
    BackgroundType = "Flat",
    OutputWorkspace = 'offset')


SaveCalFile(Filename='cal_C60_2_'+runs+'_TubeCal_sum16_long.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='Mask')
ConvertDiffCal(OffsetsWorkspace="offset",
               OutputWorkspace="cal")
SaveDiffCal(CalibrationWorkspace="cal",
            MaskWorkspace="Mask",
            Filename='cal_C60_2_'+runs+'_TubeCal_sum16_long.h5')

maskNumberPeaksFitted = np.where(mtd['NumberPeaksFitted'].extractY() <2)
MaskDetectors('Mask',DetectorList=maskNumberPeaksFitted[0])
SaveCalFile(Filename='cal_C60_2_'+runs+'_TubeCal_sum16_mask_lt_2_long.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='Mask')
ConvertDiffCal(OffsetsWorkspace="offset",
               OutputWorkspace="cal")
SaveDiffCal(CalibrationWorkspace="cal",
            MaskWorkspace="Mask",
            Filename='cal_C60_2_'+runs+'_TubeCal_sum16_mask_lt_2_long.h5')

maskNumberPeaksFitted = np.where(mtd['NumberPeaksFitted'].extractY() <3)
MaskDetectors('Mask',DetectorList=maskNumberPeaksFitted[0])
SaveCalFile(Filename='cal_C60_2_'+runs+'_TubeCal_sum16_mask_lt_3_long.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='Mask')
ConvertDiffCal(OffsetsWorkspace="offset",
               OutputWorkspace="cal")
SaveDiffCal(CalibrationWorkspace="cal",
            MaskWorkspace="Mask",
            Filename='cal_C60_2_'+runs+'_TubeCal_sum16_mask_lt_3_long.h5')
