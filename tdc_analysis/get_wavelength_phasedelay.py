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



projection = ['metadata.entry.run_number',
              'metadata.entry.daslogs.bl9:chop:skf4:wavelengthset.average_value',
              'metadata.entry.daslogs.bl9:chop:skf4:phasetimedelayset.average_value']

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
    parser.add_argument("-f", "--filename", dest="filename",
                        help="output filename, otherwise it will output to stdout")

    options = parser.parse_args()
    ipts = options.IPTS

    client = get_client()

    datafiles = client.get(
        "https://oncat.ornl.gov/api/datafiles/",
        params={
            #'experiment': "IPTS-"+str(ipts),
            'facility': "SNS",
            'instrument': "CORELLI",
            'projection': projection}
    )

    if options.filename:
        f = open(options.filename, 'w')
    else:
        f = sys.stdout

    for datafile in datafiles.json():
        f.write(','.join(extract_value(datafile, p) for p in projection)+'\n')

    if f is not sys.stdout:
        f.close()
