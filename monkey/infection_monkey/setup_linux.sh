#!/bin/bash

sudo apt-get update
sudo apt-get install -y python-pip python-dev libffi-dev upx libssl-dev libc++1
pip install -r requirements_linux.txt

mkdir ./bin
wget https://github.com/guardicore/monkey/releases/download/1.6/sc_monkey_runner64.so -O ./bin/sc_monkey_runner64.so
wget https://github.com/guardicore/monkey/releases/download/1.6/sc_monkey_runner32.so -O ./bin/sc_monkey_runner32.so

wget https://github.com/guardicore/monkey/releases/download/1.6/traceroute64 -O ./bin/traceroute64
wget https://github.com/guardicore/monkey/releases/download/1.6/traceroute32 -O ./bin/traceroute32

chmod +x build_linux.sh
./build_linux.sh
