#!/bin/bash

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

DB_DIR=${1:-"./monkey_island/bin/mongodb/db"}

mkdir -p $DB_DIR

cd $APPDIR/usr/src
./monkey_island/bin/mongodb/bin/mongod --dbpath $DB_DIR &
${python_cmd} ./monkey_island.py
