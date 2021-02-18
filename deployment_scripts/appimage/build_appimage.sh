#!/bin/bash

python_cmd="python3.7"
APPDIR="$HOME/monkey-appdir"
INSTALL_DIR="$APPDIR/usr/src"

GIT=$HOME/git

REPO_MONKEY_HOME=$GIT/monkey
REPO_MONKEY_SRC=$REPO_MONKEY_HOME/monkey

ISLAND_PATH="$INSTALL_DIR/monkey_island"
MONGO_PATH="$ISLAND_PATH/bin/mongodb"
ISLAND_BINARIES_PATH="$ISLAND_PATH/cc/binaries"

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

setup_appdir() {
    rm -rf $APPDIR | true
    mkdir -p $INSTALL_DIR
}

install_pip_37() {
    pip_url=https://bootstrap.pypa.io/get-pip.py
    curl $pip_url -o get-pip.py
    ${python_cmd} get-pip.py
    rm get-pip.py
}

install_nodejs() {
  log_message "Installing nodejs"
  node_src=https://deb.nodesource.com/setup_12.x
  curl -sL $node_src | sudo -E bash -
  sudo apt-get install -y nodejs
}

install_build_prereqs() {
    # appimage-builder prereqs
    sudo apt install -y python3 python3-pip python3-setuptools patchelf desktop-file-utils libgdk-pixbuf2.0-dev fakeroot strace

    #monkey island prereqs
    sudo apt install -y curl libcurl4 python3.7 python3.7-dev openssl git build-essential moreutils
    install_pip_37
    install_nodejs
}

install_appimage_builder() {
    sudo pip3 install appimage-builder

    install_appimage_tool
}

install_appimage_tool() {
    APP_TOOL_BIN=$HOME/bin/appimagetool
    mkdir $HOME/bin
    curl -L -o $APP_TOOL_BIN https://github.com/AppImage/AppImageKit/releases/download/12/appimagetool-x86_64.AppImage
    chmod u+x $APP_TOOL_BIN

    PATH=$PATH:$HOME/bin
}

load_monkey_binary_config() {
  tmpfile=$(mktemp)

  log_message "downloading configuration"
  curl -L -s -o $tmpfile "$config_url"

  log_message "loading configuration"
  source $tmpfile
}

clone_monkey_repo() {
  if [[ ! -d ${GIT} ]]; then
    mkdir -p "${GIT}"
  fi

  log_message "Cloning files from git"
  branch=${2:-"local-run-data-dir"}
  git clone --single-branch --recurse-submodules -b "$branch" "${MONKEY_GIT_URL}" "${REPO_MONKEY_HOME}" 2>&1 || handle_error

  chmod 774 -R "${MONKEY_HOME}"
}

copy_monkey_island_to_appdir() {
  cp $REPO_MONKEY_SRC/__init__.py $INSTALL_DIR
  cp $REPO_MONKEY_SRC/monkey_island.py $INSTALL_DIR
  cp -r $REPO_MONKEY_SRC/common $INSTALL_DIR
  cp -r $REPO_MONKEY_SRC/monkey_island $INSTALL_DIR
  cp ./run_appimage.sh $INSTALL_DIR/monkey_island/linux/
  cp ./island_logger_config.json $INSTALL_DIR/
  cp ./server_config.json.standard $INSTALL_DIR/monkey_island/cc/

  # TODO: This is a workaround that may be able to be removed after PR #848 is
  # merged. See monkey_island/cc/environment_singleton.py for more information.
  cp ./server_config.json.standard $INSTALL_DIR/monkey_island/cc/server_config.json
}

install_monkey_island_python_dependencies() {
  log_message "Installing island requirements"

  requirements_island="$ISLAND_PATH/requirements.txt"
  # TODO: This is an ugly hack. PyInstaller is a build-time dependency and should
  #		  not be installed as a runtime requirement.
  sed '4d' $requirements_island | sponge $requirements_island

  ${python_cmd} -m pip install -r "${requirements_island}"  --ignore-installed --prefix /usr --root=$APPDIR || handle_error
  ${python_cmd} -m pip install pyjwt==1.7 --ignore-installed -U --prefix /usr --root=$APPDIR || handle_error
}

