#!/bin/sh

# Build the plugin package
# Usage: ./build.sh

MANIFEST_FILENAME=manifest.yaml
SCHEMA_FILENAME=config-schema.json
VENDOR_DIRECTORY_NAME_LINUX="vendor-linux"
VENDOR_DIRECTORY_NAME_WINDOWS="vendor-windows"
ROOT="$( cd "$( dirname "$0" )" && pwd )"

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


# Package everything up
cd "$ROOT/src" || exit 1
tar -cf "$ROOT/source.tar" plugin.py $VENDOR_DIRECTORY_NAME_LINUX $VENDOR_DIRECTORY_NAME_WINDOWS
cd "$ROOT" || exit 1


# xargs strips leading whitespace
name=$(get_value_from_key $MANIFEST_FILENAME name | xargs)
type=$(lower "$(get_value_from_key $MANIFEST_FILENAME plugin_type | xargs)")

plugin_filename="${name}-${type}.tar"
tar -cf "$ROOT/$plugin_filename" $MANIFEST_FILENAME $SCHEMA_FILENAME source.tar
rm "$ROOT/source.tar"
