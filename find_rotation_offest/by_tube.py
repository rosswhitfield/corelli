from mantid.simpleapi import Load, Integration
import numpy as np

run1='CORELLI_48505'
run2='CORELLI_48513'

ws1=Load(run1)
ws2=Load(run2)
ws1=Integration(ws1)
ws2=Integration(ws2)

ws1y=ws1.extractY().reshape((-1,256))
ws2y=ws2.extractY().reshape((-1,256))


ws1ysum=ws1y.sum(axis=1)
ws2ysum=ws2y.sum(axis=1)

import matplotlib.pyplot as plt
plt.imshow(ws1y,vmax=1000)
plt.show()


plt.plot(ws1ysum)
plt.plot(ws2ysum)
plt.show()

w1=ws1ysum[480:912]
w2=ws2ysum[480:912]

plt.plot(w1)
plt.plot(w2)
plt.show()


corr=np.correlate(w1,w2[20:-20])

plt.plot(corr, 'o-')
plt.show()


w1[w1 < 150000]=150000
w2[w2 < 150000]=150000

corr=np.correlate(w1,w2[20:-20])

plt.plot(corr, 'o-')
plt.show()
