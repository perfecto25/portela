# Portela

![](portela.png)

## a simple port allocator

Portela is a Python 2 & 3 compatible port allocator with zero dependencies.

Portela can be used to test basic port connectivity on your host and lets you open up ports on various network interfaces.

You can do the same functions with netcat, SimpleHTTPServer, socat and various other tools, but Portela is more user-friendly and offers a simple way to bind to various network interfaces.

Python compatibility: 2.7.x - 3.8.x

Platform compatibility: Linux

### usage:
```
# portela 1234                      // spin up a listener on port 1234
# portela 1234 -i eth1              // spins up on port 1234 on interface 'eth1'
# portela 1234 -i eth1 -d           // spins up on port 1234 on interface 'eth1' and run as daemon
# portela 1234 -m "samba magic"     // spins up on port 1234 and return a message on HTTP call
# portela stop                 // stops all instances of portela listerner
# portela status                 // check if portela is running as daemon
# portela help / -h / --help   // prints this message
```

### Install

pip install portela

### Testing
Local testing

    sudo pip install -e /path/to/portela


### Daemon
When Portela puts the listener in background as daemon, it creates a PID file (.portela.pid) in /home/user directory

Daemon functions are taken from this article: https://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/