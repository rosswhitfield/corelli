import h5py
import json
import sys

f = h5py.File(sys.argv[1], 'r')

history = f['/MDHistoWorkspace/process/MantidAlgorithm_1']