download_monkey_agent_binaries() {
log_message "Downloading monkey agent binaries to ${ISLAND_BINARIES_PATH}"
  mkdir -p "${ISLAND_BINARIES_PATH}" || handle_error
  curl -L -o ${ISLAND_BINARIES_PATH}/${LINUX_32_BINARY_NAME} ${LINUX_32_BINARY_URL}
  curl -L -o ${ISLAND_BINARIES_PATH}/${LINUX_64_BINARY_NAME} ${LINUX_64_BINARY_URL}
  curl -L -o ${ISLAND_BINARIES_PATH}/${WINDOWS_32_BINARY_NAME} ${WINDOWS_32_BINARY_URL}
  curl -L -o ${ISLAND_BINARIES_PATH}/${WINDOWS_64_BINARY_NAME} ${WINDOWS_64_BINARY_URL}

  # Allow them to be executed
  chmod a+x "$ISLAND_BINARIES_PATH/$LINUX_32_BINARY_NAME"
  chmod a+x "$ISLAND_BINARIES_PATH/$LINUX_64_BINARY_NAME"
}

install_mongodb() {
  log_message "Installing MongoDB"

  mkdir -p $MONGO_PATH
  "${ISLAND_PATH}"/linux/install_mongo.sh ${MONGO_PATH} || handle_error
}

generate_ssl_cert() {
  log_message "Generating certificate"

  chmod u+x "${ISLAND_PATH}"/linux/create_certificate.sh
  "${ISLAND_PATH}"/linux/create_certificate.sh ${ISLAND_PATH}/cc
}

build_frontend() {
    pushd "$ISLAND_PATH/cc/ui" || handle_error
    npm install sass-loader node-sass webpack --save-dev
    npm update

    log_message "Generating front end"
    npm run dist
    popd || handle_error
}

build_appimage() {
	log_message "Building AppImage"
	appimage-builder --recipe monkey_island_builder.yml --log DEBUG --skip-appimage

	# There is a bug or unwanted behavior in appimage-builder that causes issues
	# if 32-bit binaries are present in the appimage. To work around this, we:
	#   1. Build the AppDir with appimage-builder and skip building the appimage
	#   2. Add the 32-bit binaries to the AppDir
	#   3. Build the AppImage with appimage-builder from the already-built AppDir
	#
	# Note that appimage-builder replaces the interpreter on the monkey agent binaries
	# when building the AppDir. This is unwanted as the monkey agents may execute in 
	# environments where the AppImage isn't loaded.
	#
	# See https://github.com/AppImageCrafters/appimage-builder/issues/93 for more info.
	download_monkey_agent_binaries

	appimage-builder --recipe monkey_island_builder.yml --log DEBUG --skip-build
}

if is_root; then
  log_message "Please don't run this script as root"
  exit 1
fi

if ! has_sudo; then
  log_message "You need root permissions for some of this script operations. \
Run \`sudo -v\`, enter your password, and then re-run this script."
  exit 1
fi

config_url="https://raw.githubusercontent.com/mssalvatore/monkey/linux-deploy-binaries/deployment_scripts/config"

setup_appdir

install_build_prereqs
install_appimage_builder


load_monkey_binary_config
clone_monkey_repo

copy_monkey_island_to_appdir

# Create folders
log_message "Creating island dirs under $ISLAND_PATH"
mkdir -p "${MONGO_PATH}" || handle_error

install_monkey_island_python_dependencies

install_mongodb

generate_ssl_cert

build_frontend

mkdir -p $APPDIR/usr/share/icons
cp $REPO_MONKEY_SRC/monkey_island/cc/ui/src/images/monkey-icon.svg $APPDIR/usr/share/icons/monkey-icon.svg

build_appimage

log_message "Deployment script finished."
exit 0
