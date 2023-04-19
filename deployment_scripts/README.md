# Deployment guide for a development environemnt

This guide is for you if you wish to develop for Infection Monkey. If you only want to use it, please download the relevant version from [our website](https://infectionmonkey.com).

## Prerequisites

Before running the script you must have `git` installed. If you don't have `git` installed, please follow [this guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

## Deploy on Windows

Run the following command in powershell:

```powershell
Invoke-WebRequest https://raw.githubusercontent.com/guardicore/monkey/develop/deployment_scripts/deploy_windows.ps1 -OutFile deploy_windows.ps1
```

This will download our deploy script. It's a good idea to read it quickly before executing it!

After downloading that script, execute it in  `powershell`.

The first argument is an empty directory (script can create one). The second argument is which branch you want to clone - by default, the script will check out the `develop` branch. Some example usages:

- `.\deploy_windows.ps1` (Sets up monkey in current directory under .\infection_monkey)
- `.\deploy_windows.ps1 -monkey_home "C:\test"` (Sets up monkey in C:\test)
- `.\deploy_windows.ps1 -branch 'master'` (Sets up master branch instead of develop in current dir)

You may also pass in an optional `agents=$false` parameter to disable downloading the latest agent binaries.

### Troubleshooting

- If you run into Execution Policy warnings, you can disable them by prefixing the following snippet: `powershell -ExecutionPolicy ByPass -Command "[original command here]"`
- Don't forget to add python to PATH or do so while installing it via this script.

## Deploy on Linux

Linux deployment script is meant for Ubuntu 16 and Ubuntu 18 machines.

Your user must have root permissions; however, don't run the script as root!

```sh
wget https://raw.githubusercontent.com/guardicore/monkey/develop/deployment_scripts/deploy_linux.sh
chmod u+x ./deploy_linux.sh
```

This will download our deploy script. It's a good idea to read it quickly before executing it!

Then execute the resulting script with your shell.

After downloading that script, execute it in a shell. The first argument should be an absolute path of an empty directory (the script will create one if doesn't exist, default is ./infection_monkey). The second parameter is the branch you want to clone (develop by default). Some example usages:

- `./deploy_linux.sh` (deploys under ./infection_monkey)
- `./deploy_linux.sh /home/test/monkey` (deploys under /home/test/monkey)
- `./deploy_linux.sh "" "master"` (deploys master branch in script directory)
- `./deploy_linux.sh /home/user/new "master"` (if directory "new" is not found creates it and clones master branch into it)

You may also pass in an optional third `false` parameter to disable downloading the latest agent binaries.

### Run on Linux

After the `deploy_linux.sh` script completes, you can start the monkey island.

Note: You'll need to run the commands below in a new shell in order to ensure
your PATH environment variable is up to date.

```sh
cd infection_monkey/monkey/monkey_island
pipenv run python ../monkey_island.py
```

## Pre-commit hooks

Both the Linux and Windows deployment scrips will install and configure
[pre-commit](https://pre-commit.com/). Pre-commit is a multi-language package
manager for pre-commit hooks. It will run a set of checks when you attempt to
commit. If your commit does not pass all checks, it will be reformatted and/or
you'll be given a list of errors and warnings that need to be fixed before you
can commit.

Our CI system runs the same checks when pull requests are submitted. This
system may report that the build has failed if the pre-commit hooks have not
been run or all issues have not been resolved.

### Manually installing pre-commit

To install and configure pre-commit manually, run `pip install --user
pre-commit`. Next, go to the top level directory of this repository and run
`pre-commit install -t pre-commit -t pre-push -t prepare-commit-msg` Now, pre-commit will automatically run whenever you `git commit`.
