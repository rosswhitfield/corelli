from mantid.simpleapi import *

SNSPowderReduction(Filename="CORELLI_101848,CORELLI_101849",
                   BackgroundNumber=-1,
                   VanadiumNumber=96959,
                   VanadiumBackgroundNumber=-1,
                   CalibrationFile="/SNS/CORELLI/IPTS-22673/shared/mantid_reduce/calibration/CORELLI_d56271_2017_11_17_CCR.h5",
                   Binning='0.1,0.002,15',
                   CropWavelengthMin=0.7,
                   CropWavelengthMax=2.5,
                   StripVanadiumPeaks=False,
                   GroupingFile="/SNS/users/rwp/corelli/IPTS-23542-powder/group_31-57.xml",
                   OutputFilePrefix="31-57_multi_",
                   SaveAs='fullprof,nexus',
                   OutputDirectory="/SNS/users/rwp/corelli/IPTS-23542-powder/")
