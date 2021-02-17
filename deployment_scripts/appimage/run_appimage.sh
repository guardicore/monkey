#!/bin/bash

DOT_MONKEY=$HOME/.monkey_island/

configure_default_logging() {
    if [ ! -f $DOT_MONKEY/island_logger_config.json ]; then
        cp $APPDIR/usr/src/island_logger_config.json $DOT_MONKEY
    fi
}


# Detecting command that calls python 3.7
python_cmd=""
if [[ $(python --version 2>&1) == *"Python 3.7"* ]]; then
  python_cmd="python"
fi
if [[ $(python37 --version 2>&1) == *"Python 3.7"* ]]; then
  python_cmd="python37"
fi
if [[ $(python3.7 --version 2>&1) == *"Python 3.7"* ]]; then
  python_cmd="python3.7"
fi

mkdir --mode=0700 --parents $DOT_MONKEY

DB_DIR=$DOT_MONKEY/db
mkdir -p $DB_DIR

configure_default_logging

cd $APPDIR/usr/src
./monkey_island/bin/mongodb/bin/mongod --dbpath $DB_DIR &
${python_cmd} ./monkey_island.py --server-config $DOT_MONKEY/server_config.json --logger-config $DOT_MONKEY/island_logger_config.json
