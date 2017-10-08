Infection Monkey
====================

### Data center Security Testing Tool
------------------------

Welcome to the Infection Monkey! 

The Infection Monkey is an open source security tool for testing a data center's resiliency to perimeter breaches and internal server infection. The Monkey uses various methods to self propagate across a data center and reports success to a centralized C&C server. To read more about the Monkey, visit https://www.guardicore.com/infectionmonkey/ 

### http://www.guardicore.com/the-infected-chaos-monkey/

Features include:

* Multiple propagation techniques:
  * Predefined passwords
  * Common exploits
* Multiple exploit methods:
  * SSH
  * SMB
  * RDP
  * WMI
  * Shellshock
* A C&C server with a dedicated UI to visualize the Monkey's progress inside the data center

Getting Started
---------------

The Infection Monkey is comprised of two parts: the Monkey and the C&C server.
The monkey is the tool which infects other machines and propagates to them, while the C&C server collects all Monkey reports and displays them to the user.

### Requirements

The C&C Server has been tested on Ubuntu 14.04,15.04 and 16.04. 
The Monkey itself has been tested on Windows XP, 7, 8.1 and 10. The Linux build has been tested on Ubuntu server 14.04 and 15.10.

### Installation

Warning! The Debian package will uninstall the python library 'bson' because of an issue with pymongo. You can reinstall it later, but monkey island will probably not work.

For off-the-shelf use, download our Debian package from our website and follow the guide [written in our blog](https://www.guardicore.com/2016/07/infection-monkey-loose-2/). 
 To manually set up and the C&C server follow the instructions on [Monkey Island readme](monkey_island/readme.txt).  If you wish to compile the binaries yourself, follow the instructions under Building the Monkey from Source.  
 
### Initial configuration.
Whether you're downloading or building the Monkey from source, the Infection Monkey is comprised of 4 executable files for different platforms plus a default configuration file.

Monkey configuration is stored in two places:
1. By default, the Monkey uses a local configuration file (usually, config.bin). This configuration file must include the address of the Monkey's C&C server.
2. After successfully connecting to the C&C server, the monkey downloads a new configuration from the server and discards the local configuration. It is possible to change the default configuration from the C&C server's UI.

In both cases the command server hostname should be modified to point to your local instance of the Monkey Island (note that this doesn't require connectivity right off the bat). In addition, to improve the Monkey's chances of spreading, you can pre-seed it with credentials and usernames commonly used.

Both configuration options use a JSON format for specifying options; see "Options" below for details.

### Running the C&C Server

To run the C&C Server, install our infected Monkey debian package on a specific server. The initial infected machine doesn't require a direct link to this server. 

### Unleashing the Monkey

Once configured, run the monkey using ```./monkey-linux-64 m0nk3y -c config.bin -s 41.50.73.31:5000``` (Windows is identical). This can be done at multiple points in the network simultaneously. 

Command line options include:
* `-c`, `--config`: set configuration file. JSON file with configuration values, will override compiled configuration.
* `-p`, `--parent`: set monkey’s parent uuid, allows better recognition of exploited monkeys in c&c
* `-t`, `--tunnel`: ip:port, set default tunnel for Monkey when connecting to c&c.
* `-d`, `--depth` : sets the Monkey's current operation depth.


How the Monkey works
---------------------

1.  Wakeup connection to c&c, sends basic info of the current machine and the configuration the monkey uses to the c&c.
  1. First try direct connection to c&c.
  2. If direct connection fails, try connection through a tunnel, a tunnel is found according to specified parameter (the default tunnel) or by sending a multicast query and waiting for another monkey to answer.
  3. If no connection can be made to c&c, continue without it.
2. If a firewall app is running on the machine (supports Windows Firewall for Win XP and Windows Advanced Firewall for Win 7+), try to add a rule to allow all our traffic.
3. Startup of tunnel for other Monkeys (if connection to c&c works).
  1. Firewall is checked to allow listening sockets (if we failed to add a rule to Windows firewall for example, the tunnel will not be created)
  2. Will answer multicast requests from other Monkeys in search of a tunnel.
4. Running exploitation sessions, will run x sessions according to configuration:
  1. Connect to c&c and get the latest configuration
  2. Scan ip ranges according to configuration.
  3. Try fingerprinting each host that answers, using the classes defined in the configuration (SMBFinger, SSHFinger, etc)
  4. Try exploitation on each host found, for each exploit class in configuration:
    1. check exploit class supports target host (can be disabled by configuration)
    2. each exploitation class will use the data acquired in fingerprinting, or during the exploit, to find the suitable Monkey executable for the host from the c&c. 
      1. If c&c connection fails, and the source monkey’s executable is suitable, we use it. 
      2. If a suitable executable isn’t found, exploitation will fail.
      3. Executables are cached in memory.
  5. will skip hosts that are already exploited in next run
  6. will skip hosts that failed during exploitation in next run (can be disabled by configuration)
5. Close tunnel before exiting
Wait for monkeys using the tunnel to unregister for it
Cleanup
Remove firewall rules if added

Building the Monkey from source
-------------------------------
If you want to build the monkey from source instead of using our provided packages, follow the instructions at the readme files under [chaos_monkey](chaos_monkey) and [monkey_island](monkey_island). 


License
=======
Copyright (c) 2016 Guardicore Ltd

See the [LICENSE](LICENSE) file for license rights and limitations (GPLv3).

