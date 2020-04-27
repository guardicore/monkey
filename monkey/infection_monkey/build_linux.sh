#!/bin/bash

# Allow custom build ID
# If the first argument is not empty...
if [[ -n "$1" ]]
then
  # Validate argument is a valid build string
  if [[ "$1" =~ ^[\da-zA-Z]*$ ]]
  then
    # And put it in the BUILD file
    echo "$1" > ../common/BUILD
  else
    echo "Build ID $1 invalid!"
  fi
fi

pyinstaller -F --log-level=DEBUG --clean monkey.spec
