WORKSPACE=${WORKSPACE:-$HOME}
DEFAULT_REPO_MONKEY_HOME=$WORKSPACE/git/monkey
MONKEY_ORIGIN_URL="https://github.com/guardicore/monkey.git"
NODE_SRC=https://nodejs.org/dist/v20.7.0/node-v20.7.0-linux-x64.tar.xz
BUILD_SCRIPTS_DIR="$(realpath $(dirname $BASH_SOURCE[0]))"
DIST_DIR="$BUILD_SCRIPTS_DIR/dist"

log_message() {
  echo -e "\n\n"
  echo -e "MONKEY ISLAND BUILDER: $1"
}

exit_if_missing_argument() {
  if [ -z "$2" ] || [ "${2:0:1}" == "-" ]; then
    echo "Error: Argument for $1 is missing" >&2
    exit 1
  fi
}

echo_help() {
  echo "usage: build_package.sh [--help] [--agent-binary-dir <PATH>] [--branch <BRANCH>]"
  echo "                         [--monkey-repo <PATH>] [--version <MONKEY_VERSION>]"
  echo "                         [--deployment <DEPLOYMENT_TYPE>]"
  echo ""
  echo "Creates a package for Infection Monkey."
  echo ""
  echo "--agent-binary-dir             A directory containing the agent binaries that"
  echo "                               you'd like to include with the package. If this"
  echo "                               parameter is unspecified, the latest release"
  echo "                               binaries will be downloaded from GitHub."
  echo ""
  echo "--as-root                      Throw caution to the wind and allow this script"
  echo "                               to be run as root."
  echo ""
  echo "--branch                       The git branch you'd like the package to be"
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
  echo "--version                      A version number for the package."
  echo ""
  echo "--deployment                   A deployment type for the package."
  echo "                               (Default: develop)"
  echo ""
  echo "--package                      Which package to build (\"appimage\" or \"docker.\")"

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

handle_error() {
  echo "Fix the errors above and rerun the script"
  exit 1
}

install_nodejs() {
  log_message "Installing nodejs"

  dest_path=/usr/local/lib/nodejs
  sudo mkdir -p $dest_path
  curl -sL $NODE_SRC | sudo sudo tar xJf - -C $dest_path -
  sudo ln -s "$dest_path/node-$VERSION-$DISTRO/bin/node" /usr/bin/node
  sudo ln -s "$dest_path/node-$VERSION-$DISTRO/bin/npm" /usr/bin/npm
  sudo ln -s "$dest_path/node-$VERSION-$DISTRO/bin/npx" /usr/bin/npx
}

is_valid_git_repo() {
  pushd "$1" 2>/dev/null || return 1
  git status >/dev/null 2>&1
  success="$?"
  popd || exit 1

  return $success
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

install_build_prereqs() {
  sudo apt-get update
  sudo apt-get upgrade -y -o Dpkg::Options::="--force-confold"

  # monkey island prereqs
  sudo apt-get install -y curl libcurl4 openssl git build-essential moreutils
  install_nodejs
}

format_version() {
  local unformatted_version=$1
  local commit_id=$2

  if [ -n "$unformatted_version" ]; then
      echo "v$monkey_version"
  else
      echo "$commit_id"
  fi
}

agent_binary_dir=""
as_root=false
branch="develop"
monkey_repo="$DEFAULT_REPO_MONKEY_HOME"
monkey_version=""
package=""
deployment_type=""

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
    --deployment)
      exit_if_missing_argument "$1" "$2"

      deployment_type=$2
      shift 2
      ;;
    --package)
      exit_if_missing_argument "$1" "$2"

      package=$2
      shift 2
      ;;
    *)
      echo "Error: Unsupported parameter $1" >&2
      exit 1
      ;;
  esac
done

if ! [[ $package =~ ^(appimage|docker)$ ]]; then
    log_message "Invalid package: $package."
    exit 1
fi

if ! $as_root && is_root; then
  log_message "Please don't run this script as root"
  exit 1
fi

if ! has_sudo; then
  log_message "You need root permissions for some of this script operations. \
Run \`sudo -v\`, enter your password, and then re-run this script."
  exit 1
fi

log_message "Building Monkey Island: $package"

source "./$package/$package.sh"

if ! is_valid_git_repo "$monkey_repo"; then
  clone_monkey_repo "$monkey_repo" "$branch"
fi

if [ ! -d "$DIST_DIR" ]; then
    mkdir "$DIST_DIR"
fi

install_build_prereqs
install_package_specific_build_prereqs "$WORKSPACE"

commit_id=$(get_commit_id "$monkey_repo")

is_release_build=false
# Monkey version is empty on release build
if [ ! -z "$monkey_version" ]; then
    is_release_build=true
    echo -n "" > "$monkey_repo/monkey/common/BUILD"
else
    echo $commit_id > "$monkey_repo/monkey/common/BUILD"
fi

setup_build_dir "$agent_binary_dir" "$monkey_repo" "$deployment_type" "$is_release_build"

monkey_version=$(format_version "$monkey_version" "$commit_id")

build_package "$monkey_version" "$DIST_DIR"

cleanup "$monkey_version"

log_message "Finished building package: $package"
exit 0
