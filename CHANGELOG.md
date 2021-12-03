# Changelog
All notable changes to this project will be documented in this
file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- credentials.json file for storing Monkey Island user login information. #1206

### Changed
- "Communicate as Backdoor User" PBA's HTTP requests to request headers only and
  include a timeout. #1577
- The setup procedure for custom server_config.json files to be simpler. #1576

### Removed
- The VSFTPD exploiter. #1533
- Manual agent run command for CMD. #1570
- Sambacry exploiter. #1567
- "Kill file" option in the config. #1536
- Netstat collector, because network connection information wasn't used anywhere. #1535
- Checkbox to disable/enable sending log to server. #1537
- Checkbox for self deleting a monkey agent on cleanup. #1537
- Checkbox for file logging. #1537
- Remove serialization of config. #1537
- Checkbox that gave the option to not try to first move the dropper file. #1537
- Custom singleton mutex name config option. #1589
- Removed environment system info collector #1535
- Azure credential collector, because it was broken (not gathering credentials). #1535
- Custom monkey directory name config option. #1537
- Hostname system info collector. #1535
- Max iterations and timeout between iterations config options. #1600
- MITRE ATT&CK configuration screen. #1532
- Propagation credentials from "GET /api/monkey/<string:guid>" endpoint. #1538

### Fixed
- A bug in network map page that caused delay of telemetry log loading. #1545
- Windows "run as a user" powershell command for manual agent runs. #1570
- A bug in the "Signed Script Proxy Execution" PBA that downloaded the exe on Linux
  systems as well. #1557

### Security


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
