from mantid.simpleapi import *

runNumber = 47327

binning = "0.5,-0.004,3.5"

outDir='/tmp/'

filename = '/SNS/CORELLI/IPTS-19545/nexus/CORELLI_{}.nxs.h5'.format(runNumber)
wksp = 'CORELLI_{}'.format(runNumber)

calib = "CORELLI_calibrate_d_{}".format(runNumber)

outfile = outDir + calib

dvalues = [1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353]

LoadEventNexus(Filename=filename, OutputWorkspace=wksp, Precount=False)
FilterBadPulses(InputWorkspace=wksp, OutputWorkspace=wksp)
CompressEvents(InputWorkspace=wksp, OutputWorkspace=wksp, Tolerance=0.01)

ConvertUnits(InputWorkspace=wksp, OutputWorkspace=wksp, Target="dSpacing")

SumNeighbours(InputWorkspace=wksp, OutputWorkspace=wksp, SumX=1, SumY=16)

Rebin(InputWorkspace=wksp, OutputWorkspace=wksp, Params=binning)


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
                        MinimumResolutionFactor=0,
                        MaximumResolutionFactor=0)


SaveCalFile(OffsetsWorkspace=wksp+"offset",
            GroupingWorkspace=wksp+"group",
            MaskWorkspace=wksp+"mask",
            Filename=outfile+'.cal')
ConvertDiffCal(OffsetsWorkspace=wksp+"offset",
               OutputWorkspace=wksp+"cal")
SaveDiffCal(CalibrationWorkspace=wksp+"cal",
            GroupingWorkspace=wksp+"group",
            MaskWorkspace=wksp+"mask",
            Filename=outfile+'.h5')



# Test cal

LoadEventNexus(Filename=filename, OutputWorkspace=wksp, Precount=False)
FilterBadPulses(InputWorkspace=wksp, OutputWorkspace=wksp)
CompressEvents(InputWorkspace=wksp, OutputWorkspace=wksp, Tolerance=0.01)

MaskDetectors(Workspace=wksp, MaskedWorkspace=str(wksp)+"mask")
AlignDetectors(InputWorkspace=wksp, OutputWorkspace=wksp+'_calab',
                      CalibrationWorkspace=str(wksp)+"cal")
DiffractionFocussing(InputWorkspace=wksp+'_calab', OutputWorkspace=wksp+'_calab',
                            GroupingWorkspace=str(wksp)+"group")
Rebin(InputWorkspace=wksp+'_calab', OutputWorkspace=wksp+'_calab', Params=binning)

ConvertUnits(InputWorkspace=wksp, OutputWorkspace=wksp, Target="dSpacing")
Rebin(InputWorkspace=wksp, OutputWorkspace=wksp, Params=binning)
DiffractionFocussing(InputWorkspace=wksp, OutputWorkspace=wksp+'_d',
                     GroupingWorkspace=str(wksp)+"group")
