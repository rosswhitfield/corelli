import numpy as np
from mantid.simpleapi import *
from mantid.geometry import OrientedLattice
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

Load(Filename='CORELLI_81269-81280', OutputWorkspace='raw')

ApplyCalibration('raw','CalibTable')

CreateGroupingWorkspace(InputWorkspace='raw', GroupDetectorsBy='All', OutputWorkspace='group')

ConvertUnits(InputWorkspace='raw', OutputWorkspace='rawD', Target='dSpacing')
DiffractionFocussing('rawD', OutputWorkspace='rawD', GroupingWorkspace='group')

ModeratorTzero('raw', EMode='Elastic', OutputWorkspace='tzero')
ConvertUnits(InputWorkspace='tzero', OutputWorkspace='tzeroD', Target='dSpacing')
DiffractionFocussing('tzeroD', OutputWorkspace='tzeroD', GroupingWorkspace='group')

SetInstrumentParameter(Workspace="raw",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
ModeratorTzero('raw', EMode='Elastic', OutputWorkspace='tzero2')
ConvertUnits(InputWorkspace='tzero2', OutputWorkspace='tzero2D', Target='dSpacing')
DiffractionFocussing('tzero2D', OutputWorkspace='tzero2D', GroupingWorkspace='group')
