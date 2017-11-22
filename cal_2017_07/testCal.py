from mantid.simpleapi import *

sam = 'Si2'
runs = '47327-47334'

wksp =  'CORELLI_'+runs
cal = 'SiCal'

binning = '0.5,-0.004,3.5'

LoadDiffCal(Filename='cal_'+sam+'_'+runs+'_TubeCal_sum16_mask_lt_3.h5',
             InstrumentName='CORELLI',
             WorkspaceName=cal)

Load(Filename='CORELLI_'+runs, OutputWorkspace=wksp, Precount=False)

MaskDetectors(Workspace=wksp, MaskedWorkspace=cal+"_mask")

AlignDetectors(InputWorkspace=wksp, OutputWorkspace=wksp+'_calab',
               CalibrationWorkspace=cal+"_cal")
ConvertUnits(InputWorkspace=wksp, OutputWorkspace=wksp+'_d', Target="dSpacing")

Rebin(InputWorkspace=wksp+'_calab', OutputWorkspace=wksp+'_calab', Params=binning)
Rebin(InputWorkspace=wksp+'_d', OutputWorkspace=wksp+'_d', Params=binning)

