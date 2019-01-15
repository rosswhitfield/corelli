import numpy as np
from mantid.simpleapi import *
from mantid.geometry import OrientedLattice
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

Load(Filename='CORELLI_81269-81280', OutputWorkspace='raw')
# Load(Filename='CORELLI_59313-59320', OutputWorkspace='raw') # Silicon

ApplyCalibration('raw','CalibTable')

CreateGroupingWorkspace(InputWorkspace='raw', GroupDetectorsBy='All', OutputWorkspace='group')

ConvertUnits(InputWorkspace='raw', OutputWorkspace='rawD', Target='dSpacing')
Rebin(InputWorkspace='rawD', OutputWorkspace='rawD', Params='0.1,-0.005,20')
DiffractionFocussing('rawD', OutputWorkspace='rawD', GroupingWorkspace='group')

SetInstrumentParameter(Workspace="raw",ParameterName="t0_formula",Value="(101.9 * incidentEnergy^(-0.41) * exp(-incidentEnergy/282.0))")
ModeratorTzero('raw', EMode='Elastic', OutputWorkspace='tzero')
ConvertUnits(InputWorkspace='tzero', OutputWorkspace='tzeroD', Target='dSpacing')
Rebin(InputWorkspace='tzeroD', OutputWorkspace='tzeroD', Params='0.1,-0.005,20')
DiffractionFocussing('tzeroD', OutputWorkspace='tzeroD', GroupingWorkspace='group')

SetInstrumentParameter(Workspace="raw",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
ModeratorTzero('raw', EMode='Elastic', OutputWorkspace='tzero2')
ConvertUnits(InputWorkspace='tzero2', OutputWorkspace='tzero2D', Target='dSpacing')
Rebin(InputWorkspace='tzero2D', OutputWorkspace='tzero2D', Params='0.1,-0.005,20')
DiffractionFocussing('tzero2D', OutputWorkspace='tzero2D', GroupingWorkspace='group')



DReference = [0.9179, 0.9600, 1.0451, 1.1085, 1.2458, 1.3576, 1.6374, 1.9200, 3.1353] # Si


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
              get_d(ol, 1, 0, 3),
              get_d(ol, 1, 1, 1),
              get_d(ol, 1, 1, 2),
              get_d(ol, 1, 0, 4),
              get_d(ol, 0, 0, 5),
              get_d(ol, 1, 1, 3),
]
    

import matplotlib.pyplot as plt
from mantid import plots
fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
ax.plot(mtd['rawD'])
ax.plot(mtd['tzeroD'])
ax.plot(mtd['tzero2D'])
for d in DReference:
    ax.axvline(d)
plt.show()
