#!/bin/bash

exists() {
  command -v "$1" >/dev/null 2>&1
}

is_root() {
  return $(id -u)
}

has_sudo() {
  # 0 true, 1 false
  timeout 1 sudo id && return 0 || return 1
}

handle_error() {
  echo "Fix the errors above and rerun the script"
  exit 1
}

log_message() {
  echo -e "\n\n"
  echo -e "DEPLOYMENT SCRIPT: $1"
}

config_branch=${2:-"develop"}
config_url="https://raw.githubusercontent.com/guardicore/monkey/${config_branch}/deployment_scripts/config"

if (! exists curl) && (! exists wget); then
  log_message 'Your system does not have curl or wget, exiting'
  exit 1
fi

file=$(mktemp)
# shellcheck disable=SC2086
if exists wget; then
  # shellcheck disable=SC2086
  wget --output-document=$file "$config_url"
else
  # shellcheck disable=SC2086
  curl -s -o $file "$config_url"
fi

log_message "downloaded configuration"
# shellcheck source=deployment_scripts/config
# shellcheck disable=SC2086
source $file
log_message "loaded configuration"
# shellcheck disable=SC2086
# rm $file

# Setup monkey either in dir required or current dir
monkey_home=${1:-$(pwd)}
if [[ $monkey_home == $(pwd) ]]; then
  monkey_home="$monkey_home/$MONKEY_FOLDER_NAME"
fi

# We can set main paths after we know the home dir
ISLAND_PATH="$monkey_home/monkey/monkey_island"
MONGO_PATH="$ISLAND_PATH/bin/mongodb"
ISLAND_BINARIES_PATH="$ISLAND_PATH/cc/binaries"
INFECTION_MONKEY_DIR="$monkey_home/monkey/infection_monkey"
MONKEY_BIN_DIR="$INFECTION_MONKEY_DIR/bin"

if is_root; then
  log_message "Please don't run this script as root"
  exit 1
fi

HAS_SUDO=$(has_sudo)
if [[ ! $HAS_SUDO ]]; then
  log_message "You need root permissions for some of this script operations. Quiting."
  exit 1
fi

if [[ ! -d ${monkey_home} ]]; then
  mkdir -p "${monkey_home}"
fi

if ! exists git; then
  log_message "Please install git and re-run this script"
  exit 1
fi

log_message "Cloning files from git"
branch=${2:-"develop"}
if [[ ! -d "$monkey_home/monkey" ]]; then # If not already cloned
  git clone --single-branch --recurse-submodules -b "$branch" "${MONKEY_GIT_URL}" "${monkey_home}" 2>&1 || handle_error
  chmod 774 -R "${monkey_home}"
fi

# Create folders
log_message "Creating island dirs under $ISLAND_PATH"
mkdir -p "${MONGO_PATH}" || handle_error
mkdir -p "${ISLAND_BINARIES_PATH}" || handle_error

# Detecting command that calls python 3.7
python_cmd=""
if [[ $(python --version 2>&1) == *"Python 3.7"* ]]; then
  python_cmd="python"
fi
if [[ $(python37 --version 2>&1) == *"Python 3.7"* ]]; then
  python_cmd="python37"
fi
if [[ $(python3.7 --version 2>&1) == *"Python 3.7"* ]]; then
  python_cmd="python3.7"
fi

if [[ ${python_cmd} == "" ]]; then
  log_message "Python 3.7 command not found. Installing python 3.7."
  sudo add-apt-repository ppa:deadsnakes/ppa
  sudo apt-get update
  sudo apt install python3.7 python3.7-dev
  log_message "Python 3.7 is now available with command 'python3.7'."
  python_cmd="python3.7"
fi

log_message "Installing build-essential"
sudo apt install build-essential

log_message "Installing or updating pip"
# shellcheck disable=SC2086
pip_url=https://bootstrap.pypa.io/get-pip.py
if exists wget; then
  wget --output-document=get-pip.py $pip_url
else
  curl $pip_url -o get-pip.py
fi
${python_cmd} get-pip.py
rm get-pip.py

log_message "Installing island requirements"
requirements_island="$ISLAND_PATH/requirements.txt"
${python_cmd} -m pip install -r "${requirements_island}" --user --upgrade || handle_error

