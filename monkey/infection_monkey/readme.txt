To get development versions of Monkey Island and Monkey look into deployment scripts folder.
If you only want to monkey from scratch you may refer to the instructions below.

The monkey is composed of three separate parts.
* The Infection Monkey itself - PyInstaller compressed python archives
* Sambacry binaries - Two linux binaries, 32/64 bit.
* Mimikatz binaries - Two windows binaries, 32/64 bit.

--- Windows ---

1. Install python 2.7. Preferably you should use ActiveState Python which includes pywin32 built in. 
    You must use an up to date version, at least version 2.7.10
    https://www.python.org/download/releases/2.7/
2.	Install pywin32 (if you didn't install ActiveState Python)
	Install pywin32, minimum build 219
		http://sourceforge.net/projects/pywin32/files/pywin32
3.	Add python directories to PATH environment variable (if you didn't install ActiveState Python)
	a. Run the following command on a cmd console (Replace C:\Python27 with your python directory if it's different)
		setx /M PATH "%PATH%;C:\Python27;C:\Pytohn27\Scripts
	b. Close the console, make sure you execute all commands in a new cmd console from now on.
4.	Install pip
	a. Download and run the pip installer
	https://bootstrap.pypa.io/get-pip.py
5.	Install further dependencies
	a. install VCForPython27.msi
		https://aka.ms/vcpython27
	b. if not installed, install Microsoft Visual C++ 2010 SP1 Redistributable Package
		32bit: http://www.microsoft.com/en-us/download/details.aspx?id=8328
		64bit: http://www.microsoft.com/en-us/download/details.aspx?id=13523
6.	Download the dependent python packages using 
		pip install -r requirements.txt
7.	Download and extract UPX binary to [source-path]\monkey\infection_monkey\bin\upx.exe:
		https://github.com/upx/upx/releases/download/v3.94/upx394w.zip
8.	Build/Download Sambacry and Mimikatz binaries
	a. Build/Download according to sections at the end of this readme.
	b. Place the binaries under [code location]\infection_monkey\bin
9.	To build the final exe:
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
		pip install -r requirements.txt
2.	Build Sambacry binaries
	a. Build/Download according to sections at the end of this readme.
	b. Place the binaries under [code location]\infection_monkey\bin
3.	To build, run in terminal:
		cd [code location]/infection_monkey
		chmod +x build_linux.sh
		./build_linux.sh
	output is placed under dist/monkey

-- Sambacry --

Sambacry requires two standalone binaries to execute remotely.
1.	Install gcc-multilib if it's not installed
	sudo apt-get install gcc-multilib
2.	Build the binaries
	cd [code location]/infection_monkey/monkey_utils/sambacry_monkey_runner
	./build.sh

-- Mimikatz --

Mimikatz is required for the Monkey to be able to steal credentials on Windows. It's possible to either compile from sources (requires Visual Studio 2013 and up) or download the binaries from 
https://github.com/guardicore/mimikatz/releases/tag/1.0.0
Download both 32 and 64 bit zipped DLLs and place them under [code location]\infection_monkey\bin
Alternatively, if you build Mimikatz, put each version in a zip file.
1. The zip should contain only the Mimikatz DLL named tmpzipfile123456.dll
2. It should be protected using the password 'VTQpsJPXgZuXhX6x3V84G'.
3. The zip file should be named mk32.zip/mk64.zip accordingly.
4. Zipping with 7zip has been tested. Other zipping software may not work.