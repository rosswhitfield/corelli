import os
import numpy as np
from mantid.simpleapi import CreateEmptyTableWorkspace
table = CreateEmptyTableWorkspace()

table.addColumn("int", "Run Number")
table.addColumn("str", "UB")

file_list = sorted(f for f in os.listdir() if 'CORELLI_' in f and '.mat' in f)

for f in file_list:
    run_number = int(os.path.basename(f).replace('CORELLI_','').replace('.mat',''))
    with open(f) as f_in:
        ub = np.array([line.split() for line in f_in.readlines()[:3]]).astype(float)

    # Convert from IPNS to Mantid convention
    ub = np.roll(ub.T, -1, axis=0)
    table.addRow([run_number, str(ub.ravel().tolist()).replace('[','').replace(']','')])

