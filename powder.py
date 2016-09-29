LoadEmptyInstrument(Filename='/SNS/users/rwp/CORELLI_Definition_91.07cm.xml',OutputWorkspace='cor')
PDCalibration(SignalWorkspace='cor',TofBinning='1,1,100',PeakPositions='1.0,2.0',OutputCalibrationTable='cal')
SaveDiffCal(CalibrationWorkspace='cal', Filename='/SNS/users/rwp/cor_cal.h5')

runs = ''
for run in range(32307,32329):
    runs += 'CORELLI_'+str(run)+','
runs = runs[:-1]
print runs

SNSPowderReduction(Filename=runs,
                   Sum=False,
                   VanadiumNumber='28119',
                   CalibrationFile='/SNS/users/rwp/cor_cal.h5',
                   Binning='0.1,-0.001,6',
                   SaveAs='fullprof',
                   OutputDirectory='/SNS/users/rwp/temp/')

MergeRuns(InputWorkspaces='CORELLI_32307,CORELLI_32308,CORELLI_32309,CORELLI_32310,CORELLI_32311,CORELLI_32312,CORELLI_32313,CORELLI_32314,CORELLI_32315,CORELLI_32316,CORELLI_32317,CORELLI_32318,CORELLI_32319,CORELLI_32320,CORELLI_32321,CORELLI_32322,CORELLI_32323,CORELLI_32324,CORELLI_32325,CORELLI_32326,CORELLI_32327,CORELLI_32328', OutputWorkspace='sumed')


"""
SNSPowderReduction(Filename=runs,
                   Sum=True,
                   VanadiumNumber='28119',
                   CalibrationFile='/SNS/users/rwp/cor_cal.h5',
                   Binning='0.1,-0.001,6',
                   SaveAs='fullprof',
                   OutputDirectory='/SNS/users/rwp/temp2/')
"""
