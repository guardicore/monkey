#!/bin/bash

MACHINE_TYPE=$(uname -m)
if [ "${MACHINE_TYPE}" == 'x86_64' ]; then
  # 64-bit stuff here
  ARCH=64
else
  # 32-bit stuff here
  ARCH=32
fi

MONKEY_FILE=monkey-linux-$ARCH
cp -f /var/monkey/monkey_island/cc/binaries/$MONKEY_FILE /tmp
/tmp/$MONKEY_FILE m0nk3y "$@"
