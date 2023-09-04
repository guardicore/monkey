#!/bin/bash

# Changes: python version
LINUXDEPLOY_URL="https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage"
PYTHON_VERSION="3.11.5"
PYTHON_APPIMAGE_URL="https://github.com/niess/python-appimage/releases/download/python3.11/python${PYTHON_VERSION}-cp311-cp311-manylinux2014_x86_64.AppImage"
APPIMAGE_DIR=$(realpath "$(dirname "${BASH_SOURCE[0]}")")
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
  local is_release_build=$4

  pushd "$APPIMAGE_DIR" || handle_error

  setup_python_appdir

  mkdir -p "$BUILD_DIR"

  copy_monkey_island_to_build_dir "$monkey_repo/monkey" "$BUILD_DIR"
  copy_server_config_to_build_dir
  copy_infection_monkey_service_to_build_dir
  modify_deployment "$deployment_type" "$BUILD_DIR"
  add_agent_binaries_to_build_dir "$agent_binary_dir" "$BUILD_DIR"

  install_monkey_island_python_dependencies
  install_mongodb

  generate_ssl_cert "$BUILD_DIR"
  build_frontend "$BUILD_DIR" "$is_release_build"

  remove_python_appdir_artifacts

  popd || handle_error
}

setup_python_appdir() {
  PYTHON_APPIMAGE="python${PYTHON_VERSION}_x86_64.AppImage"

  log_message "downloading Python Appimage"
  curl -L -o "$PYTHON_APPIMAGE" "$PYTHON_APPIMAGE_URL"

  chmod u+x "$PYTHON_APPIMAGE"

  "./$PYTHON_APPIMAGE" --appimage-extract
  rm "$PYTHON_APPIMAGE"
}

copy_infection_monkey_service_to_build_dir() {
  cp "$APPIMAGE_DIR"/install-infection-monkey-service.sh "$APPDIR"
}

copy_server_config_to_build_dir() {
  cp "$APPIMAGE_DIR"/server_config.json.standard "$BUILD_DIR"/monkey_island/cc/server_config.json
}

install_monkey_island_python_dependencies() {
  log_message "Installing island requirements"

  log_message "Installing pipenv"
  "$APPDIR"/AppRun -m pip install pipenv || handle_error
  export CI=1

  log_message "Installing dependencies"
  pushd "$BUILD_DIR/monkey_island" || handle_error
  "$APPDIR"/AppRun -m pipenv --python "$APPDIR/AppRun" requirements > requirements.txt || handle_error
  "$APPDIR"/AppRun -m pip install -r requirements.txt || handle_error
  rm requirements.txt
  popd || handle_error

  log_message "Uninstalling pipenv (build dependency only)"
  "$APPDIR"/AppRun -m pip uninstall --yes pipenv virtualenv || handle_error
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

  pushd "$APPIMAGE_DIR" || handle_error
  ARCH="x86_64" linuxdeploy \
      --appdir "$APPIMAGE_DIR/squashfs-root" \
      --icon-file "$ICON_PATH" \
      --desktop-file "$APPIMAGE_DIR/infection-monkey.desktop" \
      --custom-apprun  "$APPIMAGE_DIR/AppRun" \
      --deploy-deps-only="$MONGO_PATH/bin/mongod"\
      --output appimage

  dst_name="InfectionMonkey-$version.AppImage"
  move_package_to_dist_dir "$dist_dir" "$dst_name"

  popd || handle_error
}

move_package_to_dist_dir() {
    mv Infection*Monkey*.AppImage "$1/$2"
}

cleanup() {
  echo "Cleaning appimage build dirs"

  rm -rf "$APPIMAGE_DIR/squashfs-root"
}
