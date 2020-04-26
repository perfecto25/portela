from __future__ import print_function
import sys
import os
import socket
import subprocess
import psutil
import multiprocessing
import argparse
import textwrap



class color:
    GREEN = '\x1b[0;32;40m' 
    BLUE = '\x1b[0;34;40m' 
    YELLOW = '\x1b[0;33;40m'
    TEAL = '\x1b[0;36;40m'
    WHITE = '\x1b[0;37;40m'
    RED = '\x1b[1;31;40m'
    GRAY = '\x1b[2;37;40m'
    END = '\x1b[0m'


def __get_network():
    ''' get primary IP and Hostname of your host '''
    network = []
    # add your Hostname
    # network.append(socket.gethostname())

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
    network.append(IP)
    return network[0]


def __serve(args):
    ''' start a local webserver on a port '''
    
    port = str(args.port)
    msg = str(args.m)

    if not port.isdigit():
        print('pass a numeric port, ie: 7500')
        sys.exit()

    ## check python version thats currently running Portela
    
    # Python 2
    if sys.version_info[0] is 2:
        import SimpleHTTPServer as shs
        import BaseHTTPServer as bhs
        import SocketServer as ss

        network = __get_network()
        print(network)
        handler = shs.SimpleHTTPRequestHandler
        server = ss.TCPServer((network, int(port)), handler)
        print(color.GREEN + '\nPortela serving on port: ' + port + color.END)
        print(color.GREEN + 'Connect to this machine using netcat: ' + color.END)
        print(color.TEAL + 'nc -zv ' + network[0] + ' ' + port + color.END)
        print(color.TEAL + 'nc -zv ' + network[1] + ' ' + port + color.END)
        return server.serve_forever()



    # Python 3
    elif sys.version_info[0] is 3:
        
        from http.server import HTTPServer, BaseHTTPRequestHandler
        from io import BytesIO
        
        class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'Hello, world!')

            def do_POST(self):
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length)
                self.send_response(200)
                self.end_headers()
                response = BytesIO()
                response.write(b'This is POST request. ')
                response.write(b'Received: ')
                response.write(body)
                self.wfile.write(response.getvalue())
        network = __get_network()
        httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
        print(color.GREEN + '\nPortela serving on port: ' + port + color.END)
        print(color.GREEN + 'Connect to this machine using netcat: ' + color.END)
        print(color.TEAL + 'nc -zv ' + network[0] + ' ' + port + color.END)
        print(color.TEAL + 'nc -zv ' + network[1] + ' ' + port + color.END)
        return httpd.serve_forever()
        
    else:
        print('Python version mismatch, only comptabile with Python2 or Python3')
        sys.exit()




def __stop(args):
    ps = subprocess.Popen(('ps', 'aux'), stdout=subprocess.PIPE)
    procs = ps.communicate()[0]
    for proc in procs.split('\n'):
        if 'portela' in proc:
            if 'portela stop' not in proc:
                #print(proc.split())
                p = psutil.Process(int(proc.split()[1]))
                print(p)
                p.terminate()  #or p.kill()



def __status(args):
    print('status')

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
serve_parser.add_argument('-m', action='store', help='message to output during HTTP connection')
serve_parser.set_defaults(func=__serve)

stop_parser = subparsers.add_parser('stop')
stop_parser.set_defaults(func=__stop)

status_parser = subparsers.add_parser('status')
status_parser.set_defaults(func=__status)

def entry():
    args = parser.parse_args()
    print(args)
    args.func(args)  # call the default function
