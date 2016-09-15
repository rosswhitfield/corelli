from mantid.simpleapi import *
import numpy as np
#import matplotlib.pyplot as plt
import sys

filename = sys.argv[1]
bank = int(sys.argv[2])

ws=LoadEventNexus(Filename=r'/SNS/CORELLI/IPTS-15796/nexus/'+filename+'.nxs.h5',OutputWorkspace=filename,FilterByTofMin='1000',FilterByTofMax='16000')
#LoadInstrument(Workspace=filename,Filename='/SNS/users/rwp/CORELLI_Definition.xml')

sequence = map(float,ws.getInstrument().getComponentByName('correlation-chopper').getStringParameter('sequence')[0].split())
sequence_sum=np.cumsum(sequence)

#i=ws.getInstrument()
#r=i.getDetector(169600).getDistance(i.getSample())

Lmc=17.999347
Lcs=20-Lmc
Lsd=ws.getInstrument().getDetector(168064).getDistance(ws.getInstrument().getSample())
L=Lmc+Lcs+Lsd


chopper_tdc = ws.getSampleDetails().getProperty("chopper4_TDC").times
#chopper_frq = ws.getSampleDetails().getProperty("BL9:Chop:Skf4:SpeedSetReq").value[0]
chopper_frq = ws.getSampleDetails().getProperty("BL9:Chop:Skf4:MotorSpeed").timeAverageValue()
chopper_per = 1e6/chopper_frq

print 'Chopper Frequency =', chopper_frq, 'Hz, Period =', chopper_per, 'uS'

bin_size=10. # 10ms bins
bin_size_tof=1. # 10ms bins
y = int(np.ceil( chopper_per/bin_size ))
x = int(np.ceil( 1e6/60/bin_size_tof ))

results = np.zeros((y,x))
total_counts=0
pixel_list = []
for tube in range(16): #range(16)
    for pixels in range(256):
        pixel = (bank-1)*256*16 + tube*256 + pixels
        print bank,tube,pixels,pixel
        pixel_list.append(pixel)
    
for pixelID in pixel_list:
    r=ws.getInstrument().getDetector(pixelID).getDistance(ws.getInstrument().getSample())
    if r > 2.584:
        continue
    events=ws.getEventList(pixelID)
    n=events.getNumberEvents()
    total_counts+=n
    print 'PixelID =',pixelID,'Count at pixel =',n,'Total counts = ',total_counts
    pulse = events.getPulseTimes()
    tofs = events.getTofs()
    tdc_index=0
    for event in range(n):
        while pulse[event]>chopper_tdc[tdc_index]:
            tdc_index+=1
        yyy=(chopper_tdc[tdc_index]-pulse[event]).total_microseconds()%chopper_per
        xxx=int(tofs[event]/bin_size_tof)
        for pk in range(y):
            ij = ((pk*bin_size-yyy)/chopper_per*360.)%360
            if np.searchsorted(sequence_sum,ij)%2==1:
                results[pk,xxx]+=1
            else:
                results[pk,xxx]-=1

np.save(filename+'_results_events_b1_bank_r2.584'+str(bank),results)
