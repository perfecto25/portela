#!/usr/bin/env python
# -*- encoding: utf-8 -*-

### PORTELA
# Simple testing webserver, can spin up webserver on port or a specific network interface

# USAGE:
# portela 1234                 // spin up a listener on port 1234, netcat to it 'nc <hostname or IP> 1234 -vv'
# portela 1234 eth1            // spins up on port 1234 on interface 'eth1'
# portela 1234 eth1 -d         // spins up on port 1234 on interface 'eth1' and run in background
# portela status               // shows active ports
# portela stop                 // stops all instances of portela listerner
# portela help / -h / --help   // prints this message


from __future__ import print_function
import SimpleHTTPServer as shs
import BaseHTTPServer as bhs
import SocketServer as ss
import sys
import os
import socket
import subprocess
import psutil
import multiprocessing

class color:
    GREEN = '\x1b[0;32;40m' 
    BLUE = '\x1b[0;34;40m' 
    YELLOW = '\x1b[0;33;40m'
    TEAL = '\x1b[0;36;40m'
    WHITE = '\x1b[0;37;40m'
    RED = '\x1b[1;31;40m'
    GRAY = '\x1b[2;37;40m'
    END = '\x1b[0m'

# def check_port(port):
#     ''' checks port for propert syntax '''
#     if port.isdigit() is False:

def get_network():
    ''' get primary IP and Hostname of your host '''
    network = []
    # add your Hostname
    network.append(socket.gethostname())

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
    return network

def start_server(port):
    ''' start a local webserver on a port '''
    network = get_network()
    handler = shs.SimpleHTTPRequestHandler
    server = ss.TCPServer(('', int(port)), handler)
    print(color.GREEN + '\nPyserver serving at port: ' + port + color.END)
    print(color.GREEN + '\nConnect to this machine using netcat: ' + color.END)
    print(color.TEAL + '\nnc ' + network[0] + ' ' + port + ' -vv' + color.END)
    print(color.TEAL + '\nnc ' + network[1] + ' ' + port + ' -vv \n' + color.END)
    return server.serve_forever()

def stop_process():
    ps = subprocess.Popen(('ps', 'aux'), stdout=subprocess.PIPE)
    procs = ps.communicate()[0]
    for proc in procs.split('\n'):
        if 'pyserver' in proc:
            if 'pyserver stop' not in proc:
                #print(proc.split())
                p = psutil.Process(int(proc.split()[1]))
                print(p)
                p.terminate()  #or p.kill()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(color.RED + '\nNo arguments provided..exiting.\n' + color.END)
        print(color.WHITE + 'usage: \n')
        print('pyserver 1234  ' + color.GRAY + '# runs test pyserver on port 1234' +
        color.WHITE + 'pyserver 1234 eth1  ' + color.GRAY + '# runs test pyserver on port 1234 on interface eth1' +
        color.WHITE + 'pyserver 1234 -d  ' + color.GRAY + '# run in background as daemon' +
        color.WHITE + 'pyserver stop  ' + color.GRAY + '# stop all instances of pyserver\n' + color.END)
        sys.exit()

    # run as non daemon with port
    if len(sys.argv) == 2:
        if sys.argv[1] != 'stop':
            port = sys.argv[1]
            
            # check if 2nd arg is a port
            if port.isdigit():
                start_server(port)
            elif sys.argv[1] == 'help' or sys.argv[1] == '--help' or sys.argv[1] == '-h':
                print(color.WHITE + 'help text here \n' + color.END)
            else:
                print(color.RED + 'ERROR ' + color.WHITE + 'provided Port is not numeric: %s' % color.YELLOW + port + color.END)
        elif sys.argv[1] == 'stop':
            stop_process()

    # Daemon
    if len(sys.argv) == 3:
        if sys.argv[2] == '-d':
            
            port = sys.argv[1]

            if port.isdigit():
                #port = int(port)
                d = multiprocessing.Process(target=start_server, args=port)
                d.start()
                d.join()
#                #d.daemon = True
#                d.start()
#                d.join()
#                t = threading.Thread(target=bg_run.display)
#t.daemon = True
#t.start()
#     else:
#         import psutil
#         addrs = psutil.net_if_addrs()
#         interfaces = addrs.keys()
#         if sys.argv[2] not in interfaces:
#             print('selected network interface: %s is not available' % sys.argv[2])
#             print('available interfaces: %s' % interfaces)

# print(color.YELLOW+'Running test pyserver..'+color.END)
# # handler = shs.SimpleHTTPRequestHandler
# # py_web_server = ss.TCPServer(('', port), handler)
# # print 'python web server. serving at port', port
# # py_web_server.serve_forever()



#, SimpleHTTPServer as shs; bhs.HTTPServer(("192.168.200.99", 8331), shs.SimpleHTTPRequestHandler).serve_forever()