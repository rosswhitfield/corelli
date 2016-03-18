from mantid.simpleapi import *
import numpy as np

# Generate fit window workspace
DReference = [2.7251,2.8904,4.2694,5.0063,8.1753]
fitwindict = {}
fitwindict[8.1753] = (7.5, 10.0)
fitwindict[5.0063] = (4.85,6.0)
fitwindict[4.2694] = (4.0, 4.9)
fitwindict[2.8904] = (2.82, 3.0)
fitwindict[2.7251] = (2.65, 2.81)
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

for run in range(20501,20509):
        LoadEventNexus(Filename='/SNS/CORELLI/IPTS-15796/nexus/CORELLI_'+str(run)+'.nxs.h5', OutputWorkspace='rawC60')
        LoadInstrument(Workspace="rawC60",Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",RewriteSpectraMap=False)
        SetInstrumentParameter(Workspace="rawC60",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
        ModeratorTzero(InputWorkspace="rawC60",OutputWorkspace="rawC60",EMode="Elastic")
        MaskBTP(Workspace='rawC60',Pixel="1-16,241-256")
        ConvertUnits(InputWorkspace='rawC60',OutputWorkspace='C60D',Target='dSpacing')
        Rebin(InputWorkspace='C60D',OutputWorkspace='C60D',Params='0.5,-0.004,10')
        SumNeighbours(InputWorkspace="C60D", OutputWorkspace="C60D", SumX=1, SumY=4)
        GetDetOffsetsMultiPeaks(
                InputWorkspace = 'C60D',
                DReference = FinalDReference,
                FitwindowTableWorkspace='fitwinws',
                PeakFunction = "Gaussian",
                BackgroundType = "Linear",
                HighBackground = True,
                OutputWorkspace = 'offset',
                MaskWorkspace='mask')
        # Save calibration
        SaveCalFile(Filename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_'+str(run)+'_sum4.cal',
                    OffsetsWorkspace="offset",
                    MaskWorkspace='mask')
        maskNumberPeaksFitted = np.where(mtd['NumberPeaksFitted'].extractY() <3)
        MaskDetectors('mask',DetectorList=maskNumberPeaksFitted[0])
        SaveCalFile(Filename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_'+str(run)+'_sum4_mask_lt_3.cal',
                    OffsetsWorkspace="offset",
                    MaskWorkspace='mask')

# Average
LoadEventNexus(Filename='/SNS/CORELLI/IPTS-15796/nexus/CORELLI_20501.nxs.h5', OutputWorkspace='rawC60')
LoadInstrument(Workspace="rawC60",Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",RewriteSpectraMap=False)
SetInstrumentParameter(Workspace="rawC60",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
ModeratorTzero(InputWorkspace="rawC60",OutputWorkspace="rawC60",EMode="Elastic")
for run in range(20502,20509):
        LoadEventNexus(Filename='/SNS/CORELLI/IPTS-15796/nexus/CORELLI_'+str(run)+'.nxs.h5', OutputWorkspace='rawC60_2')
        LoadInstrument(Workspace="rawC60_2",Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",RewriteSpectraMap=False)
        SetInstrumentParameter(Workspace="rawC60_2",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
        ModeratorTzero(InputWorkspace="rawC60_2",OutputWorkspace="rawC60_2",EMode="Elastic")
        Plus(LHSWorkspace="rawC60",RHSWorkspace="rawC60_2",OutputWorkspace="rawC60",ClearRHSWorkspace=True)

MaskBTP(Workspace='rawC60',Pixel="1-16,241-256")
ConvertUnits(InputWorkspace='rawC60',OutputWorkspace='C60D',Target='dSpacing')
Rebin(InputWorkspace='C60D',OutputWorkspace='C60D',Params='0.5,-0.004,10')
SumNeighbours(InputWorkspace="C60D", OutputWorkspace="C60D", SumX=1, SumY=4)
GetDetOffsetsMultiPeaks(
        InputWorkspace = 'C60D',
        DReference = FinalDReference,
        FitwindowTableWorkspace='fitwinws',
        PeakFunction = "Gaussian",
        BackgroundType = "Linear",
        HighBackground = True,
        OutputWorkspace = 'offset',
        MaskWorkspace='mask')
# Save calibration
SaveCalFile(Filename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_20501-8_sum4.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='mask')
maskNumberPeaksFitted = np.where(mtd['NumberPeaksFitted'].extractY() <3)
MaskDetectors('mask',DetectorList=maskNumberPeaksFitted[0])
SaveCalFile(Filename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_20501-8_sum4_mask_lt_3.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='mask')

# L1 = 20.03
LoadEventNexus(Filename='/SNS/CORELLI/IPTS-15796/nexus/CORELLI_20501.nxs.h5', OutputWorkspace='rawC60')
LoadInstrument(Workspace="rawC60",Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",RewriteSpectraMap=False)
MoveInstrumentComponent(Workspace='rawC60',ComponentName='moderator',Z=-20.03,RelativePosition=False)
SetInstrumentParameter(Workspace="rawC60",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
ModeratorTzero(InputWorkspace="rawC60",OutputWorkspace="rawC60",EMode="Elastic")
for run in range(20502,20509):
        LoadEventNexus(Filename='/SNS/CORELLI/IPTS-15796/nexus/CORELLI_'+str(run)+'.nxs.h5', OutputWorkspace='rawC60_2')
        LoadInstrument(Workspace="rawC60_2",Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",RewriteSpectraMap=False)
        MoveInstrumentComponent(Workspace='rawC60_2',ComponentName='moderator',Z=-20.03,RelativePosition=False)
        SetInstrumentParameter(Workspace="rawC60_2",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
        ModeratorTzero(InputWorkspace="rawC60_2",OutputWorkspace="rawC60_2",EMode="Elastic")
        Plus(LHSWorkspace="rawC60",RHSWorkspace="rawC60_2",OutputWorkspace="rawC60",ClearRHSWorkspace=True)

MaskBTP(Workspace='rawC60',Pixel="1-16,241-256")
ConvertUnits(InputWorkspace='rawC60',OutputWorkspace='C60D',Target='dSpacing')
Rebin(InputWorkspace='C60D',OutputWorkspace='C60D',Params='0.5,-0.004,10')
SumNeighbours(InputWorkspace="C60D", OutputWorkspace="C60D", SumX=1, SumY=4)
GetDetOffsetsMultiPeaks(
        InputWorkspace = 'C60D',
        DReference = FinalDReference,
        FitwindowTableWorkspace='fitwinws',
        PeakFunction = "Gaussian",
        BackgroundType = "Linear",
        HighBackground = True,
        OutputWorkspace = 'offset',
        MaskWorkspace='mask')
# Save calibration
SaveCalFile(Filename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_20501-8_sum4_L1_20.03.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='mask')
maskNumberPeaksFitted = np.where(mtd['NumberPeaksFitted'].extractY() <3)
MaskDetectors('mask',DetectorList=maskNumberPeaksFitted[0])
SaveCalFile(Filename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_20501-8_sum4_mask_lt_3_L1_20.03.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='mask')


# Save every spectra
c60d=mtd['C60D']
x=c60d.readX(0)
for s in range(c60d.getNumberHistograms()):
        if c60d.getSpectrum(s).getNumberEvents() == 0:
                continue
        y=c60d.readY(s)
        np.savetxt('c60d/c60d_'+str(s)+'.txt',np.transpose([x[:-1],y]))

#for s in range(c60d.getNumberHistograms()):
for s in range(55000):
        print s,c60d.getSpectrum(s).getDetectorIDs()

# L1 = 20.03 MaxChiSq=5
LoadEventNexus(Filename='/SNS/CORELLI/IPTS-15796/nexus/CORELLI_20501.nxs.h5', OutputWorkspace='rawC60')
LoadInstrument(Workspace="rawC60",Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",RewriteSpectraMap=False)
MoveInstrumentComponent(Workspace='rawC60',ComponentName='moderator',Z=-20.03,RelativePosition=False)
SetInstrumentParameter(Workspace="rawC60",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
ModeratorTzero(InputWorkspace="rawC60",OutputWorkspace="rawC60",EMode="Elastic")
for run in range(20502,20509):
        LoadEventNexus(Filename='/SNS/CORELLI/IPTS-15796/nexus/CORELLI_'+str(run)+'.nxs.h5', OutputWorkspace='rawC60_2')
        LoadInstrument(Workspace="rawC60_2",Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",RewriteSpectraMap=False)
        MoveInstrumentComponent(Workspace='rawC60_2',ComponentName='moderator',Z=-20.03,RelativePosition=False)
        SetInstrumentParameter(Workspace="rawC60_2",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
        ModeratorTzero(InputWorkspace="rawC60_2",OutputWorkspace="rawC60_2",EMode="Elastic")
        Plus(LHSWorkspace="rawC60",RHSWorkspace="rawC60_2",OutputWorkspace="rawC60",ClearRHSWorkspace=True)

MaskBTP(Workspace='rawC60',Pixel="1-16,241-256")
ConvertUnits(InputWorkspace='rawC60',OutputWorkspace='C60D',Target='dSpacing')
Rebin(InputWorkspace='C60D',OutputWorkspace='C60D',Params='0.5,-0.004,10')
SumNeighbours(InputWorkspace="C60D", OutputWorkspace="C60D", SumX=1, SumY=4)
GetDetOffsetsMultiPeaks(
        InputWorkspace = 'C60D',
        DReference = FinalDReference,
        FitwindowTableWorkspace='fitwinws',
        PeakFunction = "Gaussian",
        BackgroundType = "Linear",
        HighBackground = True,
        OutputWorkspace = 'offset',
        MaskWorkspace='mask',
        MaxChiSq=5)
# Save calibration
SaveCalFile(Filename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_20501-8_sum4_L1_20.03_MaxChiSq_5.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='mask')
maskNumberPeaksFitted = np.where(mtd['NumberPeaksFitted'].extractY() <3)
MaskDetectors('mask',DetectorList=maskNumberPeaksFitted[0])
SaveCalFile(Filename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_20501-8_sum4_mask_lt_3_L1_20.03_MaxChiSq_5.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='mask')
