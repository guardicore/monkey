#!/bin/bash

APPDIR="$HOME/squashfs-root"
CONFIG_URL="https://raw.githubusercontent.com/guardicore/monkey/develop/deployment_scripts/config"
INSTALL_DIR="$APPDIR/usr/src"

GIT=$HOME/git

REPO_MONKEY_HOME=$GIT/monkey
REPO_MONKEY_SRC=$REPO_MONKEY_HOME/monkey

ISLAND_PATH="$INSTALL_DIR/monkey_island"
MONGO_PATH="$ISLAND_PATH/bin/mongodb"
ISLAND_BINARIES_PATH="$ISLAND_PATH/cc/binaries"

NODE_SRC=https://deb.nodesource.com/setup_12.x
APP_TOOL_URL=https://github.com/AppImage/AppImageKit/releases/download/12/appimagetool-x86_64.AppImage
PYTHON_APPIMAGE_URL="https://github.com/niess/python-appimage/releases/download/python3.7/python3.7.9-cp37-cp37m-manylinux1_x86_64.AppImage"

is_root() {
  return "$(id -u)"
}

has_sudo() {
  # 0 true, 1 false
  sudo -nv > /dev/null 2>&1
  return $?
}

handle_error() {
  echo "Fix the errors above and rerun the script"
  exit 1
}

log_message() {
  echo -e "\n\n"
  echo -e "DEPLOYMENT SCRIPT: $1"
}

install_nodejs() {
  log_message "Installing nodejs"

  curl -sL $NODE_SRC | sudo -E bash -
  sudo apt-get install -y nodejs
}

install_build_prereqs() {
    sudo apt update
    sudo apt upgrade

    # monkey island prereqs
    sudo apt install -y curl libcurl4 openssl git build-essential moreutils
    install_nodejs
}

install_appimage_tool() {
    APP_TOOL_BIN=$HOME/bin/appimagetool

    mkdir -p "$HOME"/bin
    curl -L -o "$APP_TOOL_BIN" "$APP_TOOL_URL"
    chmod u+x "$APP_TOOL_BIN"

    PATH=$PATH:$HOME/bin
}

load_monkey_binary_config() {
  tmpfile=$(mktemp)

  log_message "downloading configuration"
  curl -L -s -o "$tmpfile" "$CONFIG_URL"

  log_message "loading configuration"
  source "$tmpfile"
}

clone_monkey_repo() {
  if [[ ! -d ${GIT} ]]; then
    mkdir -p "${GIT}"
  fi

  log_message "Cloning files from git"
  branch=${2:-"postgresql-workaround-2"}
  git clone --single-branch --recurse-submodules -b "$branch" "${MONKEY_GIT_URL}" "${REPO_MONKEY_HOME}" 2>&1 || handle_error

  chmod 774 -R "${REPO_MONKEY_HOME}"
}

setup_appdir() {
	setup_python_37_appdir

	copy_monkey_island_to_appdir
	download_monkey_agent_binaries

	install_monkey_island_python_dependencies
	install_mongodb

	generate_ssl_cert
	build_frontend

	add_monkey_icon
	add_desktop_file
	add_apprun
}

setup_python_37_appdir() {
    PYTHON_APPIMAGE="python3.7.9_x86_64.AppImage"
    rm -rf "$APPDIR" || true
    curl -L -o "$PYTHON_APPIMAGE" "$PYTHON_APPIMAGE_URL"

    chmod u+x "$PYTHON_APPIMAGE"

    ./"$PYTHON_APPIMAGE" --appimage-extract
    rm "$PYTHON_APPIMAGE"
    mv ./squashfs-root "$APPDIR"
    mkdir -p "$INSTALL_DIR"
}

