# Infection Monkey
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/guardicore/monkey)](https://github.com/guardicore/monkey/releases)

[![Build Status](https://travis-ci.com/guardicore/monkey.svg?branch=develop)](https://travis-ci.com/guardicore/monkey)
[![codecov](https://codecov.io/gh/guardicore/monkey/branch/master/graph/badge.svg)](https://codecov.io/gh/guardicore/monkey)

![GitHub stars](https://img.shields.io/github/stars/guardicore/monkey)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/guardicore/monkey)

## Data center Security Testing Tool

Welcome to the Infection Monkey! 

The Infection Monkey is an open source security tool for testing a data center's resiliency to perimeter breaches and internal server infection. The Monkey uses various methods to self propagate across a data center and reports success to a centralized Monkey Island server.

<img src=".github/map-full.png" >

<img src=".github/Security-overview.png" width="800" height="500">

The Infection Monkey is comprised of two parts:

* **Monkey** - A tool which infects other machines and propagates to them.
* **Monkey Island** - A dedicated server to control and visualize the Infection Monkey's progress inside the data center.

To read more about the Monkey, visit [infectionmonkey.com](https://infectionmonkey.com). 

## Main Features

The Infection Monkey uses the following techniques and exploits to propagate to other machines.

* Multiple propagation techniques:
  * Predefined passwords
  * Common logical exploits
  * Password stealing using Mimikatz
* Multiple exploit methods:
  * SSH
  * SMB
  * WMI
  * Shellshock
  * Conficker
  * SambaCry
  * Elastic Search (CVE-2015-1427)

## Setup
Check out the [Setup](https://github.com/guardicore/monkey/wiki/setup) page in the Wiki or a quick getting [started guide](https://www.guardicore.com/infectionmonkey/wt/).

The Infection Monkey supports a variety of platforms, documented [in the wiki](https://github.com/guardicore/monkey/wiki/OS-compatibility).

## Building the Monkey from source
To deploy development version of monkey you should refer to readme in the [deployment scripts](deployment_scripts) folder.
If you only want to build the monkey from source, see [Setup](https://github.com/guardicore/monkey/wiki/Setup#compile-it-yourself)
and follow the instructions at the readme files under [infection_monkey](monkey/infection_monkey) and [monkey_island](monkey/monkey_island). 

### Build status
| Branch | Status |
| ------ | :----: |
| Develop | [![Build Status](https://travis-ci.com/guardicore/monkey.svg?branch=develop)](https://travis-ci.com/guardicore/monkey) |
| Master | [![Build Status](https://travis-ci.com/guardicore/monkey.svg?branch=master)](https://travis-ci.com/guardicore/monkey) | 

## Tests

### Unit Tests

In order to run all of the Unit Tests, run the command `python -m pytest` in the `monkey` directory. 

To get a coverage report, first make sure the `coverage` package is installed using `pip install coverage`. Run the command 
`coverage run -m unittest` in the `monkey` directory and then `coverage html`. The coverage report can be found in 
`htmlcov.index`.  

### Blackbox tests

In order to run the Blackbox tests, refer to `envs/monkey_zoo/blackbox/README.md`. 

# License

Copyright (c) Guardicore Ltd

See the [LICENSE](LICENSE) file for license rights and limitations (GPLv3).
