#from mantid.simpleapi import LoadMD
import h5py
import json
import sys
import getpass
import datetime
import os

output_file = sys.argv[1]

f = h5py.File(output_file, 'r')

output = {}

output['output_files'] = [{'location':output_file, 'type':'MDHistoWorkspace'}]
output['user'] = getpass.getuser()
output['created'] = datetime.datetime.fromtimestamp(os.path.getmtime('/SNS/CORELLI/IPTS-15526/shared/Normalized_300K_noCC_Simple.nxs')).isoformat()

history = f['/MDHistoWorkspace/process/MantidAlgorithm_1/data']

output['input_files'] = []

for hist in history:
    for prop in hist.decode().split('Name: '):
        for part in prop.split(', '):
            if part[0] == 'SolidAngle' or part[0] == 'Flux':
                output['input_files'].append({'location':part[1], 'type':'type'})

print(json.dumps(output))

