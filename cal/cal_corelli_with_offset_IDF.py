# Calibration for Corelli

# Load data and process 
LoadEventNexus(Filename='CORELLI_525.nxs.h5', OutputWorkspace='COR_525')
LoadInstrument(Workspace='COR_525',Filename='/SNS/users/rwp/CORELLI_Definition_offset_fix.xml',RewriteSpectraMap=0)
ChangeBinOffset(InputWorkspace='COR_525', OutputWorkspace='COR_525', Offset='500', IndexMin='237568', IndexMax='249855')
ConvertUnits(InputWorkspace='COR_525', OutputWorkspace='COR_525_d', Target='dSpacing')
Rebin(InputWorkspace='COR_525_d', OutputWorkspace='COR_525_d', Params='0.5, -0.004, 3.5')

# Generate fit window workspace
sourcews = mtd["COR_525"]
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
        InputWorkspace = "COR_525_d",
        DReference = FinalDReference,
	FitwindowTableWorkspace=fitwinws,
        PeakFunction = "Gaussian",
        BackgroundType = "Linear",
        HighBackground = True,
        OutputWorkspace = "COR_525_offset")
	
# Check
AlignDetectors(InputWorkspace='COR_525', OutputWorkspace='COR_525_Aligned', OffsetsWorkspace='COR_525_offset')
Rebin(InputWorkspace='COR_525_Aligned', OutputWorkspace='COR_525_Aligned', Params='0.5, -0.004, 3.5')
