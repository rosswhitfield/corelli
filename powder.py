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

SNSPowderReduction(Filename=runs,
                   Sum=True,
                   VanadiumNumber='28119',
                   CalibrationFile='/SNS/users/rwp/cor_cal.h5',
                   Binning='0.1,-0.001,6',
                   SaveAs='fullprof',
                   OutputDirectory='/SNS/users/rwp/temp2/',
                   FrequencyLogNames="BL9:Chop:Skf1:SetSpeed",
                   WaveLengthLogNames="BL9:Chop:Skf23:CenterWavelength")

PropertyManagerDataService.remove("__pd_reduction_properties")
PDDetermineCharacterizations(InputWorkspace='CORELLI_32307.nxs',
FrequencyLogNames="BL9:Chop:Skf1:SpeedSet,BL9:Chop:Skf1:MotorSpeed,frequency",
WaveLengthLogNames="BL9:Chop:Skf23:CenterWavelength")
char=PropertyManagerDataService.retrieve("__pd_reduction_properties")
print char.getPropertyValue('frequency')
print char.getPropertyValue('wavelength')

