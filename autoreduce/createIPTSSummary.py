#!/usr/bin/python
import os
import sys
import subprocess

instrument='CORELLI'
summary_script = os.path.join('/SNS', instrument, 'shared', 'autoreduce', "sumRun_%s.py" % instrument)

if __name__ == "__main__":
    # set up the options 
    if len(sys.argv) != 3:
        print("run_info takes 2 arguments: ITPS number and output file. Exiting...")
        sys.exit(-1)

    nexus_path = '/SNS/'+instrument+'/IPTS-'+sys.argv[1]+'/nexus/'
    files = os.listdir(nexus_path)
    files.sort()
    for f in files:
        subprocess.call([summary_script, instrument, nexus_path+f, sys.argv[2]])
