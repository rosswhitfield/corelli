#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function, unicode_literals)

import oauthlib
import requests_oauthlib
import getpass
import sys
import re

CLIENT_ID = '9e736eae-f90c-4513-89cf-53607eee5165'
CLIENT_SECRET = None


class InMemoryTokenStore(object):
    def __init__(self):
        self._token = None

    def set_token(self, token):
        self._token = token

    def get_token(self):
        return self._token


token_store = InMemoryTokenStore()


def get_client():
    if token_store.get_token() is None:
        username = getpass.getuser()
        password = getpass.getpass()
        initial_oauth_client = requests_oauthlib.OAuth2Session(
            client=oauthlib.oauth2.LegacyApplicationClient(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
            )
        )
        token = initial_oauth_client.fetch_token(
            'https://oncat.ornl.gov/oauth/token',
            username=username,
            password=password,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
        )
        token_store.set_token(token)

    auto_refresh_client = requests_oauthlib.OAuth2Session(
        CLIENT_ID,
        token=token_store.get_token(),
        auto_refresh_url='https://oncat.ornl.gov/oauth/token',
        auto_refresh_kwargs={
            'client_id': CLIENT_ID,
        },
        token_updater=token_store.set_token
    )

    return auto_refresh_client


SAMPLEENV = ['CCR', 'SlimSAM', 'dilfridge', 'dilfridge.SilmSAM', 'OC', 'He3insert', 'Micas70mm']

title = {'CCR': "RUN,IPTS,START TIME,END TIME,DURATION,PROTON CHARGE,TITLE,TOTAL COUNTS,SAMPLE OMEGA,CCR-ColdTip,CCR-Sample\n",
         'SlimSAM': "RUN,IPTS,START TIME,END TIME,DURATION,PROTON CHARGE,TITLE,TOTAL COUNTS,SAMPLE PHI,OC-COLD-TIP,OC-SAMPLE,Mag-Field\n",
         'dilfridge': "RUN,IPTS,START TIME,END TIME,DURATION,PROTON CHARGE,TITLE,TOTAL COUNTS,SAMPLE PHI,DILFRIDGE-COLD-TIP,DILFRIDGE-SAMPE\n",
         'dilfridge.SilmSAM': "RUN,IPTS,START TIME,END TIME,DURATION,PROTON CHARGE,TITLE,TOTAL COUNTS,SAMPLE PHI,DILFRIDGE-COLD-TIP,DILFRIDGE-SAMPE,Mag-Field\n",
         'OC': "RUN,IPTS,START TIME,END TIME,DURATION,PROTON CHARGE,TITLE,TOTAL COUNTS,SAMPLE PHI,OC-COLD-TIP,OC-SAMPE\n",
         'He3insert': "RUN,IPTS,START TIME,END TIME,DURATION,PROTON CHARGE,TITLE,TOTAL COUNTS,SAMPLE PHI,He3Sample,He3VTI\n",
         'Micas70mm': "RUN,IPTS,START TIME,END TIME,DURATION,PROTON CHARGE,TITLE,TOTAL COUNTS,SAMPLE OMEGA,MicasSamp,MicasOT\n"}

