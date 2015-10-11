How to setup C&C server:
On Windows:
1. Install python 2.7
	https://www.python.org/download/releases/2.7
2. Download & Run get-pip.py
	https://bootstrap.pypa.io/get-pip.py
3. Run:
	setx path "%path%;C:\Python27\;C:\Python27\Scripts"
	python -m pip install flask
	python -m pip install Flask-Pymongo
	python -m pip install Flask-Restful
	python -m pip install python-dateutil
	mkdir C:\MonkeyIsland\bin
	mkdir C:\MonkeyIsland\db
	mkdir C:\MonkeyIsland\cc\binaries
4. Put monkey binaries in C:\MonkeyIsland\cc\binaries:
	monkey-linux-64 - monkey binary for linux 64bit
	monkey-linux-32 - monkey binary for linux 32bit
	monkey-windows-32.exe - monkey binary for windows 32bit
	monkey-windows-64.exe - monkey binary for windows 64bit
4. Download MongoDb & Extract to C:\MonkeyIsland\bin\mongodb
	http://downloads.mongodb.org/win32/mongodb-win32-x86_64-2008plus-ssl-latest.zip
5. Install OpenSSL
	https://slproweb.com/download/Win64OpenSSL_Light-1_0_2d.exe
6. Generate SSL Certificate, Run create_certificate.bat

How to Connect to build environment:
1. set hostname to MONKEYCC
2. Put monkey source code at C:\Code\monkey
3. Run:
	net share binaries=C:\MonkeyIsland\cc\binaries
	net share sources=C:\Code\monkey\chaos_monkey
4. Run batch/sh script according to build environment readme

How to run:
1. start run_mongodb.bat
2. start run_cc.bat
3. to clear db, run clear_db.bat