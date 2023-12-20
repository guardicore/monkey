# Changelog
All notable changes to this project will be documented in this
file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- Ability to change wallpaper as part of the ransomware simulation on Windows.
  #1247

### Changed
- Response from `PUT /api/propagation-credentials/configured-credentials`
  in the case of invalid credentials. #3942

### Fixed
- Ports in Hadoop exploiter configuration can no longer be floating-point numbers. #3734
- Ports in Log4Shell exploiter configuration can no longer be floating-point numbers. #3734
- Ports in MSSQL exploiter configuration can no longer be floating-point numbers. #3734
- SMB exploiter configuration bug that wouldn't allow submission. #3839
- Hadoop exploiter configuration bug that wouldn't allow submission. #3839
- Inconsistent error messages on login screen. #3702
- A bug that prevented filtering on certain event types. #3864
- Link-local IPs are no longer shown under Run Monkey -> Manual in the UI. #3825
- A bug that would allow tunnels/relays to prematurely close. #3947

### Removed
- Fingerprinter configuration from UI. #3769, #3826

### Security

## [2.3.0 - 2023-09-19]
### Added
- Ability to filter Agent events by timestamp. #3397
- Ability to filter Agent events by tag. #3396
- Provide a common server object to the plugins that can be used to serve agent
  binaries to the exploited machine over HTTP. #3410
- CPUConsumptionEvent. #3411
- RAMConsumptionEvent. #3411
- HTTPRequestEvent. #3411
- DefacementEvent. #1247
- RDP exploiter plugin. #3425
- A cryptojacker payload to simulate cryptojacker attacks. #3411
- `PUT /api/install-agent-plugin`. #3417
- `GET /api/agent-plugins/installed/manifests`. #3424
- `GET /api/agent-plugins/available/index`. #3420
- `POST /api/uninstall-agent-plugin` # 3422
- Chrome credentials collector plugin. #3426
- A plugin interface for payloads. #3390
- The ability to install plugins from an online repository. #3413, #3418, #3616
- Support for SMBv2+ in SMB exploiter. #3577
- A UI for uploading agent plugin archives. #3417, #3611

### Changed
- Plugin source is now gzipped. #3392
- Allowed characters in Agent event tags. #3399, #3676
- Hard-coded Log4Shell exploiter to a plugin. #3388
- Hard-coded SSH exploiter to a plugin. #3170
- Identities and secrets can be associated when configuring credentials in the
  UI. #3393
- Hard-coded ransomware payload to a plugin. #3391
- Text on the registration screen to improve clarity. #1984

### Fixed
- Agent hanging if plugins do not shut down. #3557
- WMI exploiter hanging. #3543
- Discovered network services are displayed in reports. #3000
- Services count in scanned servers table in security report. #3701

### Removed
- Island mode configuration. #3400
- Agent plugins from Island packages. #3616
- "Reset the Island" button from UI. #3694

### Security
- Fixed a ReDoS issue when validating ransomware file extensions. #3391

## [2.2.1 - 2023-06-21]

### Fixed
- A configuration issue that prevents Mimikatz from being used. #3433

## [2.2.0 - 2023-05-31]
### Added
- `PortScanData.open` property. #3238
- `{GET,PUT} /api/agent-binaries/<string:os>/masque`. #3249
- Placeholder values for empty plugin configuration fields having defaults. #3310
- Malware masquerading. #3241, #3242, #3243
- Support for plugin manifest files with the "yml" extension. #3097
- Randomize Agent binary hash (polymorphism) feature. #3244
- Agent binary's SHA256 to `AgentRegistrationData`. #3244
- `EmailAddress` identity type. #3270
- SNMP exploiter (CVE-2020-15862). #3234
- A plugin interface for credentials collectors. #3167

### Changed
- Renamed "Credential collector" to "Credentials collector". #3167
- Hard-coded WMI exploiter to a plugin. #3163
- Hard-coded Mimikatz credentials collector to a plugin. #3168
- Hard-coded Zerologon exploiter to a plugin. #3164
- Hard-coded SSH credentials collector to a plugin. #3169
- SSH credentials collector's private-key search algorithm. #1882
- Manual run command includes all Island IP addresses. #2593
- Hard-coded MSSQL exploiter to a plugin. #3171
- Hard-coded PowerShell exploiter to a plugin. #3165

