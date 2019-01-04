import numpy as np
from mantid.simpleapi import *
from mantid.geometry import OrientedLattice
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

def get_d(ol, h, k, l):
    return 2*np.pi/np.linalg.norm(ol.qFromHKL([h,k,l]))

ol=OrientedLattice(3.905044, 3.905044, 11.166629, 90, 90, 90)

DReference = [get_d(ol, 0, 0, 1), # 11.166629
              #get_d(ol, 0, 0, 2), # 5.5833145
              get_d(ol, 1, 0, 0), # 3.9050440
              #get_d(ol, 0, 0, 3), # 3.7222097
              #get_d(ol, 1, 0, 1), # 3.6861455
              get_d(ol, 1, 0, 2), # 3.2000186
              # 2.79165725
              get_d(ol, 1, 1, 0), # 2.7612831
              #get_d(ol, 1, 0, 3), # 2.6943178
              #get_d(ol, 1, 1, 1), # 2.6805448
              #get_d(ol, 1, 1, 2), # 2.4751292 maybe
              # 2.27102109
              # 2.2333258
              # 2.2176826
              # 1.96317278
              # 1.952522
              # 1.93866933
              # 1.92334155
              # 1.86110483
              # 1.84307275
]

DReference = [get_d(ol, 0, 0, 1), # 11.166629
              get_d(ol, 1, 0, 0)] # 3.9050440

Load(Filename='CORELLI_81269-81280', OutputWorkspace='raw')


ApplyCalibration('raw','CalibTable')


#ConvertUnits(InputWorkspace='raw', OutputWorkspace='rawD', Target='dSpacing')


#LoadIsawDetCal('raw','/SNS/users/rwp/corelli/cal_2018_05/0a/Aligned_row_si_c60.nxs.detcal')

TofBinning='3000,-0.005,16660'


PDCalibration(InputWorkspace='raw',
              TofBinning=TofBinning,
              PeakPositions=DReference,
              MinimumPeakHeight=1,
              PeakWidthPercent=0.05,
              PeakWindow=2.0,
              OutputCalibrationTable='cal',
              DiagnosticWorkspaces='diag')
