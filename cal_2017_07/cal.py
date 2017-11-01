import numpy as np
from mantid.simpleapi import (CreateEmptyTableWorkspace,
                              LoadEventNexus, ApplyCalibration,
                              SetInstrumentParameter, ModeratorTzero,
                              MaskBTP, ConvertUnits, Rebin,
                              SumNeighbours, GetDetOffsetsMultiPeaks,
                              SaveCalFile, MaskDetectors, mtd, Load)
import sys
import tube
tube.readCalibrationFile('CalibTable',
                         '/SNS/users/rwp/corelli/tube_calibration/CalibTableNew.txt')

run_dict = {'Si': (47327, 47334), 'C60': (47367, 47374), 'Diamond': (47344, 47351)}

sample = 'Si'
first = 47327
last = 47334

sample = 'C60'
first = 47367
last = 47374

sample = 'Diamond'
first = 47344
last = 47351

tube_cal = False
tube_cal = True

if len(sys.argv) > 1:
    sample = sys.argv[1]
    first, last = run_dict[sample]
    tube_cal = bool(sys.argv[2])

tube_string = "_TubeCal" if tube_cal else ""

# Generate fit window workspace
DReference = [2.7251, 2.8904, 4.2694, 5.0063, 8.1753]
fitwindict = {}
fitwindict[8.1753] = (7.5, 10.0)
fitwindict[5.0063] = (4.85, 6.0)
fitwindict[4.2694] = (4.0, 4.9)
fitwindict[2.8904] = (2.82, 3.0)
fitwindict[2.7251] = (2.65, 2.81)
FinalDReference = sorted(fitwindict.keys())

fitwinws = CreateEmptyTableWorkspace()
fitwinws.addColumn("int", "spectrum")
for ipk in range(len(FinalDReference)):
    fitwinws.addColumn("double", "Peak_%d_Left" % (ipk))
    fitwinws.addColumn("double", "Peak_%d_Right" % (ipk))

row = [-1]
for refpeak in FinalDReference:
    leftbound = fitwindict[refpeak][0]
    rightbound = fitwindict[refpeak][1]
    row.append(leftbound)
    row.append(rightbound)

fitwinws.addRow(row)

for run in range(first, last+1):
    LoadEventNexus(Filename='CORELLI_'+str(run), OutputWorkspace='data')
    if tube_cal:
        ApplyCalibration('data', 'CalibTable')
    SetInstrumentParameter(Workspace="data",
                           ParameterName="t0_formula",
                           Value="(23.5 * exp(-incidentEnergy/205.8))")
    ModeratorTzero(InputWorkspace="data",
                   OutputWorkspace="data",
                   EMode="Elastic")
    MaskBTP(Workspace='data', Pixel="1-16,241-256")
    ConvertUnits(InputWorkspace='data',
                 OutputWorkspace='data',
                 Target='dSpacing')
    Rebin(InputWorkspace='data',
          OutputWorkspace='data',
          Params='0.5,-0.004,10')
    SumNeighbours(InputWorkspace="data",
                  OutputWorkspace="data",
                  SumX=1, SumY=16)
    GetDetOffsetsMultiPeaks(
        InputWorkspace='data',
        DReference=FinalDReference,
        FitwindowTableWorkspace='fitwinws',
        PeakFunction="Gaussian",
        BackgroundType="Linear",
        HighBackground=True,
        OutputWorkspace='offset',
        MaskWorkspace='mask')
    # Save calibration
    SaveCalFile(Filename='cal_'+sample+'_'+str(run)+tube_string+'_sum16.cal',
                OffsetsWorkspace="offset",
                MaskWorkspace='mask')
    maskNumberPeaksFitted = np.where(mtd['NumberPeaksFitted'].extractY() < 3)
    MaskDetectors('mask', DetectorList=maskNumberPeaksFitted[0])
    SaveCalFile(Filename='cal_'+sample+'_'+str(run)+tube_string+'_sum16_mask_lt_3.cal',
                OffsetsWorkspace="offset",
                MaskWorkspace='mask')

# Average
Load(Filename='CORELLI_'+str(first)+'-'+str(last), OutputWorkspace='data')
if tube_cal:
    ApplyCalibration('data', 'CalibTable')
SetInstrumentParameter(Workspace="data",
                       ParameterName="t0_formula",
                       Value="(23.5 * exp(-incidentEnergy/205.8))")
ModeratorTzero(InputWorkspace="data", OutputWorkspace="data", EMode="Elastic")

MaskBTP(Workspace='data', Pixel="1-16,241-256")
ConvertUnits(InputWorkspace='data',
             OutputWorkspace='data',
             Target='dSpacing')
Rebin(InputWorkspace='data',
      OutputWorkspace='data',
      Params='0.5,-0.004,10')
SumNeighbours(InputWorkspace="data",
              OutputWorkspace="data",
              SumX=1, SumY=16)
GetDetOffsetsMultiPeaks(
        InputWorkspace='data',
        DReference=FinalDReference,
        FitwindowTableWorkspace='fitwinws',
        PeakFunction="Gaussian",
        BackgroundType="Linear",
        HighBackground=True,
        OutputWorkspace='offset',
        MaskWorkspace='mask')
# Save calibration
SaveCalFile(Filename='cal_'+sample+'_'+str(first)+'-'+str(last)+tube_string+'_sum16.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='mask')
maskNumberPeaksFitted = np.where(mtd['NumberPeaksFitted'].extractY() < 3)
MaskDetectors('mask', DetectorList=maskNumberPeaksFitted[0])
SaveCalFile(Filename='cal_'+sample+'_'+str(first)+'-'+str(last)+tube_string+'_sum16_mask_lt_3.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='mask')