log_message "Installing monkey requirements"
sudo apt-get install libffi-dev upx libssl-dev libc++1
requirements_monkey="$INFECTION_MONKEY_DIR/requirements.txt"
${python_cmd} -m pip install -r "${requirements_monkey}" --user --upgrade || handle_error


agents=${3:-true}
# Download binaries
if [ "$agents" = true ] ; then
  log_message "Downloading binaries"
  if exists wget; then
    wget -c -N -P ${ISLAND_BINARIES_PATH} ${LINUX_32_BINARY_URL}
    wget -c -N -P ${ISLAND_BINARIES_PATH} ${LINUX_64_BINARY_URL}
    wget -c -N -P ${ISLAND_BINARIES_PATH} ${WINDOWS_32_BINARY_URL}
    wget -c -N -P ${ISLAND_BINARIES_PATH} ${WINDOWS_64_BINARY_URL}
  else
    curl -o ${ISLAND_BINARIES_PATH}\monkey-linux-32 ${LINUX_32_BINARY_URL}
    curl -o ${ISLAND_BINARIES_PATH}\monkey-linux-64 ${LINUX_64_BINARY_URL}
    curl -o ${ISLAND_BINARIES_PATH}\monkey-windows-32.exe ${WINDOWS_32_BINARY_URL}
    curl -o ${ISLAND_BINARIES_PATH}\monkey-windows-64.exe ${WINDOWS_64_BINARY_URL}
  fi
fi

# Allow them to be executed
chmod a+x "$ISLAND_BINARIES_PATH/$LINUX_32_BINARY_NAME"
chmod a+x "$ISLAND_BINARIES_PATH/$LINUX_64_BINARY_NAME"

# If a user haven't installed mongo manually check if we can install it with our script
if ! exists mongod; then
  log_message "Installing MongoDB"
  "${ISLAND_PATH}"/linux/install_mongo.sh ${MONGO_PATH} || handle_error
fi
log_message "Installing openssl"
sudo apt-get install openssl

# Generate SSL certificate
log_message "Generating certificate"

"${ISLAND_PATH}"/linux/create_certificate.sh ${ISLAND_PATH}/cc

# Update node
if ! exists npm; then
  log_message "Installing nodejs"
  node_src=https://deb.nodesource.com/setup_12.x
  if exists curl; then
    curl -sL $node_src | sudo -E bash -
  else
    wget -q -O - $node_src | sudo -E bash -
  fi
  sudo apt-get install -y nodejs
fi

pushd "$ISLAND_PATH/cc/ui" || handle_error
npm install sass-loader node-sass webpack --save-dev
npm update

log_message "Generating front end"
npm run dist
popd || handle_error

# Making dir for binaries
mkdir "${MONKEY_BIN_DIR}"

# Download sambacry binaries
log_message "Downloading sambacry binaries"
# shellcheck disable=SC2086
if exists wget; then
  wget -c -N -P "${MONKEY_BIN_DIR}" ${SAMBACRY_64_BINARY_URL}
  wget -c -N -P "${MONKEY_BIN_DIR}" ${SAMBACRY_32_BINARY_URL}
else
  curl -o ${MONKEY_BIN_DIR}/sc_monkey_runner64.so ${SAMBACRY_64_BINARY_URL}
  curl -o ${MONKEY_BIN_DIR}/sc_monkey_runner32.so ${SAMBACRY_32_BINARY_URL}
fi
# Download traceroute binaries
log_message "Downloading traceroute binaries"
# shellcheck disable=SC2086
if exists wget; then
  wget -c -N -P "${MONKEY_BIN_DIR}" ${TRACEROUTE_64_BINARY_URL}
  wget -c -N -P "${MONKEY_BIN_DIR}" ${TRACEROUTE_32_BINARY_URL}
else
  curl -o ${MONKEY_BIN_DIR}/traceroute64 ${TRACEROUTE_64_BINARY_URL}
  curl -o ${MONKEY_BIN_DIR}/traceroute32 ${TRACEROUTE_32_BINARY_URL}
fi

sudo chmod +x "${INFECTION_MONKEY_DIR}/build_linux.sh"

log_message "Deployment script finished."
exit 0
