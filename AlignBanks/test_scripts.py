from mantid.simpleapi import *

LoadCalFile(InstrumentName='CORELLI', CalFilename='/SNS/users/rwp/cal/c60_t0.cal', MakeGroupingWorkspace=False, MakeMaskWorkspace=False, WorkspaceName='cor')

AlignComponents(CalibrationTable="cor_cal",
                InstrumentFilename="/home/rwp/mantidgeometry/CORELLI_Definition.xml",
                ComponentList="B row",
                PosX=False, PosZ=False,
                RotX=False, RotY=False, RotZ=False)

AlignComponents(CalibrationTable="cor_cal",
                InputWorkspace="alignedWorkspace",
                ComponentList="bank56/sixteenpack",
                PosY=False)

SaveNexus(Filename='/SNS/users/rwp/cal/test_cor.nxs',InputWorkspace='alignedWorkspace')
LoadNexus(Filename='/SNS/users/rwp/cal/test_cor.nxs',OutputWorkspace='alignedWorkspace2')

w=mtd['alignedWorkspace']
w2=mtd['alignedWorkspace2']
