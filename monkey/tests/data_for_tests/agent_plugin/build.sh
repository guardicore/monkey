#!/bin/sh

# Build the plugin package
# Usage: ./build.sh <version>

DEFAULT_DEPENDENCY_VERSION=1.0.0
MANIFEST_FILENAME=plugin.yaml
SCHEMA_FILENAME=config-schema.json
DEPENDENCY_FILE="src/vendor/mock_dependency.py"
ROOT="$( cd "$( dirname "$0" )" && pwd )"
OUTDIR="$ROOT"

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
if [ "$1" ]; then
    version=$1
fi
echo "__version__ = \"${version}\"" > "$ROOT/$DEPENDENCY_FILE"

tempdir=$(mktemp -d)
cp "$ROOT/$MANIFEST_FILENAME" "$ROOT/$SCHEMA_FILENAME" "$tempdir/"

# Package everything up
cd "$ROOT/src" || exit 1
tar -cf "$tempdir/plugin.tar" plugin.py vendor

cd "$tempdir" || exit 1
name=$(get_value_from_key $MANIFEST_FILENAME name)
type=$(lower "$(get_value_from_key $MANIFEST_FILENAME plugin_type)")
plugin_filename="${name}-${type}.tar"
mkdir -p "$OUTDIR"
tar -cf "$OUTDIR/$plugin_filename" $MANIFEST_FILENAME $SCHEMA_FILENAME plugin.tar
