#!/bin/bash

cd /var/monkey_island/cc
/var/monkey_island/bin/mongodb/bin/mongod --quiet --dbpath /var/monkey_island/db &
/var/monkey_island/bin/python/bin/python main.py