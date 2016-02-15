from mantid.simpleapi import *
from matplotlib import pyplot as plt
import numpy as np

shift=-0.0005
x=np.arange(0.05,18666.65,0.1)
rebin_x=str(shift)+',0.1,'+str(18666.6+shift)

#load data
def load_data(run_numbers,ws):
    try:
        for run in run_numbers:
            LoadNexusMonitors(Filename="CORELLI_"+str(run),OutputWorkspace=str(run))
        MergeRuns(InputWorkspaces=run_numbers,OutputWorkspace=ws)
    except:
        LoadNexusMonitors(Filename="CORELLI_"+str(run_numbers),OutputWorkspace=ws)

#ploting
def plot_monitors(ws):
    monitors=mtd[ws]
    m1,m2,m3=monitors.extractY()
    x1,x2,x3=monitors.extractX()
    plt.plot(x,m2)
    plt.plot(x,m3)
    plt.show()

def plot_derivatives(ws):
    derivatives=mtd[ws+'_derivatives_smooth']
    d1,d2,d3=derivatives.extractY()
    x1,x2,x3=derivatives.extractX()
    plt.plot(x,d2)
    plt.plot(x,d3)
    plt.show()
    
def save_m_d(ws):
    monitors=mtd[ws]
    m1,m2,m3=monitors.extractY()
    derivatives=mtd[ws+'_derivatives_smooth']
    d1,d2,d3=derivatives.extractY()
    np.savetxt(ws+"_m2.txt",np.transpose(np.array([x,m2])))
    np.savetxt(ws+"_m3.txt",np.transpose(np.array([x,m3])))
    np.savetxt(ws+"_d2.txt",np.transpose(np.array([x,d2])))
    np.savetxt(ws+"_d3.txt",np.transpose(np.array([x,d3])))

def fix_second_frame(ws,cutPoint=2000):
    CropWorkspace(InputWorkspace=ws,OutputWorkspace='monitors_temp',Xmin=0,Xmax=cutPoint)
    CropWorkspace(InputWorkspace=ws,OutputWorkspace=ws,Xmin=cutPoint,Xmax=16666.6)
    ChangeBinOffset(InputWorkspace='monitors_temp',OutputWorkspace='monitors_temp',Offset=16666.6)
    ChangePulsetime(InputWorkspace='monitors_temp',OutputWorkspace='monitors_temp',TimeOffset=-0.0166666)
    MergeRuns(InputWorkspaces=[ws,'monitors_temp'],OutputWorkspace=ws)
    DeleteWorkspace('monitors_temp')


name="CORELLI_14161"
load_data(14161,name)
name="CORELLI_13116"
load_data(13116,name)
name="CORELLI_14329"
load_data(14329,name)
name="CORELLI_14061-4"
load_data(range(14061,14065),name)

fix_second_frame(name)

# process data
Rebin(InputWorkspace=name, OutputWorkspace=name, Params=rebin_x)
SmoothData(InputWorkspace=name, OutputWorkspace=name+'_smooth',NPoints=100)

plot_monitors(name)
plot_monitors(name+'_smooth')

# calculate derivative
FFTDerivative(InputWorkspace=name+'_smooth',OutputWorkspace=name+'_derivatives')
SmoothData(InputWorkspace=name+'_derivatives', OutputWorkspace=name+'_derivatives_smooth', NPoints=10)
SmoothData(InputWorkspace=name+'_derivatives_smooth', OutputWorkspace=name+'_derivatives_smooth', NPoints=10)
SmoothData(InputWorkspace=name+'_derivatives_smooth', OutputWorkspace=name+'_derivatives_smooth', NPoints=10)

plot_derivatives(name)

save_m_d(name)
