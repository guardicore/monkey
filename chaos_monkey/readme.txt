How to build a monkey binary from scratch.

The monkey is composed of three separate parts.
* The Infection Monkey itself - PyInstaller compressed python archives
* Sambacry binaries - Two linux binaries, 32/64 bit.
* Mimikatz binaries - Two windows binaries, 32/64 bit.

--- Windows ---

1. Install python 2.7. Preferably you should use ActiveState Python which includes pywin32 built in. 
    You must use an up to date version, at least version 2.7.10
    https://www.python.org/download/releases/2.7/
    If not using ActiveState, install pywin32, minimum build 219
    http://sourceforge.net/projects/pywin32/files/pywin32
3. a. install VCForPython27.msi
    https://aka.ms/vcpython27
   b. if not installed, install Microsoft Visual C++ 2010 SP1 Redistributable Package
    32bit: http://www.microsoft.com/en-us/download/details.aspx?id=8328
    64bit: http://www.microsoft.com/en-us/download/details.aspx?id=13523
4. Download the dependent python packages using 
    pip install -r requirements.txt
5. Download and extract UPX binary to [source-path]\monkey\chaos_monkey\bin\upx.exe:
    https://github.com/upx/upx/releases/download/v3.94/upx394w.zip
6. To build the final exe:
    cd [code location]/chaos_monkey
    build_windows.bat 
    output is placed under dist\monkey.exe

--- Linux ---

Tested on Ubuntu 16.04 and 17.04.

1. Run:
    sudo apt-get update
    sudo apt-get install python-pip python-dev libffi-dev upx libssl-dev libc++1
    Install the python packages listed in requirements.txt using pip
        pip install -r requirements.txt
2. Place the source code in code/monkey/chaos_monkey
3. To build, run in terminal:
    cd [code location]/chaos_monkey
    chmod +x build_linux.sh
    ./build_linux.sh
   output is placed under dist/monkey

-- Sambacry --

Sambacry requires two standalone binaries to execute remotely.
Compiling them requires gcc.
cd [code location]/chaos_monkey/monkey_utils/sambacry_monkey_runner
./build.sh

-- Mimikatz --

Mimikatz is required for the Monkey to be able to steal credentials on Windows. It's possible to either compile from sources (requires Visual Studio 2013 and up) or download the binaries from 
https://github.com/guardicore/mimikatz/releases/tag/1.0.0
Download both 32 and 64 bit DLLs and place them under [code location]\chaos_monkey\bin