from mantid.simpleapi import SaveNexus
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration/calib_quad_new3.txt')
SaveNexus('CalibTable','/SNS/users/rwp/corelli/tube_calibration/calibtable.nxs')
