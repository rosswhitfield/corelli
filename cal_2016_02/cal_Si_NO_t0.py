from mantid.simpleapi import *

LoadEventNexus(Filename='/SNS/CORELLI/IPTS-15796/nexus/CORELLI_19284.nxs.h5', OutputWorkspace='rawSi')
LoadInstrument(Workspace="rawSi",Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",RewriteSpectraMap=False)

LoadEventNexus(Filename='/SNS/CORELLI/IPTS-15796/nexus/CORELLI_19285.nxs.h5', OutputWorkspace='rawSi2')
LoadInstrument(Workspace="rawSi2",Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",RewriteSpectraMap=False)
Plus(LHSWorkspace="rawSi",RHSWorkspace="rawSi2",OutputWorkspace="rawSi",ClearRHSWorkspace=True)

MaskBTP(Workspace='rawSi',Pixel="1-16,241-256")

ConvertUnits(InputWorkspace='rawSi',OutputWorkspace='siliconD',Target='dSpacing')
Rebin(InputWorkspace='siliconD',OutputWorkspace='siliconD',Params='0.5,-0.004,3.5')

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

SumNeighbours(InputWorkspace="siliconD", OutputWorkspace="siliconD", SumX=1, SumY=4)
GetDetOffsetsMultiPeaks(
        InputWorkspace = 'siliconD',
        DReference = FinalDReference, 
        FitwindowTableWorkspace='fitwinws',
        PeakFunction = "Gaussian",
        BackgroundType = "Linear",
        HighBackground = True,
        OutputWorkspace = 'offset',
        MaskWorkspace='mask')

# Save calibration
SaveCalFile(Filename='/SNS/users/rwp/corelli/cal_2016_02/cal_Si_19284_19285_sum4_NO_t0.cal',
            OffsetsWorkspace="offset",
            MaskWorkspace='mask')