copy_monkey_island_to_appdir() {
  cp "$REPO_MONKEY_SRC"/__init__.py "$INSTALL_DIR"
  cp "$REPO_MONKEY_SRC"/monkey_island.py "$INSTALL_DIR"
  cp -r "$REPO_MONKEY_SRC"/common "$INSTALL_DIR/"
  cp -r "$REPO_MONKEY_SRC"/monkey_island "$INSTALL_DIR/"
  cp ./run_appimage.sh "$INSTALL_DIR"/monkey_island/linux/
  cp ./island_logger_config.json "$INSTALL_DIR"/
  cp ./server_config.json.standard "$INSTALL_DIR"/monkey_island/cc/

  # TODO: This is a workaround that may be able to be removed after PR #848 is
  # merged. See monkey_island/cc/environment_singleton.py for more information.
  cp ./server_config.json.standard "$INSTALL_DIR"/monkey_island/cc/server_config.json
}

install_monkey_island_python_dependencies() {
  log_message "Installing island requirements"

  requirements_island="$ISLAND_PATH/requirements.txt"
  # TODO: This is an ugly hack. PyInstaller and VirtualEnv are build-time
  #       dependencies and should not be installed as a runtime requirement.
  cat "$requirements_island" | grep -Piv "virtualenv|pyinstaller" | sponge "$requirements_island"

  "$APPDIR"/AppRun -m pip install -r "${requirements_island}"  --ignore-installed || handle_error
}

download_monkey_agent_binaries() {
log_message "Downloading monkey agent binaries to ${ISLAND_BINARIES_PATH}"
  mkdir -p "${ISLAND_BINARIES_PATH}" || handle_error
  curl -L -o "${ISLAND_BINARIES_PATH}/${LINUX_32_BINARY_NAME}" "${LINUX_32_BINARY_URL}"
  curl -L -o "${ISLAND_BINARIES_PATH}/${LINUX_64_BINARY_NAME}" "${LINUX_64_BINARY_URL}"
  curl -L -o "${ISLAND_BINARIES_PATH}/${WINDOWS_32_BINARY_NAME}" "${WINDOWS_32_BINARY_URL}"
  curl -L -o "${ISLAND_BINARIES_PATH}/${WINDOWS_64_BINARY_NAME}" "${WINDOWS_64_BINARY_URL}"

  # Allow them to be executed
  chmod a+x "$ISLAND_BINARIES_PATH/$LINUX_32_BINARY_NAME"
  chmod a+x "$ISLAND_BINARIES_PATH/$LINUX_64_BINARY_NAME"
}

install_mongodb() {
  log_message "Installing MongoDB"

  mkdir -p "$MONGO_PATH"
  "${ISLAND_PATH}"/linux/install_mongo.sh "${MONGO_PATH}" || handle_error
}

generate_ssl_cert() {
  log_message "Generating certificate"

  chmod u+x "${ISLAND_PATH}"/linux/create_certificate.sh
  "${ISLAND_PATH}"/linux/create_certificate.sh "${ISLAND_PATH}"/cc
}

build_frontend() {
    pushd "$ISLAND_PATH/cc/ui" || handle_error
    npm install sass-loader node-sass webpack --save-dev
    npm update

    log_message "Generating front end"
    npm run dist
    popd || handle_error
}

add_monkey_icon() {
	unlink "$APPDIR"/python.png
	mkdir -p "$APPDIR"/usr/share/icons
	cp "$REPO_MONKEY_SRC"/monkey_island/cc/ui/src/images/monkey-icon.svg "$APPDIR"/usr/share/icons/infection-monkey.svg
	ln -s "$APPDIR"/usr/share/icons/infection-monkey.svg "$APPDIR"/infection-monkey.svg
}

add_desktop_file() {
	unlink "$APPDIR"/python3.7.9.desktop
	cp ./infection-monkey.desktop "$APPDIR"/usr/share/applications
	ln -s "$APPDIR"/usr/share/applications/infection-monkey.desktop "$APPDIR"/infection-monkey.desktop
}

add_apprun() {
	cp ./AppRun "$APPDIR"
}

build_appimage() {
    log_message "Building AppImage"
    ARCH="x86_64" appimagetool "$APPDIR"
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


install_build_prereqs
install_appimage_tool

load_monkey_binary_config
clone_monkey_repo "$@"

setup_appdir

build_appimage

log_message "Deployment script finished."
exit 0
