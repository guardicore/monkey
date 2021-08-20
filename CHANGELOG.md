# Changelog
All notable changes to this project will be documented in this
file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Removed
- Internet access check on agent start. #1402
- The "internal.monkey.internet_services" configuration option that enabled
  internet access checks. #1402
- Disused traceroute binaries. #1397

### Fixed
- Misaligned buttons and input fields on exploiter and network configuration
  pages. #1353
- Credentials shown in plain text on configuration screens. #1183
- Typo "trough" -> "through" in telemetry and docstring.
- Crash when unexpected character encoding is used by ping command on German
  language systems. #1175

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
  island". #997
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
- Automatically register if BlackBox tests are run on a fresh installation.
  #1180
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
