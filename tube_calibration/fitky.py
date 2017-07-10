from mantid.simpleapi import LoadEventNexus, Integration
import numpy as np

# 47299 23, 56, 85
# 47300 33, 45, 57

dirc='/SNS/users/rwp/corelli/tube_calibration/'

for bank in [23,56,85]:
    COR_47299=LoadEventNexus('/SNS/CORELLI/IPTS-18479/nexus/CORELLI_47299.nxs.h5',BankName='bank'+str(bank))
    COR_47299=Integration(COR_47299)
    COR_47299_Y=COR_47299.extractY()*-1
    for tube in range(8):
        np.savetxt(dirc+'COR_47299_'+str(bank)+'_'+str(tube+1)+'.txt', np.concatenate((np.array(range(256),ndmin=2).T, COR_47299_Y[range(256*tube,256*(tube+1))]),axis=1))

for bank in [33,45,57]:
    COR_47299=LoadEventNexus('/SNS/CORELLI/IPTS-18479/nexus/CORELLI_47300.nxs.h5',BankName='bank'+str(bank))
    COR_47299=Integration(COR_47299)
    COR_47299_Y=COR_47299.extractY()*-1
    for tube in range(8):
        np.savetxt(dirc+'COR_47300_'+str(bank)+'_'+str(tube+1)+'.txt', np.concatenate((np.array(range(256),ndmin=2).T, COR_47299_Y[range(256*tube,256*(tube+1))]),axis=1))