### Fixed
- Agents were being caught by Windows Defender (and other antiviruses). #1289
- Plugins are now being checked for local OS compatibility. #3275
- A bug that could prevent multi-hop propagation via SMB. #3173
- Exceptions being raised when WMI and Zerologon are used together. #1774
- A bug that caused failing configuration imports to be marked as successful. #3341
- A bug where target hostnames with dashes were not being scanned. #3231
- A bug in URL sanitization. #3318

### Security
- Fixed a bug where OTPs can be leaked by the hadoop exploiter. #3296
- Fixed pypykatz leaking sensitive information into the logs. #3168, #3293

## [2.1.0] - 2023-04-19
### Added
- Logout button. #3063
- An option to the Hadoop exploiter to try all discovered HTTP ports. #2136
- `GET /api/agent-otp`. #3076
- `POST /api/agent-otp-login` endpoint. #3076
- A smarter brute-forcing strategy for SMB exploiter. #3039
- `POST /api/refresh-authentication-token` endpoint that allows refreshing of
  the access token. #3181

### Changed
- Migrated the hard-coded SMB exploiter to a plugin. #2952
- Python version from 3.7 to 3.11.2. #2705
- MSI installer is now build with InnoSetup. #1911

### Fixed
- A UI deficiency where invalid configurations could be submitted to the
  backend. #1301, #2989
- Notification spam bug. #2731
- Agent propagator crashes if exploiters malfunction. #2992
- Configuration order not preserved in debugging output. #2860
- A bug in the Hadoop exploiter that resulted in speculative execution of
  multiple agents. #2758
- Formatting of the manual run command when copy/pasting from the web UI. #3115
- A bug where plugins received an incorrect agent ID. #3119
- Random logouts when the UI is being actively used. #2049, #3079, #3137

### Security
- Fixed plaintext private key in SSHKey pair list in UI. #2950
- Upgraded MongoDB version from 4.x to 6.0.4. #2706
- Replaced the `SystemSingleton` component, which could allow local users to
  execute a DoS attack against agents. #2817
- Replaced our bespoke authentication solution with `flask-security-too`.
  #2049, #2157, #3078, #3138
- Enforced access control around sensitive API endpoints. #2049, #2157
- Upgraded 3rd-party dependencies. #2705, #2970, #2865, #3125
- Fixed a potential XSS issue in exploiter plugins. #3081

## [2.0.0] - 2023-02-08
### Added
- `credentials.json` file for storing Monkey Island user login information. #1206
- `GET /api/propagation-credentials/<string:guid>` endpoint for agents to
  retrieve updated credentials from the Island. #1538
- `GET /api/island/ip-addresses` endpoint to get IP addresses of the Island server
  network interfaces. #1996
- SSHCollector as a configurable System info Collector. #1606
- deployment_scrips/install-infection-monkey-service.sh to install an AppImage
  as a service. #1552
- The ability to download the Monkey Island logs from the Infection Map page. #1640
- `POST /api/reset-agent-configuration` endpoint. #2036
- `POST /api/clear-simulation-data` endpoint. #2036
- `GET /api/registration-status` endpoint. #2149
- Authentication to `/api/island/version`. #2109
- The ability to customize the file extension used by the ransomware payload
  when encrypting files. #1242
- `{GET,POST} /api/agents` endpoint. #2362
- `GET /api/agent-signals` endpoint. #2261
- `GET /api/agent-logs/<uuid:agent_id>` endpoint. #2274
- `GET /api/machines` endpoint. #2362
- `{GET,POST} /api/agent-events` endpoints. #2405
- `GET /api/nodes` endpoint. #2155, #2300, #2334
- Scrollbar to preview pane's exploit timeline in the map page. #2455
- `GET /api/agent-plugins/<string:os>/<string:type>/<string:name>` endpoint. #2578, #2811
- `GET /api/agent-configuration-schema` endpoint. #2710
- `GET /api/agent-plugins/<string:type>/<string:name>/manifest` endpoint. #2786
- `GET /api/agent-binaries/<string:os>` endpoint. #1675, #1978

### Changed
- Reset workflow. Now it's possible to delete data gathered by agents without
  resetting the configuration. Additionally, the reset procedure requires fewer
  clicks. #957
