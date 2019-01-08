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
              get_d(ol, 1, 0, 1),
              get_d(ol, 1, 0, 2),
              get_d(ol, 0, 0, 4),
              get_d(ol, 1, 1, 0),
              get_d(ol, 1, 0, 3),
              get_d(ol, 1, 1, 1),
              get_d(ol, 1, 1, 2),
              get_d(ol, 1, 1, 3),





              get_d(ol, 2, 0, 6),
]

DReference = [get_d(ol, 0, 0, 1), # 11.166629
              get_d(ol, 1, 0, 0)] # 3.9050440

DReference = [get_d(ol, 0, 0, 1), # 11.166629
              get_d(ol, 1, 0, 2)] # 3.2000186

Load(Filename='CORELLI_81269-81280', OutputWorkspace='raw')

# raw = LoadNexus('/SNS/users/rwp/corelli/cal_2018_10/raw.nxs')


ApplyCalibration('raw','CalibTable')


#ConvertUnits(InputWorkspace='raw', OutputWorkspace='rawD', Target='dSpacing')

corelli=LoadEmptyInstrument(InstrumentName='CORELLI')
ApplyCalibration('corelli','CalibTable')
difc0=CalculateDIFC('corelli')


#LoadIsawDetCal('raw','/SNS/users/rwp/corelli/cal_2018_05/0a/Aligned_row_si_c60.nxs.detcal')

TofBinning='3000,-0.005,16660'


PDCalibration(InputWorkspace='raw',
              TofBinning=TofBinning,
              PeakPositions=DReference,
              MinimumPeakHeight=2,
              PeakWidthPercent=0.1,
              PeakWindow=2.0,
              OutputCalibrationTable='cal',
              DiagnosticWorkspaces='diag')

difc=CalculateDIFC('corelli',CalibrationWorkspace='cal')
diff = difc/difc0

SaveDiffCal('cal',MaskWorkspace='cal_mask', Filename='/SNS/users/rwp/corelli/cal_2018_10/cal.h5')

PDCalibration(InputWorkspace='raw',
              TofBinning=TofBinning,
              PeakPositions=DReference,
              MinimumPeakHeight=2,
              PeakWidthPercent=0.1,
              PeakWindow=2.0,
              AllowSinglePeakCalibration=True,
              OutputCalibrationTable='cal1',
              DiagnosticWorkspaces='diag1')

difc1=CalculateDIFC('corelli',CalibrationWorkspace='cal1')
diff1 = difc1/difc0

SaveDiffCal('cal1',MaskWorkspace='cal1_mask', Filename='/SNS/users/rwp/corelli/cal_2018_10/cal1.h5')

