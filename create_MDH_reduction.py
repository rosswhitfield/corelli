from mantid.simpleapi import LoadMD
from mantid.kernel import version_str
import json
import sys
import getpass
import datetime

output_file = sys.argv[1]

md = LoadMD(output_file)

if not md.isMDHistoWorkspace():
    raise ValueError('Needs to be MDHistoWorkspace')

output = {}

output['output_files'] = [{'location': output_file,
                           'type': 'processed',
                           'purpose': 'reduced-data',
                           'fields':{'foo':'bar'}}]
output['user'] = getpass.getuser()
output['created'] = datetime.datetime.now().replace(microsecond=0).isoformat()+'.00-05:00'

output['input_files'] = []


def get_children_algs(history, result):
    if history.childHistorySize() == 0:
        result.append(history)
    else:
        for histories in history.getChildHistories():
            get_children_algs(histories, result)


history = md.getHistory()
for hist in history.getAlgorithmHistories()[:-1]:
    algs = []
    get_children_algs(hist, algs)
    for alg in algs:
        if 'Load' in alg.name():
            file_type = 'user-provided'
            purpose =  'sample-data'
            if alg.name() in ["Load", "LoadEventNexus", "LoadWANDSCD"]:
                file_type = 'raw'
            elif alg.name() in ["LoadNexus"]:
                file_type = 'processed'
                purpose = 'intermediate'
                continue
            elif alg.name() in ["LoadInstrument", "LoadIsawUB"]:
                continue
            for prop in alg.getProperties():
                if "Filename" in prop.name():
                    output['input_files'].append({'location': prop.value(),
                                                  'type': file_type,
                                                  'purpose': purpose})

metadata = {}

"""
metadata['dimensions'] = []
for ndim in range(md.getNumDims()):
    dim = md.getDimension(ndim)
    metadata['dimensions'].append({'id': dim.getDimensionId(),
                                   'name': dim.getName(),
                                   'units': dim.getUnits(),
                                   'minimum': dim.getMinimum(),
                                   'maximum': dim.getMaximum(),
                                   'number_of_bins': dim.getNBins(),
                                   'bin_width': dim.getBinWidth()})
"""
sample = {}
sample['name'] = md.getExperimentInfo(0).sample().getName()
ol = md.getExperimentInfo(0).sample().getOrientedLattice()
sample['a'] = ol.a()
sample['b'] = ol.b()
sample['c'] = ol.c()
sample['alpha'] = ol.alpha()
sample['beta'] = ol.beta()
sample['gamma'] = ol.gamma()
"""
sample['UB'] = str(ol.getUB())
"""
metadata['sample'] = sample

output['metadata'] = metadata
#output['mantid_version'] = version_str()

with open('out.json', 'w') as f:
    json.dump(output, f)