projections = {'CCR': ['metadata.entry.run_number',
                       'metadata.entry.experiment_identifier',
                       'metadata.entry.start_time',
                       'metadata.entry.end_time',
                       'metadata.entry.duration',
                       'metadata.entry.proton_charge',
                       'metadata.entry.title',
                       'metadata.entry.total_counts',
                       'metadata.entry.daslogs.bl9:mot:sample:axis1.average_value',
                       'metadata.entry.daslogs.bl9:se:lakeshore:krdg2.average_value',
                       'metadata.entry.daslogs.bl9:se:lakeshore:krdg3.average_value'],
               'SlimSAM': ['metadata.entry.run_number',
                           'metadata.entry.experiment_identifier',
                           'metadata.entry.start_time',
                           'metadata.entry.end_time',
                           'metadata.entry.duration',
                           'metadata.entry.proton_charge',
                           'metadata.entry.title',
                           'metadata.entry.total_counts',
                           'metadata.entry.daslogs.bl9:mot:sample:axis2.average_value',
                           'metadata.entry.daslogs.bl9:se:cryo:temp:krdg1.average_value',
                           'metadata.entry.daslogs.bl9:se:cryo:temp:krdg2.average_value',
                           'metadata.entry.daslogs.bl9:se:slimsam:fieldset.average_value'],
               'dilfridge': ['metadata.entry.run_number',
                             'metadata.entry.experiment_identifier',
                             'metadata.entry.start_time',
                             'metadata.entry.end_time',
                             'metadata.entry.duration',
                             'metadata.entry.proton_charge',
                             'metadata.entry.title',
                             'metadata.entry.total_counts',
                             'metadata.entry.daslogs.bl9:mot:sample:axis2.average_value',
                             'metadata.entry.daslogs.bl9:se:dilfridge:temperature5.average_value',
                             'metadata.entry.daslogs.bl9:se:dilfridge:temperature5.average_value'],
               'dilfridge.SilmSAM': ['metadata.entry.run_number',
                                     'metadata.entry.experiment_identifier',
                                     'metadata.entry.start_time',
                                     'metadata.entry.end_time',
                                     'metadata.entry.duration',
                                     'metadata.entry.proton_charge',
                                     'metadata.entry.title',
                                     'metadata.entry.total_counts',
                                     'metadata.entry.daslogs.bl9:mot:sample:axis2.average_value',
                                     'metadata.entry.daslogs.bl9:se:dilfridge:temperature5.average_value',
                                     'metadata.entry.daslogs.bl9:se:dilfridge:temperature5.average_value',
                                     'metadata.entry.daslogs.bl9:se:slimsam:fieldset.average_value'],
               'OC': ['metadata.entry.run_number',
                      'metadata.entry.experiment_identifier',
                      'metadata.entry.start_time',
                      'metadata.entry.end_time',
                      'metadata.entry.duration',
                      'metadata.entry.proton_charge',
                      'metadata.entry.title',
                      'metadata.entry.total_counts',
                      'metadata.entry.daslogs.bl9:mot:sample:axis2.average_value',
                      'metadata.entry.daslogs.bl9:se:cryo:temp:krdg0.average_value',
                      'metadata.entry.daslogs.bl9:se:cryo:temp:krdg1.average_valus'],
               'He3insert': ['metadata.entry.run_number',
                             'metadata.entry.experiment_identifier',
                             'metadata.entry.start_time',
                             'metadata.entry.end_time',
                             'metadata.entry.duration',
                             'metadata.entry.proton_charge',
                             'metadata.entry.title',
                             'metadata.entry.total_counts',
                             'metadata.entry.daslogs.bl9:mot:sample:axis2.average_value',
                             'metadata.entry.daslogs.bl9:se:lakeshore:krdg0.average_value',
                             'metadata.entry.daslogs.bl9:se:lakeshore:krdg2.average_value'],
               'Micas70mm': ['metadata.entry.run_number',
                             'metadata.entry.experiment_identifier',
                             'metadata.entry.start_time',
                             'metadata.entry.end_time',
                             'metadata.entry.duration',
                             'metadata.entry.proton_charge',
                             'metadata.entry.title',
                             'metadata.entry.total_counts',
                             'metadata.entry.daslogs.bl9:mot:sample:axis1.average_value',
                             'metadata.entry.daslogs.bl9:se:nd1:ch1:pv.average_value',
                             'metadata.entry.daslogs.bl9:se:nd1:ch2:pv.average_value']}


def extract_value(datafile, proj):
    output = datafile
    proj = proj.split('.')
    try:
        while len(proj) > 0:
            output = output.get(proj.pop(0))
        output = str(output).replace(',', ' ')  # Remove any `,` from values
        output = re.sub('T(..:..:..).*', 'T\g<1>', output)  # Remove fractional seconds
        output = re.sub('(\.[0-9]{4})[0-9]*', '\g<1>', output)  # Truncate decimals after 4 digits
        return output
    except AttributeError:
        return ''


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Create experiment summary using ONCat")
    parser.add_argument('IPTS', help='Specify the IPTS number')
    parser.add_argument("-s", "--sampleenvironment", dest="sampleenvironment", default="CCR",
                        choices=SAMPLEENV,
                        help="Specify the sample enviroment to use")
    parser.add_argument("-f", "--filename", dest="filename",
                        help="output filename, otherwise it will output to stdout")

    options = parser.parse_args()
    ipts = options.IPTS

    client = get_client()

    sampleenv = options.sampleenvironment

    datafiles = client.get(
        "https://oncat.ornl.gov/api/datafiles/",
        params={
            'experiment': "IPTS-"+str(ipts),
            'facility': "SNS",
            'instrument': "CORELLI",
            'projection': projections[sampleenv]}
    )

    if options.filename:
        f = open(options.filename, 'w')
    else:
        f = sys.stdout

    f.write(title[sampleenv])
    for datafile in datafiles.json():
        f.write(','.join(extract_value(datafile, projection) for projection in projections[sampleenv])+'\n')

    if f is not sys.stdout:
        f.close()
