# Usage Example:
#
# from corelli_calc_tdc_offset_func import calc_tdc_offset
# calc_tdc_offset('CORELLI_7221')

from mantid.simpleapi import *
import numpy as np

def calc_tdc_offset(data='CORELLI_7221',bin_size=1):
 LoadNexusMonitors(filename=data,OutputWorkspace=data)
 LoadInstrument(Workspace=data,InstrumentName='CORELLI',RewriteSpectraMap=False)
 #ModeratorTzero(InputWorkspace=data,OutputWorkspace=data,EMode='Elastic')
 w = mtd[data]
 
 distance_chopper_to_monitor=w.getInstrument().getComponentByName('correlation-chopper').getDistance(w.getInstrument().getComponentByName('monitor2'))
 distance_chopper_to_moderator=w.getInstrument().getComponentByName('correlation-chopper').getDistance(w.getInstrument().getComponentByName('moderator'))
 scale=distance_chopper_to_moderator/(distance_chopper_to_moderator+distance_chopper_to_monitor)
 
 ScaleX(InputWorkspace=data,OutputWorkspace=data,Factor=str(scale))
 Rebin(InputWorkspace=data,OutputWorkspace=data,Params=str(bin_size))
 
 chopper_tdc = w.getRun().getProperty("chopper4_TDC").times
 sequence = map(float,w.getInstrument().getComponentByName('correlation-chopper').getStringParameter('sequence')[0].split())
 chopper_freq = w.getRun().getProperty("BL9:Chop:Skf4:MotorSpeed").timeAverageValue()
 chopper_per = 1e6/chopper_freq
 
 sequence2=np.append(sequence,sequence)
 s=np.cumsum(sequence2)
 
 tof=w.getEventList(1).getTofs()
 pulse=w.getEventList(1).getPulseTimes()
 
 bins=int(chopper_per/bin_size)+1
 x=np.arange(0,chopper_per+bin_size,bin_size)
 chopper=np.zeros(bins)
 
 for n in range(bins-1):
  if np.searchsorted(s,((x[n]+x[n+1]) / 2 / chopper_per)*360.)%2==1:
   chopper[n]=1
   
 chopper2 = np.zeros(len(chopper)*2)
 chopper2 = np.append(chopper,chopper)
 
 y=np.zeros(bins)
 tdc_index=1
 for event in range(len(tof)):
  while tdc_index<len(chopper_tdc) and pulse[event]+int(tof[event]*1000)>chopper_tdc[tdc_index]:
   tdc_index+=1
  y[int(((pulse[event]+int(tof[event]*1000)-chopper_tdc[tdc_index-1]).total_nanoseconds()/bin_size/1000.)%(chopper_per/bin_size))]+=1
  
 corr=np.correlate(y,chopper2)
 r=np.argmax(corr)
 r2=x[r] * 1000
 print data
 print ' Number of monitor events = '+str(len(tof))
 print ' MotorSpeed               = '+str(chopper_freq)+' Hz'
 print ' Chopper period           = '+str(chopper_per)+'uS'
 print ' Number of monitor events = '+str(len(tof))
 print ' Chopper sequence offset  = '+str(r2)+'ns'
