# Monkey island dev. env. setup guide

>To easily setup development environment for Monkey Island and the Monkey look into [deployment scripts](../../deployment_scripts) folder.
>If you want to setup dev. env. for the Monkey manually, refer to the instructions below.

The monkey is a PyInstaller compressed python archives.

## Windows

1. Install python 3.7.4 and choose **ADD to PATH** option when installing.

    Download and install from: <https://www.python.org/ftp/python/3.7.4/>

    In case you still need to add python directories to path:
    - Run the following command on a cmd console (Replace C:\Python37 with your python directory if it's different)
    `setx /M PATH "%PATH%;C:\Python37;C:\Python37\Scripts`
    - Close the console, make sure you execute all commands in a new cmd console from now on.
1. Install further dependencies
    - if not installed, install Microsoft Visual C++ 2017 SP1 Redistributable Package
        - 32bit: <https://aka.ms/vs/16/release/vc_redist.x86.exe>
        - 64bit: <https://go.microsoft.com/fwlink/?LinkId=746572>
1. Download the dependent python packages using
        `pip install -r requirements.txt`
1. Download and extract UPX binary to monkey\infection_monkey\bin\upx.exe:
        <https://github.com/upx/upx/releases/download/v3.94/upx394w.zip>
1. To build the final exe:
    - `cd monkey\infection_monkey`
    - `build_windows.bat`

    Output is placed under `dist\monkey64.exe`.

## Linux

Tested on Ubuntu 16.04.
1. On older distributions of Ubuntu (16.04) you'll need to download python3.7 via ppa:
    - `sudo add-apt-repository ppa:deadsnakes/ppa`
    - `sudo apt-get update`
    - `sudo apt install python3.7`

1. Install dependencies by running:
    - `sudo apt install python3-pip`
    - `python3.7 -m pip install pip`
    - `sudo apt-get install python3.7-dev libffi-dev upx libssl-dev libc++1`

1. Install the python packages listed in requirements.txt using pip
    - `cd [code location]/infection_monkey`
    - `python3.7 -m pipenv lock -r --dev > requirements.txt`
    - `python3.7 -m pip install -r requirements.txt`

1. To build, run in terminal:
    - `cd [code location]/infection_monkey`
    - `chmod +x build_linux.sh`
    - `pipenv run ./build_linux.sh`

    Output is placed under `dist/monkey64`.

### Troubleshooting

Some of the possible errors that may come up while trying to build the infection monkey:

#### Linux

When committing your changes for the first time, you may encounter some errors thrown by the pre-commit hooks. This is most likely because some python dependencies are missing from your system.
To resolve this, use `pipenv` to create a `requirements.txt` for both the `infection_monkey/` and `monkey_island/` requirements and install it with `pip`.

   - `cd [code location]/infection_monkey`
   - `python3.7 -m pipenv lock -r --dev > requirements.txt`
   - `python3.7 -m pip install -r requirements.txt`

   and

   - `cd [code location]/monkey_island`
   - `python3.7 -m pipenv lock -r --dev > requirements.txt`
   - `python3.7 -m pip install -r requirements.txt`
