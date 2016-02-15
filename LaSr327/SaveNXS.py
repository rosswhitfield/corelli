from mantid.simpleapi import *
import numpy as np
import h5py
import nxs

fileIn='/SNS/users/rwp/5021.nxs'
fileOut='COR_5021.h5'

ws=LoadMD(Filename=fileIn)
binned=BinMD(InputWorkspace=ws,AxisAligned='0',
        BasisVector0='[H,0,0],(r.l.u.),1,0,0',
        BasisVector1='[0,K,0],(r.l.u.),0,1,0',
        BasisVector2='[0,0,L],(r.l.u.),0,0,1',
        OutputExtents='-2.5025,2.5025,-2.5025,2.5025,9.95,20.05',
        OutputBins='301,301,301',Parallel='1')




s=binned.getSignalArray()

ndims=binned.getNumDims()

axis_min=[]
axis_max=[]
axis_bins=[]
axis_units=[]
axis_name=[]
axes_name=""

for i in range(ndims):
    axis_min.append(binned.getDimension(i).getMinimum())
    axis_max.append(binned.getDimension(i).getMaximum())
    axis_bins.append(binned.getDimension(i).getNBins())
    axis_units.append(binned.getDimension(i).getUnits())
    axis_name.append(binned.getDimension(i).getDimensionId())

# nexpy appears to not like '[',']' in axis names
#axis_name=['H','K','L']

# Get title from first run only
title=binned.getExperimentInfo(0).run().getProperty('run_title').value


# Write nexus file using h5py
h5f = h5py.File(fileOut, 'w')
nxentry = h5f.create_group("entry")
nxentry.attrs["NX_class"] = 'NXentry'
nxdata = nxentry.create_group("data")
nxdata.attrs["NX_class"] = 'NXdata'

for i in range(ndims):
    nxdata.create_dataset(axis_name[i],data=np.linspace(axis_min[i],axis_max[i],axis_bins[i]+1)).attrs['units']=axis_units[i]

sq=nxdata.create_dataset('Sq',data=s)
sq.attrs['units'] = 'Intensity'
sq.attrs["signal"]=1
sq.attrs["title"]=title

axis_name.reverse()
axes_names=':'.join(axis_name)
sq.attrs["axes"]=axes_names

h5f.close()
