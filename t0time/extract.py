from mantid.simpleapi import *
import numpy as np

filename="CORELLI_11005"
LoadNexusMonitors(Filename='/SNS/CORELLI/IPTS-12310/nexus/'+filename+'.nxs.h5',OutputWorkspace=filename)
w = mtd[filename]
bin_size=1
Rebin(InputWorkspace=filename,OutputWorkspace=filename,Params="-0.02,"+str(bin_size)+",16666.98")
x0,x1,x2=w.extractX()
y0,y1,y2=w.extractY()

np.save(filename+"_x0",x0)
np.save(filename+"_y0",y0)
np.save(filename+"_y1",y1)
np.save(filename+"_y2",y2)

np.savetxt(filename+"_x0.txt",x0)
np.savetxt(filename+"_y0.txt",y0)
np.savetxt(filename+"_y1.txt",y1)
np.savetxt(filename+"_y2.txt",y2)



bin_size=0.1
Rebin(InputWorkspace=filename,OutputWorkspace=filename,Params="-0.02,"+str(bin_size)+",16666.98")
x0,x1,x2=w.extractX()
y0,y1,y2=w.extractY()

np.save(filename+"_x0_0.1",x0)
np.save(filename+"_y0_0.1",y0)
np.save(filename+"_y1_0.1",y1)
np.save(filename+"_y2_0,1",y2)

np.savetxt(filename+"_x0_0.1.txt",x0)
np.savetxt(filename+"_y0_0.1.txt",y0)
np.savetxt(filename+"_y1_0.1.txt",y1)
np.savetxt(filename+"_y2_0.1.txt",y2)
