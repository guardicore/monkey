#!/bin/bash
source config

# Setup monkey either in dir required or current dir
monkey_home=${1:-`pwd`}
if [[ $monkey_home == `pwd` ]]; then
    monkey_home="$monkey_home/$MONKEY_FOLDER_NAME"
fi

# We can set main paths after we know the home dir
ISLAND_PATH="$monkey_home/monkey/monkey_island"
MONKEY_COMMON_PATH="$monkey_home/monkey/common/"
MONGO_PATH="$ISLAND_PATH/bin/mongodb"
MONGO_BIN_PATH="$MONGO_PATH/bin"
ISLAND_DB_PATH="$ISLAND_PATH/db"
ISLAND_BINARIES_PATH="$ISLAND_PATH/cc/binaries"

handle_error () {
    echo "Fix the errors above and rerun the script"
    exit 1
}

log_message () {
    echo -e "\n\n-------------------------------------------"
    echo -e "DEPLOYMENT SCRIPT: $1"
    echo -e "-------------------------------------------\n"
}

sudo -v
if [[ $? != 0 ]]; then
    echo "You need root permissions for some of this script operations. Quiting."
    exit 1
fi

if [[ ! -d ${monkey_home} ]]; then
    mkdir -p ${monkey_home}
fi

git --version &>/dev/null
git_available=$?
if [[ ${git_available} != 0 ]]; then
    echo "Please install git and re-run this script"
    exit 1
fi

log_message "Cloning files from git"
branch=${2:-"develop"}
if [[ ! -d "$monkey_home/monkey" ]]; then # If not already cloned
    git clone --single-branch -b $branch ${MONKEY_GIT_URL} ${monkey_home} 2>&1 || handle_error
    chmod 774 -R ${monkey_home}
fi

# Create folders
log_message "Creating island dirs under $ISLAND_PATH"
mkdir -p ${MONGO_BIN_PATH}
mkdir -p ${ISLAND_DB_PATH}
mkdir -p ${ISLAND_BINARIES_PATH} || handle_error

python_version=`python --version 2>&1`
if [[ ${python_version} == *"command not found"* ]] || [[ ${python_version} != *"Python 2.7"* ]]; then
    echo "Python 2.7 is not found or is not a default interpreter for 'python' command..."
    exit 1
fi

log_message "Updating package list"
sudo apt-get update

log_message "Installing pip"
sudo apt-get install python-pip

log_message "Installing island requirements"
requirements="$ISLAND_PATH/requirements.txt"
python -m pip install --user -r ${requirements} || handle_error

# Download binaries
log_message "Downloading binaries"
wget -c -N -P ${ISLAND_BINARIES_PATH} ${LINUX_32_BINARY_URL}
wget -c -N -P ${ISLAND_BINARIES_PATH} ${LINUX_64_BINARY_URL}
wget -c -N -P ${ISLAND_BINARIES_PATH} ${WINDOWS_32_BINARY_URL}
wget -c -N -P ${ISLAND_BINARIES_PATH} ${WINDOWS_64_BINARY_URL}
# Allow them to be executed
chmod a+x "$ISLAND_BINARIES_PATH/$LINUX_32_BINARY_NAME"
chmod a+x "$ISLAND_BINARIES_PATH/$LINUX_64_BINARY_NAME"


# Get machine type/kernel version
kernel=`uname -m`
linux_dist=`lsb_release -a 2> /dev/null`

# If a user haven't installed mongo manually check if we can install it with our script
log_message "Installing MongoDB"
${ISLAND_PATH}/linux/install_mongo.sh ${MONGO_BIN_PATH} || handle_error

log_message "Installing openssl"
sudo apt-get install openssl

# Generate SSL certificate
log_message "Generating certificate"
cd ${ISLAND_PATH} || handle_error
openssl genrsa -out cc/server.key 1024 || handle_error
openssl req -new -key cc/server.key -out cc/server.csr \
-subj "/C=GB/ST=London/L=London/O=Global Security/OU=Monkey Department/CN=monkey.com" || handle_error
openssl x509 -req -days 366 -in cc/server.csr -signkey cc/server.key -out cc/server.crt || handle_error


sudo chmod +x ${ISLAND_PATH}/linux/create_certificate.sh || handle_error
${ISLAND_PATH}/linux/create_certificate.sh || handle_error

# Install npm
log_message "Installing npm"
sudo apt-get install npm

# Update node
log_message "Updating node"
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt-get install -y nodejs

log_message "Generating front end"
cd "$ISLAND_PATH/cc/ui" || handle_error
npm update
npm run dist

# Monkey setup
log_message "Installing monkey requirements"
sudo apt-get install python-pip python-dev libffi-dev upx libssl-dev libc++1
cd ${monkey_home}/monkey/infection_monkey || handle_error
python -m pip install --user -r requirements_linux.txt || handle_error

# Build samba
log_message "Building samba binaries"
sudo apt-get install gcc-multilib
cd ${monkey_home}/monkey/infection_monkey/monkey_utils/sambacry_monkey_runner
sudo chmod +x ./build.sh || handle_error
./build.sh

sudo chmod +x ${monkey_home}/monkey/infection_monkey/build_linux.sh

log_message "Deployment script finished."
exit 0
