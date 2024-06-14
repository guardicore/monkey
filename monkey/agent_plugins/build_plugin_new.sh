#!/bin/bash

# TODO: See about translating this to a Python script
ROOT="$( cd "$( dirname "$0" )" && pwd )"

if [ -z "$1" ]; then
    echo "No plugin path specified."
    exit 1
else
    PLUGIN_PATH=$(realpath "$1")
fi

#shellcheck disable=SC1091
source "$ROOT/util.sh"
GID=$(id -g)
LINUX_IMAGE="infectionmonkey/agent-builder:latest"
WINDOWS_IMAGE="plugin-builder:latest"

# Build plugin:
# - Dependencies
#   - python: to run the script
#   - pipenv | poetry: to output requirements.txt
#   - pyyaml: to parse the manifest file
#   - monkey-types: to parse the manifest file, generate config schema
#   - monkeyevents: to generate config schema
#   - pydantic (^2.5.0): for model file
# 1. Determine which platforms the plugin supports
#   - get_supported_platforms.py
# 2. Read build config, to see if common or separate vendor directories should be used
#   - Read the build config file: build.yaml
#     - platform_dependencies: common | separate | autodetect (default)
# 3. Build vendor directories
#   - Create a build directory: /tmp/build-<plugin_type>-<plugin_name>-<random_string>
#   - Copy plugin source to build directory
#   - Write build logs:
#     - build.log: top-level log file -- what is printed to the command line
#     - requirements.txt: the requirements file for the plugin
#     - autodetect-<platform>.log: log file containing the output of the autodetect script for a platform
#     - autodetect-<platform>-deps.json: the dependencies for a platform
#     -
# 4. Build plugin

get_plugin_supported_operating_systems() {
    _manifest_file_path="$1"

    python3.11 $ROOT/scripts/get_supported_platforms.py "$_manifest_file_path"
}

check_if_common_vendor_dir_possible() {
    _build_dir="$1"
    (cd $_build_dir && pipenv requirements > requirements.txt)

    DOCKER_COMMANDS_LINUX="
    export PYENV_ROOT=\"\$HOME/.pyenv\"
    command -v pyenv >/dev/null || export PATH=\"\$PYENV_ROOT/bin:\$PATH\"
    eval \"\$(pyenv init -)\"
    cd /plugin &&
    pip install --dry-run -r requirements.txt --report linux.json &&
    chown ${UID}:${GID} /plugin/linux.json
    "

    DOCKER_COMMANDS_WINDOWS="
    cd /plugin &&
    wine pip install --dry-run -r requirements.txt --report windows.json
    chown ${UID}:${GID} /plugin/windows.json
    "

    # TODO: Redirect output to a log file
    docker run \
        --rm \
        -v "$_build_dir:/plugin" \
        $LINUX_IMAGE \
        /bin/bash -c "$DOCKER_COMMANDS_LINUX" | ts '[%Y-%m-%d %H:%M:%S]' \
        1>&2

    docker run \
        --rm \
        -v "$_build_dir:/plugin" \
        $WINDOWS_IMAGE \
        /bin/bash -c "$DOCKER_COMMANDS_WINDOWS" | ts '[%Y-%m-%d %H:%M:%S]' \
        1>&2

    # Parse and compare the linux.json and windows.json files to
    # determine if a common vendor directory can be built
    linux_file=$(realpath "$_build_dir/linux.json")
    windows_file=$(realpath "$_build_dir/windows.json")

    python3.11 $ROOT/scripts/compare_package_lists.py $linux_file $windows_file

    # Keep the return code, but do some cleanup
    rc=$?
    rm -f "$_build_dir/requirements.txt" $linux_file $windows_file
    $(exit $rc)
}

build_linux_vendor_dir() {
    _build_dir="$1"
    echo "Building vendor dir for Linux"
    DOCKER_COMMANDS_LINUX="
    export PYENV_ROOT=\"\$HOME/.pyenv\"
    command -v pyenv >/dev/null || export PATH=\"\$PYENV_ROOT/bin:\$PATH\"
    eval \"\$(pyenv init -)\"
    cd /plugin &&
    pip install -r requirements.txt -t src/vendor-linux &&
    chown ${UID}:${GID} -R /plugin/src/vendor-linux
    "
    docker run \
        --rm \
        -v "$_build_dir:/plugin" \
        $LINUX_IMAGE \
        /bin/bash -c "$DOCKER_COMMANDS_LINUX" | ts '[%Y-%m-%d %H:%M:%S]' \
        1>&2
}

build_windows_vendor_dir() {
    _build_dir="$1"
    echo "Building vendor dir for Windows"
    DOCKER_COMMANDS_WINDOWS="
    cd /plugin &&
    wine pip install -r requirements.txt -t src/vendor-windows &&
    chown ${UID}:${GID} -R /plugin/src/vendor-windows
    "
    docker run \
        --rm \
        -v "$_build_dir:/plugin" \
        $WINDOWS_IMAGE \
        /bin/bash -c "$DOCKER_COMMANDS_WINDOWS" | ts '[%Y-%m-%d %H:%M:%S]' \
        1>&2
}

