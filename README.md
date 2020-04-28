# Portela
## a simple port allocator

Portela is a Python 2 & 3 compatible network tool with zero dependencies.

Portela can be used to test port c
### usage:
```
# portela 1234                 // spin up a listener on port 1234, netcat to it 'nc <hostname or IP> 1234 -vv'
# portela 1234 eth1            // spins up on port 1234 on interface 'eth1'
# portela 1234 eth1 -d         // spins up on port 1234 on interface 'eth1' and run in background
# portela stop                 // stops all instances of portela listerner
# portela help / -h / --help   // prints this message
```

### Install

pip install portela

### Testing
Local testing

    sudo pip install -e /path/to/portela


### Daemon
Daemon functions are taken from this article: https://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/