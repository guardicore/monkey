# Monkey island dev. env. setup guide

>To easily setup development environment for Monkey Island and the Monkey look into [deployment scripts](../../deployment_scripts) folder.
>If you want to setup dev. env. for the Monkey manually, refer to the instructions below.

The monkey is composed of three separate parts.

- The Infection Monkey itself - PyInstaller compressed python archives
- Sambacry binaries - Two linux binaries, 32/64 bit.
- Traceroute binaries - Two linux binaries, 32/64bit.

## Windows

1. Install python 3.7.4 and choose **ADD to PATH** option when installing.

    Download and install from: <https://www.python.org/ftp/python/3.7.4/>
    
    In case you still need to add python directories to path:
    - Run the following command on a cmd console (Replace C:\Python37 with your python directory if it's different) 
    `setx /M PATH "%PATH%;C:\Python37;C:\Python37\Scripts`
    - Close the console, make sure you execute all commands in a new cmd console from now on.
2. Install further dependencies
    - if not installed, install Microsoft Visual C++ 2017 SP1 Redistributable Package
        - 32bit: <https://aka.ms/vs/16/release/vc_redist.x86.exe>
        - 64bit: <https://go.microsoft.com/fwlink/?LinkId=746572>
3. Download the dependent python packages using 
        `pip install -r requirements.txt`
4. Download and extract UPX binary to monkey\infection_monkey\bin\upx.exe:
        <https://github.com/upx/upx/releases/download/v3.94/upx394w.zip>
5. Build/Download Sambacry
    - Build/Download according to sections at the end of this readme.
    - Place the binaries under monkey\infection_monkey\bin
6. To build the final exe:
    - `cd monkey\infection_monkey`
    - `build_windows.bat`
    - output is placed under `dist\monkey32.exe` or `dist\monkey64.exe` depending on your version of Python

## Linux

Tested on Ubuntu 16.04.
0. On older distributions of Ubuntu (16.04) you'll need to download python3.7 via ppa:
    - `sudo add-apt-repository ppa:deadsnakes/ppa`
    - `sudo apt-get update`
    - `sudo apt install python3.7`

1. Install dependencies by running:
    - `sudo apt install python3-pip`
    - `python3.7 -m pip install pip`
    - `sudo apt-get install python3.7-dev libffi-dev upx libssl-dev libc++1`

2. Install the python packages listed in requirements.txt using pip
    - `cd [code location]/infection_monkey`
    - `python3.7 -m pip install -r requirements.txt`

3. Build Sambacry binaries
    - Build/Download according to sections at the end of this readme.
    - Place the binaries under [code location]/infection_monkey/bin, under the names 'sc_monkey_runner32.so', 'sc_monkey_runner64.so'

4. Build Traceroute binaries
    - Build/Download according to sections at the end of this readme.
    - Place the binaries under [code location]/infection_monkey/bin, under the names 'traceroute32', 'traceroute64'

5. To build, run in terminal:
    - `cd [code location]/infection_monkey`
    - `chmod +x build_linux.sh`
    - `./build_linux.sh`
    
    output is placed under `dist/monkey32` or `dist/monkey64` depending on your version of python

### Sambacry

Sambacry requires two standalone binaries to execute remotely.

1. Build sambacry binaries yourself
    - Install gcc-multilib if it's not installed `sudo apt-get install gcc-multilib`
    - Build the binaries
         1. `cd [code location]/infection_monkey/exploit/sambacry_monkey_runner`
         2. `./build.sh`

2. Download our pre-built sambacry binaries
    - Available here:
        - 32bit: <https://github.com/guardicore/monkey/releases/download/1.6/sc_monkey_runner32.so>
        - 64bit: <https://github.com/guardicore/monkey/releases/download/1.6/sc_monkey_runner64.so>

### Traceroute

Traceroute requires two standalone binaries to execute remotely.
The monkey carries the standalone binaries since traceroute isn't built in all Linux distributions.
You can either build them yourself or download pre-built binaries.

1. Build traceroute yourself
    - The sources of traceroute are available here with building instructions: <http://traceroute.sourceforge.net>
1. Download our pre-built traceroute binaries
    - Available here:
        - 32bit: <https://github.com/guardicore/monkey/releases/download/1.6/traceroute32>
        - 64bit: <https://github.com/guardicore/monkey/releases/download/1.6/traceroute64>
