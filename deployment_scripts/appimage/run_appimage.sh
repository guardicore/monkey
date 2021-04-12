#!/bin/bash

PYTHON_CMD="$APPDIR/opt/python3.7/bin/python3.7"
DOT_MONKEY=$HOME/.monkey_island/

configure_default_logging() {
    if [ ! -f $DOT_MONKEY/island_logger_config.json ]; then
        cp $APPDIR/usr/src/island_logger_config.json $DOT_MONKEY
    fi
}

configure_default_server() {
    if [ ! -f $DOT_MONKEY/server_config.json ]; then
        cp $APPDIR/usr/src/monkey_island/cc/server_config.json.standard $DOT_MONKEY/server_config.json
    fi
}




mkdir --mode=0700 --parents $DOT_MONKEY

DB_DIR=$DOT_MONKEY/db
mkdir -p $DB_DIR

configure_default_logging
configure_default_server

cd $APPDIR/usr/src
./monkey_island/bin/mongodb/bin/mongod --dbpath $DB_DIR &
${PYTHON_CMD} ./monkey_island.py --server-config $DOT_MONKEY/server_config.json --logger-config $DOT_MONKEY/island_logger_config.json
