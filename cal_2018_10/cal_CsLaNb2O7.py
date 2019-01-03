import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

DReference = [2.7251,2.8904,4.2694,5.0063,8.1753]

Load(Filename='CORELLI_81269-81280', OutputWorkspace='raw')

ApplyCalibration('rawC60','CalibTable')


LoadIsawDetCal('rawC60','/SNS/users/rwp/corelli/cal_2018_05/0a/Aligned_row_si_c60.nxs.detcal')

TofBinning='3000,-0.001,16660'
