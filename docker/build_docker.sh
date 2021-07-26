WORKSPACE=${WORKSPACE:-$HOME}

BUILD_DIR="$PWD/monkey"

GIT=$WORKSPACE/git

DEFAULT_REPO_MONKEY_HOME=$GIT/monkey

ISLAND_PATH="$BUILD_DIR/monkey_island"
ISLAND_BINARIES_PATH="$ISLAND_PATH/cc/binaries"

MONKEY_ORIGIN_URL="https://github.com/guardicore/monkey.git"
CONFIG_URL="https://raw.githubusercontent.com/guardicore/monkey/develop/deployment_scripts/config"
NODE_SRC=https://deb.nodesource.com/setup_12.x
ISLAND_DIR_COPY_TIMEOUT=60 #Seconds

OUTPUT_NAME_TGZ="$PWD/infection_monkey_docker_$(date +%Y%m%d_%H%M%S).tgz"

exit_if_missing_argument() {
  if [ -z "$2" ] || [ "${2:0:1}" == "-" ]; then
    echo "Error: Argument for $1 is missing" >&2
    exit 1
  fi
}

echo_help() {
  echo "usage: build_appimage.sh [--help] [--agent-binary-dir <PATH>] [--branch <BRANCH>]"
  echo "                         [--monkey-repo <PATH>] [--version <MONKEY_VERSION>]"
  echo ""
  echo "Creates an AppImage package for Infection Monkey."
  echo ""
  echo "--agent-binary-dir             A directory containing the agent binaries that"
  echo "                               you'd like to include with the AppImage. If this"
  echo "                               parameter is unspecified, the latest release"
  echo "                               binaries will be downloaded from GitHub."
  echo ""
  echo "--as-root                      Throw caution to the wind and allow this script"
  echo "                               to be run as root."
  echo ""
  echo "--branch                       The git branch you'd like the AppImage to be"
  echo "                               built from. (Default: develop)"
  echo ""
  echo "--monkey-repo                  A directory containing the Infection Monkey git"
  echo "                               repository. If the directory is empty or does"
  echo "                               not exist, a new repo will be cloned from GitHub."
  echo "                               If the directory is already a valid GitHub repo,"
  echo "                               it will be used as-is and the --branch parameter"
  echo "                               will have no effect."
  echo "                               (Default: $DEFAULT_REPO_MONKEY_HOME)"
  echo ""
  echo "--version                      A version number for the AppImage package."
  echo "                               (Default: dev)"

  exit 0
}

is_root() {
  return "$(id -u)"
}

has_sudo() {
  # 0 true, 1 false
  sudo -nv > /dev/null 2>&1
  return $?
}

log_message() {
  echo -e "\n\n"
  echo -e "DOCKER IMAGE BUILDER: $1"
}

handle_error() {
  echo "Fix the errors above and rerun the script"
  exit 1
}

install_nodejs() {
  log_message "Installing nodejs"

  curl -sL $NODE_SRC | sudo -E bash -
  sudo apt-get install -y nodejs
}

install_build_prereqs() {
  sudo apt-get update
  sudo apt-get upgrade -y

  # monkey island prereqs
  sudo apt-get install -y curl libcurl4 openssl git build-essential moreutils
  install_nodejs
}

install_docker() {
    sudo apt-get install -y docker.io
}

clone_monkey_repo() {
  local repo_dir=$1
  local branch=$2

  if [[ ! -d "$repo_dir" ]]; then
    mkdir -p "$repo_dir"
  fi

  log_message "Cloning files from git"
  git clone -c core.autocrlf=false --single-branch --recurse-submodules -b "$branch" "$MONKEY_ORIGIN_URL" "$repo_dir" 2>&1 || handle_error
}

is_valid_git_repo() {
  pushd "$1" 2>/dev/null || return 1
  git status >/dev/null 2>&1
  success="$?"
  popd || exit 1

  return $success
}

setup_build_dir() {
  local agent_binary_dir=$1
  local monkey_repo=$2

  mkdir "$BUILD_DIR"

  copy_entrypoint_to_build_dir

  copy_monkey_island_to_build_dir "$monkey_repo/monkey"
  add_agent_binaries_to_build_dir "$agent_binary_dir"

  generate_ssl_cert

  build_frontend
}

copy_entrypoint_to_build_dir() {
    cp ./entrypoint.sh "$BUILD_DIR"
    chmod 755 "$BUILD_DIR/entrypoint.sh"
}
copy_monkey_island_to_build_dir() {
  local src=$1
  cp "$src"/__init__.py "$BUILD_DIR"
  cp "$src"/monkey_island.py "$BUILD_DIR"
  cp -r "$src"/common "$BUILD_DIR/"
  if ! timeout "${ISLAND_DIR_COPY_TIMEOUT}" cp -r "$src"/monkey_island "$BUILD_DIR/"; then
    log_message "Copying island files takes too long. Maybe you're copying a dev folder instead of a fresh repository?"
    exit 1
  fi
  cp ./server_config.json "$BUILD_DIR"/monkey_island/cc/
}

