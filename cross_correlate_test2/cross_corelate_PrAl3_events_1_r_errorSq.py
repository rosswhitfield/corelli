from mantid.simpleapi import *
import numpy as np
import sys

filename = sys.argv[1]
bank = int(sys.argv[2])

ws = LoadEventNexus(Filename=r'/SNS/CORELLI/IPTS-15796/nexus/'+filename+'.nxs.h5',
                    OutputWorkspace=filename,
                    FilterByTofMin='1000',
                    FilterByTofMax='16000')

bin_size_tof = 1.  # 10ms bins
x = int(np.ceil(1e6/60/bin_size_tof))

results = np.zeros(x)
total_counts = 0
pixel_list = []
for tube in range(16):  # range(16)
    for pixels in range(256):
        pixel = (bank-1)*256*16 + tube*256 + pixels
        print(bank, tube, pixels, pixel)
        pixel_list.append(pixel)

for pixelID in pixel_list:
    r = ws.getInstrument().getDetector(pixelID).getDistance(ws.getInstrument().getSample())
    if r > 2.584:
        continue
    events = ws.getEventList(pixelID)
    n = events.getNumberEvents()
    total_counts += n
    print('PixelID =', pixelID, 'Count at pixel =', n, 'Total counts = ', total_counts)
    pulse = events.getPulseTimes()
    tofs = events.getTofs()
    for event in range(n):
        xxx = int(tofs[event]/bin_size_tof)
        results[xxx] += 1

np.save(filename+'_results_events_b1_bank_r2.584_errorSq_'+str(bank), results)
