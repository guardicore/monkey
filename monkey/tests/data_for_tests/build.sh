#!/bin/sh

# Build the plugin package
# Usage: ./build.sh <plugin-directory> <version>

DEFAULT_DEPENDENCY_VERSION=1.0.0
MANIFEST_FILENAME=manifest.yaml
SCHEMA_FILENAME=config-schema.json
DEPENDENCY_FILE="src/vendor/mock_dependency.py"
PLUGIN_DIRECTORY_PATH=$(realpath "$1")
ROOT="$( cd $PLUGIN_DIRECTORY_PATH && pwd )"

get_value_from_key() {
    _file="$1"
    _key="$2"
    _value=$(grep -Po "(?<=^${_key}:).*" "$_file")
    if [ -z "$_value" ]; then
        echo "Error: Plugin '$_key' not found."
        exit 1
    else
        echo "$_value"
    fi
}

lower() {
    echo "$1" | tr "[:upper:]" "[:lower:]"
}

# Generate the dependency
version=$DEFAULT_DEPENDENCY_VERSION
if [ "$2" ]; then
    version=$2
fi
echo "__version__ = \"${version}\"" > "$ROOT/$DEPENDENCY_FILE"


# Package everything up
cd "$ROOT/src" || exit 1
tar -czf $ROOT/source.tar.gz plugin.py vendor/
cd "$ROOT" || exit 1


# xargs strips leading whitespace
name=$(get_value_from_key $MANIFEST_FILENAME name | xargs)
type=$(lower "$(get_value_from_key $MANIFEST_FILENAME plugin_type | xargs)")

plugin_filename="${name}-${type}.tar"
tar -cf "$ROOT/$plugin_filename" $MANIFEST_FILENAME $SCHEMA_FILENAME source.tar.gz
rm "$ROOT/source.tar.gz"
