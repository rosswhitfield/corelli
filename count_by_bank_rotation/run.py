Bimport matplotlib.pyplot as plt
import h5py


IPTS = 21655
runs = range(91699,91771)


for run in runs:
    filename = '/SNS/CORELLI/IPTS-{}/nexus/CORELLI_{}.nxs.h5'.format(IPTS,run)
    print(run)
    with h5py.File(filename,'r') as f:
        
