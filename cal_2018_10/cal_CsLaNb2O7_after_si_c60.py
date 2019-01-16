import numpy as np
from mantid.simpleapi import *
from mantid.geometry import OrientedLattice
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

def get_d(ol, h, k, l):
    return 2*np.pi/np.linalg.norm(ol.qFromHKL([h,k,l]))

ol=OrientedLattice(3.905044, 3.905044, 11.166629, 90, 90, 90)

DReference = [get_d(ol, 0, 0, 1),
              get_d(ol, 0, 0, 2),
              get_d(ol, 1, 0, 0),
              get_d(ol, 0, 0, 3),
              #get_d(ol, 1, 0, 1), #0
              get_d(ol, 1, 0, 2),
              #get_d(ol, 0, 0, 4), #0
              get_d(ol, 1, 1, 0),
              #get_d(ol, 1, 0, 3),
              #get_d(ol, 1, 1, 1),
              get_d(ol, 1, 1, 2),
              get_d(ol, 1, 0, 4),
              get_d(ol, 0, 0, 5),
              get_d(ol, 1, 1, 3),
]

Load(Filename='CORELLI_81269-81280', OutputWorkspace='raw')

ApplyCalibration('raw','CalibTable')
LoadIsawDetCal('raw','/SNS/users/rwp/corelli/cal_2018_05/a/Aligned3.nxs.detcal')

corelli=LoadEmptyInstrument(InstrumentName='CORELLI')
ApplyCalibration('corelli','CalibTable')
LoadIsawDetCal('corelli','/SNS/users/rwp/corelli/cal_2018_05/a/Aligned3.nxs.detcal')
difc0=CalculateDIFC('corelli')

TofBinning='3000,-0.001,16660'

PDCalibration(InputWorkspace='raw',
              TofBinning=TofBinning,
              PeakPositions=DReference,
              MinimumPeakHeight=2,
              PeakWidthPercent=0.1,
              PeakWindow=2.0,
              AllowSinglePeakCalibration=True,
              OutputCalibrationTable='cal_after',
              DiagnosticWorkspaces='diag_after')

difc1=CalculateDIFC('corelli',CalibrationWorkspace='cal1')
diff1 = difc1/difc0

SaveDiffCal('cal1',MaskWorkspace='cal1_mask', Filename='/SNS/users/rwp/corelli/cal_2018_10/cal1.h5')

