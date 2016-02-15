from corelli_calc_tdc_offset_func import *

#for i in range(7219,7230):
for i in range(7229,7230):
 filename='CORELLI_'+str(i)
 results=calc_tdc_offset(filename)
 print results
