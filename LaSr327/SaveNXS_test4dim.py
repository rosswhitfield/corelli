from mantid.simpleapi import *
import numpy as np
import h5py

fileOut='dim4.h5'

Load(Filename='CNCS_7860_event.nxs', OutputWorkspace='CNCS_7860_event')
ConvertUnits(InputWorkspace='CNCS_7860_event', OutputWorkspace='CNCS_7860_event', Target='DeltaE', EMode='Direct', EFixed=3)
Rebin(InputWorkspace='CNCS_7860_event', OutputWorkspace='CNCS_7860_event', Params='-3,0.01,3')
ConvertToMD(InputWorkspace='CNCS_7860_event', QDimensions='Q3D', OutputWorkspace='md')
binned=BinMD(InputWorkspace='md', AlignedDim0='Q_lab_x,-1.70164,1.3701,100', AlignedDim1='Q_lab_y,-0.467778,0.467778,100', AlignedDim2='Q_lab_z,-0.494645,2.35524,100', AlignedDim3='DeltaE,-3,3,10', OutputWorkspace='out')




s=binned.getSignalArray()

x_min=binned.getXDimension().getMinimum()
x_max=binned.getXDimension().getMaximum()
x_bins=binned.getXDimension().getNBins()
x_units=binned.getXDimension().getUnits()
x_axis_name=binned.getXDimension().getDimensionId()
x_axis=np.linspace(x_min,x_max,x_bins)
y_min=binned.getYDimension().getMinimum()
y_max=binned.getYDimension().getMaximum()
y_bins=binned.getYDimension().getNBins()
y_units=binned.getYDimension().getUnits()
y_axis_name=binned.getYDimension().getDimensionId()
y_axis=np.linspace(y_min,y_max,y_bins)
z_min=binned.getZDimension().getMinimum()
z_max=binned.getZDimension().getMaximum()
z_bins=binned.getZDimension().getNBins()
z_units=binned.getZDimension().getUnits()
z_axis_name=binned.getZDimension().getDimensionId()
z_axis=np.linspace(z_min,z_max,z_bins)

# Doesn't appear to like the "[H,0,0]" type axis name
x_axis_name='H'
y_axis_name='K'
z_axis_name='L'
axes_names=z_axis_name+":"+y_axis_name+":"+x_axis_name

# Get title from first run only
title=binned.getExperimentInfo(0).run().getProperty('run_title').value


# Write nexus file using h5py
h5f = h5py.File(fileOut, 'w')
nxentry = h5f.create_group("entry")
nxentry.attrs["NX_class"] = 'NXentry'
nxdata = nxentry.create_group("data")
nxdata.attrs["NX_class"] = 'NXdata'

axis1=nxdata.create_dataset(z_axis_name,data=z_axis)
axis1.attrs['units']=z_units
axis2=nxdata.create_dataset(y_axis_name,data=y_axis)
axis2.attrs['units']=y_units
axis3=nxdata.create_dataset(x_axis_name,data=x_axis)
axis3.attrs['units']=x_units

sq=nxdata.create_dataset('Sq',data=s)
sq.attrs['units'] = 'Intensity'
sq.attrs["signal"]=1
sq.attrs["axes"]=axes_names
sq.attrs["title"]=title
h5f.close()





# Write nexus file using nxs
f = nxs.open(fileOut, 'w5')
f.makegroup("entry","NXentry")
f.opengroup("entry","NXentry")
f.makegroup("data","NXdata")
f.opengroup("data","NXdata")

f.makedata(x_axis_name,'float64',[x_bins])
f.opendata(x_axis_name)
f.putdata(x_axis)
f.putattr("units",x_units)
f.closedata
f.makedata(y_axis_name,'float64',[y_bins])
f.opendata(y_axis_name)
f.putdata(y_axis)
f.putattr("units",y_units)
f.closedata
f.makedata(z_axis_name,'float64',[z_bins])
f.opendata(z_axis_name)
f.putdata(z_axis)
f.putattr("units",z_units)
f.closedata

f.makedata("Sq",'float64',[z_bins,y_bins,x_bins])
f.opendata("Sq")
f.putdata(s)
f.putattr("signal",1)
f.putattr("units","Intensity")
f.putattr("axes",axes_names)
f.putattr("title",title)
f.closedata()

f.closegroup()
f.closegroup()
f.close()


