import h5py
import json
import sys
import re

output_file = sys.argv[1]

f = h5py.File(output_file, 'r')

output = {}

output['output_files'] = [{'location':output_file, 'type':'MDHistoWorkspace'}]

history = f['/MDHistoWorkspace/process/MantidAlgorithm_1/data']

output['input_files'] = 