- Reduced the map refresh rate from 5 seconds to 1.
- Cleaned up and removed duplication in the security report. #2885
- The setup procedure for custom `server_config.json` files to be simpler. #1576
- The order and content of Monkey Island's initialization logging to give
  clearer instructions to the user and avoid confusion. #1684
- The `GET /api/monkey/download` to `GET /api/agent-binaries/<string:os>. #1675, #1978
- Log messages to contain human-readable thread names. #1766
- The log file name to `infection-monkey-agent-<TIMESTAMP>-<RANDOM_STRING>.log`. #1761
- "Logs" page renamed to "Events". #1640, #2501
- Analytics and version update queries are sent separately instead of just one query. #2165
- Update MongoDB version to 4.4.x. #1924
- Depth flag (-d) on the agent now acts the way you would expect (it represents
  the current depth of the agent, not hops remaining). #2033
- Agent configuration structure. #1996, #1998, #1961, #1997, #1994, #1741,
  #1761, #1695, #1605, #2028, #2003, #2785
- `/api/island-mode` to accept and return new "unset" mode. #2036
- `/api/version-update` to `api/island/version`. #2109
- `/api/island-mode` to `/api/island/mode`. #2106
- `/api/log/island/download` endpoint to `/api/island/log`. #2107
- `/api/auth` endpoint to `/api/authenticate`. #2105
- `/api/registration` endpoint to `/api/register`. #2105
- Improved the speed of ransomware encryption by 2-3x. #2123
- `-s/--server` to `-s/--servers`. #2216
- `-s/--servers` accepts list a comma-separated list of servers. #2216
- Tunneling to relays to provide better firewall evasion, faster Island
  connection times, unlimited hops, and a more resilient way for agents to call
  home. #2216, #1583
- `/api/monkey-control/stop-all-agents` to `POST /api/agent-signals/terminate-all-agents`. #2261
- Format of scanned machines table in the security report. #2267
- "Local network scan" option to "Scan Agent's networks". #2299
- Information displayed in the preview pane in the map page. #2455
- The Hadoop exploiter to a plugin. #2826
- The Guardicore logo to Akamai logo. #2913

### Removed
- VSFTPD exploiter. #1533
- Manual agent run command for CMD. #1556
- Sambacry exploiter. #1567, #1693
- "Kill file" option in the config. #1536
- Netstat collector, because network connection information wasn't used anywhere. #1535
- Checkbox to disable/enable sending log to server. #1537
- Checkbox for self deleting a monkey agent on cleanup. #1537
- Checkbox for file logging. #1537
- Serialization of config. #1537
- Checkbox that gave the option to not try to first move the dropper file. #1537
- Custom singleton mutex name config option. #1589
- Environment system info collector #1535
- Azure credential collector, because it was broken (not gathering credentials). #1535
- Custom monkey directory name config option. #1537
- Hostname system info collector. #1535
- Max iterations config option. #1600
- Timeout between iterations config options. #1600
- MITRE ATT&CK configuration screen. #1532
- Propagation credentials from `GET /api/monkey/<string:guid>` endpoint. #1538
- `GET /api/monkey_control/check_remote_port/<string:port>` endpoint. #1635
- Max victims to find/exploit, TCP scan interval and TCP scan get banner internal options. #1597
- MySQL fingerprinter. #1648
- MS08-067 (Conficker) exploiter. #1677
- Agent bootloader. #1676
- Zero Trust integration with ScoutSuite. #1669
- ShellShock exploiter. #1733
- ElasticGroovy exploiter. #1732
- T1082 attack technique report. #1695
- 32-bit agents. #1675
- Log path config options. #1761
- "smb_service_name" option. #1741
- Struts2 exploiter. #1869
- Drupal exploiter. #1869
- WebLogic exploiter. #1869
- The /api/t1216-pba/download endpoint. #1864
- `/api/test/clear_caches` endpoint. #1888, #2092
- All `/api/monkey_control` endpoints. #1888, #2261
- Island log download button from "Events" (previously called "Logs") page. #1640
- `/api/client-monkey` endpoint. #1889
- "+dev" from version numbers. #1553
- agent's `--config` argument. #906
- Option to export monkey telemetries. #1998
- `/api/configuration/import` endpoint. #2002
- `/api/configuration/export` endpoint. #2002
- `/api/island-configuration` endpoint. #2003
- `-t/--tunnel` from agent command line arguments. #2216
- `/api/monkey-control/needs-to-stop`. #2261
- `GET /api/test/monkey` endpoint. #2269
- `GET /api/test/log` endpoint. #2269
- Node Map from Security Report. #2334
- "Accessible From" and "Services" from the preview pane in the map page. #2430
- All `GET /api/netmap` endpoints. #2334, #2453
- The MITRE ATT&CK report. #2440
- The Zero Trust report. #2441
- `GET /api/zero-trust/finding-event/<string:finding_id>` endpoint. #2441
-`"GET /api/report/zero-trust/<string:report_data>` endpoint. #2441
- AWS Security Hub integration. #2443
- The Post breach actions configuration tab. #2442
- The Custom PBA configuration tab. #2442
- All `/api/pba` endpoints. #2442
- The TelemetryLog component from the Infection Map page. #2500
- `GET /api/telemetry-feed` endpoint. #2502
- `{GET,POST} /api/log` endpoint. #2485
- `GET /api/local-monkey` endpoint. #2506
- `/api/telemetry` endpoint. #2503
- `/api/agent` endpoint. #2542
- `/api/exploitations/manual` endpoint. #2509
- `/api/island/ip-addresses` endpoint. #2565
- ElasticSearch fingerprinter. #2674

