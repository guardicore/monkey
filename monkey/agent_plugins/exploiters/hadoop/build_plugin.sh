#!/bin/sh

# Build plugin package
# Usage: ./build_plugin.sh

ROOT="$( cd "$( dirname "$0" )" && pwd )"

#shellcheck disable=SC1091
. "$ROOT/util.sh"

set -x
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

pip install pipenv
pipenv requirements >> requirements.txt
pip install -r requirements.txt -t src/vendor
rm requirements.txt

# Package everything up
cd "$ROOT/src" || exit 1

tar -cf "$ROOT/$SOURCE_FILENAME" ./*.py vendor

rm -rf vendor
cd "$ROOT" || exit 1

plugin_filename=$(get_plugin_filename) || fail "Failed to get plugin filename: $plugin_filename"
tar -cf "$ROOT/$plugin_filename" "$MANIFEST_FILENAME" "$SCHEMA_FILENAME" "$SOURCE_FILENAME"
rm "$ROOT/$SOURCE_FILENAME"
