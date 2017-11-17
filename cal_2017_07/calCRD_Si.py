from mantid.simpleapi import CalibrateRectangularDetectors

dvalues = [1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353]



CalibrateRectangularDetectors(RunNumber="CORELLI_47327",
                              Binning="0.5,-0.004,3.5",
                              YPixelSum=16,
                              PeakPositions=dvalues,
                              # control the peak fitting
                              MaxOffset=0.05,
                              CrossCorrelation=False,
                              PeakWindowMax=0.1,
                              # what function to fit with
                              BackgroundType="Flat",
                              PeakFunction="Gaussian",
                              # how to save the results
                              SaveAs="calibration",
                              OutputDirectory="/tmp")
