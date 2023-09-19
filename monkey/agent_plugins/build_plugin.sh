#!/bin/bash

# Build plugin package
# Usage: ./build_plugin.sh [plugin_path]

ROOT="$( cd "$( dirname "$0" )" && pwd )"

#shellcheck disable=SC1091
source "$ROOT/util.sh"

if [ -z "$1" ]; then
    echo "No plugin path specified."
    exit 1
else
    PLUGIN_PATH=$(realpath "$1")
fi

set -x
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

pushd "$PLUGIN_PATH" || fail "$PLUGIN_PATH does not exist"
VENDOR_DIR=vendor
if [ -d "src/vendor-windows" ]; then
    VENDOR_DIR=vendor-linux
fi

pip install pipenv
pipenv requirements >> requirements.txt
pip install -r requirements.txt -t src/$VENDOR_DIR
rm requirements.txt

# Package everything up
pushd "$PLUGIN_PATH/src" || fail "$PLUGIN_PATH/src does not exist"

source_archive=$PLUGIN_PATH/$SOURCE_FILENAME
tar -zcf "$source_archive" --exclude __pycache__ --exclude .mypy_cache --exclude .pytest_cache --exclude .git --exclude .gitignore --exclude .DS_Store -- *

rm -rf vendor*
popd || exit 1

plugin_filename=$(get_plugin_filename "$PLUGIN_PATH") || fail "Failed to get plugin filename: $plugin_filename"
plugin_manifest_filename=$(get_plugin_manifest_filename "$PLUGIN_PATH")
tar -cf "$PLUGIN_PATH/$plugin_filename" "$plugin_manifest_filename" "$SCHEMA_FILENAME" "$SOURCE_FILENAME"
rm "$source_archive"
popd || exit 1
