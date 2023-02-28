---
title: "Development setup"
date: 2020-06-08T19:53:00+03:00
draft: false
weight: 5
tags: ["contribute"]
---

## Deployment scripts

To set up a development environment using scripts, look at the readme under [`/deployment_scripts`](https://github.com/guardicore/monkey/blob/develop/deployment_scripts). If you want to set it up manually or run into problems, keep reading.

## The Infection Monkey Agent

The Agent (which we sometimes refer to as the Monkey) is a single Python project under the [`infection_monkey`](https://github.com/guardicore/monkey/blob/master/monkey/infection_monkey) folder. The Infection Monkey Agent was built for Python 3.11. You can get it up and running by setting up a [virtual environment](https://docs.python-guide.org/dev/virtualenvs/) and installing the requirements listed in the [`requirements.txt`](https://github.com/guardicore/monkey/blob/master/monkey/infection_monkey/requirements.txt) inside it.

In order to compile the Infection Monkey for distribution by the Monkey Island, you'll need to run the instructions listed in the [`readme.txt`](https://github.com/guardicore/monkey/blob/master/monkey/infection_monkey/readme.txt) on each supported environment.

This means setting up an environment with Linux 64-bit with Python installed and a Windows 64-bit machine with developer tools, along with 64-bit Python versions.

## The Monkey Island

The Monkey Island is a Python backend React frontend project. Similar to the Agent, the backend's requirements are listed in the matching [`requirements.txt`](https://github.com/guardicore/monkey/blob/master/monkey/monkey_island/requirements.txt).

To setup a working front environment, run the instructions listed in the [`readme.txt`](https://github.com/guardicore/monkey/blob/master/monkey/monkey_island/readme.txt)

## Pre-commit

Pre-commit is a multi-language package manager for pre-commit hooks. It will run a set of checks when you attempt to commit. If your commit does not pass all checks, it will be reformatted and/or you'll be given a list of errors and warnings that need to be fixed before you can commit.

Our CI system runs the same checks when pull requests are submitted. This system may report that the build has failed if the pre-commit hooks have not been run or all issues have not been resolved.

To install and configure pre-commit, run `pip install --user pre-commit`. Next, go to the top level directory of this repository and run `pre-commit install -t pre-commit -t pre-push`. Pre-commit will now run automatically whenever you `git commit`.
