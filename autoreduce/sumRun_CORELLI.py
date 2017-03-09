#!/usr/bin/python
import h5py
import os
import sys
import numpy
import csv
import re
try:
    import ConfigParser as configparser
except ImportError:
    import configparser


class RunInfo:
    def __init__(self, instrument, infilename):
        self._names = []
        self._nodes = []
        self._values = []
        self._infilename = infilename
        config_path = '/SNS/' + instrument + '/shared/autoreduce/sumRun_' + instrument + '.cfg'
        print(config_path)
        config = configparser.SafeConfigParser()
        config.read(config_path)
        self._names = config.get("header", "names").split(',')

        for name in self._names:
            self._nodes.append(config.get('node', name))

    def fillRunData(self):
        # open nexus file
        with h5py.File(self._infilename, 'r') as f:
            for node in self._nodes:
                try:
                    value = f[node].value
                    if isinstance(value, numpy.ndarray):
                        if value.shape == (1,):
                            value = value[0]
                        else:
                            value = sum(value)
                        if isinstance(value, bytes):
                            value = value.decode().replace(',','')
                        if 'time' in node.lower():
                            value = re.sub('\..*','',value) # remove fractional seconds
                except Exception as e:
                    print(e)
                    value = 'N/A'
                self._values.append(str(value))

    def getNames(self):
        return self._names

    def getValues(self):
        return self._values


if __name__ == "__main__":
    # set up the options
    if len(sys.argv) != 4:
        print("run_info takes 3 arguments: instrument, nexus file and output file. Exiting...")
        sys.exit(-1)

    print(sys.argv[1])
    print(sys.argv[2])
    print(sys.argv[3])
    runInfo = RunInfo(sys.argv[1], sys.argv[2])
    runInfo.fillRunData()

    outfile = sys.argv[3]

    # create the output file or stdout as appropriate
    if os.path.exists(outfile):
        f = open(outfile, 'a')
        writer = csv.writer(f)
    else:
        f = open(outfile, 'w')
        writer = csv.writer(f)
        handle = open(outfile, "w")
        # get header information for the csv file
        writer.writerow(runInfo.getNames())

    writer.writerow(runInfo.getValues())
    f.close()
