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

Configuration Options
---------------------

Key | Type | Description | Possible Values
--- | ---- | ----------- | ---------------
alive | bool | sets whether or not the monkey is alive. if false will stop scanning and exploiting
command_servers | array | addresses of c&c servers to try to connect | example: ["russian-mail-brides.com:5000"]
singleton_mutex_name | string | string of the mutex name for single instance | example: {2384ec59-0df8-4ab9-918c-843740924a28}
self_delete_in_cleanup | bool | sets whether or not to self delete the monkey executable when stopped
use_file_logging | bool | sets whether or not to use a log file
monkey_log_path_[windows/linux] | string | file path for monkey logger.
kill_file_path_[windows/linux] | string | file path that the Monkey checks to prevent running
timeout_between_iterations | int | how long to wait between scan iterations
max_iterations | int | how many scan iterations to perform on each run
internet_services | array | addresses of internet servers to ping and check if the monkey has internet acccess
victims_max_find | int | how many victims to look for in a single scan iteration
victims_max_exploit | int | how many victims to exploit before stopping
retry_failed_explotation | bool | sets whether or not to retry failed hosts on next scan
local_network_scan | bool | sets whether to auto detect and scan local subnets
range_class | class name | sets which ip ranges class is used to construct the list of ips to scan | `FixedRange` - scan list is a static ips list, `RelativeRange` - scan list will be constructed according to ip address of the machine and size of the scan, `ClassCRange` - will scan the entire class c the machine is in.
range_fixed | tuple of strings | list of ips to scan
RelativeRange range_size | int | number of hosts to scan in relative range
scanner_class | class name | sets which scan class to use when scanning for hosts to exploit | `TCPScanner` - searches for hosts according to open tcp ports, `PingScanner` - searches for hosts according to ping scan
finger_classes | tuple of class names | sets which fingerprinting classes to use | in the list: `SMBFinger` - get host os info by checking smb info, `SSHFinger` - get host os info by checking ssh banner, `PingScanner` - get host os type by checking ping ttl. For example: `(SMBFinger, SSHFinger, PingScanner)`
exploiter_classes | tuple of class names | | `SmbExploiter` - exploit using smb connection, `WmiExploiter` - exploit using wmi connection, `RdpExploiter` - exploit using rdp connection, `Ms08_067_Exploiter` - exploit using ms08_067 smb exploit, `SSHExploiter` - exploit using ssh connection
tcp_target_ports | list of int | which ports to scan using TCPScanner
tcp_scan_timeout | int | timeout for tcp connection in tcp scan (in milliseconds)
tcp_scan_interval | int | time to wait between ports in the tcp scan (in milliseconds)
tcp_scan_get_banner | bool  | sets whether or not to read a banner from the tcp ports when scanning
ping_scan_timeout | int | timeout for the ping command (in milliseconds) utilised by PingScanner
skip_exploit_if_file_exist | bool | sets whether or not to abort exploit if the monkey already exists in target, used by SmbExploiter
psexec_user | string | user to use for connection, utilised by SmbExploiter/WmiExploiter/RdpExploiter
psexec_passwords | list of strings | list of passwords to use when trying to exploit
rdp_use_vbs_download | bool | sets whether to use vbs payload for rdp exploitation in RdpExploiter. If false, bits payload is used (will fail if bitsadmin.exe doesn’t exist)
ms08_067_exploit_attempt | int | number of times to try and exploit using ms08_067 exploit
ms08_067_remote_user_add | string  | user to add to target when using ms08_067 exploit
ms08_067_remote_user_pass | string | password of the user the exploit will add
ssh_user | string | user to use for ssh connection, used by SSHExploiter
ssh_passwords | list of strings | list of passwords to use when trying to exploit using SSHExploiter
dropper_set_date | bool | whether or not to change the monkey file date to match other files
dropper_target_path_[windows/linux] | string | path for the dropper
serialize_config | bool | sets whether or not to locally save the running configuration after finishing


Building the Monkey from source
-------------------------------
If you want to build the monkey from source instead of using our provided packages, follow the instructions at the readme files under [chaos_monkey](chaos_monkey) and [monkey_island](monkey_island). 


License
=======
Copyright (c) 2016 Guardicore Ltd

See the [LICENSE](LICENSE) file for license rights and limitations (GPLv3).

Dependent packages
---------------------

Dependency | License | Notes
----------------------------|----------------------------|----------------------------
 libffi-dev | https://github.com/atgreen/libffi/blob/master/LICENSE 
 PyCrypto | Public domain 
 upx | Custom license, http://upx.sourceforge.net/upx-license.html
 bson | BSD 
 enum34 | BSD 
 pyasn1 | BSD 
 psutil | BSD 
 flask | BSD 
 flask-Pymongo | BSD 
 Flask-Restful | BSD 
 python-dateutil | Simplified BSD 
 zope | ZPL 2.1 
 Bootstrap | MIT 
 Bootstrap Switch | Apache 2.0 
 Bootstrap Dialog | MIT 
 JSON Editor | MIT 
 Datatables | MIT 
 jQuery | MIT 
 cffi | MIT 
 twisted | MIT 
 typeahead.js | MIT 
 Font Awesome | MIT 
 vis.js | MIT/Apache 2.0 
 impacket | Apache Modified 
 Start Bootstrap (UI Theme) | Apache 2.0 
 requests | Apache 2.0 
 grequests | BSD
 odict | Python Software Foundation License 
 paramiko | LGPL 
 rdpy | GPL-3 
 winbind | GPL-3 
 pyinstaller | GPL 
 Celery | BSD 
 mimikatz | CC BY 4.0 | We use an altered version of mimikatz. Original: https://github.com/gentilkiwi/mimikatz
