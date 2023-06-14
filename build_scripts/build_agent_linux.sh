#! /bin/bash
#
SCRIPT_NAME="$(basename "$0")"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)

BRANCH="develop"
LOCAL=false
DIST_DIR="${SCRIPT_DIR}/agent-dist"

die() {
    echo "$1" >&2
    echo ""
    echo_help
    exit 1
}

echo_help() {
  echo "Builds an Infection Monkey agent for Linux"
  echo ""
  echo "Usage:"
  echo "    ${SCRIPT_NAME}"
  echo "    ${SCRIPT_NAME} --branch <BRANCH>|--local"
  echo "    ${SCRIPT_NAME} -h|--help"
  echo ""
  echo "Options:"
  echo "    --branch                   Branch to build from. Default: ${BRANCH}"
  echo "    --local                    Build from the same repository that contains this script"
}

while (( "$#" )); do
  case "$1" in
    -h|--help)
      echo_help
      exit 0
      ;;
    --branch)
      BRANCH=$2
      shift 2
      ;;
    --local)
      LOCAL=true
      shift
      ;;
    *)
      die "Error: Unsupported parameter \"$1\"."
      ;;
  esac
done

mkdir -p "$DIST_DIR"

setup_environment_commands="
set +x &&
export PYENV_ROOT=\"\${HOME}/.pyenv\" &&
command -v pyenv >/dev/null || export PATH=\"\$PYENV_ROOT/bin:\$PATH\" &&
eval \"\$(pyenv init -)\" &&
python --version &&
pip install pipenv &&
"

clone_commands="
echo \"Cloning branch ${BRANCH}...\" &&
git clone https://github.com/guardicore/monkey.git -b \"${BRANCH}\" --single-branch --depth 1 &&
cd monkey/monkey/infection_monkey &&
"

local_commands="
cd /src/monkey/infection_monkey &&
"

build_commands="
SKIP_CYTHON=1 PIP_NO_BINARY=pydantic pipenv sync &&
pipenv run bash build_linux.sh &&
echo 'Copying agent binary to \"${DIST_DIR}\"' &&
cp dist/monkey-linux-64 /dist
"

docker_commands=""
if [ "$LOCAL" = true ]; then
  echo "Building agent from local source code..."
  docker_commands="
  ${setup_environment_commands}
  ${local_commands}
  ${build_commands}
  "
else
  echo "Building agent from remote branch \"${BRANCH}\"..."
  docker_commands="
  ${setup_environment_commands}
  ${clone_commands}
  ${build_commands}
  "
fi

TAG="latest"
docker pull infectionmonkey/agent-builder:$TAG
docker run \
    --rm \
    -v "${DIST_DIR}:/dist" \
    -v "${SCRIPT_DIR}/../:/src" \
    infectionmonkey/agent-builder:$TAG \
    /bin/bash -c "${docker_commands}" | ts  '[%Y-%m-%d %H:%M:%S]'
