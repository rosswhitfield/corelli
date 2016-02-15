from mantid.simpleapi import *

# Calibration for Corelli

# Load data and process 
LoadEventNexus(Filename='/SNS/CORELLI/IPTS-12310/nexus/CORELLI_4597.nxs.h5', OutputWorkspace='COR_4597')
LoadInstrument(Workspace="COR_4597",Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",RewriteSpectraMap=False)
RotateInstrumentComponent('COR_4597', 'bank58', X=0,Y=1,Z=0,Angle=0.23, RelativeRotation=False)
RotateInstrumentComponent('COR_4597', 'bank59', X=0,Y=1,Z=0,Angle=-0.10, RelativeRotation=False)
SetInstrumentParameter(Workspace="COR_4597",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
ModeratorTzero(InputWorkspace="COR_4597",OutputWorkspace="COR_4597",EMode="Elastic")
MaskBTP(Workspace="COR_4597",Pixel="1-15,242-256")

ConvertUnits(InputWorkspace='COR_4597', OutputWorkspace='COR_4597_d', Target='dSpacing')
Rebin(InputWorkspace='COR_4597_d', OutputWorkspace='COR_4597_d', Params='0.5, -0.004, 10')

# Generate fit window workspace
sourcews = mtd["COR_4597"]
#DReference = [0.9179, 0.9600, 1.0451, 1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353]
DReference = [2.7251,2.8904,4.2694,5.0063,8.1753]
fitwindict = {}
fitwindict[8.1753] = (7.5, 10.0)
fitwindict[5.0063] = (4.85,6.0)
fitwindict[4.2694] = (4.0, 4.9)
fitwindict[2.8904] = (2.82, 3.0)
fitwindict[2.7251] = (2.65, 2.81)
FinalDReference = sorted(fitwindict.keys())


numspec = sourcews.getNumberHistograms()

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

"""
for iws in xrange(numspec):
	row[0] = iws
	fitwinws.addRow(row)
"""
fitwinws.addRow(row)

# Calculate offsets
SumNeighbours(InputWorkspace="COR_4597_d", OutputWorkspace="COR_4597_d", SumX=2, SumY=2)

GetDetOffsetsMultiPeaks(
        InputWorkspace = "COR_4597_d",
        DReference = FinalDReference,
	FitwindowTableWorkspace=fitwinws,
        PeakFunction = "Gaussian",
        BackgroundType = "Linear",
        HighBackground = True,
        MaskWorkspace = "COR_4597_mask",
        OutputWorkspace = "COR_4597_offset")
	
SaveCalFile(Filename="/SNS/users/rwp/corelli/new_cal/c60_sn_rotate_bank_58_59.cal",OffsetsWorkspace="COR_4597_offset",MaskWorkspace="COR_4597_mask")
#MaskDetectors(Workspace='COR_4597_offset', MaskedWorkspace='COR_4597_mask')
#SaveNexus(InputWorkspace="COR_4597_mask",FileName="/SNS/users/rwp/cal/COR_4597_mask.nxs")
# Check
#AlignDetectors(InputWorkspace='COR_4597', OutputWorkspace='COR_4597_Aligned', OffsetsWorkspace='COR_4597_offset')
#Rebin(InputWorkspace='COR_4597_Aligned', OutputWorkspace='COR_4597_Aligned', Params='0.5, -0.004, 10')
