from corelli_calc_tdc_offset_func import *

for i in range(637,640):
#for i in range(2100,2110):
 filename='CORELLI_'+str(i)
 results=calc_tdc_offset(filename)
 print results
