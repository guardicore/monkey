#!/bin/bash

LINUXDEPLOY_URL="https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage"
PYTHON_VERSION="3.7.12"
PYTHON_APPIMAGE_URL="https://github.com/niess/python-appimage/releases/download/python3.7/python${PYTHON_VERSION}-cp37-cp37m-manylinux1_x86_64.AppImage"
APPIMAGE_DIR="$(realpath $(dirname $BASH_SOURCE[0]))"
APPDIR="$APPIMAGE_DIR/squashfs-root"
BUILD_DIR="$APPDIR/usr/src"

ICON_PATH="$BUILD_DIR/monkey_island/cc/ui/src/images/monkey-icon.svg"
MONGO_PATH="$BUILD_DIR/monkey_island/bin/mongodb"

source "$APPIMAGE_DIR/../common.sh"

install_package_specific_build_prereqs() {
  log_message "Installing linuxdeploy"
  WORKSPACE_BIN_DIR="$1/bin"
  LINUXDEPLOY_BIN="$WORKSPACE_BIN_DIR/linuxdeploy"

  mkdir -p "$WORKSPACE_BIN_DIR"
  curl -L -o "$LINUXDEPLOY_BIN" "$LINUXDEPLOY_URL"
  chmod u+x "$LINUXDEPLOY_BIN"

  PATH=$PATH:$WORKSPACE_BIN_DIR
}

setup_build_dir() {
  local agent_binary_dir=$1
  local monkey_repo=$2
  local deployment_type=$3

  pushd $APPIMAGE_DIR

  setup_python_37_appdir

  mkdir -p "$BUILD_DIR"

  copy_monkey_island_to_build_dir "$monkey_repo/monkey" "$BUILD_DIR"
  copy_server_config_to_build_dir
  modify_deployment "$deployment_type" "$BUILD_DIR"
  add_agent_binaries_to_build_dir "$agent_binary_dir" "$BUILD_DIR"

  install_monkey_island_python_dependencies
  install_mongodb

  generate_ssl_cert "$BUILD_DIR"
  build_frontend "$BUILD_DIR"

  remove_python_appdir_artifacts

  popd
}

setup_python_37_appdir() {
  PYTHON_APPIMAGE="python${PYTHON_VERSION}_x86_64.AppImage"

  log_message "downloading Python3.7 Appimage"
  curl -L -o "$PYTHON_APPIMAGE" "$PYTHON_APPIMAGE_URL"

  chmod u+x "$PYTHON_APPIMAGE"

  "./$PYTHON_APPIMAGE" --appimage-extract
  rm "$PYTHON_APPIMAGE"
}

copy_server_config_to_build_dir() {
    cp "$APPIMAGE_DIR"/server_config.json.standard "$BUILD_DIR"/monkey_island/cc/server_config.json
}

install_monkey_island_python_dependencies() {
  log_message "Installing island requirements"

  log_message "Installing pipenv"
  "$APPDIR"/AppRun -m pip install pipenv || handle_error

  requirements_island="$BUILD_DIR/monkey_island/requirements.txt"
  generate_requirements_from_pipenv_lock "$requirements_island"

  log_message "Installing island python requirements"
  "$APPDIR"/AppRun -m pip install -r "${requirements_island}"  --ignore-installed || handle_error
}

generate_requirements_from_pipenv_lock () {
  local requirements_island=$1

  log_message "Generating a requirements.txt file with 'pipenv lock -r'"
  pushd "$BUILD_DIR/monkey_island"
  "$APPDIR"/AppRun -m pipenv --python "$APPDIR/AppRun" lock -r > "$requirements_island" || handle_error
  popd
}


install_mongodb() {
  log_message "Installing MongoDB"

  mkdir -p "$MONGO_PATH"
  "$BUILD_DIR/monkey_island/linux/install_mongo.sh" "${MONGO_PATH}" || handle_error
}

remove_python_appdir_artifacts() {
  rm "$APPDIR"/python.png
  rm "$APPDIR"/python*.desktop
  rm "$APPDIR"/AppRun
}

build_package() {
  local version=$1
  local dist_dir=$2

  log_message "Building AppImage"
  set_version "$version"

  pushd "$APPIMAGE_DIR"
  ARCH="x86_64" linuxdeploy \
      --appdir "$APPIMAGE_DIR/squashfs-root" \
      --icon-file "$ICON_PATH" \
      --desktop-file "$APPIMAGE_DIR/infection-monkey.desktop" \
      --custom-apprun  "$APPIMAGE_DIR/AppRun" \
      --deploy-deps-only="$MONGO_PATH/bin/mongod"\
      --output appimage

  move_package_to_dist_dir $dist_dir

  popd
}

set_version() {
  # The linuxdeploy and appimage-builder tools will use the commit hash of the
  # repo to name the AppImage, which is preferable to using "dev". If the
  # version was specified in a command-line argument (i.e. not "dev"), then
  # setting the VERSION environment variable will change this behavior.
  if [ $1 != "dev" ]; then
         export VERSION=$1
  fi
}

move_package_to_dist_dir() {
    mv Infection_Monkey*.AppImage "$1/"
}
