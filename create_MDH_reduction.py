from mantid.simpleapi import LoadMD
import h5py
import json
import sys
import getpass
import datetime
import os

output_file = sys.argv[1]

md = LoadMD(output_file)

output = {}

output['output_files'] = [{'location':output_file, 'type':'MDHistoWorkspace'}]
output['user'] = getpass.getuser()
output['created'] = datetime.datetime.now().replace(microsecond=0).isoformat()


output['input_files'] = []

"""
f = h5py.File(output_file, 'r')

history = f['/MDHistoWorkspace/process/MantidAlgorithm_1/data']

for hist in history:
    for prop in hist.decode().split('Name: '):
        for part in prop.split(', '):
            if part[0] == 'SolidAngle' or part[0] == 'Flux':
                output['input_files'].append({'location':part[1], 'type':'type'})
"""

def get_children_algs(history):
    if history.childHistorySize() == 0:
        return [history]
    else:
        return [get_children_algs(histories) for histories in history.getChildHistories()]

history = md.getHistory()
for hist in history.getAlgorithmHistories():
    for alg in get_children_algs(hist):
        if 'Load' in alg.name():
            for prop in alg.getProperties():
                if "Filename" in prop.name():
                    output['input_files'].append({'location':prop.value(), 'type':'type'})


print(json.dumps(output))

