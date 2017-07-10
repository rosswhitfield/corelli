from mantid.simpleapi import LoadEventNexus, Integration
import numpy as np
import matplotlib.pyplot as plt

COR_47299_23 = LoadEventNexus('/SNS/CORELLI/IPTS-18479/nexus/CORELLI_47299.nxs.h5',BankName='bank23')
COR_47299_23=Integration(COR_47299_23)
COR_47299_23_Y = COR_47299_23.extractY()

plt.plot(COR_47299_23_Y)
plt.show()

np.savetxt('COR_47299_23.txt', np.concatenate((np.array(range(256*16)).reshape((4096, 1)), COR_47299_23_Y*-1),axis=1))


# Tube 1
centers = [133.028,
           208.028,
           178.07,
           223.244,
           162.902,
           148.055,
           193.13,
           72.9872,
           118.006,
           103.016,
           87.9981,
           58.1475,
           43.3181,
           28.5941,
           238.329,
           14.0629]
centers.sort()
centers = np.asarray(centers)

a=(2*25.4+2)/1000
knownPositions=np.arange(-7.5*a,8.5*a,a)

np.savetxt('COR_47299_23_1.txt', np.concatenate((knownPositions.reshape((16,1)),centers.reshape((16,1))),axis=1))
