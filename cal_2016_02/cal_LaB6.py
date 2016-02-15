from mantid.simpleapi import *

LoadEventNexus(Filename='/SNS/CORELLI/IPTS-15796/nexus/CORELLI_19286.nxs.h5', OutputWorkspace='rawLaB6')
LoadInstrument(Workspace="rawLaB6",Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",RewriteSpectraMap=False)
SetInstrumentParameter(Workspace="rawLaB6",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
ModeratorTzero(InputWorkspace="rawLaB6",OutputWorkspace="rawLaB6",EMode="Elastic")

LoadEventNexus(Filename='/SNS/CORELLI/IPTS-15796/nexus/CORELLI_19287.nxs.h5', OutputWorkspace='rawLaB62')
LoadInstrument(Workspace="rawLaB62",Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",RewriteSpectraMap=False)
SetInstrumentParameter(Workspace="rawLaB62",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
ModeratorTzero(InputWorkspace="rawLaB62",OutputWorkspace="rawLaB62",EMode="Elastic")
Plus(LHSWorkspace="rawLaB6",RHSWorkspace="rawLaB62",OutputWorkspace="rawLaB6",ClearRHSWorkspace=True)

MaskBTP(Workspace='rawLaB6',Pixel="1-16,241-256")

ConvertUnits(InputWorkspace='rawLaB6',OutputWorkspace='LaBD',Target='dSpacing')
Rebin(InputWorkspace='LaBD',OutputWorkspace='LaBD',Params='0.5,-0.004,5')

# Generate fit window workspace
DReference=[1.2000, 1.3146, 1.3857, 1.6971, 1.8591, 2.0785, 2.4000, 2.9394, 4.1570]
fitwindict = {}
fitwindict[4.1570] = (3.85, 4.45)
fitwindict[2.9394] = (2.78, 3.15)
fitwindict[2.4000] = (2.28, 2.55)
fitwindict[2.0785] = (2.01, 2.17)
fitwindict[1.8591] = (1.81, 1.92)
fitwindict[1.6971] = (1.65, 1.75)
fitwindict[1.3857] = (1.355, 1.435)
fitwindict[1.3146] = (1.29, 1.35)
fitwindict[1.2000] = (1.182, 1.22)
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

SumNeighbours(InputWorkspace="LaBD", OutputWorkspace="LaBD", SumX=1, SumY=4)
GetDetOffsetsMultiPeaks(
        InputWorkspace = 'LaBD',
        DReference = FinalDReference, 
        FitwindowTableWorkspace='fitwinws',
        PeakFunction = "Gaussian",
        BackgroundType = "Linear",
        HighBackground = True,
        OutputWorkspace = 'offset',
        MaskWorkspace='mask')

# Save calibration
SaveCalFile(Filename='/SNS/users/rwp/cal_2016_02/cal_LaB6_19286_19287_sum4.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='mask')
