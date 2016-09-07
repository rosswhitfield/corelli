from mantid.simpleapi import *
import numpy as np

for run in range(20492,20494):
    LoadDiffCal(Filename='/SNS/users/rwp/corelli/PDCalibration/cal_Si_'+str(run)+'.h5',
                InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_91.07cm.xml',
                WorkspaceName='cal')
    cal = mtd['cal_cal']
    a=np.array([cal.column(0),cal.column(1),cal.column(2),cal.column(3),cal.column(4)]).T
    np.savetxt('/SNS/users/rwp/corelli/PDCalibration/cal_Si_'+str(run)+'.txt',a)
