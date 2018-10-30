# PYSERVER
## simple port connectivity testing tool

### usage:
```
# pyserver 1234                 // spin up a listener on port 1234, netcat to it 'nc <hostname or IP> 1234 -vv'
# pyserver 1234 eth1            // spins up on port 1234 on interface 'eth1'
# pyserver 1234 eth1 -d         // spins up on port 1234 on interface 'eth1' and run in background
# pyserver stop                 // stops all instances of pyserver listerner
# pyserver help / -h / --help   // prints this message
```

### Install

place pyserver into /usr/local/bin

you should now be able to call pyserver from command line