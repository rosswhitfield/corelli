import numpy as np
import re

re_float = re.compile(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?")

d = dict()

with open('../tube_calibration/CalibTableNew_sort.txt','r') as file_p:
    for line in file_p:
        detID, *det_pos = re.findall(re_float, line)
        d[detID] = [float(x) for x in det_pos]

with open('CalibTable2_sort.txt','r') as file_p:
    for line in file_p:
        detID, *det_pos = re.findall(re_float, line)
        d[detID] = [float(x) for x in det_pos]

with open('CalibTable2_combined.txt','w') as file_p:
    for detID, det_pos in d.items():
        file_p.write('{},{}\n'.format(detID, det_pos))