### Fixed
- Various bugs that prevented agents from stopping reliably. #556, #578, #581,
  #594, #1635, #2261
- A bug in the network map where it would drift away and
  improved overall stability of the map. #2939
- Windows "run as a user" powershell command for manual agent runs. #1556
- A bug in the map where side pane would not appear if the node was
  dragged around before click. #2914
- Unnecessary collection of kerberos credentials. #1771
- A bug where bogus users were collected by Mimikatz and added to the config. #1860
- A bug where windows executable was not self deleting. #1763
- 2-second delay when the Island server starts, and it's not running on AWS. #1636
- Malformed MSSQL agent launch command. #2018
- A bug where the Log4Shell exploiter could leave LDAP servers and child
  processes running. #2820
- A bug in registration process that caused the button to be stuck with loading icon. #2916
- Configurability of SSH key pairs. #1416
- A bug in the security report that didn't show the correct percentage of exploited machines. #2954
- A bug where ransomware README file is not readable on older Windows machines. #2951
- An exception being raised if the ransomware target directory does not exist. #2953
- A bug where the ransomware payload could follow a symlink. #2953

### Security
- Upgrade Cryptography dependency. #1482
- Log files are created with random names and secure permissions. #1761, #2775
- Change SSH exploiter so that it does not set the permissions of the agent
  binary in /tmp on the target system to 777, as this could allow a malicious
  actor with local access to escalate their privileges. #1750
- Fixed constant agent file names in `/tmp`. #1782
- Update MongoDB version to 4.4.x. #1924
- The `/api/telemetry` endpoint allowed arbitrary queries to be submitted,
  which could result in javascript execution. #2503

## [1.13.0] - 2022-01-25
### Added
- A new exploiter that allows propagation via the Log4Shell vulnerability
 (CVE-2021-44228). #1663

### Fixed
- Exploiters attempting to start servers listening on privileged ports,
  resulting in failed propagation. 8f53a5c


## [1.12.0] - 2021-10-27
### Added
- A new exploiter that allows propagation via PowerShell Remoting. #1246
- A warning regarding antivirus when agent binaries are missing. #1450
- A deployment.json file to store the deployment type. #1205

### Changed
- The name of the "Communicate as new user" post-breach action to "Communicate
   as backdoor user". #1410
- Resetting login credentials also cleans the contents of the database. #1495
- ATT&CK report messages (more accurate now). #1483
- T1086 (PowerShell) now also reports if ps1 scripts were run by PBAs. #1513
- ATT&CK report messages to include internal config options as reasons
  for unscanned attack techniques. #1518

### Removed
- Internet access check on agent start. #1402
- The "internal.monkey.internet_services" configuration option that enabled
  internet access checks. #1402
- Disused traceroute binaries. #1397
- "Back door user" post-breach action. #1410
- Stale code in the Windows system info collector that collected installed
  packages and WMI info. #1389
- Insecure access feature in the Monkey Island. #1418
- The "deployment" field from the server_config.json. #1205
- The "Execution through module load" ATT&CK technique,
  since it can no longer be exercise with current code. #1416
- Browser window pop-up when Monkey Island starts on Windows. #1428

