#!/bin/bash

start_mongo() {
    # TODO: Handle starting and cleaning up mongo inside monkey_island.py or
    # monkey_island/main.py.
    ./bin/mongodb/bin/mongod --dbpath ./bin/mongodb/db &
}

cd_to_monkey() {
    # Pipenv must be run from monkey/monkey/monkey_island, but monkey_island.py
    # must be executed from monkey/monkey.
    cd ..
}

start_monkey_island() {
    cd_to_monkey
    python ./monkey_island.py
}

start_mongo
start_monkey_island
