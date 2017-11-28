from mantid.simpleapi import LoadDiffCal, mtd, LoadEmptyInstrument, CalculateDIFC
import matplotlib.pyplot as plt
import tube
import numpy as np
import numpy.ma as ma

tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration/CalibTableNew.txt')

corelli = LoadEmptyInstrument(InstrumentName='CORELLI')
corelli = CalculateDIFC(corelli)
difc0 = corelli.extractY().flatten()
ApplyCalibration('corelli','CalibTable')
corelli = CalculateDIFC(corelli)
difc = corelli.extractY().flatten()

#plt.plot(difc/difc0)
#plt.show()

LoadDiffCal(Filename='../cal_Si_C60/cal_Si2_47327-47334_TubeCal_sum16.cal',
            InstrumentName='CORELLI',
            WorkspaceName='si')
MaskBTP(Workspace='si_mask',Pixel="1-16,241-256")

LoadDiffCal(Filename='../cal_Si_C60/cal_C60_2_47367-47382_TubeCal_sum16.h5',
            InstrumentName='CORELLI',
            WorkspaceName='c60')
MaskBTP(Workspace='c60_mask',Pixel="1-16,241-256")

si=mtd['si_cal']
c60=mtd['c60_cal']
si_mask=mtd['si_mask']
c60_mask=mtd['c60_mask']

plt.plot(corelli.extractY())
plt.plot(si.column(0),si.column(1))
plt.plot(c60.column(0),c60.column(1))
plt.show()

plt.plot(si.column(0),(si.column(1)-difc)/difc)
plt.plot(c60.column(0),(c60.column(1)-difc)/difc)
plt.show()


def bank2pixel(bank):
    return range((bank-1)*4096,bank*4096)


# Masked
si_ma = ma.masked_array(si.column(1), si_mask.extractY())
c60_ma = ma.masked_array(c60.column(1), c60_mask.extractY())
ave = (si_ma+c60_ma)/2
plt.plot((si_ma-difc)/difc)
plt.plot((c60_ma-difc)/difc)
plt.plot((ave-difc)/difc)
plt.show()



"""
Si 1-16, 30-47 , 62-78
C60 17-29, 48-61, 79-91
"""
