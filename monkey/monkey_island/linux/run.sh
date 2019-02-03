#!/bin/bash

cd /var/monkey
/var/monkey/monkey_island/bin/mongodb/bin/mongod --quiet --dbpath /var/monkey/monkey_island/db &
/var/monkey/monkey_island/bin/python/bin/python monkey_island.py