add_agent_binaries_to_build_dir() {
  local agent_binary_dir=$1

  if [ -z "$agent_binary_dir" ]; then
    download_monkey_agent_binaries
  else
    copy_agent_binaries_to_appdir "$agent_binary_dir"
  fi

  make_linux_binaries_executable
}

download_monkey_agent_binaries() {
  log_message "Downloading monkey agent binaries to ${ISLAND_BINARIES_PATH}"

  load_monkey_binary_config

  mkdir -p "${ISLAND_BINARIES_PATH}" || handle_error
  curl -L -o "${ISLAND_BINARIES_PATH}/${LINUX_32_BINARY_NAME}" "${LINUX_32_BINARY_URL}"
  curl -L -o "${ISLAND_BINARIES_PATH}/${LINUX_64_BINARY_NAME}" "${LINUX_64_BINARY_URL}"
  curl -L -o "${ISLAND_BINARIES_PATH}/${WINDOWS_32_BINARY_NAME}" "${WINDOWS_32_BINARY_URL}"
  curl -L -o "${ISLAND_BINARIES_PATH}/${WINDOWS_64_BINARY_NAME}" "${WINDOWS_64_BINARY_URL}"
}

load_monkey_binary_config() {
  tmpfile=$(mktemp)

  log_message "Downloading prebuilt binary configuration"
  curl -L -s -o "$tmpfile" "$CONFIG_URL"

  log_message "Loading configuration"
  source "$tmpfile"
}

copy_agent_binaries_to_appdir() {
  cp "$1"/* "$ISLAND_BINARIES_PATH/"
}

make_linux_binaries_executable() {
  chmod a+x "$ISLAND_BINARIES_PATH"/monkey-linux-*
}

generate_ssl_cert() {
  log_message "Generating certificate"

  chmod u+x "${ISLAND_PATH}"/linux/create_certificate.sh
  "${ISLAND_PATH}"/linux/create_certificate.sh "${ISLAND_PATH}"/cc
}

build_frontend() {
  pushd "$ISLAND_PATH/cc/ui" || handle_error

  log_message "Generating front end"
  npm ci
  npm run dist

  popd || handle_error

  remove_node_modules
}

remove_node_modules() {
  # Node has served its purpose. We don't need to deliver the node modules with
  # the AppImage.
  rm -rf "$ISLAND_PATH"/cc/ui/node_modules
}

build_docker_image() {
  local version=$1

  docker_image_name=guardicore/monkey-island:$version
  tar_name=./dk.monkeyisland.$version.tar

  build_docker_image_tar "$docker_image_name" "$tar_name"
  build_docker_image_tgz "$tar_name" "$version"
}

build_docker_image_tar() {
  sudo docker build . -t "$1"
  sudo docker save "$1" > "$2"
}

build_docker_image_tgz() {
  mkdir tgz
  cp "$1" ./tgz
  cp ./DOCKER_README.md ./tgz/README.md
  tar -C ./tgz -cvf "$OUTPUT_NAME_TGZ" --gzip .
}

agent_binary_dir=""
as_root=false
branch="develop"
monkey_repo="$DEFAULT_REPO_MONKEY_HOME"
monkey_version="dev"


while (( "$#" )); do
  case "$1" in
    --agent-binary-dir)
      exit_if_missing_argument "$1" "$2"

      agent_binary_dir=$2
      shift 2
      ;;
    --as-root)
      as_root=true
      shift
      ;;
    --branch)
      exit_if_missing_argument "$1" "$2"

      branch=$2
      shift 2
      ;;
    -h|--help)
      echo_help
      ;;
    --monkey-repo)
      exit_if_missing_argument "$1" "$2"

      monkey_repo=$2
      shift 2
      ;;
    --version)
      exit_if_missing_argument "$1" "$2"

      monkey_version=$2
      shift 2
      ;;
    *)
      echo "Error: Unsupported parameter $1" >&2
      exit 1
      ;;
  esac
done

log_message "Building Monkey Island Docker image."

if ! $as_root && is_root; then
  log_message "Please don't run this script as root"
  exit 1
fi

if ! has_sudo; then
  log_message "You need root permissions for some of this script operations. \
Run \`sudo -v\`, enter your password, and then re-run this script."
  exit 1
fi

install_build_prereqs
install_docker

if ! is_valid_git_repo "$monkey_repo"; then
  clone_monkey_repo "$monkey_repo" "$branch"
fi

setup_build_dir "$agent_binary_dir" "$monkey_repo"
build_docker_image "$monkey_version"

log_message "Docker build script finished."
exit 0
