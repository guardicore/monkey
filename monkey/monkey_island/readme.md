>To easily setup development environment for Monkey Island and the Monkey look into deployment scripts folder.

>If you want to setup dev. env. for Island manually, refer to the instructions below.

## How to set up the Monkey Island server:

### On Windows:
0. Exclude the folder you are planning to install the Monkey in from your AV software, as it might block or delete files from the installation.
1. Create folder "bin" under monkey_island
2. Place portable version of Python 3.7.4
	- Download and install from: https://www.python.org/ftp/python/3.7.4/
	- Install virtualenv using "python -m pip install virtualenv"
	- Create a virtualenv using "python -m virtualenv --always-copy <PATH TO BIN>\Python37" Where <PATH TO BIN> is the path to the bin folder created on step 1.
	- Run "python -m virtualenv --relocatable <PATH TO BIN>\Python37"
	- Install the required python libraries using "<PATH TO BIN>\Python37\Scripts\python -m pip install -r monkey_island\requirements.txt"
	- Copy DLLs from installation path (Usually C:\Python27\DLLs) to <PATH TO BIN>\Python37\DLLs
	- (Optional) You may uninstall Python3.7 if you like.
3. Setup mongodb (Use one of the following two options):
    - Place portable version of mongodb
	   1. Download from: https://downloads.mongodb.org/win32/mongodb-win32-x86_64-2008plus-ssl-latest.zip
 	   2. Extract contents from bin folder to monkey_island\bin\mongodb.
	   3. Create monkey_island\db folder.
	   
	OR
    - Use already running instance of mongodb
		1. Run 'set MONKEY_MONGO_URL="mongodb://<SERVER ADDR>:27017/monkeyisland"'. Replace '<SERVER ADDR>' with address of mongo server

4. Place portable version of OpenSSL
	- Download from: https://indy.fulgan.com/SSL/Archive/openssl-1.0.2l-i386-win32.zip
	- Extract content from bin folder to monkey_island\bin\openssl
5. Download and install Microsoft Visual C++ redistributable for Visual Studio 2017
	- Download and install from: https://go.microsoft.com/fwlink/?LinkId=746572
6. Generate SSL Certificate
	- run create_certificate.bat when your current working directory is monkey_island
7. Create the monkey_island\cc\binaries folder and put Infection Monkey binaries inside (binaries can be found in releases on github)
	monkey-linux-64 - monkey binary for linux 64bit
	monkey-linux-32 - monkey binary for linux 32bit
	monkey-windows-32.exe - monkey binary for windows 32bit
	monkey-windows-64.exe - monkey binary for windows 64bit
8. Install npm
	- Download and install from: https://www.npmjs.com/get-npm
9. Build Monkey Island frontend
	- cd to 'monkey_island\cc\ui'
	- run 'npm update'
	- run 'npm run dist'

#### How to run:
1. When your current working directory is monkey_island, run monkey_island\windows\run_server.bat

### On Linux:
0. Get python 3.7 and pip if your linux distribution doesn't have it built in (following steps are for Ubuntu 16):
    - `sudo add-apt-repository ppa:deadsnakes/ppa`
    - `sudo apt-get update`
    - `sudo apt install python3.7`
	- `sudo apt install python3-pip`
    - `python3.7 -m pip install pip`
    - `sudo apt-get install python3.7-dev`
1. Install required packages:
    - `sudo apt-get install libffi-dev upx libssl-dev libc++1 openssl`
2. Create the following directories in monkey island folder (execute from ./monkey):
    - `mkdir -p ./monkey_island/bin/mongodb`
    - `mkdir -p ./monkey_island/db`
    - `mkdir -p ./monkey_island/cc/binaries`

2. Install the packages from monkey_island/requirements.txt:
	- `sudo python3.7 -m pip install -r ./monkey_island/requirements.txt`

3. Put monkey binaries in /monkey_island/cc/binaries (binaries can be found in releases on github)
    monkey-linux-64 - monkey binary for linux 64bit
	monkey-linux-32 - monkey binary for linux 32bit
	monkey-windows-32.exe - monkey binary for windows 32bit
	monkey-windows-64.exe - monkey binary for windows 64bi

4. Setup MongoDB (Use one of the two following options):
    - Download MongoDB and extract it to /var/monkey_island/bin/mongodb:
        1. Run `./monkey_island/linux/install_mongo.sh ./monkey_island/bin/mongodb`. This will download and extract the relevant mongoDB for your OS.
    
    OR
    - Use already running instance of mongodb
        1. Run `set MONKEY_MONGO_URL="mongodb://<SERVER ADDR>:27017/monkeyisland"`. Replace '<SERVER ADDR>' with address of mongo server

6. Generate SSL Certificate:
    - `cd ./monkey_island`
    - `./linux/create_certificate.sh`

8. Install npm and node by running:
	- `sudo apt-get install curl`
    - `curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -`
    - `sudo apt-get install -y nodejs`

9. Build Monkey Island frontend
	- cd to 'monkey_island/cc/ui'
    - `npm install sass-loader node-sass webpack --save-dev`
    - `npm update`
	- `npm run dist`

#### How to run:
1. When your current working directory is monkey, run ./monkey_island/linux/run.sh (located under /linux)
