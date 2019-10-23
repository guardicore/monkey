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
ISLAND_BINARIES_PATH="$ISLAND_PATH/cc/binaries"
INFECTION_MONKEY_DIR="$monkey_home/monkey/infection_monkey"
MONKEY_BIN_DIR="$INFECTION_MONKEY_DIR/bin"

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
mkdir -p ${MONGO_PATH}
mkdir -p ${ISLAND_BINARIES_PATH} || handle_error

# Detecting command that calls python 3.7
python_cmd=""
if [[ `python --version 2>&1` == *"Python 3.7"* ]]; then
  python_cmd="python"
fi
if [[ `python37 --version 2>&1` == *"Python 3.7"* ]]; then
  python_cmd="python37"
fi
if [[ `python3.7 --version 2>&1` == *"Python 3.7"* ]]; then
  python_cmd="python3.7"
fi

if [[ ${python_cmd} == "" ]]; then
  log_message "Python 3.7 command not found. Installing python 3.7."
  sudo apt-get update
  sudo apt-get install python3.7
  log_message "Python 3.7 is now available with command 'python3.7'."
  python_cmd="python3.7"
fi

log_message "Updating package list"
sudo apt-get update

log_message "Installing pip"
sudo apt install python3-pip
${python_cmd} -m pip install pip

log_message "Install python3.7-dev"
sudo apt-get install python3.7-dev

log_message "Installing island requirements"
requirements="$ISLAND_PATH/requirements.txt"
${python_cmd} -m pip install --user --upgrade -r ${requirements} || handle_error

log_message "Installing monkey requirements"
sudo apt-get install libffi-dev upx libssl-dev libc++1
cd ${monkey_home}/monkey/infection_monkey || handle_error
${python_cmd} -m pip install -r requirements_linux.txt --user --upgrade || handle_error

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
${ISLAND_PATH}/linux/install_mongo.sh ${MONGO_PATH} || handle_error

log_message "Installing openssl"
sudo apt-get install openssl

# Generate SSL certificate
log_message "Generating certificate"
sudo chmod +x ${ISLAND_PATH}/linux/create_certificate.sh || handle_error
${ISLAND_PATH}/linux/create_certificate.sh || handle_error

# Update node
log_message "Installing nodejs"
sudo apt-get install -y nodejs

# Install npm
log_message "Installing npm"
sudo apt-get install npm
npm update

log_message "Generating front end"
cd "$ISLAND_PATH/cc/ui" || handle_error
npm run dist

# Making dir for binaries
mkdir ${MONKEY_BIN_DIR}

# Download sambacry binaries
log_message "Downloading sambacry binaries"
wget -c -N -P ${MONKEY_BIN_DIR} ${SAMBACRY_64_BINARY_URL}
wget -c -N -P ${MONKEY_BIN_DIR} ${SAMBACRY_32_BINARY_URL}

# Download traceroute binaries
log_message "Downloading traceroute binaries"
wget -c -N -P ${MONKEY_BIN_DIR} ${TRACEROUTE_64_BINARY_URL}
wget -c -N -P ${MONKEY_BIN_DIR} ${TRACEROUTE_32_BINARY_URL}


sudo chmod +x ${monkey_home}/monkey/infection_monkey/build_linux.sh

log_message "Deployment script finished."
exit 0
