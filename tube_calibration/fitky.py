from mantid.simpleapi import LoadEventNexus, Integration
import numpy as np

# 47299 23, 56, 85
# 47300 33, 45, 57

dirc='/SNS/users/rwp/corelli/tube_calibration/'

run=47299

for bank in [23,56,85]:
    data=LoadEventNexus('/SNS/CORELLI/IPTS-18479/nexus/CORELLI_'+str(run)+'.nxs.h5',BankName='bank'+str(bank))
    data=Integration(data)
    data_Y=data.extractY()*-1
    for tube in range(16):
        np.savetxt(dirc+'COR_'+str(run)+'_'+str(bank)+'_'+str(tube+1)+'.txt', np.concatenate((np.array(range(256),ndmin=2).T, data_Y[range(256*tube,256*(tube+1))]),axis=1))

for run in range(47300,47305):
    for bank in [33,45,57]:
        data=LoadEventNexus('/SNS/CORELLI/IPTS-18479/nexus/CORELLI_'+str(run)+'.nxs.h5',BankName='bank'+str(bank))
        data=Integration(data)
        data_Y=data.extractY()*-1
        for tube in range(16):
            np.savetxt(dirc+'COR_'+str(run)+'_'+str(bank)+'_'+str(tube+1)+'.txt', np.concatenate((np.array(range(256),ndmin=2).T, data_Y[range(256*tube,256*(tube+1))]),axis=1))

