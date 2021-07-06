# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- PostgreSQL fingerprinter. #892
- A runtime-configurable option to specify a data directory where runtime
  configuration and other artifacts can be stored. #994
- Scripts to build an AppImage for Monkey Island. #1069, #1090, #1136
- `log_level` option to server config. #1151
- A ransomware simulation payload. #1238
- API endpoint for ransomware report. #1297

### Changed
- server_config.json can be selected at runtime. #963
- Logger configuration can be selected at runtime. #971
- `mongo_key.bin` file location can be selected at runtime. #994
- Monkey agents are stored in the configurable data_dir when monkey is "run
  from the island". #997
- Reformated all code using black. #1070
- Sorted all imports usind isort. #1081
- Addressed all flake8 issues. #1071
- Use pipenv for python dependency management. #1091
- Moved unit tests to a dedicated `tests/` directory to improve pytest
  collection time. #1102
- Default BB test suite behavior: if `--run-performance-tests` flag is not
  specified, performance tests are skipped.
- Zerologon exploiter writes runtime artifacts to a secure temporary directory
  instead of $HOME. #1143
- Authentication mechanism to use bcrypt on server side. #1139
- `server_config.json` puts environment config options in a separate section
  named "environment". #1161
- BlackBox tests can now register if they are ran on a fresh installation. #1180
- Improved the structure of unit tests by scoping fixtures only to relevant modules
  instead of having a one huge fixture file, improved and renamed the directory
  structure of unit tests and unit test infrastructure. #1178
- MongoDb now gets launched by the Island via python. #1148
- Create/check data directory on Island init. #1170

### Removed
- Relevant dead code as reported by Vulture. #1149
- Island logger config and --logger-config CLI option. #1151

### Fixed
- Attempted to delete a directory when monkey config reset was called. #1054
- An errant space in the windows commands to run monkey manually. #1153

### Security
- Address minor issues discovered by Dlint. #1075
- Generate random passwords when creating a new user (create user PBA, ms08_67 exploit). #1174
- Implemented configuration encryption/decryption. #1189, #1204
