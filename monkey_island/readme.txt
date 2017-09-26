How to set C&C server:

---------------- On Windows ----------------:
1. Create bin folder
	1.1. create folder "bin" under monkey_island
2. Place portable version of Python 2.7
	2.1. Download and install from: https://www.python.org/download/releases/2.7/
	2.2. Download & Run get-pip.py from: https://bootstrap.pypa.io/get-pip.py
	2.3. Install required python libraries using "python -m pip install -r monkey_island\requirements.txt"
	2.4. Copy Contents from Installation path (Usually C:\Python27) to monkey_island\bin\Python27
	2.5. Copy Python27.dll from System32 folder (Usually C:\Windows\System32) to monkey_island\bin\Python27
	2.6. (Optional) You may uninstall Python27 if you like.
3. Place portable version of mongodb
	3.1. Download from: http://downloads.mongodb.org/win32/mongodb-win32-x86_64-2008plus-ssl-latest.zip
	3.2. Extract contents from bin folder to monkey_island\bin\mongodb.
4. Place portable version of OpenSSL
	4.1. Download from: http://downloads.sourceforge.net/gnuwin32/openssl-0.9.8h-1-bin.zip
	4.2. Extract content from bin folder to monkey_island\bin\openssl
5. Download and install Microsoft Visual C++ Redisutable for Visual Studio 2017
	5.1. Download and install from: https://go.microsoft.com/fwlink/?LinkId=746572
6. Generate SSL Certificate
	6.1. run create_certificate.bat when your current working directory is monkey_island
7. Put chaos monkey binaries in monkey_island\cc\binaries (create folder if it doesn't exist):
	monkey-linux-64 - monkey binary for linux 64bit
	monkey-linux-32 - monkey binary for linux 32bit
	monkey-windows-32.exe - monkey binary for windows 32bit
	monkey-windows-64.exe - monkey binary for windows 64bit
8. Install npm
	8.1. Download and install from: https://www.npmjs.com/get-npm
9. Build Monkey Island frontend
	9.1. cd to 'monkey_island\cc\ui'
	9.2. run 'npm run dist'

How to run:
1. start monkey_island\windows\run_server.bat (when your current working directory is monkey_island)

---------------- On Linux ----------------:
1. Create the following directories:
    sudo mkdir /var/monkey_island
    sudo chmod 777 /var/monkey_island
    mkdir -p /var/monkey_island/bin/mongodb
    mkdir -p /var/monkey_island/db
    mkdir -p /var/monkey_island/cc/binaries

2. Install the packages from monkey_island/requirements.txt:
	sudo python -m pip install -r /var/monkey_island/requirements.txt
	
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

8. Install npm
	8.1. Download and install from: https://www.npmjs.com/get-npm
	
9. Build Monkey Island frontend
	9.1. cd to 'monkey_island/cc/ui'
	9.2. run 'npm run dist'
	
How to run:
1. run run.sh
