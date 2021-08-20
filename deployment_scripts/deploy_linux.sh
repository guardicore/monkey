#!/bin/bash

exists() {
  command -v "$1" >/dev/null 2>&1
}

is_root() {
  return $(id -u)
}

has_sudo() {
  # 0 true, 1 false
  return $(sudo -nv > /dev/null 2>&1)
}

handle_error() {
  echo "Fix the errors above and rerun the script"
  exit 1
}

log_message() {
  echo -e "\n\n"
  echo -e "DEPLOYMENT SCRIPT: $1"
}

configure_precommit() {
    $1 -m pip install --user pre-commit
    pushd "$2"
    $HOME/.local/bin/pre-commit install -t pre-commit -t pre-push
    popd
}

if is_root; then
  log_message "Please don't run this script as root"
  exit 1
fi

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

if ! has_sudo; then
  log_message "You need root permissions for some of this script operations. \
Run \`sudo -v\`, enter your password, and then re-run this script."
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
log_message "Branch selected: ${branch}"
if [[ ! -d "$monkey_home/monkey" ]]; then # If not already cloned
  git clone --single-branch --recurse-submodules -b "$branch" "${MONKEY_GIT_URL}" "${monkey_home}" 2>&1 || handle_error
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
  sudo apt-get install -y python3.7 python3.7-dev python3.7-venv
  log_message "Python 3.7 is now available with command 'python3.7'."
  python_cmd="python3.7"
fi

log_message "Installing build-essential"
sudo apt-get install -y build-essential

log_message "Installing python3-distutils"
sudo apt-get install -y python3-distutils

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

log_message "Installing pipenv"
${python_cmd} -m pip install --user -U pipx
${python_cmd} -m pipx ensurepath
source ~/.profile
pipx install pipenv

log_message "Installing island requirements"
pushd $ISLAND_PATH
pipenv install --dev
popd

log_message "Installing monkey requirements"
sudo apt-get install -y libffi-dev upx libssl-dev libc++1
pushd $INFECTION_MONKEY_DIR
pipenv install --dev
popd

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
  log_message "Installing libcurl4"
  sudo apt-get install -y libcurl4

  log_message "Installing MongoDB"
  "${ISLAND_PATH}"/linux/install_mongo.sh ${MONGO_PATH} || handle_error
fi
log_message "Installing openssl"
sudo apt-get install -y openssl

# Generate SSL certificate
log_message "Generating certificate"

chmod u+x "${ISLAND_PATH}"/linux/create_certificate.sh
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

# Download Swimm
log_message "Downloading swimm"
if exists wget; then
  wget ${SWIMM_URL} -O $HOME/swimm
else
  curl ${SWIMM_URL} -o $HOME/swimm
fi

log_message "Installing swimm"
sudo dpkg -i $HOME/swimm || (sudo apt-get update && sudo apt-get -f install)
rm $HOME/swimm

sudo chmod +x "${INFECTION_MONKEY_DIR}/build_linux.sh"

configure_precommit ${python_cmd} ${monkey_home}

log_message "Deployment script finished."
exit 0
