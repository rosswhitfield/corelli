# Calibration for Corelli
# NAC
# Load data and process 
LoadEventNexus(Filename='/SNS/CORELLI/IPTS-12008/nexus/CORELLI_549.nxs.h5', OutputWorkspace='COR_549')
ChangeBinOffset(InputWorkspace='COR_549', OutputWorkspace='COR_549', Offset='500', IndexMin='237568', IndexMax='249855')
ConvertUnits(InputWorkspace='COR_549', OutputWorkspace='COR_549_d', Target='dSpacing')
Rebin(InputWorkspace='COR_549_d', OutputWorkspace='COR_549_d', Params='1, -0.004, 6')

# Generate fit window workspace
sourcews = mtd["COR_549"]
#DReference = [0.9179, 0.9600, 1.0451, 1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353]
#DReference = [1.0058, 1.0156, 1.0257, 1.0361, 1.0469, 1.0579, 1.0812, 1.0934, 1.1060, 1.1191, 1.1327, 1.1468, 1.1614, 1.1766, 1.1924, 1.2088, 1.2259, 1.2438, 1.2625, 1.2821, 1.3026, 1.3468, 1.3706, 1.3958, 1.4224, 1.4506, 1.4805, 1.5123, 1.5463, 1.5827, 1.6218, 1.6639, 1.7095, 1.7591, 1.8132, 1.8727, 2.0116, 2.0937, 2.1868, 2.2935, 2.4176, 2.5642, 2.7413, 2.9609, 3.2435, 3.6264, 4.1874, 5.1285, 7.2528]
DReference = [1.0579, 1.1060, 1.3026, 1.6639, 1.8132, 1.8727, 2.0116, 2.1868, 3.6264, 4.1874, 5.1285]

fitwindict = {}
DReference = [1.0579, 1.1060, 1.3026, 1.6639, 1.8132, 1.8727, 2.0116, 2.1868, 3.6264, 4.1874, 5.1285]
fitwindict[1.0579] = (1.05,1.08)
fitwindict[1.1060] = (1.09,1.13)
fitwindict[1.3026] = (1.28,1.33)
fitwindict[1.6639] = (1.64,1.70)
fitwindict[1.8132] = (1.79,1.85)
fitwindict[1.8727] = (1.85,1.92)
fitwindict[2.0116] = (1.98,2.08)
fitwindict[2.1868] = (2.15,2.25)
fitwindict[3.6264] = (3.4,3.9)
fitwindict[4.1874] = (4,4.5)
fitwindict[5.1285] = (4.8,5.6)
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
        InputWorkspace = "COR_549_d",
        DReference = FinalDReference,
	FitwindowTableWorkspace=fitwinws,
        PeakFunction = "Gaussian",
        BackgroundType = "Linear",
        HighBackground = True,
        OutputWorkspace = "COR_549_offset")
	
# Check
AlignDetectors(InputWorkspace='COR_549', OutputWorkspace='COR_549_Aligned', OffsetsWorkspace='COR_549_offset')
Rebin(InputWorkspace='COR_549_Aligned', OutputWorkspace='COR_549_Aligned', Params='1, -0.004, 7')