build_common_vendor_dir() {
    _build_dir="$1"
    echo "Building common vendor dir"
    DOCKER_COMMANDS_LINUX="
    export PYENV_ROOT=\"\$HOME/.pyenv\"
    command -v pyenv >/dev/null || export PATH=\"\$PYENV_ROOT/bin:\$PATH\"
    eval \"\$(pyenv init -)\"
    cd /plugin &&
    pip install -r requirements.txt -t src/vendor &&
    chown ${UID}:${GID} -R /plugin/src/vendor
    "
    docker run \
        --rm \
        -v "$_build_dir:/plugin:rw" \
        $LINUX_IMAGE \
        /bin/bash -c "$DOCKER_COMMANDS_LINUX" | ts '[%Y-%m-%d %H:%M:%S]'
}

build_vendor_dirs() {
    _build_dir="$1"
    operating_systems="$2"
    echo $operating_systems | while read -r os; do
        if [ "$os" == "linux" ]; then
            build_linux_vendor_dir "$_build_dir"
        elif [ "$os" == "windows" ]; then
            build_windows_vendor_dir "$_build_dir"
        fi
    done
}

build_random_string() {
    _length=${1:-10}
    tr -dc A-Za-z0-9 < /dev/urandom | dd bs=$_length count=1 2>/dev/null
}

# Create a build directory
echo "Using plugin path: $PLUGIN_PATH"
manifest_filename=$(get_plugin_manifest_filename "$PLUGIN_PATH") || fail "Failed to get manifest filename"
manifest_file_path="$PLUGIN_PATH/$manifest_filename"
plugin_name=$(get_plugin_name "$manifest_file_path") || fail "Failed to get plugin name"
plugin_type=$(get_plugin_type "$manifest_file_path") || fail "Failed to get plugin type"
random_string=$(build_random_string)
plugin_build_dir=/tmp/build-$plugin_type-$plugin_name-$random_string
echo "Creating build directory: $plugin_build_dir"
build_log=$plugin_build_dir/build.log

# Copy the plugin source to the build directory
echo "Created build directory: $plugin_build_dir"
cp -r $PLUGIN_PATH $plugin_build_dir
echo "Writing build log to: $build_log"
touch $build_log

# Install dependencies
# TODO: Do this in a virtual environment?
pip install pyyaml > $build_log
pip install monkey-types > $build_log
pip install monkeyevents > $build_log

# Parse the manifest file to determine which platforms the plugin supports
manifest_file_path="$plugin_build_dir/$manifest_filename"
supported_operating_systems=$(get_plugin_supported_operating_systems "$manifest_file_path")
printf "Supported operating systems: \n$supported_operating_systems\n"
num_supported_operating_systems=$(echo "$supported_operating_systems" | wc -l)

# Parse the build config file to see how the plugin author wants to build the vendor directory
build_config_filename=$(get_plugin_build_config_filename "$plugin_build_dir")
build_config_file="$plugin_build_dir/$build_config_filename"
dependency_method=$(python3.11 "$ROOT/scripts/parse_plugin_build_file.py" "$build_config_file")
echo "Dependency method: $dependency_method"

# Determine if a common vendor directory should be used
if [ "$dependency_method" == "common" ]; then
    use_common_dir="true"
elif [ "$dependency_method" == "separate" ]; then
    use_common_dir="false"
else
    use_common_dir="autodetect"
    if [ $num_supported_operating_systems -gt 1 ]; then
        use_common_dir=$(check_if_common_vendor_dir_possible "$plugin_build_dir")
    fi
fi

echo "Use common vendor dir?: $use_common_dir"

(cd $plugin_build_dir && pipenv requirements > requirements.txt)

if [ $use_common_dir == true ]; then
    # Build the common vendor directory
    build_common_vendor_dir $plugin_build_dir
else
    # Build the vendor directory for each platform
    echo "$supported_operating_systems" | while read -r os; do
        build_vendor_dirs $plugin_build_dir $os
    done
fi

# Build plugin config schema
plugin_name_lowercase=$(lower "$plugin_name")
plugin_options_filename="${plugin_name_lowercase}_options"
plugin_options_filepath="${plugin_build_dir}/src/${plugin_options_filename}.py"
plugin_options_model_name="${plugin_name}Options"
config_schema_filepath="$plugin_build_dir/config-schema.json"
PYTHONPATH="$plugin_build_dir/src" python3.11 "$ROOT/scripts/construct_config_schema.py" \
    "$plugin_options_filepath" \
    -m $plugin_options_model_name \
    -o "$config_schema_filepath"

config_schema_generated=$?

# Build source archive
source_archive=$plugin_build_dir/$SOURCE_FILENAME
tar -zcf "$source_archive" --exclude __pycache__ --exclude .mypy_cache --exclude .pytest_cache --exclude .git --exclude .gitignore --exclude .DS_Store -- "$plugin_build_dir"/*

# Build plugin archive
plugin_filename=$(get_plugin_filename "$plugin_build_dir") || fail "Failed to get plugin filename: $plugin_filename"
tar -cf "$PLUGIN_PATH/$plugin_filename" \
    "$plugin_build_dir/$plugin_manifest_filename" \
    "$plugin_build_dir/$SCHEMA_FILENAME" \
    "$source_archive"

# Clean up
rm -rf $plugin_build_dir/src/vendor*
rm "$source_archive"
if [ "$config_schema_generated" -eq 0  ]; then
    echo -e "\033[0;33mRemoving generated $SCHEMA_FILENAME.\033[0m"
    rm "$plugin_build_dir/$SCHEMA_FILENAME"
fi
