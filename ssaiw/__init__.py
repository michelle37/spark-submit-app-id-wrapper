'''
A wrapper around spark-submit, specifically tested with YARN, to intercept and
extract the appliation id from stderr. Once the application id is detected, it
prints it to stderr, so that your calling script can process it.

The arguments to the app is your spark-submit command, e.g.:

# ssaiw spark-submit --master yarn-cluster --class etc etc
application_1448925599375_0050

There is no timeout functionality at the moment.
'''
from __future__ import print_function

import re
import subprocess
import sys

__version__ = '0.1.0'
__author__ = 'Gerald Kaszuba'


def wrap():
    process = subprocess.Popen(
        sys.argv[1:],
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    for line in iter(lambda: process.stderr.readline(), ''):
        print(line.strip())
        match = re.search('Submitted application (.*)$', line)
        if match:
            print(match.groups()[0], file=sys.stderr)
            process.kill()