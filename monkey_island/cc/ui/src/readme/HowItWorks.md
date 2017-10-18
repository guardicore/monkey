How It Works
=======

Whether you're downloading or building the Monkey from source, the Infection Monkey is comprised of 4 executable files for different platforms plus a default configuration file.

Monkey configuration is stored in two places:
1. By default, the Monkey uses a local configuration file (usually, config.bin). This configuration file must include the address of the Monkey's C&C server.
2. After successfully connecting to the C&C server, the monkey downloads a new configuration from the server and discards the local configuration. It is possible to change the default configuration from the C&C server's UI.

In both cases the command server hostname should be modified to point to your local instance of the Monkey Island (note that this doesn't require connectivity right off the bat). In addition, to improve the Monkey's chances of spreading, you can pre-seed it with credentials and usernames commonly used.

Both configuration options use a JSON format for specifying options; see "Options" below for details.

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

