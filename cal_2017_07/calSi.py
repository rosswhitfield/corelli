files='CORELLI_47327' # CORELLI_47327:47334

wkpsName='out'

LoadEventAndCompress(Filename=files, OutputWorkspace=wkspName,
                                          MaxChunkSize=16, FilterBadPulses=25)
CropWorkspace(InputWorkspace=wkspName, OutputWorkspace=wkspName, XMin=300, XMax=16666.7)

dvalues = (1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353)

PDCalibration(SignalWorkspace=wkspName,
              TofBinning=[300,-.001,16666.7],
              PeakPositions=dvalues,
              StartFromObservedPeakCentre=True,
              OutputCalibrationTable='new_cal',
              CalibrationParameters='DIFC')
