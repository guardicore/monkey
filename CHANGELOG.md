# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- PostgreSQL fingerprinter. #892
- A runtime-configurable option to specify a data directory where runtime
  configuration and other artifacts can be stored. #994
- Scripts to build an AppImage for Monkey Island. #1069, #1090, #1136

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
- Changed default BB test suite: if `--run-performance-tests` flag is not specified,
 performance tests are skipped.

### Fixed
- Attempted to delete a directory when monkey config reset was called. #1054

### Security
- Address minor issues discovered by Dlint. #1075
