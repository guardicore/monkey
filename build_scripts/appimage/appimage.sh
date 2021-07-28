#!/bin/bash

APP_TOOL_URL=https://github.com/AppImage/AppImageKit/releases/download/12/appimagetool-x86_64.AppImage
PYTHON_VERSION="3.7.11"
PYTHON_APPIMAGE_URL="https://github.com/niess/python-appimage/releases/download/python3.7/python${PYTHON_VERSION}-cp37-cp37m-manylinux1_x86_64.AppImage"
APPIMAGE_DIR="$(realpath $(dirname $BASH_SOURCE[0]))"

source "$APPIMAGE_DIR/../common.sh"

install_package_specific_build_prereqs() {
  log_message "Installing appimagetool"
  WORKSPACE_BIN_DIR="$1/bin"
  APP_TOOL_BIN="$WORKSPACE_BIN_DIR/appimagetool"

  mkdir -p "$WORKSPACE_BIN_DIR"
  curl -L -o "$APP_TOOL_BIN" "$APP_TOOL_URL"
  chmod u+x "$APP_TOOL_BIN"

  PATH=$PATH:$WORKSPACE_BIN_DIR
}

setup_build_dir() {
  local agent_binary_dir=$1
  local monkey_repo=$2
  local appdir=$APPIMAGE_DIR/squashfs-root
  local build_dir="$appdir/usr/src"

  pushd $APPIMAGE_DIR

  setup_python_37_appdir $build_dir

  mkdir -p "$build_dir"

  copy_monkey_island_to_build_dir "$monkey_repo/monkey" $build_dir
  copy_server_config_to_build_dir $build_dir
  add_agent_binaries_to_build_dir "$agent_binary_dir" "$build_dir"

  install_monkey_island_python_dependencies "$appdir" "$build_dir"
  install_mongodb "$build_dir"

  generate_ssl_cert "$build_dir"
  build_frontend "$build_dir"

  add_monkey_icon "$appdir" "$monkey_repo"
  add_desktop_file "$appdir"
  add_apprun "$appdir"

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
    cp "$APPIMAGE_DIR"/server_config.json.standard "$1"/monkey_island/cc/server_config.json
}

install_monkey_island_python_dependencies() {
  local appdir=$1
  local build_dir=$2
  log_message "Installing island requirements"

  log_message "Installing pipenv"
  "$appdir"/AppRun -m pip install pipenv || handle_error

  requirements_island="$build_dir/monkey_island/requirements.txt"
  generate_requirements_from_pipenv_lock "$appdir" "$build_dir" "$requirements_island"

  log_message "Installing island python requirements"
  "$appdir"/AppRun -m pip install -r "${requirements_island}"  --ignore-installed || handle_error
}

generate_requirements_from_pipenv_lock () {
  local appdir=$1
  local build_dir=$2
  local requirements_island=$3

  log_message "Generating a requirements.txt file with 'pipenv lock -r'"
  pushd "$build_dir/monkey_island"
  "$appdir"/AppRun -m pipenv --python "$appdir/AppRun" lock -r > "$requirements_island" || handle_error
  popd
}

install_mongodb() {
  local build_dir=$1
  local mongo_path="$build_dir/monkey_island/bin/mongodb"
  log_message "Installing MongoDB"

  mkdir -p "$mongo_path"
  "$build_dir/monkey_island/linux/install_mongo.sh" "${mongo_path}" || handle_error
}

add_monkey_icon() {
  local appdir=$1
  local monkey_repo=$2

  unlink "$appdir"/python.png
  mkdir -p "$appdir"/usr/share/icons
  cp "$monkey_repo"/monkey/monkey_island/cc/ui/src/images/monkey-icon.svg "$appdir"/usr/share/icons/infection-monkey.svg
  ln -s "$appdir"/usr/share/icons/infection-monkey.svg "$appdir"/infection-monkey.svg
}

add_desktop_file() {
  local appdir=$1

  unlink "$appdir"/python*.desktop
  cp ./infection-monkey.desktop "$appdir"/usr/share/applications
  ln -s "$appdir"/usr/share/applications/infection-monkey.desktop "$appdir"/infection-monkey.desktop
}

add_apprun() {
  cp ./AppRun "$1"
}

build_package() {
  local version=$1
  local dist_dir=$2
  log_message "Building AppImage"
  pushd "$APPIMAGE_DIR"

  ARCH="x86_64" appimagetool "$APPIMAGE_DIR/squashfs-root"
  apply_version_to_appimage "$version"

  move_package_to_dist_dir $dist_dir

  popd
}

apply_version_to_appimage() {
  log_message "Renaming Infection_Monkey-x86_64.AppImage -> Infection_Monkey-$1-x86_64.AppImage"
  mv "Infection_Monkey-x86_64.AppImage" "Infection_Monkey-$1-x86_64.AppImage"
}

move_package_to_dist_dir() {
    mv Infection_Monkey*.AppImage "$1/"
}
