#!/bin/bash

PYTHON_CMD="$APPDIR"/opt/python3.7/bin/python3.7
DOT_MONKEY="$HOME"/.monkey_island/

configure_default_server() {
    if [ ! -f "$DOT_MONKEY"/server_config.json ]; then
        cp "$APPDIR"/usr/src/monkey_island/cc/server_config.json.standard "$DOT_MONKEY"/server_config.json
    fi
}

# shellcheck disable=SC2174
mkdir --mode=0700 --parents "$DOT_MONKEY"

DB_DIR="$DOT_MONKEY"/db
mkdir --parents "$DB_DIR"

configure_default_server

cd "$APPDIR"/usr/src || exit 1
./monkey_island/bin/mongodb/bin/mongod --dbpath "$DB_DIR" &
${PYTHON_CMD} ./monkey_island.py --server-config "$DOT_MONKEY"/server_config.json
