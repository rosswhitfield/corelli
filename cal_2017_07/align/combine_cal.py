from mantid.simpleapi import LoadDiffCal, mtd, LoadEmptyInstrument, CalculateDIFC
import matplotlib.pyplot as plt
import tube

tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration/CalibTableNew.txt')

corelli = LoadEmptyInstrument(InstrumentName='CORELLI')
corelli = CalculateDIFC(corelli)
difc0 = corelli.extractY().flatten()
ApplyCalibration('corelli','CalibTable')
corelli = CalculateDIFC(corelli)
difc = corelli.extractY().flatten()

#plt.plot(difc/difc0)
#plt.show()

LoadDiffCal(Filename='../cal_Si_C60/cal_Si2_47327-47334_TubeCal_sum16_mask_lt_3.cal',
            InstrumentName='CORELLI',
            WorkspaceName='si')

LoadDiffCal(Filename='../cal_Si_C60/cal_C60_2_47367-47382_TubeCal_sum16_mask_lt_3.h5',
            InstrumentName='CORELLI',
            WorkspaceName='c60')

si=mtd['si_cal']
c60=mtd['c60_cal']

plt.plot(corelli.extractY())
plt.plot(si.column(0),si.column(1))
plt.plot(c60.column(0),c60.column(1))
plt.show()

plt.plot(si.column(0),(si.column(1)-difc)/difc,'o')
plt.plot(c60.column(0),(c60.column(1)-difc)/difc,'o')
plt.show()

plot(si.column(1)-c60.column(1))
plt.show()
