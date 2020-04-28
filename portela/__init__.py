from __future__ import print_function
import sys
import os
import socket
import subprocess
import argparse
import psutil
import textwrap
from daemon import Daemon
from os.path import expanduser
user_home = expanduser("~")

GREEN = '\x1b[0;32;40m' 
BLUE = '\x1b[0;34;40m' 
YELLOW = '\x1b[0;33;40m'
TEAL = '\x1b[0;36;40m'
WHITE = '\x1b[0;37;40m'
RED = '\x1b[1;31;40m'
GRAY = '\x1b[2;37;40m'
END = '\x1b[0m'


def _get_network():
    ''' get primary IP of your host '''

    # add your primary IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def _serve(args):
    ''' start a local webserver on a port '''
 
    port = str(args.port)
   

    if not port.isdigit():
        print('pass a numeric port, ie: 7500')
        sys.exit()

    ## check python version thats currently running Portela
    # Python 2
    if sys.version_info[0] is 2:
        import SimpleHTTPServer
        import BaseHTTPServer as bhs
        import SocketServer
        http_handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        http_server = SocketServer.TCPServer

    # Python 3
    elif sys.version_info[0] is 3:
        from http.server import HTTPServer, BaseHTTPRequestHandler
        http_handler = BaseHTTPRequestHandler
        http_server = HTTPServer

    else:
        print('Python version mismatch, only comptabile with Python2 or Python3')
        sys.exit()

    IP = _get_network()


    class Handler(http_handler):
            
        def _set_headers(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        def _msg(self, message):
            return message.encode("utf8")  # NOTE: must return a bytes object!

        def do_GET(self):

            if not args.message:
                message = 'portela!'
            else:
                message = str(args.message)

            self._set_headers()
            self.wfile.write(self._msg(message))

        def do_HEAD(self):
            self._set_headers()

        def do_POST(self):
            # Doesn't do anything with posted data
            self._set_headers()
            self.wfile.write(self._msg("POST!"))

    server = http_server((IP, int(port)), Handler)
    print(GREEN + '\nPortela serving on port: ' + port + END)
    print(GREEN + 'Connect to this machine using netcat: ' + END)
    print(TEAL + 'nc -zv ' + IP + ' ' + port + END)
    return server.serve_forever()


def _main(args, action='status'):
    """ start the server either as daemon or standalone """

    print(args)
    class PortelaDaemon(Daemon):
        def run(self):
            while True:
                _serve(args)
    
    d = PortelaDaemon(user_home + '/.portela.pid')

    if args.action == 'start':
        print('starting!!')
        if args.daemon:
            d.start()
            print("serving Portela as daemon")    
        else:
            _serve(args)

    if args.action == 'stop':
        d.stop()

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''

    A Simple Port Listener

    portela serve 5432                  (listens on port 5432)
    portela serve 5432 -m 'Hello there' (listens on port 5432 and outputs message)
    portela serve 5432 -i eth1          (listens on port 5432 interface eth1)
    portela serve 5432 -d               (run in background as daemon)
    portela stop                        (stop all portela instances)
    portela status                      (check if any portela ports are up)

    '''))


subparsers = parser.add_subparsers()
serve_parser = subparsers.add_parser('serve', help='serve HTTP listener on a port')
serve_parser.add_argument('port', help='port to listen on', type=int)
serve_parser.add_argument('-m', '--message', action='store', help='message to output during HTTP connection')
serve_parser.add_argument('-d', '--daemon', action='store_true', default=False, help='run Portela as a daemon')
serve_parser.set_defaults(func=_main, action='start')
stop_parser = subparsers.add_parser('stop')
stop_parser.set_defaults(func=_main, action='stop')
status_parser = subparsers.add_parser('status')
status_parser.set_defaults(func=_main, action='status')

def entry():
    args = parser.parse_args()
    args.func(args)  # call the default function
