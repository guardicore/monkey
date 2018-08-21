# Improvements needed

* Remove embedded mongodb from .deb, it forbids installation on a `debian:stretch` distro.
* Package monkey for system's python usage.
* Fix package number: (I installed the 1.5.2)
```
ii  gc-monkey-island           1.0                      amd64        Guardicore Infection Monkey Island installation package
```
* Use .deb dependencies for mongodb setup?
* Use docker-compose for stack construction.
* Remove the .sh script from the systemd unit file (`/var/monkey_island/ubuntu/systemd/start_server.sh`) which only does a `cd && localpython run`