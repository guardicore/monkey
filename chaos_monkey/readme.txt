How to create a monkey build environment:

Windows:
1. Install python 2.7
	https://www.python.org/download/releases/2.7
2. install pywin32-219.win32-py2.7.exe
	http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/
3. install VCForPython27.msi
	http://www.microsoft.com/en-us/download/details.aspx?id=44266
4. Download & Run get-pip.py
	https://bootstrap.pypa.io/get-pip.py
5. Run:
	setx path "%path%;C:\Python27\;C:\Python27\Scripts"
	python -m pip install enum34
	python -m pip install impacket
	python -m pip install PyCrypto
	python -m pip install pyasn1
	python -m pip install cffi
	python -m pip install twisted
	python -m pip install rdpy
	python -m pip install requests
	python -m pip install odict
	python -m pip install paramiko
	python -m pip install psutil	
	python -m pip install PyInstaller
	type > C:\Python27\Lib\site-packages\zope\__init__.py
7. Download and extract UPX binary to C:\Code\monkey\chaos_monkey\bin\upx.exe:
	http://upx.sourceforge.net/download/upx391w.zip
8. Run [source-path]\monkey\chaos_monkey\build_windows.bat to build, output is in dist\monkey.exe

Linux (Tested on Ubuntu 12.04):
1. Run:
	sudo apt-get update
	apt-get install python-pip python-dev libffi-dev upx
	sudo pip install enum34
	sudo pip install impacket
	sudo pip install PyCrypto --upgrade
	sudo pip install pyasn1
	sudo pip install cffi
	sudo pip install zope.interface --upgrade
	sudo pip install twisted
	sudo pip install rdpy
	sudo pip install requests --upgrade
	sudo pip install odict
	sudo pip install paramiko
	sudo pip install psutil
	sudo pip install https://github.com/pyinstaller/pyinstaller/releases/download/3.0.dev2/PyInstaller-3.0.dev2.tar.gz
	sudo apt-get install winbind
2. Put source code in /home/user/Code/monkey/chaos_monkey
3. To build, run in terminal:
	cd /home/user/Code/monkey/chaos_monkey
	chmod +x build_linux.sh
	./build_linux.sh
   output is in dist/monkey