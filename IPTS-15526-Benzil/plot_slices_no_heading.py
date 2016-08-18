import matplotlib.pyplot as plt
import numpy as np
from nexusformat import nexus as nx

a=nx.nxload("/SNS/CORELLI/IPTS-15526/shared/benzil_100K_normData_sym_All_noCC.nxs")
b=nx.nxload("/SNS/CORELLI/IPTS-15526/shared/benzil_300K_normData_sym_All_noCC.nxs")

signal_100 = np.ma.masked_invalid(a.MDHistoWorkspace.data.signal)
signal_300 = np.ma.masked_invalid(b.MDHistoWorkspace.data.signal)

x = np.linspace(-10, 10, 401)
y = np.linspace(-17.5, 17.5, 401)
X, Y = np.meshgrid(x, y)

fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(14, 9))
axes[0,0].pcolormesh(x,y,signal_100[25,:,:],vmin=0.0000025,vmax=0.00001)
axes[0,0].set_title('100K HK0')
axes[0,1].pcolormesh(x,y,signal_100[28,:,:],vmin=0.0000025,vmax=0.00001)
axes[0,1].set_title('100K HK½')
axes[0,2].pcolormesh(x,y,signal_100[30,:,:],vmin=0.0000025,vmax=0.00001)
axes[0,2].set_title('100K HK1')
axes[1,0].pcolormesh(x,y,signal_300[25,:,:],vmin=0.0000025,vmax=0.00001)
axes[1,0].set_title('300K HK0')
axes[1,1].pcolormesh(x,y,signal_300[28,:,:],vmin=0.0000025,vmax=0.00001)
axes[1,1].set_title('300K HK½')
axes[1,2].pcolormesh(x,y,signal_300[30,:,:],vmin=0.0000025,vmax=0.00001)
axes[1,2].set_title('300K HK1')
plt.savefig("benzil_100K_300K_no_heading.png",bbox_inches='tight')


part0=nx.nxload("/SNS/users/rwp/benzil/benzil_300K_normData_sym_part0_All_noCC.nxs")
part1=nx.nxload("/SNS/users/rwp/benzil/benzil_300K_normData_sym_part1_All_noCC.nxs")
part2=nx.nxload("/SNS/users/rwp/benzil/benzil_300K_normData_sym_part2_All_noCC.nxs")
part3=nx.nxload("/SNS/users/rwp/benzil/benzil_300K_normData_sym_part3_All_noCC.nxs")
part4=nx.nxload("/SNS/users/rwp/benzil/benzil_300K_normData_sym_part4_All_noCC.nxs")
part5=nx.nxload("/SNS/users/rwp/benzil/benzil_300K_normData_sym_part5_All_noCC.nxs")

fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(14, 9))
axes[0,0].pcolormesh(x,y,np.ma.masked_invalid(part0.MDHistoWorkspace.data.signal[25,:,:]),vmin=0.0000025,vmax=0.00001)
axes[0,0].set_title('x,y,z')
axes[0,1].pcolormesh(x,y,np.ma.masked_invalid(part1.MDHistoWorkspace.data.signal[25,:,:]),vmin=0.0000025,vmax=0.00001)
axes[0,1].set_title('-y,x-y,z')
axes[0,2].pcolormesh(x,y,np.ma.masked_invalid(part2.MDHistoWorkspace.data.signal[25,:,:]),vmin=0.0000025,vmax=0.00001)
axes[0,2].set_title('-x+y,-x,z')
axes[1,0].pcolormesh(x,y,np.ma.masked_invalid(part3.MDHistoWorkspace.data.signal[25,:,:]),vmin=0.0000025,vmax=0.00001)
axes[1,0].set_title('y,x,-z')
axes[1,1].pcolormesh(x,y,np.ma.masked_invalid(part4.MDHistoWorkspace.data.signal[25,:,:]),vmin=0.0000025,vmax=0.00001)
axes[1,1].set_title('x-y,-y,-z')
axes[1,2].pcolormesh(x,y,np.ma.masked_invalid(part5.MDHistoWorkspace.data.signal[25,:,:]),vmin=0.0000025,vmax=0.00001)
axes[1,2].set_title('-x,-x+y,-z')
plt.savefig("benzil_300K_sym_no_heading.png",bbox_inches='tight')