### Fixed
- Misaligned buttons and input fields on exploiter and network configuration
  pages. #1353
- Credentials shown in plain text on configuration screens. #1183
- Crash when unexpected character encoding is used by ping command on German
  language systems. #1175
- Malfunctioning timestomping PBA. #1405
- Malfunctioning shell startup script PBA. #1419
- Trap command produced no output. #1406
- Overlapping Guardicore logo in the landing page. #1441
- PBA table collapse in security report on data change. #1423
- Unsigned Windows agent binaries in Linux packages are now signed. #1444
- Some of the gathered credentials no longer appear in plaintext in the
  database. #1454
- Encryptor breaking with UTF-8 characters. (Passwords in different languages
  can be submitted in the config successfully now.) #1490
- Mimikatz collector no longer fails if Azure credential collector is disabled.
  #1512, #1493
- Unhandled error when "modify shell startup files PBA" is unable to find
  regular users. #1507
- ATT&CK report bug that showed different techniques' results under a technique
  if the PBA behind them was the same. #1514
- ATT&CK report bug that said that the technique "`.bash_profile` and
  `.bashrc`" was not attempted when it actually was attempted but failed. #1511
- Bug that periodically cleared the telemetry table's filter. #1392
- Crashes, stack traces, and other malfunctions when data from older versions
  of Infection Monkey is present in the data directory. #1114
- Broken update links. #1524

### Security
- Generate a random password when creating a new user for CommunicateAsNewUser
  PBA. #1434
- Credentials gathered from victim machines are no longer stored plaintext in
  the database. #1454
- Encrypt the database key with user's credentials. #1463


## [1.11.0] - 2021-08-13
### Added
- A runtime-configurable option to specify a data directory where runtime
  configuration and other artifacts can be stored. #994
- Scripts to build an AppImage for Monkey Island. #1069, #1090, #1136, #1381
- `log_level` option to server config. #1151
- A ransomware simulation payload. #1238
- The capability for a user to specify their own SSL certificate. #1208
- API endpoint for ransomware report. #1297
- A ransomware report. #1240
- A script to build a docker image locally. #1140

### Changed
- Select server_config.json at runtime. #963
- Select Logger configuration at runtime. #971
- Select `mongo_key.bin` file location at runtime. #994
- Store Monkey agents in the configurable data_dir when monkey is "run from the
- island". #997
- Reformat all code using black. #1070
- Sort all imports using isort. #1081
- Address all flake8 issues. #1071
- Use pipenv for python dependency management. #1091
- Move unit tests to a dedicated `tests/` directory to improve pytest collection
  time. #1102
- Skip BB performance tests by default. Run them if `--run-performance-tests`
  flag is specified.
- Write Zerologon exploiter's runtime artifacts to a secure temporary directory
  instead of $HOME. #1143
- Put environment config options in `server_config.json` into a separate
  section named "environment". #1161
- Automatically register if BlackBox tests are run on a fresh
  installation. #1180
- Limit the ports used for scanning in blackbox tests. #1368
- Limit the propagation depth of most blackbox tests. #1400
- Wait less time for monkeys to die when running BlackBox tests. #1400
- Improve the structure of unit tests by scoping fixtures only to relevant
  modules instead of having a one huge fixture file. #1178
- Improve and rename the directory structure of unit tests and unit test
  infrastructure. #1178
- Launch MongoDB when the Island starts via python. #1148
- Create/check data directory on Island initialization. #1170
- Format some log messages to make them more readable. #1283
- Improve runtime of some unit tests. #1125
- Run curl OR wget (not both) when attempting to communicate as a new user on
  Linux. #1407

### Removed
- Relevant dead code as reported by Vulture. #1149
- Island logger config and --logger-config CLI option. #1151

### Fixed
- Attempt to delete a directory when monkey config reset was called. #1054
- An errant space in the windows commands to run monkey manually. #1153
- Gevent tracebacks in console output. #859
- Crash and failure to run PBAs if max depth reached. #1374

### Security
- Address minor issues discovered by Dlint. #1075
- Hash passwords on server-side instead of client side. #1139
- Generate random passwords when creating a new user (create user PBA, ms08_67
  exploit). #1174
- Implemented configuration encryption/decryption. #1189, #1204
- Create local custom PBA directory with secure permissions. #1270
- Create encryption key file for MongoDB with secure permissions. #1232
