# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- PostgreSQL fingerprinter. #892
- A runtime-configurable option to specify a data directory where runtime
  configuration and other artifacts can be stored. #994
- Scripts to build a prototype AppImage for Monkey Island. #1069

### Changed
- server_config.json can be selected at runtime. #963
- Logger configuration can be selected at runtime. #971
- `mongo_key.bin` file location can be selected at runtime. #994
- Monkey agents are stored in the configurable data_dir when monkey is "run
  from the island". #997
- Reformated all code using black. #1070
- Sort all imports usind isort. #1081
