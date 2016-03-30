#!/usr/bin/python
import h5py
import sys

def read_write_mantid_MDHisto(inFile,outFile):
    print(inFile)
    print(outFile)
    inF = h5py.File(inFile, "r")
    outF = h5py.File(outFile, "w")
    path = 'MDHistoWorkspace/data/'

    # Copy signal
    data_out = outF.create_group("MDHistoWorkspace/data")
    signal = inF[path+'signal']
    data_out.copy(signal,'signal')

    # Copy axes
    axes = signal.attrs['axes'].decode().split(":")
    for a in axes:
        axis = inF[path+a]
        outF.copy(axis,path+a)

    # Copy sample lattice
    outF.copy(inF['MDHistoWorkspace/experiment0/sample/oriented_lattice'],'MDHistoWorkspace/experiment0/sample/oriented_lattice')

    top = outF['MDHistoWorkspace']
    top.attrs['SaveMDVersion'] = 2

    inF.close()
    outF.close()

if __name__ == "__main__":
    read_write_mantid_MDHisto(sys.argv[1],sys.argv[2])
