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

# `monkey-types` and `monkeyevents` are required for the script generating `config-schema.json`.
# TODO: When plugins are in their own repositories, this should be handled by
# activating the plugin's virtualenv.
pip install monkey-types
pip install monkeyevents

# Package everything up
pushd "$PLUGIN_PATH/src" || fail "$PLUGIN_PATH/src does not exist"

source_archive=$PLUGIN_PATH/$SOURCE_FILENAME
plugin_manifest_filename=$(get_plugin_manifest_filename "$PLUGIN_PATH")

plugin_name=$(get_plugin_name "${PLUGIN_PATH}/${plugin_manifest_filename}")

plugin_name_lowercase=$(lower "$plugin_name")
plugin_options_filename="${plugin_name_lowercase}_options"
plugin_options_filepath="${PLUGIN_PATH}/src/${plugin_options_filename}.py"
plugin_options_model_name="${plugin_name}Options"

python3.11 << EOF

import json
from pathlib import Path

def construct_config_schema():
  config_schema = {"type": "object"}
  print("Generating config-schema.json from ${plugin_options_filepath}.")
  if Path("${plugin_options_filepath}").exists():
    from $plugin_options_filename import $plugin_options_model_name
    config_schema = {"properties": $plugin_options_model_name.model_json_schema()["properties"]}

  with open("${PLUGIN_PATH}/${SCHEMA_FILENAME}", "w") as f:
    f.write(json.dumps(config_schema))

if Path("${PLUGIN_PATH}/${SCHEMA_FILENAME}").exists():
  print("\033[0m\033[91mSkipping generating config-schema. Reason: config_schema.json already exists \033[0m")
  exit(1)
else:
  construct_config_schema()
  exit(0)

EOF

config_schema_generated=$?

tar -zcf "$source_archive" --exclude __pycache__ --exclude .mypy_cache --exclude .pytest_cache --exclude .git --exclude .gitignore --exclude .DS_Store -- *

rm -rf vendor*
popd || exit 1

plugin_filename=$(get_plugin_filename "$PLUGIN_PATH") || fail "Failed to get plugin filename: $plugin_filename"
tar -cf "$PLUGIN_PATH/$plugin_filename" "$plugin_manifest_filename" "$SCHEMA_FILENAME" "$SOURCE_FILENAME"
rm "$source_archive"
if [ "$config_schema_generated" -eq 0  ]; then
    echo -e "\033[0;33mRemoving generated $SCHEMA_FILENAME.\033[0m"
    rm "$PLUGIN_PATH/$SCHEMA_FILENAME"
fi
popd || exit 1
