# Monkey island dev. env. setup guide

>To easily setup development environment for Monkey Island and the Monkey look into [deployment scripts](../../deployment_scripts) folder.
>If you want to setup dev. env. for Island manually, refer to the instructions below.

## How to set up the Monkey Island server

### On Windows

1. Exclude the folder you are planning to install the Monkey in from your AV software, as it might block or delete files from the installation.

1. Create folder "bin" under monkey\monkey_island

1. Place portable version of Python 3.11.2
    - Download and install from: <https://www.python.org/ftp/python/3.11.2/>

1. Install pipx
    - `pip install --user -U pipx`
    - `pipx ensurepath`

1. Install pipenv
    - `pipx install pipenv`

1. From the `monkey\monkey_island` directory, install python dependencies:
    - `pipenv sync --dev`

1. Setup mongodb (Use one of the following two options):
    - Place portable version of mongodb
       1. Download from: <https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-6.0.4.zip>
       2. Extract contents of bin folder to \monkey\monkey_island\bin\mongodb.

    OR
    - Use already running instance of mongodb
        1. Run 'set MONKEY_MONGO_URL="mongodb://<SERVER ADDR>:27017/monkey_island"'. Replace '<SERVER ADDR>' with address of mongo server

1. Place portable version of OpenSSL
    - Download from: <https://indy.fulgan.com/SSL/Archive/openssl-1.0.2p-i386-win32.zip>
    - Extract contents to monkey_island\bin\openssl

1. Download and install Microsoft Visual C++ redistributable for Visual Studio 2017
    - Download and install from: <https://go.microsoft.com/fwlink/?LinkId=746572>

1. Generate SSL Certificate
    - run `./windows/create_certificate.bat` when your current working directory is monkey_island

1. Put Infection Monkey binaries inside monkey_island/cc/binaries (binaries can be found in releases on github or build from source)
    monkey-linux-64 - monkey binary for linux 64bit
    monkey-windows-64.exe - monkey binary for windows 64bit

1. Install npm
    - Download and install from: <https://www.npmjs.com/get-npm>

1. Build Monkey Island frontend
    - cd to 'monkey_island\cc\ui'
    - run 'npm update'
    - run 'npm run dist'

#### How to run

1. When your current working directory is monkey_island, run monkey_island\windows\run_server_py.bat

### On Linux

1. Set your current working directory to `monkey/`.

1. Get python 3.11 and pip if your linux distribution doesn't have it built in (following steps are for Ubuntu 16):
    - `sudo add-apt-repository ppa:deadsnakes/ppa`
    - `sudo apt-get update`
    - `sudo apt install python3.11 python3-pip python3.11-dev python3.11-venv`
    - `python3.11 -m pip install pip`

1. Install pipx:
    - `python3.11 -m pip install --user pipx`
    - `python3.11 -m pipx ensurepath`
    - `source ~/.profile`

1. Install pipenv:
    - `pipx install pipenv`

1. Install required packages:
    - `sudo apt-get install libffi-dev upx libssl-dev libc++1 openssl`

1. Install the Monkey Island python dependencies:
    - `cd ./monkey_island`
    - `pipenv sync --dev`
    - `cd ..`

1. Create the following directories in monkey island folder (execute from ./monkey):
    - `mkdir -p ./monkey_island/bin/mongodb`
    - `mkdir -p ./monkey_island/cc/binaries`

1. Put monkey binaries in /monkey_island/cc/binaries (binaries can be found in releases on github).

    monkey-linux-64 - monkey binary for linux 64bit

    monkey-windows-64.exe - monkey binary for windows 64bit

    Also, if you're going to run monkeys on local machine execute:
    - `chmod 755 ./monkey_island/cc/binaries/monkey-linux-64`

1. Setup MongoDB (Use one of the two following options):
    - Download MongoDB and extract it to monkey/monkey_island/bin/mongodb:
        1. Run `./monkey_island/linux/install_mongo.sh ./monkey_island/bin/mongodb`. This will download and extract the relevant mongoDB for your OS.

    OR
    - Use already running instance of mongodb
        1. Run `set MONKEY_MONGO_URL="mongodb://<SERVER ADDR>:27017/monkey_island"`. Replace '<SERVER ADDR>' with address of mongo server

1. Generate SSL Certificate:
    - `cd ./monkey_island`
    - `chmod 755 ./linux/create_certificate.sh`
    - `./linux/create_certificate.sh`

1. Install npm and node by running:
    - `sudo apt-get install curl`
    - `sudo mkdir -p /usr/local/lib/nodejs`
    - `curl -sL https://nodejs.org/dist/v20.7.0/node-v20.7.0-linux-x64.tar.xz | sudo tar xJf - -C /usr/local/lib/nodejs`
    - `echo -e "# Nodejs\nexport PATH=/usr/local/lib/nodejs/node-v20.7.0-linux-x64/bin:\$PATH" >> ~/.profile && source ~/.profile`

1. Build Monkey Island frontend
    - cd to 'monkey_island/cc/ui'
    - `npm install sass-loader node-sass webpack --save-dev`
    - `npm update`
    - `npm run dist`

#### How to run

1. From the `monkey` directory, run `python3.11 ./monkey_island.py`


#### Troubleshooting

When committing your changes for the first time, you may encounter some errors thrown by the pre-commit hooks. This is most likely because some python dependencies are missing from your system.
To resolve this, use `pipenv` to create a `requirements.txt` for both the `infection_monkey/` and `monkey_island/` requirements and install it with `pip`.

   - `cd [code location]/infection_monkey`
   - `python3.11 -m pipenv lock -r --dev > requirements.txt`
   - `python3.11 -m pip install -r requirements.txt`

   and

   - `cd [code location]/monkey_island`
   - `python3.11 -m pipenv lock -r --dev > requirements.txt`
   - `python3.11 -m pip install -r requirements.txt`
