import os
from mantid.simpleapi import CreateEmptyTableWorkspace
table = CreateEmptyTableWorkspace()

table.addColumn("int", "Run Number")
table.addColumn("str", "UB")

file_list = sorted(f for f in os.listdir() if 'CORELLI_' in f and '.mat' in f)

for f in file_list:
    run_number = int(os.path.basename(f).replace('CORELLI_','').replace('.mat',''))
    table.addRow([run_number, 10245])

