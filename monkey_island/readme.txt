How to set C&C server:

---------------- On Windows ----------------:
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
4. Download MongoDB & Extract to C:\MonkeyIsland\bin\mongodb
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

---------------- On Linux ----------------:
1. Create the following directories:
    sudo mkdir /var/monkey_island
    sudo chmod 777 /var/monkey_island
    mkdir -p /var/monkey_island/bin/mongodb
    mkdir -p /var/monkey_island/db
    mkdir -p /var/monkey_island/cc/binaries

2. Install the following packages:
	sudo pip install flask
	sudo pip install Flask-Pymongo
	sudo pip install Flask-Restful
	sudo pip install python-dateutil
	
3. put monkey binaries in /var/monkey_island/cc/binaries
    monkey-linux-64 - monkey binary for linux 64bit
	monkey-linux-32 - monkey binary for linux 32bit
	monkey-windows-32.exe - monkey binary for windows 32bit
	monkey-windows-64.exe - monkey binary for windows 64bi

4. Download MongoDB and extract it to /var/monkey_island/bin/mongodb
    for debian64 - https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian71-3.0.7.tgz
    for ubuntu64 14.10 - https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1410-clang-3.0.7.tgz
    find more at - https://www.mongodb.org/downloads#production
	untar.gz with: tar -zxvf filename.tar.gz -C /var/monkey_island/bin/mongodb
	(make sure the content of the mongo folder is in this directory, meaning this path exists:
		/var/monkey_island/bin/mongodb/bin)

5. install OpenSSL
    sudo apt-get install openssl

6. Generate SSL Certificate, Run create_certificate.sh (located under /linux)

7. Copy monkey island server to /var/monkey_island:
    cp -r [monkey_island_source]/cc /var/monkey_island/

How to run:
1. run run.sh
2. to clear db, run clear.db.sh
