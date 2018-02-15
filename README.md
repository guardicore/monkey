Infection Monkey
====================

### Data center Security Testing Tool
------------------------

Welcome to the Infection Monkey! 

The Infection Monkey is an open source security tool for testing a data center's resiliency to perimeter breaches and internal server infection. The Monkey uses various methods to self propagate across a data center and reports success to a centralized Monkey Island Command and Control server.

The Infection Monkey is comprised of two parts:
* Chaos Monkey - A tool which infects other machines and propagates to them
* Monkey Island - A dedicated UI to visualize the Chaos Monkey's progress inside the data center

To read more about the Monkey, visit http://infectionmonkey.com 

Main Features
---------------

The Infection Monkey uses the following techniques and exploits to propagate to other machines.

* Multiple propagation techniques:
  * Predefined passwords
  * Common logical exploits
  * Password stealing using Mimikatz
* Multiple exploit methods:
  * SSH
  * SMB
  * RDP
  * WMI
  * Shellshock
  * Conficker
  * SambaCry
  * Elastic Search (CVE-2015-1427)


Getting Started
---------------

### Requirements

The Monkey Island server has been tested on Ubuntu 14.04,15.04 and 16.04 and Windows Server 2012.
The Monkey itself has been tested on Windows XP, 7, 8.1 and 10. The Linux build has been tested on Ubuntu server and Debian (multiple versions).

### Installation

For off-the-shelf use, download a Debian package from our website and follow the guide [written in our blog](https://www.guardicore.com/2016/07/infection-monkey-loose-2/).
Warning! The Debian package will uninstall the python library 'bson' because of an issue with pymongo. You can reinstall it later, but monkey island will probably not work.

To manually set up and the Monkey Island server follow the instructions on [Monkey Island readme](monkey_island/readme.txt). If you wish to compile the binaries yourself, follow the instructions under Building the Monkey from Source.

### Start Infecting

After installing the Infection Monkey on a server of your choice, just browse https://your-server-ip:5000 and follow the instructions to start infecting.


Building the Monkey from source
-------------------------------
If you want to build the monkey from source instead of using our provided packages, follow the instructions at the readme files under [chaos_monkey](chaos_monkey) and [monkey_island](monkey_island). 


License
=======
Copyright (c) 2017 Guardicore Ltd

See the [LICENSE](LICENSE) file for license rights and limitations (GPLv3).