from mantid.simpleapi import *

COMPRESS_TOL_TOF = .01

filename = '/SNS/CORELLI/IPTS-19545/nexus/CORELLI_47327.nxs.h5'
wksp = samRun = wkspName = 'CORELLI_47327'

dvalues = [1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353]


LoadEventNexus(Filename=filename, OutputWorkspace=wkspName, Precount=False)
FilterBadPulses(InputWorkspace=wkspName, OutputWorkspace=wkspName)
CompressEvents(InputWorkspace=wkspName, OutputWorkspace=wkspName, Tolerance=COMPRESS_TOL_TOF)

(_, numGroupedSpectra, numGroups) = CreateGroupingWorkspace(InputWorkspace=wkspName,
                                                            GroupDetectorsBy="All",
                                                            OutputWorkspace=wkspName+"group")


ConvertUnits(InputWorkspace=samRun, OutputWorkspace=samRun, Target="dSpacing")

SumNeighbours(InputWorkspace=samRun, OutputWorkspace=samRun, SumX=1, SumY=16)

Rebin(InputWorkspace=wksp, OutputWorkspace=wksp, Params="0.5,-0.004,3.5")


GetDetOffsetsMultiPeaks(InputWorkspace=wksp,
                        OutputWorkspace=wksp+"offset",
                        DReference=dvalues,
                        FitWindowMaxWidth=0.1,
                        MinimumPeakHeight=2,
                        MinimumPeakHeightObs=0,
                        BackgroundType="Flat",
                        MaxOffset=0.05,
                        NumberPeaksWorkspace=wksp+"peaks",
                        MaskWorkspace=wksp+"mask",
                        InputResolutionWorkspace=resws,
                        MinimumResolutionFactor=0,
                        MaximumResolutionFactor=0)
