from mantid.simpleapi import *

sam = 'Si2'
runs = '47327-47334'

LoadDiffCall(Filename='cal_'+sam+'_'+runs+'_TubeCal_sum16_mask_lt_3.h5',
             InstrumentName='CORELLI',
             WorkspaceName='SiCal')

wksp = 

Load(Filename='CORELLI_'+runs, OutputWorkspace=wksp, Precount=False) 

MaskDetectors(Workspace=wksp, MaskedWorkspace="cal_mask")
AlignDetectors(InputWorkspace=wksp, OutputWorkspace='cal',
                      CalibrationWorkspace=str(wksp)+"cal")
DiffractionFocussing(InputWorkspace=wksp+'_calab', OutputWorkspace=wksp+'_calab',
                            GroupingWorkspace=str(wksp)+"group")
Rebin(InputWorkspace=wksp+'_calab', OutputWorkspace=wksp+'_calab', Params=binning)

ConvertUnits(InputWorkspace=wksp, OutputWorkspace=wksp, Target="dSpacing")
Rebin(InputWorkspace=wksp, OutputWorkspace=wksp, Params=binning)
DiffractionFocussing(InputWorkspace=wksp, OutputWorkspace=wksp+'_d',
                     GroupingWorkspace=str(wksp)+"group")
