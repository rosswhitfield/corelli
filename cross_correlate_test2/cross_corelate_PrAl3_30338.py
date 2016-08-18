from mantid.simpleapi import *
import numpy as np
#import matplotlib.pyplot as plt
import math

filename = 'CORELLI_30338'

ws=LoadEventNexus(Filename=r'/SNS/CORELLI/IPTS-15796/nexus/'+filename+'.nxs.h5',OutputWorkspace=filename,FilterByTofMin='1000',FilterByTofMax='16000')
LoadInstrument(Workspace=filename,Filename='/SNS/users/rwp/CORELLI_Definition.xml')

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
y = int(math.ceil( chopper_per/bin_size ))
x = int(math.ceil( 1e6/60/bin_size ))
out = np.zeros((y,x))
total_counts=0


# get pixels to use
pixel_list = []
for bank in range(41,42): #range(41,43):
    for tube in range(1): #range(16)
        for pixels in range(64,192):
            pixel = (bank-1)*256*16 + tube*256+ pixels
            print bank,tube,pixels,pixel
            pixel_list.append(pixel)

for pixelID in pixel_list:
    counts=ws.getEventList(pixelID).getNumberEvents()
    total_counts+=counts
    print 'PixelID =',pixelID,'Count at pixel =',counts,'Total counts = ',total_counts
    events=ws.getEventList(pixelID)
    n=events.getNumberEvents()
    pulse = events.getPulseTimes()
    tofs = events.getTofs()
    tdc_index=0
    for event in range(n):
        while pulse[event]>chopper_tdc[tdc_index]:
            tdc_index+=1
        out[int(((chopper_tdc[tdc_index]-pulse[event]).total_microseconds()%chopper_per)/bin_size),int(tofs[event]/bin_size)]+=1


results = np.zeros((y,x))
for pi in range(y):
    print pi
    for pj in range(y):
        ij = ((pi-pj)/chopper_per*3600.)%360
        if np.searchsorted(sequence_sum,ij)%2==1:
            fact = 1
        else:
            fact = -1
        for pk in range(x):
            results[pi,pk]+=fact*out[pj,pk]


np.save(filename+'_out',out)
np.save(filename+'_results',results)
