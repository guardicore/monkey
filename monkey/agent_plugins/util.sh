#!/bin/sh

plugin_path=${1:-"."}

export SCHEMA_FILENAME=config-schema.json
export SOURCE_FILENAME=source.tar
export MANIFEST_FILENAME=manifest.yaml
# if "manifest.yaml" doesn't exist, assume the file is called "manifest.yml"
# the script will fail if that doesn't exist either
if [ ! -f "${plugin_path}/$MANIFEST_FILENAME" ]; then
    export MANIFEST_FILENAME=manifest.yml
fi

fail() {
    echo "$1"
    exit 1
}

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

ltrim() {
    # xargs removes leading whitespace
    echo "$1" | xargs
}

lower() {
    echo "$1" | tr "[:upper:]" "[:lower:]"
}

get_plugin_filename() {
    _name=$(get_value_from_key "${plugin_path}/$MANIFEST_FILENAME" name) || fail "Failed to get plugin name"
    _name=$(ltrim "$_name")
    _type=$(get_value_from_key "${plugin_path}/$MANIFEST_FILENAME" plugin_type) || fail "Failed to get plugin type"
    _type=$(ltrim "$(lower "$_type")")
    echo "${_name}-${_type}.tar"
}
