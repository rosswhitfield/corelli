from mantid.simpleapi import *
inputdir='/SNS/CORELLI/shared/Silicon/'


iws='rawSi'
ows='rawSi_Aigned'
offsetws='rawSi_offset'


MaskName='Run14324_Mask'

LoadEventNexus(Filename='/SNS/CORELLI/IPTS-12310/nexus/CORELLI_14324.nxs.h5', OutputWorkspace='rawSi')
LoadInstrument(Workspace="rawSi",Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",RewriteSpectraMap=False)
SetInstrumentParameter(Workspace="rawSi",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
ModeratorTzero(InputWorkspace="rawSi",OutputWorkspace="rawSi",EMode="Elastic")

LoadEventNexus(Filename='/SNS/CORELLI/IPTS-12310/nexus/CORELLI_14325.nxs.h5', OutputWorkspace='rawSi2')
LoadInstrument(Workspace="rawSi2",Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",RewriteSpectraMap=False)
SetInstrumentParameter(Workspace="rawSi2",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
ModeratorTzero(InputWorkspace="rawSi2",OutputWorkspace="rawSi2",EMode="Elastic")
Plus(LHSWorkspace="rawSi",RHSWorkspace="rawSi2",OutputWorkspace="rawSi",ClearRHSWorkspace=True)

LoadEventNexus(Filename='/SNS/CORELLI/IPTS-12310/nexus/CORELLI_14326.nxs.h5', OutputWorkspace='rawSi3')
LoadInstrument(Workspace="rawSi3",Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",RewriteSpectraMap=False)
SetInstrumentParameter(Workspace="rawSi3",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
ModeratorTzero(InputWorkspace="rawSi3",OutputWorkspace="rawSi3",EMode="Elastic")
Plus(LHSWorkspace="rawSi",RHSWorkspace="rawSi3",OutputWorkspace="rawSi",ClearRHSWorkspace=True)

# Define variables
rawSi = mtd['rawSi']


MaskBTP(Workspace=rawSi,Pixel="1-15,242-256")
MaskBTP(Workspace=rawSi,Bank="58",Tube="13-16",Pixel="80-130")
MaskBTP(Workspace=rawSi,Bank="59",Tube="1-4",Pixel="80-130")
MaskBTP(Workspace=rawSi,Bank="73",Tube="13")
MaskBTP(Workspace=rawSi,Bank="74",Tube="2")

siliconD=ConvertUnits(rawSi,Target='dSpacing')
siliconD=Rebin(InputWorkspace=siliconD,Params='0.5,-0.004,3.5')

# Generate fit window workspace
sourcews = mtd["siliconD"]
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

SumNeighbours(InputWorkspace="siliconD", OutputWorkspace="siliconD", SumX=1, SumY=8)
siliconD =  mtd['siliconD']
MaskName='Run14324_Mask'
offsetws_name = 'rawSi_offset'
GetDetOffsetsMultiPeaks(
        InputWorkspace = siliconD,
        DReference = FinalDReference, 
        FitwindowTableWorkspace='fitwinws',
        PeakFunction = "Gaussian",
        BackgroundType = "Linear",
        HighBackground = True,
        OutputWorkspace = offsetws_name,
        MaskWorkspace=MaskName)

# Save calibration
SaveCalFile(Filename='/SNS/users/rwp/new_cal/cal_run14324_sn8.dat',
        OffsetsWorkspace="rawSi_offset",
        MaskWorkspace=MaskName)
