To get development versions of Monkey Island and Monkey look into deployment scripts folder.
If you only want to build monkey from scratch you may reference instructions below.

The monkey is composed of three separate parts.
* The Infection Monkey itself - PyInstaller compressed python archives
* Sambacry binaries - Two linux binaries, 32/64 bit.
* Mimikatz binaries - Two windows binaries, 32/64 bit.
* Traceroute binaries - Two linux binaries, 32/64bit.

--- Windows ---

1. Install python 2.7.15
    Download and install from: https://www.python.org/downloads/release/python-2715/
2.	Add python directories to PATH environment variable (if you didn't install ActiveState Python)
	a. Run the following command on a cmd console (Replace C:\Python27 with your python directory if it's different)
		setx /M PATH "%PATH%;C:\Python27;C:\Python27\Scripts
	b. Close the console, make sure you execute all commands in a new cmd console from now on.
3.	Install further dependencies
	a. install VCForPython27.msi
		https://aka.ms/vcpython27
	b. if not installed, install Microsoft Visual C++ 2010 SP1 Redistributable Package
		32bit: http://www.microsoft.com/en-us/download/details.aspx?id=8328
		64bit: http://www.microsoft.com/en-us/download/details.aspx?id=13523
4.	Download the dependent python packages using 
		pip install -r requirements_windows.txt
5.	Download and extract UPX binary to [source-path]\monkey\infection_monkey\bin\upx.exe:
		https://github.com/upx/upx/releases/download/v3.94/upx394w.zip
6.	Build/Download Sambacry and Mimikatz binaries
	a. Build/Download according to sections at the end of this readme.
	b. Place the binaries under [code location]\infection_monkey\bin
7.	To build the final exe:
		cd [code location]/infection_monkey
		build_windows.bat 
		output is placed under dist\monkey.exe

--- Linux ---

Tested on Ubuntu 16.04 and 17.04.

1.	Install dependencies by running:
		sudo apt-get update
		sudo apt-get install python-pip python-dev libffi-dev upx libssl-dev libc++1
    Install the python packages listed in requirements.txt using pip
        cd [code location]/infection_monkey
		pip install -r requirements_linux.txt
2.	Build Sambacry binaries
	a. Build/Download according to sections at the end of this readme.
	b. Place the binaries under [code location]\infection_monkey\bin, under the names 'sc_monkey_runner32.so', 'sc_monkey_runner64.so'
3.	Build Traceroute binaries
	a. Build/Download according to sections at the end of this readme.
	b. Place the binaries under [code location]\infection_monkey\bin, under the names 'traceroute32', 'traceroute64'
4.	To build, run in terminal:
		cd [code location]/infection_monkey
		chmod +x build_linux.sh
		./build_linux.sh
	output is placed under dist/monkey

-- Sambacry --

Sambacry requires two standalone binaries to execute remotely.
a. Build sambacry binaries yourself
	a.1. Install gcc-multilib if it's not installed
		 sudo apt-get install gcc-multilib
	a.2. Build the binaries
		 cd [code location]/infection_monkey/monkey_utils/sambacry_monkey_runner
		 ./build.sh

b. Download our pre-built sambacry binaries
	b.1. Available here: 
		32bit: https://github.com/guardicore/monkey/releases/download/1.6/sc_monkey_runner32.so
		64bit: https://github.com/guardicore/monkey/releases/download/1.6/sc_monkey_runner64.so

-- Mimikatz --

Mimikatz is required for the Monkey to be able to steal credentials on Windows. It's possible to either compile binaries from source (requires Visual Studio 2013 and up) or download them from our repository.
a. Build Mimikatz yourself
	a.0. Building mimikatz requires Visual Studio 2013 and up
	a.1. Clone our version of mimikatz from https://github.com/guardicore/mimikatz/tree/1.1.0
	a.2. Build using Visual Studio.
	a.3. Put each version in a zip file
		a.3.1. The zip should contain only the Mimikatz DLL named tmpzipfile123456.dll
		a.3.2. It should be protected using the password 'VTQpsJPXgZuXhX6x3V84G'.
		a.3.3. The zip file should be named mk32.zip/mk64.zip accordingly.
		a.3.4. Zipping with 7zip has been tested. Other zipping software may not work.
		
b. Download our pre-built mimikatz binaries
	b.1. Download both 32 and 64 bit zipped DLLs from https://github.com/guardicore/mimikatz/releases/tag/1.1.0
	b.2. Place them under [code location]\infection_monkey\bin

-- Traceroute --

Traceroute requires two standalone binaries to execute remotely.
The monkey carries the standalone binaries since traceroute isn't built in all Linux distributions.
You can either build them yourself or download pre-built binaries.

a. Build traceroute yourself
	a.1. The sources of traceroute are available here with building instructions: http://traceroute.sourceforge.net
b. Download our pre-built traceroute binaries
	b.1. Available here: 
		32bit: https://github.com/guardicore/monkey/releases/download/1.6/traceroute32
		64bit: https://github.com/guardicore/monkey/releases/download/1.6/traceroute64
