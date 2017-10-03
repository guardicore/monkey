How to create a monkey build environment:

Windows:
1. Install python 2.7. Preferably you should use ActiveState Python which includes pywin32 built in. 
	You must use an up to date version, atleast version 2.7.10
	http://www.activestate.com/activepython/downloads
	https://www.python.org/downloads/release/python-2712/
2. install pywin32-219.win32-py2.7.exe at least
	http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/
3. a. install VCForPython27.msi
	http://www.microsoft.com/en-us/download/details.aspx?id=44266
   b. if not installed, install Microsoft Visual C++ 2010 SP1 Redistributable Package
    32bit: http://www.microsoft.com/en-us/download/details.aspx?id=8328
    64bit: http://www.microsoft.com/en-us/download/details.aspx?id=13523
4. Download & Run get-pip.py
	https://bootstrap.pypa.io/get-pip.py
5. Run:
	Install the python packages listed in requirements.txt. Using pip install -r requirements.txt
7. Download and extract UPX binary to [source-path]\monkey\chaos_monkey\bin\upx.exe:
	http://upx.sourceforge.net/download/upx391w.zip
8. Run [source-path]\monkey\chaos_monkey\build_windows.bat to build, output is in dist\monkey.exe

Linux (Tested on Ubuntu 12.04):
1. Run:
	sudo apt-get update
	sudo apt-get install python-pip python-dev libffi-dev upx libssl-dev libc++1
	Install the python packages listed in requirements.txt.
		Using pip install -r requirements.txt
	sudo apt-get install winbind
2. Put source code in /home/user/Code/monkey/chaos_monkey
3. To build, run in terminal:
	cd /home/user/Code/monkey/chaos_monkey
	chmod +x build_linux.sh
	./build_linux.sh
   output is in dist/monkey
