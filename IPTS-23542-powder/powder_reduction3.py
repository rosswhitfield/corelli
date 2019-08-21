from mantid.simpleapi import *

SNSPowderReduction(Filename="CORELLI_101847",
                   PreserveEvents=True,
                   BackgroundNumber=-1,
                   VanadiumNumber=-1,
                   VanadiumBackgroundNumber=-1,
                   CalibrationFile="/SNS/CORELLI/IPTS-22673/shared/mantid_reduce/calibration/CORELLI_d56271_2017_11_17_CCR.h5",
                   Binning='0.1,-0.002,15',
                   StripVanadiumPeaks=False,
                   GroupingFile="/SNS/users/rwp/corelli/IPTS-23542-powder/group_bank.xml",
                   OutputFilePrefix="output3_",
                   SaveAs='fullprof,gsas,nexus,pdfgetn,topas',
                   OutputDirectory="/SNS/users/rwp/corelli/IPTS-23542-powder/")
