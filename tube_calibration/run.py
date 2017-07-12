#!/usr/bin/env python2

# ./run.py 47301 33 output.txt

from mantid.simpleapi import Load, Integration
import subprocess
import sys
import numpy as np

run=sys.argv[1]
bank=sys.argv[2]

data=Load('CORELLI_'+str(run),BankName='bank'+str(bank))
data=Integration(data)
data_Y=data.extractY()*-1
for tube in range(16):
    np.savetxt('COR_'+str(run)+'_'+str(bank)+'_'+str(tube+1)+'.txt', np.concatenate((np.array(range(256),ndmin=2).T, data_Y[range(256*tube,256*(tube+1))]),axis=1))

p = subprocess.Popen(['/usr/bin/cfityk','-n'],stdin=subprocess.PIPE)
p.communicate("@0 < '/SNS/users/rwp/corelli/tube_calibration/COR_47301_57_16.txt'")
#p.communicate('quit')
