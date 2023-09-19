#!/bin/bash

# Usage: ./build.sh [plugin_path]

umask 077
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
GID=$(id -g)
TAG="latest"

if [ -z "$1" ]; then
    echo "No plugin path specified."
    exit 1
else
    PLUGIN_PATH=$(realpath --relative-to="$SCRIPT_DIR" "$1")
fi

#shellcheck disable=SC1091
source "$SCRIPT_DIR/util.sh"
plugin_filename=$(get_plugin_filename "$SCRIPT_DIR/$PLUGIN_PATH") || fail "Failed to get plugin filename: $plugin_filename"

DOCKER_COMMANDS="
PATH=\$HOME/.cargo/bin:\$PATH &&
cd /plugins &&
bash build_plugin.sh \"${PLUGIN_PATH}\" &&
chown ${UID}:${GID} \"/plugins/${PLUGIN_PATH}/$plugin_filename\"
"

docker pull infectionmonkey/agent-builder:$TAG
docker run \
    --rm \
    -v "$SCRIPT_DIR:/plugins" \
    infectionmonkey/agent-builder:$TAG \
    /bin/bash -c "$DOCKER_COMMANDS" | ts  '[%Y-%m-%d %H:%M:%S]'
