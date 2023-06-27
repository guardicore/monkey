#!/bin/sh

export SCHEMA_FILENAME=config-schema.json
export SOURCE_FILENAME=source.tar


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
    _plugin_path=${1:-"."}

    manifest_filename=$(get_plugin_manifest_filename)

    _name=$(get_value_from_key "${_plugin_path}/${manifest_filename}" name) || fail "Failed to get plugin name"
    _name=$(ltrim "$_name")
    _type=$(get_value_from_key "${_plugin_path}/${manifest_filename}" plugin_type) || fail "Failed to get plugin type"
    _type=$(ltrim "$(lower "$_type")")
    echo "${_name}-${_type}.tar"
}

get_plugin_manifest_filename() {
    manifest_filename=manifest.yaml
    _plugin_path=${1:-"."}

    if [ ! -f "${_plugin_path}/${manifest_filename}" ]; then
        manifest_filename=manifest.yml
    fi

    echo $manifest_filename
}
