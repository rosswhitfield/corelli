#!/usr/bin/python
import sys
import subprocess

instrument = 'CORELLI'
sumRun = '/SNS/'+instrument+"/shared/autoreduce/sumRun_%s.py" % instrument

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            """createSummary takes 2 arguments: IPTS number or run numbers and output file.

Examples:
    {0} IPTS-12310 summary.csv
    {0} 12345 summary.csv
    {0} 12345,12500,13000 summary.csv
    {0} 12345-12350 summary.csv

Exiting...""".format(sys.argv[0]))
        sys.exit()

    if 'IPTS' in sys.argv[1]:
        runs = subprocess.check_output(['finddata', instrument, '--listruns', sys.argv[1]])
        files = subprocess.check_output(['finddata', instrument, runs])
    else:
        files = subprocess.check_output(['finddata', instrument, sys.argv[1]])

    files = files.split()

    for f in files:
        subprocess.call([sumRun, instrument, f, sys.argv[2]])
