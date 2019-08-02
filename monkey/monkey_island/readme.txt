To get development versions of Monkey Island and Monkey look into deployment scripts folder.
If you only want to run the software from source you may refer to the instructions below.

How to set up the Monkey Island server:

---------------- On Windows ----------------:
0. Exclude the folder you are planning to install the Monkey in from your AV software, as it might block or delete files from the installation.
1. Create folder "bin" under monkey_island
2. Place portable version of Python 2.7.15
	2.1. Download and install from: https://www.python.org/downloads/release/python-2715/
	2.2. Install virtualenv using "python -m pip install virtualenv"
	2.3. Create a virtualenv using "python -m virtualenv --always-copy <PATH TO BIN>\Python27" Where <PATH TO BIN> is the path to the bin folder created on step 1.
	2.4. Run "python -m virtualenv --relocatable <PATH TO BIN>\Python27"
	2.5. Install the required python libraries using "<PATH TO BIN>\Python27\Scripts\python -m pip install -r monkey_island\requirements.txt"
	2.6. Copy DLLs from installation path (Usually C:\Python27\DLLs) to <PATH TO BIN>\Python27\DLLs
	2.7. (Optional) You may uninstall Python27 if you like.
3. Setup mongodb (Use one of the following two options):
    3.a Place portable version of mongodb
	   3.a.1. Download from: https://downloads.mongodb.org/win32/mongodb-win32-x86_64-2008plus-ssl-latest.zip
 	   3.a.2. Extract contents from bin folder to monkey_island\bin\mongodb.
	   3.a.3. Create monkey_island\db folder.
	OR
    3.b. Use already running instance of mongodb
		3.b.1. Run 'set MONKEY_MONGO_URL="mongodb://<SERVER ADDR>:27017/monkeyisland"'. Replace '<SERVER ADDR>' with address of mongo server
        
4. Place portable version of OpenSSL
	4.1. Download from: https://indy.fulgan.com/SSL/Archive/openssl-1.0.2l-i386-win32.zip
	4.2. Extract content from bin folder to monkey_island\bin\openssl
5. Download and install Microsoft Visual C++ redistributable for Visual Studio 2017
	5.1. Download and install from: https://go.microsoft.com/fwlink/?LinkId=746572
6. Generate SSL Certificate
	6.1. run create_certificate.bat when your current working directory is monkey_island
7. Create the monkey_island\cc\binaries folder and put Infection Monkey binaries inside
	monkey-linux-64 - monkey binary for linux 64bit
	monkey-linux-32 - monkey binary for linux 32bit
	monkey-windows-32.exe - monkey binary for windows 32bit
	monkey-windows-64.exe - monkey binary for windows 64bit
8. Install npm
	8.1. Download and install from: https://www.npmjs.com/get-npm
9. Build Monkey Island frontend
	9.1. cd to 'monkey_island\cc\ui'
	9.2. run 'npm update'
	9.3. run 'npm run dist'

How to run:
1. When your current working directory is monkey_island, run monkey_island\windows\run_server.bat

---------------- On Linux ----------------:
1. Create the following directories:
    sudo mkdir /var/monkey_island
    sudo chmod 777 /var/monkey_island
    mkdir -p /var/monkey_island/bin/mongodb
    mkdir -p /var/monkey_island/db
    mkdir -p /var/monkey_island/cc/binaries

2. Install the packages from monkey_island/requirements.txt:
	sudo python -m pip install -r /var/monkey_island/requirements.txt
	If pip is not installed, install the python-pip package. Make sure the server is running Python 2.7 and not Python 3+.
	
3. put monkey binaries in /var/monkey_island/cc/binaries
    monkey-linux-64 - monkey binary for linux 64bit
	monkey-linux-32 - monkey binary for linux 32bit
	monkey-windows-32.exe - monkey binary for windows 32bit
	monkey-windows-64.exe - monkey binary for windows 64bi

4. Setup MongoDB (Use one of the two following options):
        4.a. Download MongoDB and extract it to /var/monkey_island/bin/mongodb
			4.a.1. Run '/var/monkey_island/linux/install_mongo.sh /var/monkey_island/bin/mongodb'
				   This will download and extract the relevant mongoDB for your OS.
        OR
        4.b. Use already running instance of mongodb
			4.b.1. Run 'set MONKEY_MONGO_URL="mongodb://<SERVER ADDR>:27017/monkeyisland"'. Replace '<SERVER ADDR>' with address of mongo server

5. install OpenSSL
    sudo apt-get install openssl

6. Generate SSL Certificate, Run create_certificate.sh (located under /linux)

7. Copy monkey island server to /var/monkey_island:
    cp -r [monkey_island_source]/cc /var/monkey_island/

8. Install npm
	8.1. Download and install from: https://www.npmjs.com/get-npm
	
9. Build Monkey Island frontend
	9.1. cd to 'monkey_island/cc/ui'
	9.2. run 'npm update'
	9.3. run 'npm run dist'
	
How to run:
1. run run.sh (located under /linux)
