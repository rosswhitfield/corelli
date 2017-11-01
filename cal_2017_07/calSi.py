import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration/CalibTableNew.txt')


# Generate fit window workspace
#DReference = [0.9179, 0.9600, 1.0451, 1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353]
DReference = [1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353]
fitwindict = {}
fitwindict[3.1353] = (3.01, 3.33)
fitwindict[1.9200] = (1.88, 2.00)
fitwindict[1.6374] = (1.60, 1.70)
fitwindict[1.3576] = (1.34, 1.39)
fitwindict[1.2458] = (1.22, 1.27)
fitwindict[1.1085] = (1.08, 1.14)
FinalDReference = sorted(fitwindict.keys())

fitwinws = CreateEmptyTableWorkspace()
fitwinws.addColumn("int", "spectrum")
for ipk in range(len(FinalDReference)):
    fitwinws.addColumn("double", "Peak_%d_Left"%(ipk))
    fitwinws.addColumn("double", "Peak_%d_Right"%(ipk))

row = [-1]
for refpeak in FinalDReference:
    leftbound = fitwindict[refpeak][0]
    rightbound = fitwindict[refpeak][1]
    row.append(leftbound)
    row.append(rightbound)

fitwinws.addRow(row)


files='CORELLI_47327' # CORELLI_47327:47334

for run in range(47327,47335):
    Load('CORELLI_'+str(run), OutputWorkspace='rawSi')
    SetInstrumentParameter(Workspace="rawSi",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
    ModeratorTzero(InputWorkspace="rawSi",OutputWorkspace="rawSi",EMode="Elastic")
    MaskBTP(Workspace='rawSi',Pixel="1-16,241-256")
    ConvertUnits(InputWorkspace='rawSi',OutputWorkspace='siliconD',Target='dSpacing')
    Rebin(InputWorkspace='siliconD',OutputWorkspace='siliconD',Params='0.5,-0.004,3.5')
    SumNeighbours(InputWorkspace="siliconD", OutputWorkspace="siliconD", SumX=1, SumY=16)
    GetDetOffsetsMultiPeaks(
        InputWorkspace = 'siliconD',
        DReference = FinalDReference,
        FitwindowTableWorkspace='fitwinws',
        PeakFunction = "Gaussian",
        BackgroundType = "Linear",
        HighBackground = True,
        OutputWorkspace = 'offset',
        MaskWorkspace='mask')
    SaveCalFile(Filename='cal_Si_'+str(run)+'_sum16.cal',
                OffsetsWorkspace="offset",
                MaskWorkspace='mask')
    maskNumberPeaksFitted = np.where(mtd['NumberPeaksFitted'].extractY() <3)
    MaskDetectors('mask',DetectorList=maskNumberPeaksFitted[0])
    SaveCalFile(Filename='cal_Si_'+str(run)+'_sum16_mask_lt_3.cal',
                OffsetsWorkspace="offset",
                MaskWorkspace='mask')

# Average
Load(Filename='CORELLI_47327-47334', OutputWorkspace='rawSi')
SetInstrumentParameter(Workspace="rawSi",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
ModeratorTzero(InputWorkspace="rawSi",OutputWorkspace="rawSi",EMode="Elastic")
    
MaskBTP(Workspace='rawSi',Pixel="1-16,241-256")
ConvertUnits(InputWorkspace='rawSi',OutputWorkspace='siliconD',Target='dSpacing')
Rebin(InputWorkspace='siliconD',OutputWorkspace='siliconD',Params='0.5,-0.004,3.5')
SumNeighbours(InputWorkspace="siliconD", OutputWorkspace="siliconD", SumX=1, SumY=16)
GetDetOffsetsMultiPeaks(
    InputWorkspace = 'siliconD',
    DReference = FinalDReference,
    FitwindowTableWorkspace='fitwinws',
    PeakFunction = "Gaussian",
    BackgroundType = "Linear",
    HighBackground = True,
    OutputWorkspace = 'offset',
    MaskWorkspace='mask')
SaveCalFile(Filename='cal_Si_47327-47334_sum16.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='mask')
maskNumberPeaksFitted = np.where(mtd['NumberPeaksFitted'].extractY() <3)
MaskDetectors('mask',DetectorList=maskNumberPeaksFitted[0])
SaveCalFile(Filename='cal_Si_47327-47334_sum16_mask_lt_3.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='mask')
