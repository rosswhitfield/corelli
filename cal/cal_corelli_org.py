# Calibration for Corelli

# Load data and process 
LoadEventNexus(Filename='CORELLI_687.nxs.h5', OutputWorkspace='COR_687')
ChangeBinOffset(InputWorkspace='COR_687', OutputWorkspace='COR_687', Offset='500', IndexMin='237568', IndexMax='249855')
ConvertUnits(InputWorkspace='COR_687', OutputWorkspace='COR_687_d', Target='dSpacing')
Rebin(InputWorkspace='COR_687_d', OutputWorkspace='COR_687_d', Params='0.5, -0.004, 3.5')

# Generate fit window workspace
sourcews = mtd["COR_687"]
DReference = [0.9179, 0.9600, 1.0451, 1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353]
fitwindict = {}
fitwindict[3.1353] = (3.01, 3.33)
fitwindict[1.9200] = (1.88, 2.00)
fitwindict[1.6374] = (1.60, 1.70)
fitwindict[1.3576] = (1.34, 1.39)
fitwindict[1.2458] = (1.22, 1.27)
fitwindict[1.1085] = (1.08, 1.14)
FinalDReference = sorted(fitwindict.keys())


numspec = sourcews.getNumberHistograms()

fitwinws = CreateEmptyTableWorkspace()
fitwinws.addColumn("int", "spectrum")
for ipk in xrange(len(FinalDReference)):
	fitwinws.addColumn("double", "Peak_%d_Left"%(ipk))
	fitwinws.addColumn("double", "Peak_%d_Right"%(ipk))

row = [0]
for refpeak in FinalDReference:
		leftbound = fitwindict[refpeak][0]
		rightbound = fitwindict[refpeak][1]
		row.append(leftbound)
		row.append(rightbound)

for iws in xrange(numspec):
	row[0] = iws
	fitwinws.addRow(row)
	
# Calculate offsets
GetDetOffsetsMultiPeaks(
        InputWorkspace = "COR_687_d",
        DReference = FinalDReference,
	FitwindowTableWorkspace=fitwinws,
        PeakFunction = "Gaussian",
        BackgroundType = "Linear",
        HighBackground = True,
        OutputWorkspace = "COR_687_offset")
	
# Check
AlignDetectors(InputWorkspace='COR_687', OutputWorkspace='COR_687_Aligned', OffsetsWorkspace='COR_687_offset')
Rebin(InputWorkspace='COR_687_Aligned', OutputWorkspace='COR_687_Aligned', Params='0.5, -0.004, 3.5')
