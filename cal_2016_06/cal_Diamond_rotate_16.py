from mantid.simpleapi import *
import numpy as np

# Generate fit window workspace
#DReference = [0.9179, 0.9600, 1.0451, 1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353]
DReference = [0.6865,0.7281,0.8183,0.8918,1.0755,1.2612,2.0595]
fitwindict = {}
fitwindict[2.0595] = (1.95, 2.2)
fitwindict[1.2612] = (1.22, 1.3)
fitwindict[1.0755] = (1.04, 1.11)
fitwindict[0.8918] = (0.86, 0.92)
fitwindict[0.8183] = (0.79, 0.84)
fitwindict[0.7281] = (0.71, 0.75)
fitwindict[0.6865] = (0.66, 0.705)
FinalDReference = sorted(fitwindict.keys())

fitwinws = CreateEmptyTableWorkspace()
fitwinws.addColumn("int", "spectrum")
for ipk in xrange(len(FinalDReference)):
	fitwinws.addColumn("double", "Peak_%d_Left"%(ipk))
	fitwinws.addColumn("double", "Peak_%d_Right"%(ipk))

row = [-1]
for refpeak in FinalDReference:
		leftbound = fitwindict[refpeak][0]
		rightbound = fitwindict[refpeak][1]
		row.append(leftbound)
		row.append(rightbound)

fitwinws.addRow(row)

# Calculate offsets

for run in range(20482,20490):
        LoadEventNexus(Filename='/SNS/CORELLI/IPTS-15796/nexus/CORELLI_'+str(run)+'.nxs.h5', OutputWorkspace='rawDiamond')
        LoadInstrument(Workspace="rawDiamond",Filename="/SNS/users/rwp/CORELLI_Definition_91.07cm.xml",RewriteSpectraMap=False)
        SetInstrumentParameter(Workspace="rawDiamond",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
        ModeratorTzero(InputWorkspace="rawDiamond",OutputWorkspace="rawDiamond",EMode="Elastic")
        MaskBTP(Workspace='rawDiamond',Pixel="1-16,241-256")
        ConvertUnits(InputWorkspace='rawDiamond',OutputWorkspace='diamondD',Target='dSpacing')
        Rebin(InputWorkspace='diamondD',OutputWorkspace='diamondD',Params='0.5,-0.004,2.5')
        SumNeighbours(InputWorkspace="diamondD", OutputWorkspace="diamondD", SumX=1, SumY=16)
        GetDetOffsetsMultiPeaks(
                InputWorkspace = 'diamondD',
                DReference = FinalDReference,
                FitwindowTableWorkspace='fitwinws',
                PeakFunction = "Gaussian",
                BackgroundType = "Linear",
                HighBackground = True,
                OutputWorkspace = 'offset',
                MaskWorkspace='mask')
        SaveCalFile(Filename='/SNS/users/rwp/corelli/cal_2016_06/cal_Diamond_'+str(run)+'_sum16.cal',
                    OffsetsWorkspace="offset",
                    MaskWorkspace='mask')
        maskNumberPeaksFitted = np.where(mtd['NumberPeaksFitted'].extractY() <3)
        MaskDetectors('mask',DetectorList=maskNumberPeaksFitted[0])
        SaveCalFile(Filename='/SNS/users/rwp/corelli/cal_2016_06/cal_Diamond_'+str(run)+'_sum16_mask_lt_3.cal',
                    OffsetsWorkspace="offset",
                    MaskWorkspace='mask')

# Average
run = 20482
LoadEventNexus(Filename='/SNS/CORELLI/IPTS-15796/nexus/CORELLI_'+str(run)+'.nxs.h5', OutputWorkspace='rawDiamond')
LoadInstrument(Workspace="rawDiamond",Filename="/SNS/users/rwp/CORELLI_Definition_91.07cm.xml",RewriteSpectraMap=False)
SetInstrumentParameter(Workspace="rawDiamond",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
ModeratorTzero(InputWorkspace="rawDiamond",OutputWorkspace="rawDiamond",EMode="Elastic")
for run in range(20483,20490):
        LoadEventNexus(Filename='/SNS/CORELLI/IPTS-15796/nexus/CORELLI_'+str(run)+'.nxs.h5', OutputWorkspace='rawDiamond2')
        LoadInstrument(Workspace="rawDiamond2",Filename="/SNS/users/rwp/CORELLI_Definition_91.07cm.xml",RewriteSpectraMap=False)
        SetInstrumentParameter(Workspace="rawDiamond2",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
        ModeratorTzero(InputWorkspace="rawDiamond2",OutputWorkspace="rawDiamond2",EMode="Elastic")
        Plus(LHSWorkspace="rawDiamond",RHSWorkspace="rawDiamond2",OutputWorkspace="rawDiamond",ClearRHSWorkspace=True)

MaskBTP(Workspace='rawDiamond',Pixel="1-16,241-256")
ConvertUnits(InputWorkspace='rawDiamond',OutputWorkspace='diamondD',Target='dSpacing')
Rebin(InputWorkspace='diamondD',OutputWorkspace='diamondD',Params='0.5,-0.004,2.5')
SumNeighbours(InputWorkspace="diamondD", OutputWorkspace="diamondD", SumX=1, SumY=16)
GetDetOffsetsMultiPeaks(
        InputWorkspace = 'diamondD',
        DReference = FinalDReference,
        FitwindowTableWorkspace='fitwinws',
        PeakFunction = "Gaussian",
        BackgroundType = "Linear",
        HighBackground = True,
        OutputWorkspace = 'offset',
        MaskWorkspace='mask')
SaveCalFile(Filename='/SNS/users/rwp/corelli/cal_2016_06/cal_Diamond_20482-9_sum16.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='mask')
maskNumberPeaksFitted = np.where(mtd['NumberPeaksFitted'].extractY() <3)
MaskDetectors('mask',DetectorList=maskNumberPeaksFitted[0])
SaveCalFile(Filename='/SNS/users/rwp/corelli/cal_2016_06/cal_Diamond_20482-9_sum16_mask_lt_3.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='mask')

# Set MaxChiSq. Default 100
for maxchisq in [0.5, 1, 2, 3, 5, 10, 20, 30, 50]:
        GetDetOffsetsMultiPeaks(
                InputWorkspace = 'diamondD',
                DReference = FinalDReference,
                FitwindowTableWorkspace='fitwinws',
                PeakFunction = "Gaussian",
                BackgroundType = "Linear",
                HighBackground = True,
                OutputWorkspace = 'offset',
                MaskWorkspace='mask',
                MaxChiSq=maxchisq)
        SaveCalFile(Filename='/SNS/users/rwp/corelli/cal_2016_06/cal_Diamond_20482-9_sum16_MaxChiSq'+str(maxchisq)+'.cal',
                    OffsetsWorkspace="offset",
                    MaskWorkspace='mask')
        maskNumberPeaksFitted = np.where(mtd['NumberPeaksFitted'].extractY() <3)
        MaskDetectors('mask',DetectorList=maskNumberPeaksFitted[0])
        SaveCalFile(Filename='/SNS/users/rwp/corelli/cal_2016_06/cal_Diamond_20482-9_sum16_mask_lt_3_MaxChiSq'+str(maxchisq)+'.cal',
                    OffsetsWorkspace="offset",
                    MaskWorkspace='mask')
