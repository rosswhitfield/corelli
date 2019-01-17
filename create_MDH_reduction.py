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

def get_children_algs(history, result):
    if history.childHistorySize() == 0:
        result.append(history)
    else:
        for histories in history.getChildHistories():
            get_children_algs(histories,result)

history = md.getHistory()
for hist in history.getAlgorithmHistories():
    algs = []
    get_children_algs(hist, algs)
    for alg in algs:
        if 'Load' in alg.name():
            file_type = 'user-provided'
            if alg.name() in ["Load", "LoadEventNexus"]:
                file_type = 'raw'
            elif alg.name() in ["LoadNexus"]:
                file_type = 'processed'
            for prop in alg.getProperties():
                if "Filename" in prop.name():
                    output['input_files'].append({'location':prop.value(), 'type':file_type})

metadata = {}

metadata['dimensions'] = []
for ndim in range(md.getNumDims()):
    dim = md.getDimension(ndim)
    metadata['dimensions'].append({'id':dim.getDimensionId(),
                                   'name':dim.getName(),
                                   'units':dim.getUnits(),
                                   'minimum':dim.getMinimum(),
                                   'maximum':dim.getMaximum(),
                                   'number_of_bins':dim.getNBins(),
                                   'bin_width':dim.getBinWidth()})

metadata['sample']

output['metadata'] = metadata

print(json.dumps(output))

