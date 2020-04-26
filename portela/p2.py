from __future__ import print_function
import argparse
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(description='Portela - a simple port listener', \
 usage='''
    \nportela -p 1234           # listen on port 1234 \
    \nportela -p 1234 -d        # listen on port 1234, run daemon mode \
    \nportela -p 1234 -i eth2   # listen on specific interface \
    \nportela stop \
    \nportela status ', formatter_class=RawTextHelpFormatter, usage="")
''')

parser.add_argument('command', action="store", choices=['start', 'status', 'stop'])
parser.add_argument('-p', action="store", help="port to listen on", type=int)
parser.add_argument('-i', action="store", help="network interface name to bind to, (eth0, em1, etc)")
parser.add_argument('-d', action="store", help="run in daemon mode")
parser.add_argument('--version', '-v', action='version', version='portela 0.1.1')
args = parser.parse_args()

print(args)