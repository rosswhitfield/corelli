from mantid.simpleapi import *
import numpy as np

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

for run in range(20492,20500):
        LoadEventNexus(Filename='/SNS/CORELLI/IPTS-15796/nexus/CORELLI_'+str(run)+'.nxs.h5', OutputWorkspace='rawSi')
        LoadInstrument(Workspace="rawSi",Filename="/SNS/users/rwp/CORELLI_Definition_91.07cm.xml",RewriteSpectraMap=False)
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
        SaveCalFile(Filename='/SNS/users/rwp/corelli/cal_2016_06/cal_Si_'+str(run)+'_sum16.cal',
                    OffsetsWorkspace="offset",
                    MaskWorkspace='mask')
        maskNumberPeaksFitted = np.where(mtd['NumberPeaksFitted'].extractY() <3)
        MaskDetectors('mask',DetectorList=maskNumberPeaksFitted[0])
        SaveCalFile(Filename='/SNS/users/rwp/corelli/cal_2016_06/cal_Si_'+str(run)+'_sum16_mask_lt_3.cal',
                    OffsetsWorkspace="offset",
                    MaskWorkspace='mask')

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
SaveCalFile(Filename='/SNS/users/rwp/corelli/cal_2016_06/cal_Si_20492-9_sum16.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='mask')
maskNumberPeaksFitted = np.where(mtd['NumberPeaksFitted'].extractY() <3)
MaskDetectors('mask',DetectorList=maskNumberPeaksFitted[0])
SaveCalFile(Filename='/SNS/users/rwp/corelli/cal_2016_06/cal_Si_20492-9_sum16_mask_lt_3.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='mask')

# Set MaxChiSq. Default 100
for maxchisq in [0.5, 1, 2, 3, 5, 10, 20, 30, 50]:
        GetDetOffsetsMultiPeaks(
		InputWorkspace = 'siliconD',
                DReference = FinalDReference,
                FitwindowTableWorkspace='fitwinws',
                PeakFunction = "Gaussian",
                BackgroundType = "Linear",
                HighBackground = True,
                OutputWorkspace = 'offset',
                MaskWorkspace='mask',
                MaxChiSq=maxchisq)
	SaveCalFile(Filename='/SNS/users/rwp/corelli/cal_2016_06/cal_Si_20492-9_sum16_MaxChiSq'+str(maxchisq)+'.cal',
                    OffsetsWorkspace="offset",
                    MaskWorkspace='mask')
        maskNumberPeaksFitted = np.where(mtd['NumberPeaksFitted'].extractY() <3)
        MaskDetectors('mask',DetectorList=maskNumberPeaksFitted[0])
        SaveCalFile(Filename='/SNS/users/rwp/corelli/cal_2016_06/cal_Si_20492-9_sum16_mask_lt_3_MaxChiSq'+str(maxchisq)+'.cal',
                    OffsetsWorkspace="offset",
                    MaskWorkspace='mask')
