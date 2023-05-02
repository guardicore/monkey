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
pip install pipenv
pipenv requirements >> requirements.txt
pip install -r requirements.txt -t src/vendor
rm requirements.txt

# Package everything up
pushd "$PLUGIN_PATH/src" || fail "$PLUGIN_PATH/src does not exist"

source_archive=$PLUGIN_PATH/$SOURCE_FILENAME
tar -cf "$source_archive" --exclude __pycache__ --exclude .mypy_cache --exclude .pytest_cache --exclude .git --exclude .gitignore --exclude .DS_Store -- *

rm -rf vendor
popd || exit 1

plugin_filename=$(get_plugin_filename) || fail "Failed to get plugin filename: $plugin_filename"
tar -cf "$PLUGIN_PATH/$plugin_filename" "$MANIFEST_FILENAME" "$SCHEMA_FILENAME" "$SOURCE_FILENAME"
rm "$source_archive"
popd || exit 1
