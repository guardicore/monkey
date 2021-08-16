#!/bin/bash

echo "$@"

source /monkey/bin/activate
python /monkey/monkey_island.py "$@"
